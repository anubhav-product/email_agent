import base64
import os
import mimetypes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Optional

# Allow insecure transport for localhost OAuth
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from .models import RankedLead, EmailDraft
from .utils import log_action


SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]


def _load_credentials(credentials_path: str, token_path: str) -> Credentials:
    creds = None
    if token_path:
        try:
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        except Exception:
            creds = None
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            flow.redirect_uri = 'http://localhost'
            log_action("\nGmail Authorization Required:")
            log_action("1. Open this URL in your browser:")
            auth_url, _ = flow.authorization_url(prompt='consent')
            log_action(f"\n{auth_url}\n")
            log_action("2. Authorize the app")
            log_action("3. Copy the full redirect URL from your browser (starts with http://localhost)")
            redirect_response = input("Paste the full redirect URL here: ").strip()
            flow.fetch_token(authorization_response=redirect_response)
            creds = flow.credentials
        if token_path:
            with open(token_path, "w", encoding="utf-8") as handle:
                handle.write(creds.to_json())
    return creds


def _create_mime_message(sender: str, to_email: str, subject: str, body: str, attachment_path: Optional[str] = None) -> str:
    if attachment_path and os.path.exists(attachment_path):
        message = MIMEMultipart()
        message["to"] = to_email
        message["from"] = sender
        message["subject"] = subject
        
        # Attach the body
        message.attach(MIMEText(body, "plain", "utf-8"))
        
        # Attach the file
        content_type, encoding = mimetypes.guess_type(attachment_path)
        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        main_type, sub_type = content_type.split('/', 1)
        
        with open(attachment_path, 'rb') as fp:
            attachment = MIMEBase(main_type, sub_type)
            attachment.set_payload(fp.read())
        
        encoders.encode_base64(attachment)
        filename = os.path.basename(attachment_path)
        attachment.add_header('Content-Disposition', 'attachment', filename=filename)
        message.attach(attachment)
    else:
        message = MIMEText(body, "plain", "utf-8")
        message["to"] = to_email
        message["from"] = sender
        message["subject"] = subject
    
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    return raw


def create_gmail_drafts(
    ranked_leads: List[RankedLead],
    drafts: List[EmailDraft],
    sender_email: str,
    credentials_path: str,
    token_path: str,
    resume_attachment: Optional[str] = None,
) -> List[str]:
    log_action("Creating Gmail drafts (no sending).")
    creds = _load_credentials(credentials_path, token_path)
    service = build("gmail", "v1", credentials=creds)
    draft_ids: List[str] = []
    for ranked, draft in zip(ranked_leads, drafts):
        lead = ranked.lead
        raw = _create_mime_message(sender_email, lead.email, draft.subject, draft.body, resume_attachment)
        draft_body = {"message": {"raw": raw}}
        created = service.users().drafts().create(userId="me", body=draft_body).execute()
        draft_ids.append(created.get("id", ""))
    return draft_ids
