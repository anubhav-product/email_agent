# 📖 Complete User Guide - LeadFinder AI

**The all-in-one automation agent for job seekers, recruiters, and sales teams**

---

## 🎯 What is LeadFinder AI?

LeadFinder AI automates the most time-consuming part of outreach:
1. **Finding decision-makers** at target companies (Hunter.io)
2. **Writing personalized emails** with AI (OpenAI GPT-4o)
3. **Creating Gmail drafts** for human review (Gmail API)

**No emails sent automatically. You always review and approve.**

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Installation
```bash
git clone <repo-url>
cd email_agent
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Step 2: Open Web Interface
Go to **http://localhost:5000** in your browser.

### Step 3: Click "📖 New User? Complete Setup Guide →"
Follow the interactive 5-step wizard:
- Get Hunter.io API key (free)
- Get OpenAI API key (optional, $0.01/10 emails)
- Configure .env and config.yaml
- Set up Gmail OAuth (optional)
- Test with your first company

**That's it!** Start generating leads immediately.

---

## 💻 How to Use

### Homepage Interface

**1. Choose Career Domain**
Select your target industry:
- **Product Management** (Founders, CPOs, VPs of Product)
- **Consulting & Strategy** (Partners, Principals, Senior Consultants)
- **Software Engineering** (VPs Engineering, Senior Engineers)
- **Data Science & Analytics** (Data Directors, ML Engineers)

**2. Enter Company Details**
- **Company Name**: Optional (detected from domain)
- **Domain**: Required (e.g., `stripe.com`, `airbnb.com`)
- **Portfolio URL**: Optional (linked in email signature)
- **Resume**: Optional (URL = link, local path = attachment)
- **Subject**: Optional (leave blank for AI-generated subjects)

**3. Gmail Drafts Checkbox**
Check this to automatically create Gmail drafts after lead generation.
- First use: Browser opens for OAuth authorization
- Future uses: Silent draft creation
- **No emails sent automatically** - drafts stay in Gmail for review

**4. Click "🚀 Generate Leads & Drafts"**
Wait 10-30 seconds while the agent:
- Searches for decision-makers at the company
- Generates personalized emails for each lead
- Creates Gmail drafts (if enabled)
- Exports CSV and Markdown files

---

## 📊 Results Page

After generation, you'll see:

### Lead Count
**Large number display** showing how many leads were found (typically 5-50+).

### Download Options
- **📊 CSV**: Import into Gmail, CRM, or spreadsheet
- **📄 Markdown**: Copy-paste ready emails with formatting

### Email Preview
See the first email generated to verify quality and personalization.

### Next Steps Tips
- ✅ Review all emails in send_sheet.md
- ✅ Personalize top 5-10 for better response rates
- ✅ Check Gmail drafts (if created)
- ✅ Send 10-15 emails per day (avoid spam filters)
- ✅ Follow up after 3-5 days if no response

### Navigation
- **← Generate More Leads**: Return to homepage
- **📊 Batch Process**: Process multiple companies at once

---

## 🔁 Batch Processing

Process 5-20 companies simultaneously.

**How it works:**
1. Click "📊 Batch Process Multiple Companies" link
2. Enter company domains (one per line):
   ```
   stripe.com
   airbnb.com
   notion.so
   figma.com
   linear.app
   ```
3. Click "Process All Companies"
4. Wait 1-3 minutes for all companies to be processed
5. Download combined CSV/Markdown with all leads

**Pro Tips:**
- Process 5-10 companies at a time for optimal speed
- Mix small and large companies (variety in lead counts)
- Hunter.io free tier: 25 searches total, so plan accordingly

---

## 📂 Output Files

Every generation creates:

### 1. send_sheet.md
**Markdown formatted emails** ready to copy-paste.

Example structure:
```markdown
## Email 1 - John Smith (john@stripe.com)
**Role:** Head of Product
**Company:** Stripe

Subject: Collaboration opportunity

Hi John,

[Personalized email content...]

Best regards,
[Your Name]
---
```

### 2. send_sheet.csv
**Spreadsheet format** with columns:
- Lead Name
- Email Address
- Role
- Company
- Email Subject
- Email Body
- Portfolio URL

**Use cases:**
- Import into Gmail for bulk sending
- Upload to CRM (Salesforce, HubSpot)
- Track responses in Excel/Google Sheets

### 3. Gmail Drafts (if enabled)
**Drafts created in your Gmail account:**
- Subject line populated
- Email body formatted
- Resume attached (if local file provided)
- Portfolio linked in signature

**Review process:**
1. Go to Gmail → Drafts
2. Find emails labeled "LeadFinder AI - [Company]"
3. Review and personalize top leads
4. Click Send when ready

---

## 🔐 Security & Privacy

### What Gets Shared?
- **Hunter.io**: Company domain only (finds public emails)
- **OpenAI**: Your background summary, portfolio URL (generates emails)
- **Gmail**: Draft emails stored in your account (OAuth authorized)

### What Doesn't Get Shared?
- ❌ No emails sent automatically
- ❌ No data stored on external servers
- ❌ No tracking of responses
- ❌ No credit card required (free tier available)

### API Keys
Store in `.env` file (never commit to Git):
```bash
HUNTER_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
```

Add `.env` to `.gitignore` to prevent accidental sharing.

---

## 💡 Best Practices

### Lead Quality
- **Start with 40% confidence filter** in config.yaml
- **Test with known companies** (Airbnb, Stripe, Notion) to verify setup
- **Expect 5-50+ leads** depending on company size

### Email Personalization
- **Leave subject blank** for AI-generated subjects (higher quality)
- **Add portfolio URL** to showcase your work
- **Attach resume** for serious opportunities (local file path)
- **Manually edit top 10 emails** for best response rates

### Sending Strategy
- **Send 10-15 emails per day** to avoid spam filters
- **Stagger sends** throughout the day (morning, afternoon)
- **Follow up after 3-5 days** if no response
- **Track responses** in CSV file or spreadsheet

### Avoiding Spam
- ✅ Use professional email address (Gmail, Outlook)
- ✅ Personalize subject lines
- ✅ Include unsubscribe option if sending bulk
- ✅ Respect response requests (stop if they ask)
- ❌ Don't send 100+ emails in one day
- ❌ Don't use generic templates without customization

---

## 🔧 Advanced Configuration

### config.yaml Settings

```yaml
# Your Details
portfolio_url: https://yourname.com
candidate_background_summary: "Software Engineer with 5 years in ML/AI"
sender_email: your.email@gmail.com

# Email Generation
use_openai_drafts: true  # AI-generated emails (requires OpenAI key)
openai_model: gpt-4o-mini  # Faster, cheaper than GPT-4
min_email_confidence: 40  # Lower = more leads (range: 0-100)

# Domain-Specific Roles
domains:
  product_management:
    target_roles:
      - Founder
      - Chief Product Officer
      - Head of Product
      - VP Product
      - Director of Product
  
  consulting:
    target_roles:
      - Partner
      - Principal
      - Senior Consultant
      - Strategy Lead
  
  # ... add more domains as needed
```

### Customizing Email Templates

Edit `pm_outreach_agent/openai_client.py`:

```python
def generate_email(...):
    prompt = f"""
    Write a professional email for a job seeker reaching out to {lead['name']}.
    
    Details:
    - Recipient: {lead['name']}, {lead['role']} at {lead['company']}
    - Your background: {background_summary}
    - Your portfolio: {portfolio_url}
    
    Requirements:
    - Professional but warm tone
    - 150-200 words
    - Clear value proposition
    - Call to action (schedule call or request meeting)
    - NO subject line in body
    """
```

**Restart Flask app** after changes: `python app.py`

---

## 📈 Scaling Your Outreach

### Free Tier Limits
| Service | Free Tier | Paid Tier |
|---------|-----------|-----------|
| Hunter.io | 25 searches/month | $49/month = 500 searches |
| OpenAI | N/A (pay-per-use) | ~$0.01 per 10 emails |
| Gmail | Unlimited drafts | N/A |

**Monthly free volume**: 25 companies × 10 leads = **250 leads/month**

### Optimization Strategies

**1. Maximize Free Tier**
- Lower confidence filter to 40%
- Target large companies (more leads per search)
- Use batch processing to minimize duplicate searches

**2. Upgrade Hunter.io**
- $49/month = 500 searches = 5,000+ leads
- $99/month = 1,000 searches = 10,000+ leads

**3. Reduce OpenAI Costs**
- Use gpt-4o-mini (10x cheaper than GPT-4)
- Write subjects manually (skip AI subject generation)
- Manually write emails for top 10 leads, use AI for rest

**4. Automate with Scripts**
```bash
# Process companies.csv with 50 companies
python run_agent.py --companies companies.csv --config config.yaml

# Generates ~500+ leads in 5 minutes
```

---

## 🆘 Troubleshooting

### No Leads Found
**Symptoms**: "0 leads found" or "No emails match confidence threshold"

**Solutions**:
- Lower `min_email_confidence` to 40 or 30 in config.yaml
- Try a different company (Airbnb, Stripe, Notion are reliable)
- Check Hunter.io API key is correct
- Verify you haven't exceeded free tier (25 searches/month)

### OpenAI Errors
**Symptoms**: "OpenAI API error" or "Insufficient quota"

**Solutions**:
- Check API key in .env file
- Add credit to OpenAI account (platform.openai.com/account/billing)
- Verify GPT-4o-mini is enabled (default model)
- Set `use_openai_drafts: false` in config.yaml to skip AI (manual emails)

### Gmail Authorization Failed
**Symptoms**: Browser redirect error or "OAuth failed"

**Solutions**:
- **Skip Gmail for now**: Uncheck "Create Gmail Drafts" checkbox
- Use CSV/Markdown exports instead
- Set up OAuth later: See `/setup` guide Step 4
- Delete `token.pickle` and re-authorize

### Low Lead Count
**Symptoms**: Only 1-3 leads from large companies

**Solutions**:
- Lower `min_email_confidence` to 40
- Hunter.io free tier limits results to 10 per search
- Try batch processing (aggregates across multiple searches)
- Upgrade Hunter.io to paid tier

---

## 🎯 Use Cases

### Job Seekers
- **PM roles**: Find CPOs, Heads of Product at Series A-C startups
- **Engineering**: Reach VPs Engineering, CTOs at tech companies
- **Data Science**: Contact ML leads, Data Directors at AI companies

### Recruiters
- **Candidate sourcing**: Find engineers at competitor companies
- **Partnership outreach**: Connect with HR leaders at enterprises
- **Event invitations**: Reach decision-makers for webinars

### Sales Teams
- **B2B SaaS**: Find product leaders at target companies
- **Enterprise sales**: Reach executives at Fortune 500 companies
- **Partnership development**: Connect with BD leaders

---

## 📚 Additional Resources

- **GETTING_STARTED.md**: Checklist-style setup guide
- **FEATURES.md**: Complete feature overview
- **DEPLOYMENT.md**: Deploy to Railway, Heroku, Render
- **EXAMPLES.md**: Multi-domain examples and strategies

---

## 🚀 Next Steps

1. **Complete setup** using the web guide: http://localhost:5000/setup
2. **Test with Airbnb**: `airbnb.com` (15+ leads)
3. **Try batch processing**: Process 5-10 companies at once
4. **Deploy to cloud**: Make it accessible from anywhere (see DEPLOYMENT.md)
5. **Scale your outreach**: Upgrade Hunter.io, automate with scripts

---

**Happy Lead Hunting! 🎯**

Questions? Check the setup guide or create a GitHub issue.
