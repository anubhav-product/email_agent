# Database models for SaaS multi-tenant system
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
import base64
import hashlib
import secrets
import os

db = SQLAlchemy()

# Encryption key for API keys (in production, use env variable)
def _get_encryption_key() -> bytes:
    env_key = os.getenv('ENCRYPTION_KEY')
    if env_key:
        return env_key.encode()
    secret_key = os.getenv('SECRET_KEY')
    if secret_key:
        digest = hashlib.sha256(secret_key.encode()).digest()
        return base64.urlsafe_b64encode(digest)
    return Fernet.generate_key()


ENCRYPTION_KEY = _get_encryption_key()
cipher_suite = Fernet(ENCRYPTION_KEY)


class Organization(db.Model):
    """Organization/Team for multi-user collaboration"""
    __tablename__ = 'organizations'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False, index=True)
    
    # Shared API keys for the organization (encrypted)
    hunter_api_key_encrypted = db.Column(db.Text)
    apollo_api_key_encrypted = db.Column(db.Text)
    snov_api_key_encrypted = db.Column(db.Text)
    snov_client_secret_encrypted = db.Column(db.Text)
    findthatlead_api_key_encrypted = db.Column(db.Text)
    openai_api_key_encrypted = db.Column(db.Text)
    gmail_token_encrypted = db.Column(db.Text)
    
    # Organization settings
    allow_template_sharing = db.Column(db.Boolean, default=True)
    allow_lead_sharing = db.Column(db.Boolean, default=True)
    
    # Usage limits (null = unlimited)
    max_searches_per_month = db.Column(db.Integer)
    max_users = db.Column(db.Integer)
    
    # Billing
    plan = db.Column(db.String(50), default='free')  # free, team, enterprise
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    members = db.relationship('User', backref='organization', lazy='dynamic')
    
    def get_api_key(self, provider: str) -> str:
        """Get decrypted API key"""
        encrypted = None
        if provider == 'hunter':
            encrypted = self.hunter_api_key_encrypted
        elif provider == 'apollo':
            encrypted = self.apollo_api_key_encrypted
        elif provider == 'snov':
            encrypted = self.snov_api_key_encrypted
        elif provider == 'findthatlead':
            encrypted = self.findthatlead_api_key_encrypted
        elif provider == 'openai':
            encrypted = self.openai_api_key_encrypted
        
        if not encrypted:
            return None
        try:
            return cipher_suite.decrypt(encrypted.encode()).decode()
        except:
            return None
    
    def set_api_key(self, provider: str, key: str):
        """Encrypt and store API key"""
        if not key or key.strip() == '':
            return
        encrypted = cipher_suite.encrypt(key.encode())
        
        if provider == 'hunter':
            self.hunter_api_key_encrypted = encrypted.decode()
        elif provider == 'apollo':
            self.apollo_api_key_encrypted = encrypted.decode()
        elif provider == 'snov':
            self.snov_api_key_encrypted = encrypted.decode()
        elif provider == 'findthatlead':
            self.findthatlead_api_key_encrypted = encrypted.decode()
        elif provider == 'openai':
            self.openai_api_key_encrypted = encrypted.decode()
    
    def __repr__(self):
        return f'<Organization {self.name}>'


class User(UserMixin, db.Model):
    """User account - simple authentication, no payments"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(100))
    
    # Organization/Team membership
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), index=True)
    role = db.Column(db.String(20), default='member')  # owner, admin, member, viewer
    
    # User's own API keys (encrypted) - BYOK (Bring Your Own Keys) model
    hunter_api_key_encrypted = db.Column(db.Text)
    apollo_api_key_encrypted = db.Column(db.Text)
    snov_api_key_encrypted = db.Column(db.Text)
    snov_client_secret_encrypted = db.Column(db.Text)
    findthatlead_api_key_encrypted = db.Column(db.Text)
    
    # OpenAI key for personalized emails
    openai_api_key_encrypted = db.Column(db.Text)
    
    # Gmail OAuth tokens (encrypted JSON)
    gmail_token_encrypted = db.Column(db.Text)
    
    # Usage tracking
    total_searches = db.Column(db.Integer, default=0)
    total_leads = db.Column(db.Integer, default=0)
    
    # Preferences
    dashboard_view = db.Column(db.String(20), default='premium')  # 'premium' or 'simple'
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    searches = db.relationship('Search', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    # API Key Management (encrypted storage)
    def set_api_key(self, provider: str, key: str, secret: str = None):
        """Encrypt and store API key for a provider"""
        if not key or key.strip() == '':
            return
        
        encrypted = cipher_suite.encrypt(key.encode())
        
        if provider == 'hunter':
            self.hunter_api_key_encrypted = encrypted.decode()
        elif provider == 'apollo':
            self.apollo_api_key_encrypted = encrypted.decode()
        elif provider == 'snov':
            self.snov_api_key_encrypted = encrypted.decode()
            if secret:
                self.snov_client_secret_encrypted = cipher_suite.encrypt(secret.encode()).decode()
        elif provider == 'findthatlead':
            self.findthatlead_api_key_encrypted = encrypted.decode()
        elif provider == 'openai':
            self.openai_api_key_encrypted = encrypted.decode()
    
    def get_api_key(self, provider: str) -> str:
        """Decrypt and return API key for a provider"""
        encrypted = None
        
        if provider == 'hunter':
            encrypted = self.hunter_api_key_encrypted
        elif provider == 'apollo':
            encrypted = self.apollo_api_key_encrypted
        elif provider == 'snov':
            encrypted = self.snov_api_key_encrypted
        elif provider == 'findthatlead':
            encrypted = self.findthatlead_api_key_encrypted
        elif provider == 'openai':
            encrypted = self.openai_api_key_encrypted
        
        if not encrypted:
            return None
        
        try:
            return cipher_suite.decrypt(encrypted.encode()).decode()
        except:
            return None
    
    def get_snov_secret(self) -> str:
        """Get Snov.io client secret"""
        if not self.snov_client_secret_encrypted:
            return None
        try:
            return cipher_suite.decrypt(self.snov_client_secret_encrypted.encode()).decode()
        except:
            return None
    
    def set_gmail_token(self, token_json: str):
        """Encrypt and store Gmail OAuth token"""
        if not token_json or token_json.strip() == '':
            return
        encrypted = cipher_suite.encrypt(token_json.encode())
        self.gmail_token_encrypted = encrypted.decode()
    
    def get_gmail_token(self) -> str:
        """Decrypt and return Gmail OAuth token JSON"""
        if not self.gmail_token_encrypted:
            return None
        try:
            return cipher_suite.decrypt(self.gmail_token_encrypted.encode()).decode()
        except:
            return None
    
    def has_gmail_connected(self) -> bool:
        """Check if user has Gmail connected"""
        token = self.get_gmail_token()
        return token is not None and len(token) > 0
    
    def has_provider(self, provider: str) -> bool:
        """Check if user has configured a specific provider"""
        key = self.get_api_key(provider)
        return key is not None and len(key) > 0
    
    def get_configured_providers(self) -> list:
        """Get list of providers user has configured"""
        providers = []
        for p in ['hunter', 'apollo', 'snov', 'findthatlead']:
            if self.has_provider(p):
                providers.append(p)
        return providers
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def increment_usage(self, leads_count=0):
        """Track usage (no limits enforced)"""
        self.total_searches += 1
        self.total_leads += leads_count
        db.session.commit()
    
    def __repr__(self):
        return f'<User {self.email}>'


class Search(db.Model):
    """Search history and results"""
    __tablename__ = 'searches'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Search parameters
    company_name = db.Column(db.String(100))
    domain = db.Column(db.String(100), nullable=False)
    domain_type = db.Column(db.String(50))  # pm, consulting, engineering, etc.
    
    # Results
    lead_count = db.Column(db.Integer, default=0)
    
    # Files
    csv_file = db.Column(db.String(255))  # S3/storage path
    md_file = db.Column(db.String(255))
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    success = db.Column(db.Boolean, default=True)
    error_message = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Search {self.domain} - {self.lead_count} leads>'


class LeadCache(db.Model):
    """Cache API results to avoid duplicate calls"""
    __tablename__ = 'lead_cache'
    
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(100), nullable=False, index=True)
    domain_type = db.Column(db.String(50))
    
    # Cached data (JSON)
    leads_data = db.Column(db.Text)  # JSON string of leads
    lead_count = db.Column(db.Integer, default=0)
    
    # Provider used
    provider = db.Column(db.String(50))  # hunter, apollo, snov, etc.
    
    # Cache expiry
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    expires_at = db.Column(db.DateTime, index=True)  # Cache for 7 days
    
    def is_valid(self):
        """Check if cache is still valid"""
        return self.expires_at > datetime.utcnow()
    
    def __repr__(self):
        return f'<LeadCache {self.domain} - {self.lead_count} leads>'


class APICallLog(db.Model):
    """Track API calls for rate limiting"""
    __tablename__ = 'api_call_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    provider = db.Column(db.String(50), nullable=False, index=True)
    domain = db.Column(db.String(100))
    
    # Call status
    success = db.Column(db.Boolean, default=True)
    credits_used = db.Column(db.Integer, default=1)
    
    # Timing
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<APICall {self.provider} - {self.domain}>'


class EmailTemplate(db.Model):
    """User-customizable email templates"""
    __tablename__ = 'email_templates'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Template details
    name = db.Column(db.String(100), nullable=False)  # "PM Outreach", "Engineering Intro"
    subject = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    
    # Template variables supported: {{first_name}}, {{company_name}}, {{role}}, etc.
    
    # Metadata
    is_default = db.Column(db.Boolean, default=False)  # Default template for this user
    domain_type = db.Column(db.String(50))  # pm, consulting, etc. (null = all)
    
    # Usage stats
    times_used = db.Column(db.Integer, default=0)
    success_rate = db.Column(db.Float)  # % of emails that got responses (future)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref=db.backref('templates', lazy='dynamic'))
    
    def __repr__(self):
        return f'<EmailTemplate {self.name}>'


def init_db(app):
    """Initialize database"""
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        print("✅ Database initialized")
