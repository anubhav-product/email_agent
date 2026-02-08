# Deployment Guide 🚀

This guide covers deploying the PM Outreach Agent to production.

---

## Deployment Options

### Option 1: Railway (Recommended for Beginners)

Railway offers a simple deployment with generous free tier.

**Steps:**

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/email_agent.git
   git push -u origin main
   ```

2. **Deploy to Railway**
   - Go to [railway.app](https://railway.app)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your `email_agent` repository
   - Railway auto-detects `railway.json` and starts deployment

3. **Configure Environment Variables**
   - In Railway dashboard → Variables
   - Add:
     - `HUNTER_API_KEY` = your_hunter_key
     - `OPENAI_API_KEY` = your_openai_key
   - Click "Deploy"

4. **Get Your Live URL**
   - Railway auto-generates a URL like `https://email-agent-production.up.railway.app`
   - Open it to access your agent!

**Pricing:** Free tier includes 500 hours/month (~$5 after)

---

### Option 2: Heroku

Classic platform with extensive documentation.

**Steps:**

1. **Install Heroku CLI**
   ```bash
   curl https://cli-assets.heroku.com/install.sh | sh
   heroku login
   ```

2. **Create Heroku App**
   ```bash
   heroku create your-app-name
   ```

3. **Set Environment Variables**
   ```bash
   heroku config:set HUNTER_API_KEY=your_key
   heroku config:set OPENAI_API_KEY=your_key
   ```

4. **Deploy**
   ```bash
   git push heroku main
   heroku open
   ```

**Files Required:**
- `Procfile` ✅ (already included)
- `runtime.txt` ✅ (already included)
- `requirements.txt` ✅ (already included)

**Pricing:** Hobby tier ~$7/month

---

### Option 3: Render

Modern alternative with free tier.

**Steps:**

1. **Connect GitHub**
   - Go to [render.com](https://render.com)
   - Click "New Web Service"
   - Connect your GitHub repo

2. **Configure Build**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Environment:** Python 3

3. **Add Environment Variables**
   - `HUNTER_API_KEY`
   - `OPENAI_API_KEY`

4. **Deploy**
   - Click "Create Web Service"
   - Wait 2-3 minutes for deployment

**Pricing:** Free tier (750 hours/month)

---

### Option 4: Google Cloud Run (Serverless)

Best for production-scale apps with variable traffic.

**Steps:**

1. **Install gcloud CLI**
   ```bash
   curl https://sdk.cloud.google.com | bash
   gcloud auth login
   ```

2. **Create Dockerfile**
   ```dockerfile
   FROM python:3.12-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080"]
   ```

3. **Deploy**
   ```bash
   gcloud run deploy email-agent --source .
   ```

**Pricing:** Pay-per-request (free tier: 2M requests/month)

---

## Post-Deployment Setup

### 1. Gmail OAuth for Production

**Important:** OAuth with `credentials.json` won't work in production (requires browser).

**Solution:**

1. Generate a **Service Account** in Google Cloud Console
2. Download service account JSON
3. Set `GOOGLE_APPLICATION_CREDENTIALS` env var
4. OR disable Gmail drafts for production (users export CSV instead)

### 2. Environment Variables Checklist

Ensure these are set in your deployment platform:

- ✅ `HUNTER_API_KEY`
- ✅ `OPENAI_API_KEY`
- ❌ `GOOGLE_APPLICATION_CREDENTIALS` (optional)

### 3. Security Best Practices

- Never commit `.env` file to GitHub
- Use platform secrets management (Railway Variables, Heroku Config Vars)
- Rotate API keys every 90 days
- Add rate limiting (e.g., Flask-Limiter)

---

## Monitoring & Logs

**Railway:**
```bash
# View logs
railway logs
```

**Heroku:**
```bash
# View logs
heroku logs --tail
```

**Render:**
- Check dashboard → Logs tab

---

## Scaling Recommendations

- **Free Tier:** Railway/Render (good for personal use, 10-50 searches/day)
- **Small Scale:** Heroku Hobby ($7/month, 100+ searches/day)
- **Large Scale:** Google Cloud Run (pay-per-use, unlimited scale)

---

## Troubleshooting

**"Application Error" on first visit:**
- Check logs for missing env variables
- Verify `gunicorn` is in requirements.txt ✅

**Gmail OAuth not working:**
- Expected in production; disable `use_gmail_drafts` in config.yaml
- Users can download CSV and import to Gmail manually

**Slow response times:**
- Hunter.io API can take 5-10 seconds per request
- Consider adding a loading spinner in UI
- Implement background jobs with Celery (advanced)

---

## Custom Domain (Optional)

**Railway:**
- Settings → Networking → Custom Domain
- Add CNAME record: `cname.railway.app`

**Heroku:**
```bash
heroku domains:add www.yourdomain.com
```

**Render:**
- Settings → Custom Domain → Follow DNS instructions

---

## Need Help?

- [Railway Discord](https://discord.gg/railway)
- [Heroku Support](https://help.heroku.com)
- [Render Docs](https://render.com/docs)

---

**Your agent is now live! 🎉**

Share your deployment URL with the team or add it to your resume/portfolio!
