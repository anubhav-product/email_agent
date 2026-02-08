# Production Readiness Checklist ✅

Use this checklist before deploying to production or sharing with others.

---

## Pre-Deployment Checklist

### 1. Code & Configuration

- [x] Virtual environment created (`venv/`)
- [x] All dependencies in `requirements.txt`
- [x] `gunicorn` added to requirements.txt
- [x] `.env.example` created (no secrets)
- [x] `.gitignore` includes `.env`, `token.json`, `credentials.json`
- [x] `config.yaml` has placeholder values
- [x] Multi-domain profiles configured

### 2. API Keys & Secrets

- [ ] Hunter.io API key obtained (free tier: https://hunter.io/api)
- [ ] OpenAI API key obtained (https://platform.openai.com/api-keys)
- [ ] Keys added to `.env` file
- [ ] `.env` file NOT committed to git
- [ ] Gmail OAuth credentials downloaded (optional)

**Security Check:**
```bash
# Verify .env is ignored
git status  # Should NOT show .env

# Verify no secrets in config.yaml
grep -i "api" config.yaml  # Should show placeholders only
```

### 3. Documentation

- [x] README.md updated with multi-domain features
- [x] FEATURES.md created (feature overview)
- [x] EXAMPLES.md created (domain examples)
- [x] DEPLOYMENT.md created (deployment guide)
- [x] License added (MIT)

### 4. Deployment Files

- [x] `Procfile` created (Heroku)
- [x] `runtime.txt` created (Python version)
- [x] `railway.json` created (Railway config)

### 5. Testing

**Local Testing:**
- [ ] Web app runs: `python app.py`
- [ ] Domain selector shows 4 options
- [ ] Lead generation works (test with Stripe)
- [ ] CSV/Markdown exports created
- [ ] No console errors in browser

**Production Testing (after deploy):**
- [ ] Web app accessible via public URL
- [ ] Environment variables loaded correctly
- [ ] Hunter API calls succeed
- [ ] OpenAI email generation works
- [ ] Error messages display properly

---

## Deployment Steps

### Option 1: Railway (Recommended)

- [ ] Code pushed to GitHub
- [ ] Railway project created
- [ ] GitHub repo connected
- [ ] Environment variables set:
  - [ ] `HUNTER_API_KEY`
  - [ ] `OPENAI_API_KEY`
- [ ] Deployment successful
- [ ] Public URL generated
- [ ] Test deployment with sample company

### Option 2: Heroku

- [ ] Heroku CLI installed
- [ ] App created: `heroku create app-name`
- [ ] Config vars set:
  - [ ] `heroku config:set HUNTER_API_KEY=...`
  - [ ] `heroku config:set OPENAI_API_KEY=...`
- [ ] Pushed to Heroku: `git push heroku main`
- [ ] App opened: `heroku open`
- [ ] Logs checked: `heroku logs --tail`

### Option 3: Render

- [ ] Render account created
- [ ] Web service created from GitHub
- [ ] Build command set: `pip install -r requirements.txt`
- [ ] Start command set: `gunicorn app:app`
- [ ] Environment variables added
- [ ] Deployment triggered

---

## Post-Deployment

### 1. Smoke Tests

Test each domain:

**Product Management:**
```
Company: Stripe
Domain: stripe.com
Expected: 3-5 PM leads
```

**Consulting:**
```
Company: McKinsey
Domain: mckinsey.com
Expected: 2-4 consulting leads
```

**Engineering:**
```
Company: Google
Domain: google.com
Expected: 5+ engineering leads
```

**Data Science:**
```
Company: Netflix
Domain: netflix.com
Expected: 2-3 data science leads
```

### 2. Performance Check

- [ ] Response time < 30 seconds for 10 leads
- [ ] No timeout errors
- [ ] CSV downloads work
- [ ] Flash messages appear correctly

### 3. Error Handling

Test edge cases:
- [ ] Invalid domain → Shows error message
- [ ] No leads found → Helpful message
- [ ] Hunter API limit hit → Falls back to limit=10
- [ ] OpenAI failure → Falls back to template emails

### 4. Security Review

- [ ] No API keys visible in browser
- [ ] No credentials in source code
- [ ] HTTPS enabled (auto on Railway/Heroku/Render)
- [ ] Rate limiting considered (optional)

---

## Sharing with Others

### For Public Use

- [ ] Update `config.yaml` with generic placeholder values
- [ ] Remove personal portfolio URL
- [ ] Add `.env.example` with variable names only
- [ ] Update README with setup instructions
- [ ] Add MIT license
- [ ] Create GitHub repo (optional)

### For Team Use

- [ ] Share deployment URL
- [ ] Provide API keys securely (1Password/Bitwarden)
- [ ] Document domain customization process
- [ ] Set up monitoring (optional)

---

## Monitoring & Maintenance

### Logs

**Railway:**
```bash
railway logs
```

**Heroku:**
```bash
heroku logs --tail
```

**Render:**
Dashboard → Logs tab

### Alerts

Optional monitoring:
- [ ] Uptime monitoring (UptimeRobot)
- [ ] Error tracking (Sentry)
- [ ] API usage tracking (Hunter.io dashboard)

### Updates

- [ ] Monthly API key rotation
- [ ] Quarterly dependency updates: `pip list --outdated`
- [ ] Hunter.io quota check (free tier: 50 searches/month)

---

## Troubleshooting Common Issues

### "Module not found" error
**Fix:** Add missing package to `requirements.txt`

### "Application Error" on deployment
**Fix:** Check logs for missing environment variables

### Hunter API returns 0 leads
**Fix:** 
1. Try larger companies (Stripe, Airbnb)
2. Lower `min_email_confidence` in config
3. Check domain spelling

### Gmail OAuth not working in production
**Expected:** OAuth requires browser; disable `use_gmail_drafts` for production

### Slow response times
**Fix:**
1. Hunter API is inherently slow (5-10 sec)
2. Consider adding loading spinner
3. Implement background jobs (advanced)

---

## Success Metrics

Track these after deployment:

- [ ] Number of searches performed
- [ ] Average leads per search
- [ ] Email response rate (manual tracking)
- [ ] User feedback collected
- [ ] Error rate < 5%

---

## Final Pre-Launch Check

- [ ] All tests pass
- [ ] Documentation complete
- [ ] Deployment successful
- [ ] Public URL works
- [ ] Error handling verified
- [ ] Security reviewed
- [ ] Performance acceptable
- [ ] Ready to share! 🎉

---

**Your PM Outreach Agent is production-ready!**

Share the URL, update your resume/portfolio, or use it for your own job search. Good luck! 🚀
