# Feature Overview 🚀

## What's New in v2.0

### 🎯 Multi-Domain Support
**Before:** Only Product Management roles
**Now:** PM, Consulting, Engineering, Data Science

**How it works:**
- Select domain from dropdown in web UI
- Agent automatically targets domain-specific roles
- Customized email tone per domain

---

## Core Features

### 1. Smart Lead Discovery
- **Hunter.io Integration:** Domain search API
- **Bulk Discovery:** No artificial limits (5-50+ leads per company)
- **Confidence Scoring:** Filter by email verification confidence
- **Role Filtering:** Exclude recruiters, HR, marketing automatically

**Example:**
```
stripe.com → 5 PM leads found
  ✓ Arielle Bail (Head of Product) - 94% confidence
  ✓ John Smith (VP Product) - 88% confidence
  ✓ Sarah Johnson (Senior PM) - 85% confidence
```

---

### 2. AI-Powered Email Generation

**OpenAI Integration (GPT-4o-mini):**
- Personalized job-seeking emails
- Professional, non-spammy tone
- Auto-adjusts based on domain
- Fallback to templates if API fails

**Email Structure:**
1. Brief intro (name + background)
2. Why you're reaching out
3. Specific ask (conversation/advice)
4. Portfolio link

**Sample Email:**
```
Subject: Builder PM (BITS Goa) exploring product fit

Hi Arielle,

I'm Anubhav, a BITS Goa graduate currently working as a Product Manager 
and building AI-powered analytics tools end-to-end.

I've admired how Stripe has scaled while maintaining product clarity, 
and I'm actively exploring PM roles where structured decision-making matters.

Would you be open to a brief conversation about product leadership at Stripe?

Best regards,
Anubhav
https://portfolio-o5n7.onrender.com
```

---

### 3. Gmail Integration

**OAuth2 Flow:**
- One-time authorization
- Creates drafts (never sends)
- Batch creation (all leads at once)
- Human review required

**Security:**
- No automatic sending
- Respects Gmail API limits
- OAuth token stored locally

---

### 4. Export Options

**Markdown Send Sheet:**
- Copy-paste ready emails
- Organized by lead
- Includes all contact details

**CSV Export:**
- Import to Gmail/CRM
- Bulk email tools compatible
- Tracking-friendly

**Example CSV:**
```
Name,Role,Company,Email,Confidence,Subject,Body
Arielle Bail,Head of Product,Stripe,arielle@stripe.com,94,"Builder PM exploring fit","Hi Arielle..."
```

---

### 5. Web Interface

**Flask-based UI:**
- No terminal needed
- Domain selector dropdown
- Company input form
- Gmail draft toggle
- Real-time feedback

**Features:**
- Flash messages (success/error)
- Download links (CSV/MD)
- Lead count summary
- Mobile-responsive

---

### 6. CLI Interface

**For Power Users:**
```bash
# Single company
./run_with_gmail.sh --company "Stripe" --domain "stripe.com"

# Batch processing
python run_agent.py --companies companies.csv --config config.yaml
```

---

## Configuration System

### Global Settings
- `portfolio_url` - Your portfolio/website
- `min_email_confidence` - Filter threshold (default: 80)
- `use_openai_drafts` - Enable AI emails
- `use_gmail_drafts` - Enable Gmail creation

### Domain Profiles

**Product Management:**
- 9 target roles (Founder → PM)
- PM-focused email tone

**Consulting:**
- 7 target roles (Partner → Analyst)
- Strategy/problem-solving emphasis

**Engineering:**
- 6 target roles (CTO → SWE)
- Technical skills focus

**Data Science:**
- 5 target roles (Head of Data → Data Scientist)
- ML/analytics highlight

**Easy Customization:**
```yaml
domains:
  your_domain:
    target_roles:
      - Role 1
      - Role 2
    background: "Your customized background"
```

---

## Technical Architecture

### Stack
- **Backend:** Python 3.12, Flask
- **APIs:** Hunter.io, OpenAI, Gmail API
- **Auth:** OAuth2 (Google)
- **Storage:** Local files (.env, config.yaml)

### Data Flow
```
User Input (Web/CLI)
    ↓
Hunter.io API (Lead Discovery)
    ↓
Lead Filtering (Role + Confidence)
    ↓
OpenAI API (Email Generation)
    ↓
Gmail API (Draft Creation) OR CSV Export
    ↓
Output (Markdown + CSV)
```

### Error Handling
- Hunter API rate limits → Auto-retry with lower limit
- OpenAI failures → Fallback to templates
- Gmail OAuth errors → Export-only mode
- Network issues → Clear error messages

---

## Use Cases

### 1. Active Job Search
**Scenario:** Sending 20-30 emails/week to PM roles

**Workflow:**
1. Select "Product Management" domain
2. Enter 5 dream companies
3. Generate 25+ leads total
4. Review Gmail drafts
5. Send 5-10 personalized emails/day

**Time Saved:** ~3 hours/week (vs manual research)

---

### 2. Career Transition
**Scenario:** PM → Data Science role transition

**Workflow:**
1. Use "Data Science" domain
2. Target data-heavy companies (Netflix, Spotify)
3. Customize email background in config.yaml
4. Generate 10-15 data science leads
5. Highlight analytics projects in emails

---

### 3. Multi-Domain Exploration
**Scenario:** Exploring PM, Consulting, and Data roles

**Workflow:**
1. Run 3 separate searches (same company, different domains)
2. Compare role availability
3. Send to most responsive domain
4. Track responses to refine strategy

---

### 4. Batch Processing
**Scenario:** Outreach to 50 companies at once

**Workflow:**
1. Create `companies.csv` with 50 domains
2. Run: `python run_agent.py --companies companies.csv`
3. Agent processes all companies sequentially
4. Export one master CSV with 200+ leads
5. Filter top 50, send over 2 weeks

---

## Safety Features

✅ **No Auto-Sending:** Gmail drafts only, you click send
✅ **Rate Limit Handling:** Respects Hunter.io free tier
✅ **Professional Tone:** Job-seeking, not spammy cold sales
✅ **Transparent Logs:** See every API call
✅ **Privacy-First:** No data sent to 3rd parties (except APIs)

---

## Performance

**Speed:**
- Lead discovery: 2-5 seconds per company
- Email generation: 1-2 seconds per lead (OpenAI)
- Gmail draft creation: 0.5 seconds per draft
- **Total:** ~30 seconds for 10 leads end-to-end

**Limits:**
- Hunter free tier: 10 leads/request (agent auto-handles)
- OpenAI: No practical limit (rate limits at 10k requests/min)
- Gmail API: 100 drafts/day (more than enough)

---

## Future Roadmap

- [ ] Resume attachment to emails
- [ ] Email tracking/analytics (open rates)
- [ ] LinkedIn integration (manual export)
- [ ] Custom email templates (per domain)
- [ ] Multi-language support
- [ ] Company research integration (Crunchbase)

---

**Your PM Outreach Agent is production-ready! 🎉**

Questions? Check [README.md](README.md), [DEPLOYMENT.md](DEPLOYMENT.md), or [EXAMPLES.md](EXAMPLES.md).
