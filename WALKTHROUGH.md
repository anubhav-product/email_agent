# 🎨 Visual Walkthrough - LeadFinder AI

**Step-by-step visual guide with screenshots and explanations**

---

## 📸 Homepage Tour

### Main Interface
```
┌─────────────────────────────────────────────────┐
│                                                 │
│         🚀 LeadFinder AI                       │
│    Automated outreach agent for job seekers    │
│                                                 │
│    📖 New User? Complete Setup Guide →         │
│                                                 │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│                                                 │
│  📊 STATS DASHBOARD                            │
│  ┌──────┐  ┌──────┐  ┌──────┐                 │
│  │ 10+  │  │  4   │  │  AI  │                 │
│  │Leads │  │Domain│  │Powered│                │
│  └──────┘  └──────┘  └──────┘                 │
│                                                 │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│                                                 │
│  🎯 Career Domain *                            │
│  [Product Management ▼]                        │
│  💡 Choose your target career path             │
│                                                 │
│  🏢 Company Name (Optional)                    │
│  [e.g., Stripe, Airbnb, Google            ]    │
│  Leave blank and we'll detect it               │
│                                                 │
│  🌐 Company Domain *                           │
│  [stripe.com                              ]    │
│  ✨ Try: airbnb.com, notion.so for 10+ leads   │
│                                                 │
│  💼 Your Portfolio URL (Optional)              │
│  [https://yourname.com                    ]    │
│  📎 Added to email signature                   │
│                                                 │
│  📄 Resume (Optional)                          │
│  [URL or /path/to/resume.pdf              ]    │
│  🔗 URL = Link | 📎 Local = Attachment        │
│                                                 │
│  ✉️ Email Subject (Optional)                   │
│  [Leave blank for AI-generated subjects   ]    │
│  🤖 AI creates personalized subjects           │
│                                                 │
│  ☐ Create Gmail Drafts (requires OAuth)       │
│                                                 │
│  [ 🚀 Generate Leads & Drafts ]                │
│                                                 │
│  📊 Batch Process Multiple Companies →         │
│                                                 │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│                                                 │
│  FEATURES                                      │
│  🔍 Smart Discovery   🤖 AI Email Writer       │
│  📧 Gmail Drafts      📊 Export CSV            │
│                                                 │
│  🔒 100% Safe: No auto-send. Human review.     │
│  Powered by Hunter.io, OpenAI, Gmail API       │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## 🎯 Step-by-Step Usage

### Step 1: Choose Your Domain
Click the **Career Domain** dropdown to select your target industry.

**Available Options:**
- 🎯 **Product Management** → Finds CPOs, Heads of Product, VPs
- 💼 **Consulting & Strategy** → Finds Partners, Principals
- 💻 **Software Engineering** → Finds VPs Engineering, CTOs
- 📊 **Data Science & Analytics** → Finds Data Directors, ML leads

**Why it matters**: Each domain targets different roles. PM searches for product leaders, Engineering searches for tech leaders.

---

### Step 2: Enter Company Information

**Company Name** (Optional)
```
Example: Stripe
Leave blank → Auto-detected from domain
```

**Company Domain** (Required)
```
✅ Good: stripe.com, airbnb.com, notion.so
❌ Bad: https://stripe.com, www.stripe.com
```

**Pro Tip**: Use the base domain only, no protocols or www.

---

### Step 3: Add Your Details (Optional)

**Portfolio URL**
```
Example: https://yourportfolio.com
Result: Linked in email signature
Benefit: Showcases your work to leads
```

**Resume**
```
Option 1 (URL): https://drive.google.com/your-resume
→ Result: Link added to email body

Option 2 (Local): /Users/you/Desktop/resume.pdf
→ Result: Attached to Gmail drafts
→ Note: Only works with Gmail Drafts enabled
```

---

### Step 4: Customize Subject (Optional)

**Leave Blank** (Recommended)
```
AI generates personalized subjects like:
- "Collaboration opportunity at Stripe"
- "Exploring PM roles at your team"
- "Quick intro from [Your Name]"
```

**Custom Subject**
```
Example: "Product Manager with 5 years ML experience"
Result: Same subject for all leads
Use when: You have a tested subject line
```

---

### Step 5: Gmail Drafts Checkbox

**Unchecked** (Default)
```
✅ CSV and Markdown files generated
✅ No Gmail authorization needed
✅ Manual sending from your email client
```

**Checked** (Requires OAuth)
```
✅ Automatic Gmail draft creation
✅ Resume attached (if local file)
✅ Ready to review and send
⚠️ First use: Browser opens for authorization
```

**When to use Gmail Drafts**:
- You want fastest workflow (draft → review → send)
- You have resume to attach
- You're comfortable with OAuth

**When to skip Gmail Drafts**:
- First-time user (learn the flow first)
- You prefer manual email clients
- No resume to attach

---

### Step 6: Click Generate

```
[ 🚀 Generate Leads & Drafts ]
      ↓
  Loading...
  (10-30 seconds)
      ↓
  Results Page
```

**What happens behind the scenes**:
1. Hunter.io searches company domain
2. Finds decision-makers matching your domain
3. OpenAI generates personalized emails
4. Creates Gmail drafts (if enabled)
5. Exports CSV and Markdown files

---

## 📊 Results Page Tour

### Success Screen
```
┌─────────────────────────────────────────────────┐
│                                                 │
│              ✅ Success!                        │
│                  15                             │
│    High-quality leads generated                 │
│                                                 │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│                   🎉                            │
│                                                 │
│  [ 📊 Download CSV ]  [ 📄 Download Markdown ] │
│                                                 │
│  📧 Email Preview (First Lead)                 │
│  ┌───────────────────────────────────────────┐ │
│  │ Subject: Collaboration opportunity         │ │
│  │                                            │ │
│  │ Hi John,                                   │ │
│  │                                            │ │
│  │ I came across Stripe's approach to...      │ │
│  │ [Preview shows first 500 characters]       │ │
│  └───────────────────────────────────────────┘ │
│                                                 │
│  💡 Next Steps:                                │
│  ✅ Review all emails in send_sheet.md         │
│  ✅ Personalize top 5-10 emails                │
│  ✅ Check Gmail drafts if created              │
│  ✅ Send 10-15 emails per day                  │
│  ✅ Follow up after 3-5 days                   │
│                                                 │
│  ← Generate More Leads | 📊 Batch Process      │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## 📂 Output Files Explained

### send_sheet.md (Markdown Format)
```markdown
# Send Sheet - Stripe - 2026-01-30

Generated 15 leads

---

## Email 1 - John Smith (john@stripe.com)
**Role:** Head of Product
**Company:** Stripe

Subject: Collaboration opportunity at Stripe

Hi John,

I came across Stripe's innovative approach to payment processing
and was impressed by your work on [recent product].

I'm a Product Manager with 5 years of experience in fintech,
currently building [your project]. I'd love to explore opportunities
to contribute to your team.

Would you be open to a brief call next week?

Portfolio: https://yourportfolio.com

Best regards,
[Your Name]

---

## Email 2 - Sarah Johnson (sarah@stripe.com)
...
```

**How to use**:
1. Open in any text editor
2. Copy individual emails
3. Paste into Gmail/Outlook
4. Personalize and send

---

### send_sheet.csv (Spreadsheet Format)
```csv
Lead Name,Email,Role,Company,Subject,Body,Portfolio
John Smith,john@stripe.com,Head of Product,Stripe,Collaboration opportunity,...,https://...
Sarah Johnson,sarah@stripe.com,VP Product,Stripe,Quick intro,...,https://...
```

**How to use**:
1. Open in Excel or Google Sheets
2. Filter by role or company
3. Import into Gmail using mail merge tools
4. Track responses in new column

---

### Gmail Drafts (if enabled)
```
Gmail → Drafts → Search "LeadFinder"

Draft 1: john@stripe.com
Subject: Collaboration opportunity at Stripe
Attachments: resume.pdf (if local file provided)

[Ready to review and send]
```

**How to use**:
1. Go to Gmail → Drafts
2. Find emails labeled "LeadFinder AI"
3. Review email body
4. Personalize top 5-10 leads
5. Click Send when ready

---

## 🔁 Batch Processing Walkthrough

### Batch Page Interface
```
┌─────────────────────────────────────────────────┐
│                                                 │
│         🚀 Batch Processing                     │
│      Process multiple companies at once         │
│                                                 │
│  ← Back to Single Company                      │
│                                                 │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│                                                 │
│  📝 Enter Company Domains                      │
│  One per line (5-20 companies recommended)     │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │ stripe.com                                 │ │
│  │ airbnb.com                                 │ │
│  │ notion.so                                  │ │
│  │ figma.com                                  │ │
│  │ linear.app                                 │ │
│  │                                            │ │
│  │                                            │ │
│  └───────────────────────────────────────────┘ │
│                                                 │
│  [ 🚀 Process All Companies ]                  │
│                                                 │
│  💡 Pro Tips:                                  │
│  • 5-10 companies = optimal speed              │
│  • Mix small/large for variety                 │
│  • Free tier: 25 searches total                │
│                                                 │
└─────────────────────────────────────────────────┘
```

**Batch Process Results**:
```
✅ Success! 73 leads generated

Combined files created:
- send_sheet.csv (all 73 leads)
- send_sheet.md (all emails)

Breakdown:
- Stripe: 12 leads
- Airbnb: 18 leads
- Notion: 15 leads
- Figma: 14 leads
- Linear: 14 leads
```

---

## 🛠️ Setup Guide Walkthrough

### Step 1: Hunter.io API
```
┌─────────────────────────────────────────────────┐
│  📝 Step 1: Get Hunter.io API Key              │
│                                                 │
│  1. Go to hunter.io/users/sign_up              │
│  2. Sign up (no credit card)                   │
│  3. Navigate to API → API Keys                 │
│  4. Copy your API key                          │
│                                                 │
│  ⚠️ Free Tier Limits:                          │
│  25 searches/month = 250 leads/month           │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Step 2: OpenAI API
```
┌─────────────────────────────────────────────────┐
│  🤖 Step 2: Get OpenAI API Key (Optional)      │
│                                                 │
│  1. Go to platform.openai.com/signup           │
│  2. Add $5-10 credit                           │
│  3. Create API key                             │
│  4. Copy and save securely                     │
│                                                 │
│  💰 Cost: ~$0.01 per 10 emails                 │
│  Model: GPT-4o-mini (10x cheaper than GPT-4)   │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Step 3: Configuration
```
┌─────────────────────────────────────────────────┐
│  ⚙️ Step 3: Configure .env and config.yaml     │
│                                                 │
│  Create .env file:                             │
│  ┌───────────────────────────────────────────┐ │
│  │ HUNTER_API_KEY=your_hunter_key            │ │
│  │ OPENAI_API_KEY=your_openai_key            │ │
│  └───────────────────────────────────────────┘ │
│                                                 │
│  Edit config.yaml:                             │
│  ┌───────────────────────────────────────────┐ │
│  │ portfolio_url: https://yourname.com       │ │
│  │ sender_email: you@gmail.com               │ │
│  │ min_email_confidence: 40                  │ │
│  └───────────────────────────────────────────┘ │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Step 4: Gmail OAuth (Optional)
```
┌─────────────────────────────────────────────────┐
│  📧 Step 4: Gmail OAuth Setup (Optional)       │
│                                                 │
│  1. Go to console.cloud.google.com             │
│  2. Create project: "LeadFinder AI"            │
│  3. Enable Gmail API                           │
│  4. Create OAuth 2.0 Client ID (Desktop)       │
│  5. Download credentials.json                  │
│  6. Place in project root                      │
│                                                 │
│  ⚠️ Skip if you just want CSV exports          │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Step 5: Test Run
```
┌─────────────────────────────────────────────────┐
│  🎯 Step 5: Test Your Setup                    │
│                                                 │
│  Test Configuration:                           │
│  • Domain: Product Management                  │
│  • Company: Airbnb                             │
│  • Domain: airbnb.com                          │
│  • Gmail Drafts: Unchecked (first test)        │
│                                                 │
│  Expected Result: 10-20 leads                  │
│                                                 │
│  [ 🚀 Run Test ]                               │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## 🎯 Common Workflows

### Workflow 1: Job Seeker (PM Roles)
```
1. Homepage → Select "Product Management"
2. Enter: airbnb.com
3. Add: Your portfolio URL
4. Leave subject blank (AI generates)
5. Uncheck Gmail Drafts (manual send)
6. Generate → 15 leads
7. Download Markdown
8. Personalize top 5 emails
9. Send 5-10 per day from Gmail
10. Follow up after 3 days
```

### Workflow 2: Recruiter (Sourcing Engineers)
```
1. Homepage → Select "Software Engineering"
2. Batch Process → 10 tech companies
3. Add: Company careers page URL
4. Check Gmail Drafts (fast workflow)
5. Generate → 80+ leads across all companies
6. Gmail Drafts → Sort by company
7. Review and send top 20
8. Import CSV to Salesforce
```

### Workflow 3: Sales Team (B2B Outreach)
```
1. Homepage → Select "Product Management"
2. Enter: Target company domain
3. Custom subject: "Partnership opportunity"
4. Add: Company deck URL
5. Check Gmail Drafts
6. Generate → 10 leads
7. Review all drafts
8. Personalize subject lines
9. Send immediately
10. Track in CRM
```

---

## 📈 Optimization Tips

### Maximizing Lead Count
```
Before:
min_email_confidence: 80
Company: stripe.com
Result: 1-2 leads

After:
min_email_confidence: 40
Company: stripe.com
Result: 5-7 leads
```

**Recommendation**: Start at 40, increase to 60 if too many bounces.

---

### AI Subject Quality
```
Bad Custom: "Job Application"
→ Generic, low open rate

Good Custom: "5 years PM experience - exploring opportunities"
→ Specific, shows value

Best (AI): "Collaboration on payment processing initiatives"
→ Personalized, contextual, high open rate
```

**Recommendation**: Leave blank for AI unless you have tested subject.

---

### Batch vs. Single
```
Single Processing:
- 1 company at a time
- 10-30 seconds per company
- Good for: Testing, specific targets

Batch Processing:
- 5-20 companies at once
- 1-3 minutes total
- Good for: Scaling, weekly campaigns
```

**Recommendation**: Single for first 5 companies, then switch to batch.

---

## ✅ Success Checklist

After setup, verify:
- [ ] Homepage loads at http://localhost:5000
- [ ] Setup guide accessible
- [ ] Test run with Airbnb returns 10+ leads
- [ ] CSV downloads successfully
- [ ] Markdown file contains formatted emails
- [ ] Gmail drafts created (if enabled)
- [ ] No errors in terminal

If all checked → You're ready to scale! 🚀

---

**Questions?** See USER_GUIDE.md for detailed explanations.
