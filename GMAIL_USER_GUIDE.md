# Gmail Integration User Guide

## 🚀 Quick Start - Connect Your Gmail in 3 Steps

### For Users (Non-Admin)

**If Gmail OAuth is already configured by your admin:**

1. **Visit Gmail Setup Page**
   - Click "📧 Gmail" in the navigation menu
   - Or go to Settings → "Set Up Gmail Integration"

2. **Connect Your Account**
   - Click the big "🔗 Connect Gmail Account" button
   - Sign in with your Google/Gmail account
   - Click "Allow" to authorize draft creation (we only create drafts, never read or send)

3. **Start Using It**
   - Go back to the main page
   - Check the "Create Gmail Drafts" checkbox when generating leads
   - Drafts will appear in your Gmail Drafts folder automatically!

**That's it!** Your email drafts are now automated. Just review and send from Gmail.

---

## 🛠️ For Administrators - One-Time Setup

If users see "Administrator Setup Required", follow these steps **once** to enable Gmail for all users:

### Step 1: Create Google Cloud Project (5 minutes)

1. Go to [Google Cloud Console](https://console.cloud.google.com/projectcreate)
2. Click "Create Project"
3. Name it: `LeadFinder Gmail Integration`
4. Click "Create"

### Step 2: Enable Gmail API (1 minute)

1. Go to [Gmail API Library](https://console.cloud.google.com/apis/library/gmail.googleapis.com)
2. Make sure your project is selected
3. Click "Enable"

### Step 3: Configure OAuth Consent Screen (3 minutes)

1. Go to [OAuth Consent Screen](https://console.cloud.google.com/apis/credentials/consent)
2. Choose "External" (if not a Google Workspace organization)
3. Click "Create"
4. Fill in:
   - **App name:** LeadFinder AI
   - **User support email:** your-email@company.com
   - **Developer contact:** your-email@company.com
5. Click "Save and Continue"
6. Click "Add or Remove Scopes"
7. Search for `gmail.compose` and select:
   - `https://www.googleapis.com/auth/gmail.compose`
8. Click "Update" → "Save and Continue"
9. Click "Save and Continue" on Test Users
10. Click "Back to Dashboard"

### Step 4: Create OAuth Credentials (2 minutes)

1. Go to [Credentials](https://console.cloud.google.com/apis/credentials)
2. Click "Create Credentials" → "OAuth client ID"
3. Application type: **Web application**
4. Name: `LeadFinder Web Client`
5. **Authorized redirect URIs** - Add both:
   ```
   http://127.0.0.1:5000/oauth2callback
   http://localhost:5000/oauth2callback
   ```
   (Add your production domain too if deployed)
6. Click "Create"
7. Click "Download JSON" on the popup
8. Save the file

### Step 5: Install Credentials File (1 minute)

1. Rename the downloaded file to `credentials.json`
2. Place it in the LeadFinder app root directory:
   ```bash
   /workspaces/email_agent/credentials.json
   ```
3. **Restart the Flask app**

**Done!** All users can now connect their Gmail accounts.

---

## ✨ Features

### What It Does
- ✅ **Automatic Draft Creation** - Creates email drafts in Gmail for every lead
- ✅ **Bulk Processing** - Handles multiple leads at once (10-50 drafts per search)
- ✅ **Review Before Send** - All emails are drafts, you decide when to send
- ✅ **Secure OAuth 2.0** - Industry-standard Google authentication
- ✅ **Token Encryption** - Your credentials encrypted in database (Fernet)
- ✅ **Connection Status** - See which Gmail account is connected
- ✅ **Easy Disconnect** - Remove access anytime with one click

### What It Doesn't Do
- ❌ **Never reads your emails** - Only creates drafts
- ❌ **Never sends emails** - You manually send from Gmail
- ❌ **Never shares your data** - Tokens stored encrypted, never shared
- ❌ **No auto-renewals** - Free Gmail API (no billing)

---

## 🔐 Security & Privacy

### Your Data is Safe
- **OAuth 2.0**: Same technology Google uses for third-party apps
- **Encrypted Storage**: Tokens encrypted with Fernet symmetric encryption
- **Minimal Permissions**: Only `gmail.compose` scope (create drafts only)
- **No Reading**: Cannot read your existing emails
- **No Sending**: Cannot send emails without your manual action
- **Revocable**: Disconnect anytime from Gmail Setup page

### What We Store
- Encrypted OAuth tokens (refresh token + access token)
- That's it! No emails, no contacts, no other data.

### How to Revoke Access
1. **In LeadFinder**: Go to Gmail Setup → Disconnect
2. **In Google**: [Google Account Permissions](https://myaccount.google.com/permissions) → Remove "LeadFinder AI"

---

## 🎯 Usage Examples

### Example 1: Basic Lead Generation with Gmail

```
1. Go to main page
2. Enter company domain: "stripe.com"
3. Select career domain: "Product Management"
4. ✓ Check "Create Gmail Drafts"
5. Click "Generate Leads & Drafts"
6. Wait 30 seconds
7. Open Gmail → Drafts folder
8. See 15+ personalized email drafts ready to review
```

### Example 2: Batch Processing

```
1. Go to Batch page
2. Upload CSV with 20 companies
3. ✓ Enable "Create Gmail Drafts for all"
4. Submit batch
5. Get 200+ drafts in Gmail (10 per company)
6. Review and send at your pace
```

### Example 3: Reconnecting After Token Expiry

```
If you see "Gmail token expired":
1. Go to Gmail Setup page
2. Click "Disconnect Gmail"
3. Click "Connect Gmail Account"
4. Sign in again
5. Done! Fresh tokens loaded
```

---

## 🐛 Troubleshooting

### Issue: "Gmail OAuth not configured"
**Solution**: Admin needs to complete the 5-step setup above and add `credentials.json`

### Issue: "Invalid OAuth state"
**Solution**: Clear browser cookies or try in incognito mode

### Issue: "Gmail connected but drafts not appearing"
**Solution**: 
1. Check Gmail Drafts folder (might take 10-30 seconds)
2. Check if you selected the right Gmail account
3. Try disconnecting and reconnecting

### Issue: "Connection test failed"
**Solution**:
1. Disconnect Gmail
2. Delete `credentials.json`
3. Re-download from Google Cloud Console
4. Reconnect

### Issue: "Drafts created but missing some leads"
**Solution**: Normal - Gmail API has rate limits. Wait 1 minute and try failed ones again.

---

## 📊 Technical Details

### API Limits
- **Google Gmail API**: 250 drafts/second, 1 billion/day (you'll never hit this)
- **OAuth Tokens**: Valid for 7 days, auto-refreshed

### Database Schema
```python
class User:
    gmail_token_encrypted: Text  # Fernet encrypted JSON
    
    def set_gmail_token(self, credentials_json: str)
    def get_gmail_token(self) -> Optional[str]
    def has_gmail_connected(self) -> bool
```

### Gmail Service API
```python
from gmail_service import gmail_service

# Check if configured
gmail_service.is_configured()  # bool

# Get OAuth URL
url, state = gmail_service.get_oauth_url(redirect_uri)

# Handle callback
token = gmail_service.handle_oauth_callback(state, redirect_uri, auth_response)

# Create drafts
result = gmail_service.create_drafts_bulk(token, [
    {'to': 'lead@company.com', 'subject': 'Hi', 'body': 'Hello...'}
])
# Returns: {'success': 1, 'failed': 0, 'draft_ids': [...], 'errors': []}
```

---

## 🎉 Success Stories

### Time Saved
- **Before**: Copy-paste 20 emails manually (20 minutes)
- **After**: Click checkbox, wait 30 seconds, review in Gmail (2 minutes)
- **Savings**: 90% time reduction!

### Professional Workflow
- All emails start as drafts
- Review before sending (catch typos, personalize more)
- Send from your real Gmail (not a tool)
- Track opens/replies in Gmail

---

## 📞 Support

### Need Help?
1. Check this guide first
2. Visit Gmail Setup page → See step-by-step instructions
3. Check [Google OAuth Documentation](https://developers.google.com/identity/protocols/oauth2)

### Common Questions

**Q: Can I use multiple Gmail accounts?**
A: One Gmail per user account. Disconnect and reconnect to switch.

**Q: What happens if I disconnect?**
A: Previous drafts stay in Gmail, but new lead generations won't create drafts.

**Q: Can I use G Suite/Google Workspace?**
A: Yes! Same process. Admin might need to approve the app in Workspace console.

**Q: Is there a cost?**
A: No! Gmail API is free for draft creation. No quotas, no billing.

---

## 🔄 Changelog

### v2.0 - User-Friendly Gmail Service
- ✅ Dedicated Gmail Setup page
- ✅ Visual step-by-step instructions
- ✅ Connection status indicators
- ✅ Bulk draft creation
- ✅ Better error handling
- ✅ Auto token refresh
- ✅ One-click disconnect

### v1.0 - Initial Gmail Integration
- Basic OAuth flow
- Single draft creation
- Manual token management

---

**Happy Lead Generating!** 🚀

Made with ❤️ by the LeadFinder AI team
