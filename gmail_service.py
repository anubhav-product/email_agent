# Gmail Service - User-Friendly Gmail OAuth Integration
"""
This module provides a simple, secure Gmail integration service.
Handles OAuth authentication, token management, and draft creation.
"""

import os
import json
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from flask import url_for, session, flash
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class GmailService:
    """User-friendly Gmail service for OAuth and draft creation"""
    
    SCOPES = ['https://www.googleapis.com/auth/gmail.compose']
    CREDENTIALS_FILE = 'credentials.json'
    
    def __init__(self, app=None):
        """Initialize Gmail service"""
        self.app = app
        self.credentials_path = None
        if app:
            self.credentials_path = os.path.join(
                os.path.dirname(__file__), 
                self.CREDENTIALS_FILE
            )
    
    def is_configured(self) -> bool:
        """Check if Gmail OAuth is configured (credentials.json exists)"""
        if not self.credentials_path:
            return False
        return os.path.exists(self.credentials_path)
    
    def get_simple_auth_flow(self) -> Optional[tuple]:
        """
        Create a simple OAuth flow that works with Desktop/Installed app type
        No need to configure redirect URIs in Google Cloud Console!
        Returns: (flow, authorization_url) or None if not configured
        """
        if not self.is_configured():
            return None
        
        try:
            # Use urn:ietf:wg:oauth:2.0:oob for installed apps (no redirect needed)
            flow = Flow.from_client_secrets_file(
                self.credentials_path,
                scopes=self.SCOPES,
                redirect_uri='urn:ietf:wg:oauth:2.0:oob'
            )
            
            authorization_url, _ = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true',
                prompt='consent'
            )
            
            return flow, authorization_url
        
        except Exception as e:
            print(f"Error generating OAuth flow: {e}")
            return None
    
    def get_oauth_url(self, redirect_uri: str) -> Optional[tuple]:
        """
        Generate OAuth authorization URL
        Returns: (authorization_url, state) or None if not configured
        """
        if not self.is_configured():
            return None
        
        try:
            flow = Flow.from_client_secrets_file(
                self.credentials_path,
                scopes=self.SCOPES,
                redirect_uri=redirect_uri
            )
            
            authorization_url, state = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true',
                prompt='consent'
            )
            
            return authorization_url, state
        
        except Exception as e:
            print(f"Error generating OAuth URL: {e}")
            return None
    
    def exchange_code_for_token(self, flow, code: str) -> Optional[str]:
        """
        Exchange authorization code for tokens (for simple flow)
        Returns: credentials JSON string or None on error
        """
        if not self.is_configured():
            return None
        
        try:
            # Exchange code for credentials
            flow.fetch_token(code=code)
            credentials = flow.credentials
            
            # Return credentials as JSON for storage
            return credentials.to_json()
        
        except Exception as e:
            print(f"Error exchanging code for token: {e}")
            return None
    
    def handle_oauth_callback(self, state: str, redirect_uri: str, authorization_response: str) -> Optional[str]:
        """
        Handle OAuth callback and exchange code for tokens
        Returns: credentials JSON string or None on error
        """
        if not self.is_configured():
            return None
        
        try:
            flow = Flow.from_client_secrets_file(
                self.credentials_path,
                scopes=self.SCOPES,
                state=state,
                redirect_uri=redirect_uri
            )
            
            # Exchange authorization code for credentials
            flow.fetch_token(authorization_response=authorization_response)
            credentials = flow.credentials
            
            # Return credentials as JSON for storage
            return credentials.to_json()
        
        except Exception as e:
            print(f"Error handling OAuth callback: {e}")
            return None
    
    def get_credentials_from_json(self, credentials_json: str) -> Optional[Credentials]:
        """
        Convert stored JSON credentials to Credentials object
        Handles token refresh if needed
        """
        try:
            credentials = Credentials.from_authorized_user_info(
                json.loads(credentials_json),
                scopes=self.SCOPES
            )
            
            # Refresh if expired
            if credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
                # Return refreshed credentials (caller should save)
            
            return credentials
        
        except Exception as e:
            print(f"Error loading credentials: {e}")
            return None
    
    def get_user_info(self, credentials_json: str) -> Optional[Dict[str, Any]]:
        """
        Get connected Gmail account information
        Returns: dict with email, name, etc. or None on error
        """
        credentials = self.get_credentials_from_json(credentials_json)
        if not credentials:
            return None
        
        try:
            service = build('gmail', 'v1', credentials=credentials)
            profile = service.users().getProfile(userId='me').execute()
            
            return {
                'email': profile.get('emailAddress'),
                'messages_total': profile.get('messagesTotal', 0),
                'threads_total': profile.get('threadsTotal', 0)
            }
        
        except HttpError as e:
            print(f"Error fetching user info: {e}")
            return None
    
    def test_connection(self, credentials_json: str) -> bool:
        """
        Test if Gmail connection is working
        Returns: True if connection is valid, False otherwise
        """
        credentials = self.get_credentials_from_json(credentials_json)
        if not credentials:
            return False
        
        try:
            service = build('gmail', 'v1', credentials=credentials)
            # Simple API call to test connection
            service.users().getProfile(userId='me').execute()
            return True
        
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False
    
    def create_draft(
        self, 
        credentials_json: str,
        to_email: str,
        subject: str,
        body: str,
        from_email: Optional[str] = None
    ) -> Optional[str]:
        """
        Create a single Gmail draft
        Returns: draft ID or None on error
        """
        credentials = self.get_credentials_from_json(credentials_json)
        if not credentials:
            return None
        
        try:
            service = build('gmail', 'v1', credentials=credentials)
            
            # Create message
            message = MIMEText(body, 'plain', 'utf-8')
            message['to'] = to_email
            message['subject'] = subject
            if from_email:
                message['from'] = from_email
            
            # Encode message
            raw = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            
            # Create draft
            draft_body = {'message': {'raw': raw}}
            draft = service.users().drafts().create(
                userId='me', 
                body=draft_body
            ).execute()
            
            return draft.get('id')
        
        except HttpError as e:
            print(f"Error creating draft: {e}")
            return None
    
    def create_drafts_bulk(
        self,
        credentials_json: str,
        drafts: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        Create multiple Gmail drafts at once
        
        Args:
            credentials_json: User's Gmail credentials
            drafts: List of dicts with 'to', 'subject', 'body' keys
        
        Returns:
            Dict with 'success', 'failed', 'draft_ids', 'errors' keys
        """
        credentials = self.get_credentials_from_json(credentials_json)
        if not credentials:
            return {
                'success': 0,
                'failed': len(drafts),
                'draft_ids': [],
                'errors': ['Invalid credentials']
            }
        
        service = build('gmail', 'v1', credentials=credentials)
        
        success = 0
        failed = 0
        draft_ids = []
        errors = []
        
        for draft_data in drafts:
            try:
                # Create message
                message = MIMEText(draft_data['body'], 'plain', 'utf-8')
                message['to'] = draft_data['to']
                message['subject'] = draft_data['subject']
                
                # Encode and create draft
                raw = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
                draft_body = {'message': {'raw': raw}}
                
                draft = service.users().drafts().create(
                    userId='me',
                    body=draft_body
                ).execute()
                
                draft_ids.append(draft.get('id'))
                success += 1
            
            except Exception as e:
                failed += 1
                errors.append(f"{draft_data['to']}: {str(e)}")
        
        return {
            'success': success,
            'failed': failed,
            'draft_ids': draft_ids,
            'errors': errors
        }
    
    def get_setup_instructions(self) -> Dict[str, Any]:
        """Get step-by-step setup instructions for users"""
        return {
            'configured': self.is_configured(),
            'steps': [
                {
                    'number': 1,
                    'title': 'Create Google Cloud Project',
                    'description': 'Visit Google Cloud Console and create a new project',
                    'link': 'https://console.cloud.google.com/projectcreate',
                    'completed': self.is_configured()
                },
                {
                    'number': 2,
                    'title': 'Enable Gmail API',
                    'description': 'Enable the Gmail API for your project',
                    'link': 'https://console.cloud.google.com/apis/library/gmail.googleapis.com',
                    'completed': self.is_configured()
                },
                {
                    'number': 3,
                    'title': 'Configure OAuth Consent Screen',
                    'description': 'Set up the OAuth consent screen with app name and scopes',
                    'link': 'https://console.cloud.google.com/apis/credentials/consent',
                    'completed': self.is_configured()
                },
                {
                    'number': 4,
                    'title': 'Create OAuth Credentials',
                    'description': 'Create OAuth 2.0 credentials and download credentials.json',
                    'link': 'https://console.cloud.google.com/apis/credentials',
                    'completed': self.is_configured()
                },
                {
                    'number': 5,
                    'title': 'Upload Credentials File',
                    'description': 'Place credentials.json in the app root directory',
                    'completed': self.is_configured()
                }
            ]
        }


# Global instance
gmail_service = GmailService()
