from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import os
from dotenv import load_dotenv

from pm_outreach_agent.hunter_client import HunterClient
from pm_outreach_agent.lead_filter import filter_leads, rank_leads
from pm_outreach_agent.email_generator import generate_emails
from pm_outreach_agent.output_writer import write_markdown, write_csv
from pm_outreach_agent.models import CompanyInput, Lead
from pm_outreach_agent.utils import load_config, require_env, normalize_domain
from pm_outreach_agent.openai_client import OpenAIDraftClient, OpenAIDraftConfig
from pm_outreach_agent.gmail_client import create_gmail_drafts

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/setup')
def setup():
    return render_template('setup.html')

@app.route('/generate', methods=['POST'])
def generate():
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
        
        config = load_config('config.yaml')
        
        # Get custom inputs from form
        portfolio_url = request.form.get('portfolio_url', '').strip()
        resume_url = request.form.get('resume_url', '').strip()
        custom_subject = request.form.get('custom_subject', '').strip()
        
        # Override portfolio if provided
        if portfolio_url:
            config.portfolio_url = portfolio_url
        
        # Override target roles based on selected domain
        if config.domains and domain_type in config.domains:
            domain_config = config.domains[domain_type]
            config.target_roles = domain_config['target_roles']
            if 'background' in domain_config:
                config.candidate_background_summary = domain_config['background']
        
        hunter_key = require_env('HUNTER_API_KEY')
        client = HunterClient(api_key=hunter_key)
        
        openai_client = None
        if config.use_openai_drafts:
            openai_key = require_env('OPENAI_API_KEY')
            openai_client = OpenAIDraftClient(openai_key, OpenAIDraftConfig(model=config.openai_model))
        
        company = CompanyInput(name=company_name or domain, domain=normalize_domain(domain))
        
        try:
            leads = client.domain_search(company.domain)
        except Exception as e:
            flash(f'Hunter API error: {str(e)}', 'error')
            return redirect(url_for('index'))
        
        for lead in leads:
            if not lead.company:
                lead.company = company.name
        
        total_leads = len(leads)
        filtered = filter_leads(leads, config.target_roles, config.excluded_roles, config.min_email_confidence)
        ranked = rank_leads(filtered)
        ordered_leads = [item.lead for item in ranked]
        
        if not ordered_leads:
            flash(f'Found {total_leads} leads but none matched {domain_type.replace("_", " ").title()} roles with confidence ≥{config.min_email_confidence}. Try another company.', 'error')
            return redirect(url_for('index'))
        
        # Generate emails for ALL leads (no limit)
        drafts = generate_emails(
            ordered_leads,
            config.portfolio_url,
            config.candidate_background_summary,
            config.tone,
            openai_client=openai_client,
            custom_subject=custom_subject if custom_subject else None,
            resume_url=resume_url if resume_url else None,
        )
        
        write_markdown("send_sheet.md", ranked, drafts)
        write_csv("send_sheet.csv", ranked, drafts)
        
        if create_gmail and config.sender_email:
            try:
                # Check if resume file exists for attachment
                resume_file = None
                if resume_url and resume_url.startswith('/'):
                    # Local file path
                    if os.path.exists(resume_url):
                        resume_file = resume_url
                
                create_gmail_drafts(ranked, drafts, config.sender_email, config.gmail_credentials_path, config.gmail_token_path, resume_file)
                flash(f'Generated {len(filtered)} {domain_type.replace("_", " ").title()} leads and created Gmail drafts!', 'success')
            except Exception as e:
                flash(f'Generated {len(filtered)} leads but Gmail draft creation failed: {str(e)}', 'error')
        else:
            flash(f'Generated {len(filtered)} {domain_type.replace("_", " ").title()} leads! Check send_sheet.md and send_sheet.csv', 'success')
        
        return redirect(url_for('results', count=len(filtered)))
    
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/results')
def results():
    count = request.args.get('count', 0)
    try:
        with open('send_sheet.md', 'r') as f:
            content = f.read()
        return render_template('results.html', content=content, count=count)
    except FileNotFoundError:
        flash('No results found. Generate leads first.', 'error')
        return redirect(url_for('index'))

@app.route('/download/<filename>')
def download(filename):
    if filename in ['send_sheet.md', 'send_sheet.csv']:
        return send_file(filename, as_attachment=True)
    return 'File not found', 404

@app.route('/batch', methods=['GET', 'POST'])
def batch():
    if request.method == 'GET':
        return render_template('batch.html')
    
    companies_text = request.form.get('companies_text', '').strip()
    if not companies_text:
        flash('Please enter at least one company domain', 'error')
        return redirect(url_for('batch'))
    
    # Parse companies (one per line)
    companies = [line.strip() for line in companies_text.split('\\n') if line.strip()]
    
    total_leads = 0
    all_ranked = []
    all_drafts = []
    
    config = load_config('config.yaml')
    hunter_key = require_env('HUNTER_API_KEY')
    client = HunterClient(api_key=hunter_key)
    
    openai_client = None
    if config.use_openai_drafts:
        openai_key = require_env('OPENAI_API_KEY')
        openai_client = OpenAIDraftClient(openai_key, OpenAIDraftConfig(model=config.openai_model))
    
    for company_domain in companies:
        try:
            leads = client.domain_search(normalize_domain(company_domain))
            filtered = filter_leads(leads, config.target_roles, config.excluded_roles, config.min_email_confidence)
            ranked = rank_leads(filtered)
            
            if ranked:
                drafts = generate_emails(
                    [r.lead for r in ranked],
                    config.portfolio_url,
                    config.candidate_background_summary,
                    config.tone,
                    openai_client=openai_client,
                )
                all_ranked.extend(ranked)
                all_drafts.extend(drafts)
                total_leads += len(ranked)
        except Exception:
            continue
    
    if total_leads > 0:
        write_markdown("send_sheet.md", all_ranked, all_drafts)
        write_csv("send_sheet.csv", all_ranked, all_drafts)
        flash(f'Batch processed {len(companies)} companies → {total_leads} total leads!', 'success')
    else:
        flash('No leads found from any company. Try different domains.', 'error')
    
    return redirect(url_for('batch'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
