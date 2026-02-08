# PM Outreach Agent 🚀

**Automated lead discovery and personalized email generation for Product Management, Consulting, Engineering, and Data Science job seekers.**

Scale your job search with AI-powered outreach that discovers decision-makers, generates professional emails, and creates Gmail drafts—while keeping you in full control.

---

## 🆕 **New Users Start Here!**

**Never used this before?** Follow our interactive setup guide:

1. **Start the web app:**
   ```bash
   python app.py
   ```

2. **Open http://localhost:5000** in your browser

3. **Click "📖 New User? Complete Setup Guide →"** at the top

4. **Follow the 5-step wizard** to:
   - Get Hunter.io API key (free)
   - Get OpenAI API key (optional)
   - Configure .env and config.yaml
   - Set up Gmail OAuth (optional)
   - Test your first lead generation

**Setup takes 5 minutes.** The guide includes direct links, code snippets, and cost breakdowns.

---

## ✨ Features

- 🎯 **Multi-Domain Support** - Target PM, Consulting, Engineering, or Data Science roles
- 🔍 **Smart Lead Discovery** - Finds leaders at target companies using Hunter.io
- 🤖 **AI Email Generation** - Creates personalized, job-seeking emails via OpenAI
- 📧 **Gmail Integration** - Auto-creates drafts (never sends automatically)
- 📊 **Bulk Lead Generation** - No artificial limits (find 5, 10, or 50+ leads per company)
- 📈 **Export Options** - Markdown and CSV send sheets for bulk outreach
- 🌐 **Web Interface** - Easy-to-use Flask app (no terminal needed)
- 🔒 **Privacy-First** - No auto-sending, human review required
- 💼 **Professional Tone** - Job-seeking emails that work

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Hunter.io API key (free tier: 10 leads/month)
- OpenAI API key (optional, for AI drafts)
- Gmail account (optional, for draft creation)

---

## 📚 Documentation

- **[FEATURES.md](FEATURES.md)** - Complete feature overview and technical architecture
- **[EXAMPLES.md](EXAMPLES.md)** - Multi-domain examples and workflow strategies  
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production deployment guide (Railway, Heroku, Render)

---

### Installation

```bash
# Clone the repository
git clone https://github.com/anubhav-product/email_agent.git
cd email_agent

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and add your API keys
```

### Configuration

Edit `config.yaml`:

```yaml
# Your details
portfolio_url: https://your-portfolio.com
candidate_background_summary: "Your Name, building AI/ML solutions"
sender_email: your.email@gmail.com

# General settings
use_openai_drafts: true
openai_model: gpt-4o-mini

# Domain-specific role profiles
domains:
  product_management:
    target_roles:
      - Founder
      - Head of Product
      - Chief Product Officer
      - VP Product
      - Senior Product Manager
      
  consulting:
    target_roles:
      - Partner
      - Principal
      - Senior Consultant
source venv/bin/activate  # Activate virtual environment
python app.py
```

Open http://localhost:5000 in your browser. Select your target domain (PM/Consulting/Engineering/Data Science), enter company details, click generate, and review your drafts.

**No Limits:** The agent finds ALL matching leads (minimum 5 recommended, maximum unlimited based on company size)
      - VP Engineering
      - Senior Software Engineer
      
  data_science:
    target_roles:
      - Head of Data
      - Data Science Manager
```

---

## 💻 Usage

### Option 1: Web Interface (Recommended)

```bash
python app.py
```

Open http://localhost:5000 in your browser. Enter company details, click generate, and review your drafts.

### Option 2: Command Line

**Single company:**
```bash
./run_with_gmail.sh --company "Stripe" --domain "stripe.com" --config config.yaml
```

**Multiple companies (CSV):**
```bash
python run_agent.py --companies companies.csv --config config.yaml
```

**Without Gmail (generate send sheets only):**
```bash
python run_agent.py --company "Airbnb" --domain "airbnb.com" --config config.yaml
```

---

## 📂 Outputs

Every run generates:

1. **send_sheet.md** - Copy-paste ready emails
2. **send_sheet.csv** - Bulk import for Gmail/CRM
3. **Gmail Drafts** (optional) - Review and send from Gmail
4. **Terminal Summary** - Lead count and top contacts

---

## 🔐 Gmail Setup (Optional)

For automatic draft creation:

1. **Enable Gmail API**
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create project → Enable Gmail API
   - Create OAuth client (Desktop app)
   - Download credentials as `credentials.json`

2. **First Run Authorization**
   - The agent will show a URL
   - Open it, authorize the app
   - Copy the redirect URL back
   - Token saved for future runs

---

## 📊 Example Output

```markdown
## Email 1: Arielle Bail — Stripe

**Role:** Head of Product
**Email:** arielle@stripe.com
**Confidence:** 94

**Subject:** Builder PM (BITS Goa) exploring product fit

Hi Arielle,

I'm Anubhav, a BITS Goa graduate currently working as a Product Manager 
and building AI-powered product analytics and decision-support tools end-to-end.

I've admired how Stripe has scaled while maintaining product clarity and 
technical depth, and I'm actively exploring PM roles where structured 
decision-making and impact matter.

I'd really appreciate learning how you think about product leadership and 
decision-making as Stripe continues to grow.

Best regards,
Anubhav
Portfolio: https://portfolio-o5n7.onrender.com
```

---

## 🎯 Use Cases

- **Targeted Outreach** - Reach PM leaders at dream companies
- **Scale Job Search** - Generate 10-50+ personalized emails daily
- **Career Transitions** - Professional intro for PM role seekers
- **Networking** - Build relationships with product leaders

---

## 🛡️ Safety & Ethics

- ✅ No automatic sending (human review required)
- ✅ Respects Hunter.io rate limits
- ✅ Professional, non-spammy tone
- ✅ No LinkedIn scraping
- ✅ Transparent logging
- ❌ Never bypasses email verification

---

## 🌐 Deployment

Ready to make it live? Deploy to production with Railway, Heroku, Render, or Google Cloud Run.

**Quick Deploy to Railway:**
```bash
# Push to GitHub
git init
git add .
git commit -m "Initial commit"
git push

# Deploy via Railway Dashboard
# 1. Go to railway.app
# 2. Connect GitHub repo
# 3. Add env variables (HUNTER_API_KEY, OPENAI_API_KEY)
# 4. Deploy!
```

**📚 Full deployment guide:** See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

---

## 🔧 Troubleshooting

**Hunter returns 400 error:**
- Free tier limited to 10 leads per request
- Agent auto-retries with limit=10

**0 leads after filtering:**
- Company may not have target roles publicly listed
- Try lowering `min_email_confidence` in config.yaml
- Use larger companies (Stripe, Airbnb, Notion)

**Gmail OAuth fails:**
- Ensure `credentials.json` is in project root
- Check redirect URI is set to `http://localhost`
- Run from terminal for OAuth flow

**OpenAI errors:**
- Falls back to template emails automatically
- Check API key in `.env`
- Verify sufficient credits

---

## 📝 License

MIT License - feel free to use for personal job search or commercial purposes.

---

## 🤝 Contributing

Contributions welcome! Open an issue or PR for:
- New domain profiles (Finance, Marketing, etc.)
- Better email templates
- Additional export formats
- UI improvements

---

**Built with ❤️ for PM job seekers**
---

## 📈 Roadmap

- [ ] LinkedIn integration (manual upload)
- [ ] Resume attachment support
- [ ] Multi-domain batch processing
- [ ] Email tracking/analytics
- [ ] Custom email templates
- [ ] Deployment guide (Heroku/Railway)

---

## 🤝 Contributing

Pull requests welcome! Please:
1. Fork the repo
2. Create feature branch
3. Add tests if applicable
4. Submit PR with description

---

## 📄 License

MIT License - see LICENSE file

---

## 💡 Tips for Success

1. **Research First** - Only target companies you genuinely admire
2. **Customize Portfolio** - Keep your portfolio updated and relevant
3. **Follow Up** - Use send sheets to track and follow up after 1 week
4. **Quality > Quantity** - 10 thoughtful emails > 100 generic ones
5. **Test Templates** - Review first few drafts before scaling

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/anubhav-product/email_agent/issues)
- **Discussions:** [GitHub Discussions](https://github.com/anubhav-product/email_agent/discussions)

---

**Built with ❤️ for PM job seekers by PMs**
