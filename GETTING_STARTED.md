# 🚀 Getting Started Checklist

Welcome to LeadFinder AI! Follow this checklist to get up and running in 5 minutes.

---

## ✅ Pre-Flight Checklist

### Step 1: Install & Run (2 minutes)
- [ ] Clone repository: `git clone <repo-url>`
- [ ] Create virtual environment: `python -m venv venv`
- [ ] Activate environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Start Flask app: `python app.py`
- [ ] Open browser: http://localhost:5000

---

### Step 2: Get API Keys (3 minutes)

#### Hunter.io (Required - Free)
- [ ] Go to https://hunter.io/users/sign_up
- [ ] Sign up (no credit card needed)
- [ ] Navigate to **API** → **API Keys**
- [ ] Copy your API key
- [ ] **Free Tier**: 25 searches/month, 10 leads per search = 250 leads/month

#### OpenAI (Optional - $0.01 per 10 emails)
- [ ] Go to https://platform.openai.com/signup
- [ ] Add $5-10 credit (if you want AI-generated emails)
- [ ] Go to **API Keys** → **Create new secret key**
- [ ] Copy your API key
- [ ] **Cost**: ~$0.01 per 10 emails with GPT-4o-mini

---

### Step 3: Configure (1 minute)
- [ ] Create `.env` file in project root
- [ ] Add this content:
```bash
HUNTER_API_KEY=your_hunter_key_here
OPENAI_API_KEY=your_openai_key_here
```
- [ ] Edit `config.yaml`:
```yaml
portfolio_url: https://your-portfolio.com  # Your portfolio/website
candidate_background_summary: "Your Name, building X at Y"
sender_email: your.email@gmail.com
min_email_confidence: 40  # Lower = more leads
```

---

### Step 4: Gmail OAuth (Optional - 2 minutes)
Only needed if you want automatic Gmail draft creation.

- [ ] Go to https://console.cloud.google.com
- [ ] Create new project: "LeadFinder AI"
- [ ] Enable **Gmail API**
- [ ] Create **OAuth 2.0 Client ID** (Desktop app)
- [ ] Download `credentials.json` to project root
- [ ] First run will open browser for authorization
- [ ] Click "Gmail Drafts" checkbox when generating leads

**Skip this if you just want CSV/Markdown exports.**

---

### Step 5: Test Run (30 seconds)
- [ ] Go to http://localhost:5000
- [ ] Select domain: **Product Management**
- [ ] Enter company: **Airbnb**
- [ ] Enter domain: **airbnb.com**
- [ ] Leave portfolio/resume blank for now
- [ ] Leave subject blank (AI will generate it)
- [ ] **Don't** check Gmail Drafts (skip OAuth for first test)
- [ ] Click **Generate Leads & Drafts**
- [ ] Wait 10-20 seconds
- [ ] You should see 5-15+ leads!
- [ ] Download CSV or Markdown

---

## 🎯 What You Should See

### Success Indicators:
✅ **Lead Count**: 5-20+ leads (varies by company size)  
✅ **Download Buttons**: CSV and Markdown available  
✅ **Email Preview**: See personalized email sample  
✅ **No Errors**: Clean success page with tips  

### Common Issues:

**"No leads found"**
- Try a different company (Airbnb, Stripe, Notion work well)
- Lower `min_email_confidence` in config.yaml to 30-40
- Check Hunter.io API key is correct

**"OpenAI error"**
- Check API key in .env
- Verify you have credit balance at platform.openai.com
- AI emails are optional - you can write manually

**"Gmail authorization failed"**
- Skip Gmail for now (uncheck the box)
- Use CSV/Markdown exports instead
- Set up OAuth later when comfortable

---

## 🚀 Next Steps

Once your test run succeeds:

1. **Process Multiple Companies**: Click "Batch Process" link
2. **Generate More Leads**: Try different domains (PM, Consulting, Engineering, Data Science)
3. **Set Up Gmail**: Enable automatic draft creation
4. **Customize Emails**: Edit templates in `pm_outreach_agent/openai_client.py`
5. **Deploy to Cloud**: See DEPLOYMENT.md for Railway/Heroku guides

---

## 📊 Usage Tips

### Maximizing Lead Volume:
- **Lower confidence filter**: Set `min_email_confidence: 40` in config.yaml
- **Try larger companies**: Airbnb (15+ leads), Google (50+), Microsoft (100+)
- **Process in batches**: Use batch processing for 5-20 companies at once

### Best Practices:
- **Review before sending**: Always check emails for personalization
- **Send 10-15 per day**: Avoid spam filters
- **Follow up**: Reply after 3-5 days if no response
- **Customize top emails**: Personalize your top 5-10 leads
- **Track responses**: Use CSV to log who replies

---

## 🆘 Need Help?

- **Setup Guide**: Click "New User? Complete Setup Guide" on homepage
- **Documentation**: See README.md, FEATURES.md, DEPLOYMENT.md
- **Issues**: Check GitHub Issues or create a new one

---

**Happy Lead Hunting! 🎯**
