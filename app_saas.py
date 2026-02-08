from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify, session
from flask_login import login_required, current_user
import os
from dotenv import load_dotenv
from datetime import datetime

from pm_outreach_agent.hunter_client import HunterClient
from pm_outreach_agent.multi_provider_finder import email_finder
from pm_outreach_agent.lead_filter import filter_leads, rank_leads
from pm_outreach_agent.email_generator import generate_emails
from pm_outreach_agent.output_writer import write_markdown, write_csv
from pm_outreach_agent.models import CompanyInput, Lead
from pm_outreach_agent.utils import load_config, require_env, normalize_domain
from pm_outreach_agent.openai_client import OpenAIDraftClient, OpenAIDraftConfig
from pm_outreach_agent.gmail_client import create_gmail_drafts

# Import SaaS components
from database import db, init_db, User, Search
from auth import auth_bp, init_auth

# Import Gmail service
from gmail_service import gmail_service

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', os.urandom(24))

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', 
    'sqlite:///leadfinder.db'
).replace('postgres://', 'postgresql://')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database and authentication
init_db(app)
init_auth(app)
app.register_blueprint(auth_bp)

# Initialize Gmail service
gmail_service.app = app
gmail_service.credentials_path = os.path.join(os.path.dirname(__file__), 'credentials.json')


@app.route('/')
def landing():
    """Homepage - Landing page or App"""
    if current_user.is_authenticated:
        # If logged in, check if they have providers configured
        provider_count = len(current_user.get_configured_providers())
        if provider_count == 0:
            # No providers - redirect to settings first
            flash('👋 Welcome! Please add at least one email provider API key to get started.', 'info')
            return redirect(url_for('settings'))
        return render_template('index.html', user=current_user, provider_count=provider_count)
    else:
        return render_template('landing_new.html')


@app.route('/app')
@login_required
def index():
    """Main app interface (requires login)"""
    provider_count = len(current_user.get_configured_providers())
    enabled_providers = email_finder.get_enabled_providers(current_user)
    return render_template('index.html', user=current_user, 
                         provider_count=provider_count,
                         enabled_providers=enabled_providers)


@app.route('/generate', methods=['POST'])
@login_required
def generate():
    """Generate leads and emails"""
    try:
        company_name = request.form.get('company_name', '').strip()
        domain = request.form.get('domain', '').strip()
        domain_type = request.form.get('domain_type', 'product_management').strip()
        create_gmail = request.form.get('create_gmail') == 'on'
        portfolio_url = request.form.get('portfolio_url', '').strip()
        resume_url = request.form.get('resume_url', '').strip()
        custom_subject = request.form.get('custom_subject', '').strip()
        
        if not domain:
            flash('Domain is required', 'error')
            return redirect(url_for('index'))
        
        # Proactive check: Does user have any email providers configured?
        if not current_user.get_configured_providers():
            flash('⚠️ No email providers configured! Please add at least one API key in Settings to find leads.', 'error')
            return redirect(url_for('settings'))
        
        config = load_config('config.yaml')
        
        if portfolio_url:
            config.portfolio_url = portfolio_url
        
        if config.domains and domain_type in config.domains:
            domain_config = config.domains[domain_type]
            config.target_roles = domain_config['target_roles']
            if 'background' in domain_config:
                config.candidate_background_summary = domain_config['background']
        
        # Use multi-provider email finder with caching
        openai_client = None
        if config.use_openai_drafts:
            openai_key = require_env('OPENAI_API_KEY')
            openai_client = OpenAIDraftClient(openai_key, OpenAIDraftConfig(model=config.openai_model))
        
        company = CompanyInput(name=company_name or domain, domain=normalize_domain(domain))
        
        try:
            # Use scalable multi-provider finder (auto-fallback, caching, rate limiting)
            leads_raw = email_finder.find_leads(company.domain, domain_type, current_user)
        except Exception as e:
            flash(f"⚠️ Could not fetch leads: {str(e)}. Please check your API keys in Settings.", "error")
            return redirect(url_for('settings'))
        
        if not leads_raw:
            # Check if it's a configuration issue or just no results
            providers = email_finder.get_enabled_providers(current_user)
            provider_list = ', '.join(providers) if providers else 'none'
            flash(f"No leads found for {company.domain} using providers: {provider_list}. This could mean: (1) No employees listed publicly, (2) Rate limits reached, or (3) Try adding more API keys in Settings.", "warning")
            return redirect(url_for('index'))
        
        leads_filtered = filter_leads(leads_raw, config)
        leads_ranked = rank_leads(leads_filtered, config.target_roles)
        
        if not leads_ranked:
            flash(f"No leads matched target roles for {domain_type}", "error")
            return redirect(url_for('landing'))
        
        drafts = generate_emails(leads_ranked, company.name, config, openai_client=openai_client, custom_subject=custom_subject if custom_subject else None)
        
        write_markdown(company, drafts, 'send_sheet.md')
        write_csv(company, drafts, 'send_sheet.csv')
        
        # Create Gmail drafts if requested and user is connected
        if create_gmail:
            if not current_user.has_gmail_connected():
                flash('⚠️ Gmail not connected. Please connect your Gmail account first.', 'warning')
            else:
                try:
                    # Get user's Gmail credentials
                    gmail_token = current_user.get_gmail_token()
                    
                    if gmail_token:
                        # Prepare draft data for bulk creation
                        draft_data_list = []
                        for draft in drafts:
                            draft_data_list.append({
                                'to': draft.email,
                                'subject': draft.subject,
                                'body': draft.body
                            })
                        
                        # Create drafts using Gmail service
                        result = gmail_service.create_drafts_bulk(gmail_token, draft_data_list)
                        
                        if result['success'] > 0:
                            flash(f'✅ Created {result["success"]} Gmail draft(s)! Check your Gmail Drafts folder.', 'success')
                        if result['failed'] > 0:
                            flash(f'⚠️ {result["failed"]} draft(s) failed to create. Check console for details.', 'warning')
                            for error in result['errors'][:3]:  # Show first 3 errors
                                print(f"Draft creation error: {error}")
                    else:
                        flash('⚠️ Gmail token expired. Please reconnect your Gmail account.', 'warning')
                
                except Exception as e:
                    print(f"Gmail error: {e}")
                    flash(f"⚠️ Gmail draft creation failed: {str(e)}. CSV/MD files still available.", "warning")
        
        lead_count = len(drafts)
        current_user.increment_usage(lead_count)
        
        search = Search(
            user_id=current_user.id,
            company_name=company_name or domain,
            domain=domain,
            domain_type=domain_type,
            lead_count=lead_count,
            csv_file='send_sheet.csv',
            md_file='send_sheet.md',
            success=True
        )
        db.session.add(search)
        db.session.commit()
        
        flash(f'✅ Success! Generated {lead_count} leads.', 'success')
        return redirect(url_for('results', count=lead_count))
    
    except Exception as e:
        print(f"Error: {e}")
        search = Search(
            user_id=current_user.id,
            company_name=request.form.get('company_name', ''),
            domain=request.form.get('domain', ''),
            domain_type=request.form.get('domain_type', ''),
            lead_count=0,
            success=False,
            error_message=str(e)
        )
        db.session.add(search)
        db.session.commit()
        flash(f"Error: {str(e)}", "error")
        return redirect(url_for('landing'))


@app.route('/results')
@login_required
def results():
    count = request.args.get('count', 0)
    return render_template('results.html', count=count, user=current_user)


@app.route('/download/<filename>')
@login_required
def download(filename):
    if filename not in ['send_sheet.csv', 'send_sheet.md']:
        return "Invalid file", 400
    filepath = os.path.join(os.getcwd(), filename)
    if not os.path.exists(filepath):
        return "File not found", 404
    return send_file(filepath, as_attachment=True)


@app.route('/batch', methods=['GET', 'POST'])
@login_required
def batch():
    if request.method == 'POST':
        companies_text = request.form.get('companies', '').strip()
        if not companies_text:
            flash('Please enter at least one company domain', 'error')
            return render_template('batch.html', user=current_user)
        
        domains = [d.strip() for d in companies_text.split('\n') if d.strip()]
        domain_type = request.form.get('domain_type', 'product_management').strip()
        config = load_config('config.yaml')
        
        if config.domains and domain_type in config.domains:
            domain_config = config.domains[domain_type]
            config.target_roles = domain_config['target_roles']
            if 'background' in domain_config:
                config.candidate_background_summary = domain_config['background']
        
        # Use multi-provider finder for batch processing
        openai_client = None
        if config.use_openai_drafts:
            openai_key = require_env('OPENAI_API_KEY')
            openai_client = OpenAIDraftClient(openai_key, OpenAIDraftConfig(model=config.openai_model))
        
        all_drafts = []
        all_leads = 0
        
        for domain in domains:
            try:
                company = CompanyInput(name=domain, domain=normalize_domain(domain))
                # Use multi-provider finder with caching
                leads_raw = email_finder.find_leads(company.domain, domain_type, current_user)
                
                if leads_raw:
                    leads_filtered = filter_leads(leads_raw, config)
                    leads_ranked = rank_leads(leads_filtered, config.target_roles)
                    
                    if leads_ranked:
                        drafts = generate_emails(leads_ranked, company.name, config, openai_client=openai_client)
                        all_drafts.extend(drafts)
                        all_leads += len(drafts)
                        
                        search = Search(
                            user_id=current_user.id,
                            company_name=domain,
                            domain=domain,
                            domain_type=domain_type,
                            lead_count=len(drafts),
                            success=True
                        )
                        db.session.add(search)
            except Exception as e:
                print(f"Error processing {domain}: {e}")
                continue
        
        current_user.increment_usage(all_leads)
        db.session.commit()
        
        if all_drafts:
            write_markdown(CompanyInput(name="Batch", domain="batch"), all_drafts, 'send_sheet.md')
            write_csv(CompanyInput(name="Batch", domain="batch"), all_drafts, 'send_sheet.csv')
            flash(f'✅ Batch complete! {all_leads} total leads from {len(domains)} companies.', 'success')
            return redirect(url_for('results', count=all_leads))
        else:
            flash('No leads found from any companies', 'error')
            return redirect(url_for('batch'))
    
    return render_template('batch.html', user=current_user)


@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard with usage stats and search history"""
    # Get recent searches
    recent_searches = Search.query.filter_by(
        user_id=current_user.id
    ).order_by(Search.created_at.desc()).limit(10).all()
    
    # Use user's dashboard preference
    template = 'dashboard.html' if current_user.dashboard_view == 'premium' else 'dashboard_simple.html'
    
    return render_template(template, user=current_user, searches=recent_searches)


@app.route('/toggle-dashboard')
@login_required
def toggle_dashboard():
    """Toggle between premium and simple dashboard views"""
    # Switch view preference
    if current_user.dashboard_view == 'premium':
        current_user.dashboard_view = 'simple'
    else:
        current_user.dashboard_view = 'premium'
    
    db.session.commit()
    flash(f'Switched to {current_user.dashboard_view} dashboard view!', 'success')
    return redirect(url_for('dashboard'))


@app.route('/api/provider-status')
@login_required
def provider_status():
    """Get status of all email providers"""
    status = email_finder.get_provider_status(current_user)
    return jsonify(status)


@app.route('/settings')
@login_required
def settings():
    """Settings page - User's own API key management"""
    user_provider_count = len(current_user.get_configured_providers())
    
    return render_template('settings_user.html', 
                         user=current_user,
                         user_provider_count=user_provider_count)


@app.route('/templates')
@login_required
def templates():
    """Email template management page"""
    from database import EmailTemplate
    user_templates = EmailTemplate.query.filter_by(user_id=current_user.id).order_by(EmailTemplate.created_at.desc()).all()
    return render_template('templates.html', user=current_user, templates=user_templates)


@app.route('/templates/create', methods=['POST'])
@login_required
def create_template():
    """Create new email template"""
    from database import EmailTemplate
    try:
        name = request.form.get('name', '').strip()
        subject = request.form.get('subject', '').strip()
        body = request.form.get('body', '').strip()
        domain_type = request.form.get('domain_type', '').strip() or None
        is_default = request.form.get('is_default') == 'on'
        
        if not name or not subject or not body:
            flash('Name, subject, and body are required', 'error')
            return redirect(url_for('templates'))
        
        # If setting as default, unset other defaults for this domain type
        if is_default:
            EmailTemplate.query.filter_by(
                user_id=current_user.id,
                domain_type=domain_type,
                is_default=True
            ).update({'is_default': False})
        
        template = EmailTemplate(
            user_id=current_user.id,
            name=name,
            subject=subject,
            body=body,
            domain_type=domain_type,
            is_default=is_default
        )
        db.session.add(template)
        db.session.commit()
        
        flash(f'✅ Template "{name}" created successfully!', 'success')
    except Exception as e:
        flash(f'Error creating template: {str(e)}', 'error')
    
    return redirect(url_for('templates'))


@app.route('/templates/<int:template_id>/edit', methods=['POST'])
@login_required
def edit_template(template_id):
    """Edit existing email template"""
    from database import EmailTemplate
    try:
        template = EmailTemplate.query.filter_by(id=template_id, user_id=current_user.id).first()
        if not template:
            flash('Template not found', 'error')
            return redirect(url_for('templates'))
        
        template.name = request.form.get('name', '').strip()
        template.subject = request.form.get('subject', '').strip()
        template.body = request.form.get('body', '').strip()
        template.domain_type = request.form.get('domain_type', '').strip() or None
        is_default = request.form.get('is_default') == 'on'
        
        if is_default and not template.is_default:
            # Unset other defaults
            EmailTemplate.query.filter_by(
                user_id=current_user.id,
                domain_type=template.domain_type,
                is_default=True
            ).update({'is_default': False})
        
        template.is_default = is_default
        template.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash(f'✅ Template "{template.name}" updated!', 'success')
    except Exception as e:
        flash(f'Error updating template: {str(e)}', 'error')
    
    return redirect(url_for('templates'))


@app.route('/templates/<int:template_id>/delete', methods=['POST'])
@login_required
def delete_template(template_id):
    """Delete email template"""
    from database import EmailTemplate
    try:
        template = EmailTemplate.query.filter_by(id=template_id, user_id=current_user.id).first()
        if not template:
            flash('Template not found', 'error')
            return redirect(url_for('templates'))
        
        name = template.name
        db.session.delete(template)
        db.session.commit()
        flash(f'✅ Template "{name}" deleted!', 'success')
    except Exception as e:
        flash(f'Error deleting template: {str(e)}', 'error')
    
    return redirect(url_for('templates'))


@app.route('/analytics')
@login_required
def analytics():
    """Analytics dashboard showing usage stats"""
    from database import Search, APICallLog
    from datetime import datetime, timedelta
    from sqlalchemy import func
    
    # Date ranges
    today = datetime.utcnow().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # Total stats
    total_searches = Search.query.filter_by(user_id=current_user.id).count()
    total_leads = db.session.query(func.sum(Search.lead_count)).filter_by(user_id=current_user.id).scalar() or 0
    total_providers = len(current_user.get_configured_providers())
    
    # Recent searches
    recent_searches = Search.query.filter_by(user_id=current_user.id).order_by(Search.created_at.desc()).limit(10).all()
    
    # Searches by date (last 30 days)
    searches_by_date = db.session.query(
        func.date(Search.created_at).label('date'),
        func.count(Search.id).label('count'),
        func.sum(Search.lead_count).label('leads')
    ).filter(
        Search.user_id == current_user.id,
        Search.created_at >= month_ago
    ).group_by(func.date(Search.created_at)).all()
    
    # API calls by provider
    api_calls_by_provider = db.session.query(
        APICallLog.provider,
        func.count(APICallLog.id).label('calls'),
        func.sum(APICallLog.credits_used).label('credits')
    ).filter(
        APICallLog.user_id == current_user.id
    ).group_by(APICallLog.provider).all()
    
    # Success rate
    successful_searches = Search.query.filter_by(user_id=current_user.id, success=True).count()
    success_rate = (successful_searches / total_searches * 100) if total_searches > 0 else 0
    
    # Average leads per search
    avg_leads = total_leads / total_searches if total_searches > 0 else 0
    
    # This week stats
    week_searches = Search.query.filter(
        Search.user_id == current_user.id,
        Search.created_at >= week_ago
    ).count()
    
    week_leads = db.session.query(func.sum(Search.lead_count)).filter(
        Search.user_id == current_user.id,
        Search.created_at >= week_ago
    ).scalar() or 0
    
    # Format data for charts
    chart_labels = []
    chart_searches = []
    chart_leads = []
    
    # Fill in missing dates
    for i in range(30):
        date = today - timedelta(days=29-i)
        chart_labels.append(date.strftime('%b %d'))
        
        # Find matching data
        found = False
        for row in searches_by_date:
            if row.date == date:
                chart_searches.append(row.count)
                chart_leads.append(row.leads or 0)
                found = True
                break
        
        if not found:
            chart_searches.append(0)
            chart_leads.append(0)
    
    return render_template('analytics.html',
                         user=current_user,
                         total_searches=total_searches,
                         total_leads=total_leads,
                         total_providers=total_providers,
                         recent_searches=recent_searches,
                         api_calls_by_provider=api_calls_by_provider,
                         success_rate=success_rate,
                         avg_leads=avg_leads,
                         week_searches=week_searches,
                         week_leads=week_leads,
                         chart_labels=chart_labels,
                         chart_searches=chart_searches,
                         chart_leads=chart_leads)


@app.route('/export/searches')
@login_required
def export_searches():
    """Export all searches as CSV"""
    from database import Search
    import csv
    from io import StringIO
    
    searches = Search.query.filter_by(user_id=current_user.id).order_by(Search.created_at.desc()).all()
    
    # Create CSV in memory
    output = StringIO()
    writer = csv.writer(output)
    
    # Headers
    writer.writerow(['Date', 'Company', 'Domain', 'Type', 'Leads', 'Status', 'Error'])
    
    # Data rows
    for search in searches:
        writer.writerow([
            search.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            search.company_name or search.domain,
            search.domain,
            search.domain_type or 'default',
            search.lead_count,
            'Success' if search.success else 'Failed',
            search.error_message or ''
        ])
    
    # Prepare response
    output.seek(0)
    from flask import Response
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename=leadfinder_searches_{datetime.utcnow().strftime("%Y%m%d")}.csv'}
    )


@app.route('/export/analytics')
@login_required
def export_analytics():
    """Export analytics data as CSV"""
    from database import Search, APICallLog
    import csv
    from io import StringIO
    from datetime import datetime, timedelta
    from sqlalchemy import func
    
    output = StringIO()
    writer = csv.writer(output)
    
    # Summary stats
    writer.writerow(['LeadFinder AI - Analytics Export'])
    writer.writerow(['Generated:', datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')])
    writer.writerow(['User:', current_user.email])
    writer.writerow([])
    
    # Overall stats
    writer.writerow(['Overall Statistics'])
    writer.writerow(['Metric', 'Value'])
    writer.writerow(['Total Searches', Search.query.filter_by(user_id=current_user.id).count()])
    writer.writerow(['Total Leads', db.session.query(func.sum(Search.lead_count)).filter_by(user_id=current_user.id).scalar() or 0])
    writer.writerow(['Providers Configured', len(current_user.get_configured_providers())])
    writer.writerow([])
    
    # API usage by provider
    writer.writerow(['API Usage by Provider'])
    writer.writerow(['Provider', 'Total Calls', 'Credits Used'])
    
    api_calls = db.session.query(
        APICallLog.provider,
        func.count(APICallLog.id).label('calls'),
        func.sum(APICallLog.credits_used).label('credits')
    ).filter(
        APICallLog.user_id == current_user.id
    ).group_by(APICallLog.provider).all()
    
    for provider in api_calls:
        writer.writerow([provider.provider, provider.calls, provider.credits or 0])
    
    writer.writerow([])
    
    # Daily activity (last 30 days)
    writer.writerow(['Daily Activity (Last 30 Days)'])
    writer.writerow(['Date', 'Searches', 'Leads'])
    
    today = datetime.utcnow().date()
    for i in range(30):
        date = today - timedelta(days=29-i)
        day_searches = Search.query.filter(
            Search.user_id == current_user.id,
            func.date(Search.created_at) == date
        ).count()
        day_leads = db.session.query(func.sum(Search.lead_count)).filter(
            Search.user_id == current_user.id,
            func.date(Search.created_at) == date
        ).scalar() or 0
        
        writer.writerow([date.strftime('%Y-%m-%d'), day_searches, day_leads])
    
    output.seek(0)
    from flask import Response
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename=leadfinder_analytics_{datetime.utcnow().strftime("%Y%m%d")}.csv'}
    )


@app.route('/team')
@login_required
def team():
    """Team management page"""
    from database import Organization, User
    
    # Create org if user doesn't have one
    if not current_user.organization_id:
        org = Organization(
            name=f"{current_user.name}'s Team",
            slug=f"team_{current_user.id}",
            plan='free'
        )
        db.session.add(org)
        db.session.flush()
        
        current_user.organization_id = org.id
        current_user.role = 'owner'
        db.session.commit()
    
    org = Organization.query.get(current_user.organization_id)
    team_members = User.query.filter_by(organization_id=org.id).order_by(User.created_at).all()
    
    return render_template('team.html', user=current_user, organization=org, team_members=team_members)


@app.route('/team/invite', methods=['POST'])
@login_required
def invite_team_member():
    """Invite new team member"""
    if current_user.role not in ['owner', 'admin']:
        flash('Only owners and admins can invite team members', 'error')
        return redirect(url_for('team'))
    
    email = request.form.get('email', '').strip().lower()
    role = request.form.get('role', 'member')
    
    if not email:
        flash('Email is required', 'error')
        return redirect(url_for('team'))
    
    # Check if user already exists
    from database import User
    existing_user = User.query.filter_by(email=email).first()
    
    if existing_user:
        if existing_user.organization_id == current_user.organization_id:
            flash('User is already in your team', 'warning')
        elif existing_user.organization_id:
            flash('User is already in another organization', 'error')
        else:
            # Add to team
            existing_user.organization_id = current_user.organization_id
            existing_user.role = role
            db.session.commit()
            flash(f'✅ {email} added to your team!', 'success')
    else:
        # For now, just show message (in production, send invite email)
        flash(f'💡 Invite link would be sent to {email}. User needs to sign up first.', 'info')
    
    return redirect(url_for('team'))


@app.route('/team/<int:user_id>/role', methods=['POST'])
@login_required
def update_team_member_role(user_id):
    """Update team member role"""
    if current_user.role != 'owner':
        flash('Only owners can change roles', 'error')
        return redirect(url_for('team'))
    
    from database import User
    member = User.query.filter_by(id=user_id, organization_id=current_user.organization_id).first()
    
    if not member:
        flash('Team member not found', 'error')
        return redirect(url_for('team'))
    
    new_role = request.form.get('role', 'member')
    member.role = new_role
    db.session.commit()
    
    flash(f'✅ Updated {member.name}\'s role to {new_role}', 'success')
    return redirect(url_for('team'))


@app.route('/team/<int:user_id>/remove', methods=['POST'])
@login_required
def remove_team_member(user_id):
    """Remove team member"""
    if current_user.role not in ['owner', 'admin']:
        flash('Only owners and admins can remove team members', 'error')
        return redirect(url_for('team'))
    
    from database import User
    member = User.query.filter_by(id=user_id, organization_id=current_user.organization_id).first()
    
    if not member:
        flash('Team member not found', 'error')
        return redirect(url_for('team'))
    
    if member.id == current_user.id:
        flash('You cannot remove yourself', 'error')
        return redirect(url_for('team'))
    
    member.organization_id = None
    member.role = 'member'
    db.session.commit()
    
    flash(f'✅ Removed {member.name} from team', 'success')
    return redirect(url_for('team'))


def _validate_hunter_key(api_key: str) -> tuple:
    """Validate Hunter.io API key by making a test request"""
    import requests
    try:
        response = requests.get(
            f'https://api.hunter.io/v2/account?api_key={api_key}',
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            if data.get('data'):
                return (True, "✓ Verified")
        return (False, "Invalid API key")
    except:
        return (True, "⚠️ Could not verify (network issue)")


def _validate_apollo_key(api_key: str) -> tuple:
    """Validate Apollo.io API key by making a test request"""
    import requests
    try:
        response = requests.get(
            'https://api.apollo.io/v1/auth/health',
            headers={'X-Api-Key': api_key},
            timeout=5
        )
        if response.status_code == 200:
            return (True, "✓ Verified")
        return (False, "Invalid API key")
    except:
        return (True, "⚠️ Could not verify (network issue)")


def _validate_openai_key(api_key: str) -> tuple:
    """Validate OpenAI API key"""
    import requests
    try:
        response = requests.get(
            'https://api.openai.com/v1/models',
            headers={'Authorization': f'Bearer {api_key}'},
            timeout=5
        )
        if response.status_code == 200:
            return (True, "✓ Verified")
        return (False, "Invalid API key")
    except:
        return (True, "⚠️ Could not verify (network issue)")


@app.route('/save-api-keys', methods=['POST'])
@login_required
def save_api_keys():
    """Save user's API keys (encrypted in database) with validation"""
    try:
        # Get form data
        hunter_key = request.form.get('hunter_api_key', '').strip()
        apollo_key = request.form.get('apollo_api_key', '').strip()
        snov_key = request.form.get('snov_api_key', '').strip()
        snov_secret = request.form.get('snov_client_secret', '').strip()
        ftl_key = request.form.get('findthatlead_api_key', '').strip()
        openai_key = request.form.get('openai_api_key', '').strip()
        
        validated_count = 0
        failed_validations = []
        
        # Save and validate each key if provided (skip if dots which means unchanged)
        if hunter_key and not hunter_key.startswith('•'):
            valid, msg = _validate_hunter_key(hunter_key)
            if valid:
                current_user.set_api_key('hunter', hunter_key)
                validated_count += 1
                if "Verified" in msg:
                    flash(f'Hunter.io: {msg}', 'success')
            else:
                failed_validations.append(f'Hunter.io: {msg}')
        
        if apollo_key and not apollo_key.startswith('•'):
            valid, msg = _validate_apollo_key(apollo_key)
            if valid:
                current_user.set_api_key('apollo', apollo_key)
                validated_count += 1
                if "Verified" in msg:
                    flash(f'Apollo.io: {msg}', 'success')
            else:
                failed_validations.append(f'Apollo.io: {msg}')
        
        if snov_key and not snov_key.startswith('•'):
            current_user.set_api_key('snov', snov_key, snov_secret if snov_secret and not snov_secret.startswith('•') else None)
            validated_count += 1
        
        if ftl_key and not ftl_key.startswith('•'):
            current_user.set_api_key('findthatlead', ftl_key)
            validated_count += 1
        
        if openai_key and not openai_key.startswith('•'):
            valid, msg = _validate_openai_key(openai_key)
            if valid:
                current_user.set_api_key('openai', openai_key)
                if "Verified" in msg:
                    flash(f'OpenAI: {msg}', 'success')
            else:
                failed_validations.append(f'OpenAI: {msg}')
        
        db.session.commit()
        
        # Show results
        if failed_validations:
            for err in failed_validations:
                flash(err, 'error')
        
        provider_count = len(current_user.get_configured_providers())
        if provider_count > 0:
            flash(f'✅ {provider_count} provider(s) configured. You can now generate leads!', 'success')
        elif validated_count == 0:
            flash('💡 No new API keys added. Paste your keys and click Save to get started.', 'info')
        
    except Exception as e:
        flash(f'Error saving API keys: {str(e)}', 'error')
    
    return redirect(url_for('settings'))


@app.route('/gmail-setup')
@login_required
def gmail_setup():
    """Dedicated Gmail setup page with user-friendly interface"""
    connected = current_user.has_gmail_connected()
    user_info = None
    
    if connected:
        # Get Gmail account info
        user_info = gmail_service.get_user_info(current_user.get_gmail_token())
    
    setup_instructions = gmail_service.get_setup_instructions()
    
    return render_template(
        'gmail_setup.html',
        connected=connected,
        user_info=user_info,
        is_configured=gmail_service.is_configured(),
        setup_instructions=setup_instructions
    )


@app.route('/connect-gmail')
@login_required
def connect_gmail():
    """Initiate Gmail OAuth flow (improved with service)"""
    if not gmail_service.is_configured():
        flash('⚠️ Gmail OAuth not configured. Please complete the setup steps first.', 'warning')
        return redirect(url_for('gmail_setup'))
    
    try:
        # Generate OAuth URL using service
        redirect_uri = url_for('gmail_oauth_callback', _external=True)
        result = gmail_service.get_oauth_url(redirect_uri)
        
        if not result:
            flash('❌ Error generating OAuth URL. Please try again.', 'error')
            return redirect(url_for('gmail_setup'))
        
        authorization_url, state = result
        
        # Store state in session for verification
        session['oauth_state'] = state
        
        # Redirect to Google's OAuth page
        return redirect(authorization_url)
        
    except Exception as e:
        flash(f'❌ Error initiating Gmail OAuth: {str(e)}', 'error')
        return redirect(url_for('gmail_setup'))


@app.route('/oauth2callback')
@login_required
def gmail_oauth_callback():
    """Handle OAuth callback from Google (improved with service)"""
    # Verify state to prevent CSRF
    state = session.get('oauth_state')
    if not state:
        flash('⚠️ Invalid OAuth state. Please try connecting again.', 'warning')
        return redirect(url_for('gmail_setup'))
    
    try:
        # Handle OAuth callback using service
        redirect_uri = url_for('gmail_oauth_callback', _external=True)
        credentials_json = gmail_service.handle_oauth_callback(
            state=state,
            redirect_uri=redirect_uri,
            authorization_response=request.url
        )
        
        if not credentials_json:
            flash('❌ Error connecting Gmail. Please try again.', 'error')
            return redirect(url_for('gmail_setup'))
        
        # Store credentials in database (encrypted)
        current_user.set_gmail_token(credentials_json)
        db.session.commit()
        
        # Test the connection
        if gmail_service.test_connection(credentials_json):
            # Get user info for confirmation
            user_info = gmail_service.get_user_info(credentials_json)
            if user_info:
                flash(f'✅ Gmail connected successfully! Account: {user_info["email"]}', 'success')
            else:
                flash('✅ Gmail connected successfully! You can now create email drafts automatically.', 'success')
        else:
            flash('⚠️ Gmail connected but connection test failed. You may need to reconnect.', 'warning')
        
    except Exception as e:
        flash(f'❌ Error connecting Gmail: {str(e)}', 'error')
    
    return redirect(url_for('gmail_setup'))



@app.route('/disconnect-gmail', methods=['POST'])
@login_required
def disconnect_gmail():
    """Disconnect Gmail account"""
    try:
        current_user.gmail_token_encrypted = None
        db.session.commit()
        flash('✅ Gmail disconnected successfully! You can reconnect anytime.', 'success')
    except Exception as e:
        flash(f'❌ Error disconnecting Gmail: {str(e)}', 'error')
    return redirect(url_for('gmail_setup'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
