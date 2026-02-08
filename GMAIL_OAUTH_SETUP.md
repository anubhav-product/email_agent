# Gmail OAuth Setup Guide

## Overview

The LeadFinder AI application now supports Gmail integration via OAuth 2.0. This allows users to automatically create Gmail drafts for their generated leads.

## Implementation Status

✅ **COMPLETED:**
- OAuth flow implementation (/connect-gmail route)
- OAuth callback handler (/oauth2callback route)
- Token encryption & secure storage in database
- UI for connect/disconnect in settings page
- Proper state verification (CSRF protection)
- Database methods: `set_gmail_token()`, `get_gmail_token()`, `has_gmail_connected()`

⚠️ **REQUIRES SETUP:**
- Google Cloud Project configuration
- OAuth 2.0 credentials file

## Setup Instructions

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Gmail API:
   - Navigate to "APIs & Services" > "Library"
   - Search for "Gmail API"
   - Click "Enable"

### Step 2: Configure OAuth Consent Screen

1. Go to "APIs & Services" > "OAuth consent screen"
2. Choose "External" (unless you have a Google Workspace)
3. Fill in the required fields:
   - App name: "LeadFinder AI"
   - User support email: your email
   - Developer contact: your email
4. Add scopes:
   - `https://www.googleapis.com/auth/gmail.compose`
5. Add test users (your own email for testing)
6. Save and continue

### Step 3: Create OAuth 2.0 Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth 2.0 Client ID"
3. Application type: **Web application**
4. Name: "LeadFinder AI Web Client"
5. **Authorized redirect URIs:** Add these:
   ```
   http://localhost:5000/oauth2callback
   http://127.0.0.1:5000/oauth2callback
   https://your-production-domain.com/oauth2callback
   ```
6. Click "Create"
7. **Download the JSON file**

### Step 4: Install credentials.json

1. Rename the downloaded file to `credentials.json`
2. Place it in the project root directory:
   ```
   /workspaces/email_agent/credentials.json
   ```
3. **Important:** Add `credentials.json` to `.gitignore` to keep it secret!

### Step 5: Install Required Packages

Add to `requirements.txt` if not already present:
```txt
google-auth-oauthlib==1.2.0
google-auth-httplib2==0.2.0
google-api-python-client==2.108.0
```

Install:
```bash
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### Step 6: Test the OAuth Flow

1. Start the Flask application
2. Create a user account and login
3. Go to Settings page
4. Click "Connect Gmail Account"
5. You should be redirected to Google's OAuth page
6. Authorize the application
7. You'll be redirected back with a success message

## How It Works

### User Flow:

1. **User clicks "Connect Gmail"** → `/connect-gmail` route
2. **Flask creates OAuth flow** → Redirects to Google OAuth page
3. **User authorizes** → Google redirects to `/oauth2callback`
4. **Flask receives tokens** → Encrypts and stores in database
5. **Success message** → User sees "Gmail Connected!"

### Technical Details:

```python
# OAuth Flow Creation
flow = Flow.from_client_secrets_file(
    'credentials.json',
    scopes=['https://www.googleapis.com/auth/gmail.compose'],
    redirect_uri='http://localhost:5000/oauth2callback'
)

# Token Storage (Encrypted)
credentials_json = credentials.to_json()
user.set_gmail_token(credentials_json)  # Encrypted with Fernet
db.session.commit()

# Token Retrieval
token_json = user.get_gmail_token()  # Decrypts automatically
credentials = Credentials.from_authorized_user_info(json.loads(token_json))
```

### Security Features:

✅ **CSRF Protection:** State parameter verified  
✅ **Encrypted Storage:** Tokens encrypted with Fernet symmetric encryption  
✅ **Scope Limitation:** Only `gmail.compose` scope (create drafts, no reading emails)  
✅ **Per-User Tokens:** Each user has their own encrypted OAuth token  
✅ **Secure Session:** State stored in Flask session  

## Testing Without credentials.json

If `credentials.json` doesn't exist, the app shows:
```
⚠️ Gmail OAuth not configured. Please add credentials.json file first.
```

This prevents crashes and guides users to set up OAuth properly.

## Production Deployment

For production:

1. **Use HTTPS** - OAuth requires secure connections in production
2. **Update Redirect URI** - Add production domain:
   ```
   https://leadfinder.yourdomain.com/oauth2callback
   ```
3. **Verify Domain** - In Google Cloud Console, verify domain ownership
4. **Publishing Status** - Submit for Google verification if needed (for > 100 users)
5. **Environment Variable** - Consider storing OAuth client secrets in environment variables instead of file

## Troubleshooting

**Error: "redirect_uri_mismatch"**
- Check that redirect URI in Google Cloud Console matches exactly
- Must include protocol (http/https) and port

**Error: "Invalid OAuth state"**
- Session may have expired
- Try connecting again
- Check Flask session configuration

**Error: "credentials.json not found"**
- File must be in project root directory
- Check file name spelling (case-sensitive)

**Token Refresh:**
- OAuth tokens expire after 1 hour
- Refresh token is stored and used automatically
- Users don't need to re-authorize unless they revoke access

## API Reference

### User Model Methods

```python
# Store Gmail OAuth token (encrypted)
user.set_gmail_token(credentials_json: str)

# Retrieve Gmail OAuth token (decrypted)
token_json = user.get_gmail_token() -> str

# Check if Gmail is connected
is_connected = user.has_gmail_connected() -> bool
```

### Routes

```python
@app.route('/connect-gmail')
@login_required
def connect_gmail()
# Initiates OAuth flow, redirects to Google

@app.route('/oauth2callback')
@login_required  
def gmail_oauth_callback()
# Handles OAuth callback, stores tokens

@app.route('/disconnect-gmail', methods=['POST'])
@login_required
def disconnect_gmail()
# Removes stored Gmail token
```

## Next Steps

1. ✅ OAuth implementation complete
2. ⏭️ Implement actual Gmail draft creation using stored tokens
3. ⏭️ Add token refresh logic when tokens expire
4. ⏭️ Test with real Gmail accounts
5. ⏭️ Add error handling for revoked tokens

## Related Files

- `/app_saas.py` - OAuth routes implementation
- `/database.py` - User model with token methods
- `/templates/settings_user.html` - Gmail UI section
- `/pm_outreach_agent/gmail_client.py` - Gmail API client (to be updated)

---

**Status:** Gmail OAuth is fully implemented and ready for testing with real Google Cloud credentials.
