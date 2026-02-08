# LeadFinder AI - Render Deployment Guide

## 🚀 Quick Deploy to Render

### Option 1: One-Click Deploy (Recommended)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

1. Click the button above
2. Connect your GitHub repository
3. Render will auto-detect `render.yaml` and set up:
   - Web service (Flask app)
   - PostgreSQL database
   - Environment variables

### Option 2: Manual Setup

#### Step 1: Create PostgreSQL Database

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "PostgreSQL"
3. Settings:
   - **Name**: `leadfinder-db`
   - **Database**: `leadfinder`
   - **User**: `leadfinder`
   - **Region**: Oregon (or closest to you)
   - **Plan**: Starter ($7/month) or Free
4. Click "Create Database"
5. **Copy the Internal Database URL** from the database page

#### Step 2: Create Web Service

1. Click "New +" → "Web Service"
2. Connect your GitHub repository: `anubhav-product/email_agent`
3. Settings:
   - **Name**: `leadfinder-ai`
   - **Region**: Oregon (same as database)
   - **Branch**: `main`
   - **Root Directory**: (leave blank)
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app_saas:app --workers 2 --threads 4 --timeout 120 --bind 0.0.0.0:$PORT`
   - **Plan**: Starter ($7/month) or Free

#### Step 3: Set Environment Variables

In the web service settings, add these environment variables:

| Key | Value | Notes |
|-----|-------|-------|
| `SECRET_KEY` | (generate random string) | Use: `python -c "import secrets; print(secrets.token_hex(32))"` |
| `FLASK_ENV` | `production` | Production mode |
| `DATABASE_URL` | (from Step 1) | Internal Database URL from PostgreSQL |
| `PYTHON_VERSION` | `3.12.0` | Python version |

**Optional (add later in Settings page):**
- `HUNTER_API_KEY` - Your Hunter.io API key
- `APOLLO_API_KEY` - Your Apollo.io API key
- `OPENAI_API_KEY` - Your OpenAI API key

#### Step 4: Deploy

1. Click "Create Web Service"
2. Render will:
   - Install dependencies
   - Start your Flask app
   - Assign a URL: `https://leadfinder-ai.onrender.com`

**First deploy takes ~5 minutes**

#### Step 5: Access Your App

1. Visit: `https://leadfinder-ai.onrender.com`
2. Sign up for an account
3. Add API keys in Settings
4. Start generating leads!

---

## 🔐 Gmail OAuth Setup on Render

#### Step 1: Google Cloud Console

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create credentials (see `GMAIL_USER_GUIDE.md`)
3. **Authorized redirect URIs** - Add:
   ```
   https://your-app-name.onrender.com/oauth2callback
   ```
4. Download `credentials.json`

#### Step 2: Upload credentials.json

Render doesn't support file uploads directly. Two options:

**Option A: Environment Variable (Simple)**
```bash
# Convert credentials.json to base64
cat credentials.json | base64
```

Add to Render environment variables:
- Key: `GOOGLE_CREDENTIALS_BASE64`
- Value: (paste base64 string)

Update `gmail_service.py` to decode:
```python
import base64
import os
import json

credentials_base64 = os.getenv('GOOGLE_CREDENTIALS_BASE64')
if credentials_base64:
    credentials_json_content = base64.b64decode(credentials_base64)
    with open('credentials.json', 'wb') as f:
        f.write(credentials_json_content)
```

**Option B: Persistent Disk (Advanced)**
1. Create a Render Disk
2. Mount it to your web service
3. Upload credentials.json via SSH/SFTP

---

## 📊 Database Migration

Your SQLite database won't transfer to PostgreSQL automatically. Options:

### Option 1: Start Fresh (Recommended for new deployments)
- Render creates new PostgreSQL database
- Users sign up again
- Clean start

### Option 2: Migrate Data
```bash
# Export from SQLite
sqlite3 instance/leadfinder.db .dump > backup.sql

# Convert to PostgreSQL format (manual editing needed)
# Import to Render PostgreSQL
psql $DATABASE_URL < backup_postgresql.sql
```

---

## 🎛️ Production Configuration

### Auto-Scaling
Render Starter plan:
- 512 MB RAM
- 0.5 CPU
- Auto-sleeps after 15 min inactivity (Free tier)
- Always-on with Starter+ ($7/month)

### Performance
- **Workers**: 2 (handles ~500 concurrent users)
- **Threads**: 4 per worker
- **Timeout**: 120s (for API calls)

### Monitoring
1. Go to Render Dashboard → Your Service
2. Check:
   - **Logs**: Real-time application logs
   - **Metrics**: CPU, RAM, requests/sec
   - **Events**: Deploys, crashes, restarts

---

## 🔧 Troubleshooting

### Issue: "Application Error"
**Solution**: Check logs in Render Dashboard
```bash
# Common issues:
1. Missing environment variables
2. Database connection failed
3. Port binding error
```

### Issue: Database connection fails
**Solution**: Verify DATABASE_URI format
```python
# Should be:
postgresql://user:pass@host:port/dbname

# NOT:
postgres://... (old format)
```

### Issue: Gmail OAuth not working
**Solution**: Check redirect URI in Google Cloud Console matches:
```
https://your-app-name.onrender.com/oauth2callback
```

### Issue: Slow first request after sleep
**Solution**: Upgrade to Starter plan ($7/month) for always-on

---

## 🔄 Continuous Deployment

Render automatically deploys when you push to GitHub:

```bash
git add .
git commit -m "Update feature"
git push origin main
```

Render will:
1. Detect push
2. Pull latest code
3. Rebuild & redeploy
4. Zero-downtime deployment

---

## 💰 Pricing

### Render Costs
- **Web Service**: 
  - Free: $0 (sleeps after 15 min)
  - Starter: $7/month (always-on, 512MB RAM)
  - Standard: $25/month (2GB RAM)

- **PostgreSQL**:
  - Free: $0 (90 day limit, then deleted)
  - Starter: $7/month (1GB storage)
  - Standard: $20/month (10GB storage)

**Recommended Setup**: $14/month (Starter web + Starter DB)

### External API Costs
- Hunter.io: 50 free/month, then $39/month
- Apollo.io: 50 free/month, then $49/month
- OpenAI: Pay-per-use (~$0.002/email)
- Gmail API: **FREE** (no quotas for drafts)

---

## 🎯 Post-Deployment Checklist

- [ ] App loads at `https://your-app.onrender.com`
- [ ] Can sign up and log in
- [ ] Database persists data (create account, refresh, still logged in)
- [ ] Settings page loads
- [ ] Can add API keys (they persist)
- [ ] Lead generation works (test with stripe.com)
- [ ] Gmail OAuth setup (optional)
- [ ] Custom domain setup (optional)

---

## 🌐 Custom Domain (Optional)

1. Go to Render Dashboard → Your Service → Settings
2. Click "Add Custom Domain"
3. Enter: `app.yourdomain.com`
4. Add DNS records provided by Render:
   ```
   Type: CNAME
   Name: app
   Value: your-app.onrender.com
   ```
5. Wait for DNS propagation (5-60 min)
6. Render auto-provisions SSL certificate

---

## 📚 Resources

- [Render Python Guide](https://render.com/docs/deploy-flask)
- [Render PostgreSQL](https://render.com/docs/databases)
- [Environment Variables](https://render.com/docs/environment-variables)
- [Custom Domains](https://render.com/docs/custom-domains)

---

## 🆘 Support

**Render Issues:**
- Render Docs: https://render.com/docs
- Community: https://community.render.com

**App Issues:**
- Check `GMAIL_USER_GUIDE.md` for Gmail setup
- Review logs in Render Dashboard
- Test locally first: `python app_saas.py`

---

**🎉 Your LeadFinder AI app is now live on Render!**

Share your link: `https://your-app-name.onrender.com`
