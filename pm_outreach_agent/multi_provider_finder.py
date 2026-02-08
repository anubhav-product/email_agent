"""
Multi-Provider Email Finder with Caching, Rate Limiting, and Automatic Fallback
Scales for production use with multiple users - BYOK (Bring Your Own Keys) model
"""
import os
import json
import requests
from datetime import datetime, timedelta
from typing import List, Optional, Dict, TYPE_CHECKING
from database import db, LeadCache, APICallLog

if TYPE_CHECKING:
    from database import User

from pm_outreach_agent.models import Lead


class MultiProviderEmailFinder:
    """
    Scalable email finder with:
    - User-specific API keys (stored encrypted in database)
    - Multiple API providers with automatic fallback
    - Result caching (7 days) to avoid duplicate API calls
    - Rate limiting per user
    - Provider rotation to distribute load
    """
    
    def get_user_providers(self, user: 'User') -> Dict:
        """Get provider config for a specific user's API keys"""
        return {
            'hunter': {
                'api_key': user.get_api_key('hunter'),
                'credits_per_month': 50,
                'enabled': user.has_provider('hunter')
            },
            'apollo': {
                'api_key': user.get_api_key('apollo'),
                'credits_per_month': 50,
                'enabled': user.has_provider('apollo')
            },
            'snov': {
                'api_key': user.get_api_key('snov'),
                'client_secret': user.get_snov_secret(),
                'credits_per_month': 50,
                'enabled': user.has_provider('snov')
            },
            'findthatlead': {
                'api_key': user.get_api_key('findthatlead'),
                'credits_per_month': 50,
                'enabled': user.has_provider('findthatlead')
            }
        }
    
    def find_leads(self, domain: str, domain_type: str, user: 'User') -> List[Lead]:
        """
        Find leads with caching and multi-provider fallback using user's API keys
        
        Args:
            domain: Company domain
            domain_type: Type of company (pm, consulting, etc.)
            user: User object with their API keys
        
        Returns:
            List of Lead objects
        """
        # Get user's configured providers
        providers = self.get_user_providers(user)
        
        # 0. Check if user has any providers configured
        if not any(p['enabled'] for p in providers.values()):
            print(f"❌ User {user.email} has no email providers configured.")
            return []
        
        # 1. Check cache first
        cached = self._get_from_cache(domain, domain_type)
        if cached:
            print(f"✅ Cache hit! Using cached results for {domain}")
            return cached
        
        # 2. Try each provider in order
        for provider_name, config in providers.items():
            if not config['enabled']:
                continue
            
            # Check if user has hit rate limit with this provider
            if self._is_rate_limited(user.id, provider_name):
                print(f"⚠️  Rate limit reached for {provider_name}, trying next provider...")
                continue
            
            try:
                print(f"🔍 Trying {provider_name} with user's API key...")
                leads = self._fetch_from_provider(provider_name, domain, domain_type, config)
                
                if leads:
                    # Success! Cache results and log API call
                    self._save_to_cache(domain, domain_type, leads, provider_name)
                    self._log_api_call(user.id, provider_name, domain, success=True)
                    
                    print(f"✅ Success! Found {len(leads)} leads using {provider_name}")
                    return leads
                    
            except Exception as e:
                print(f"❌ {provider_name} failed: {e}")
                self._log_api_call(user.id, provider_name, domain, success=False)
                continue
        
        # 3. All providers failed
        print("❌ All user's providers exhausted or failed")
        return []
    
    def _get_from_cache(self, domain: str, domain_type: str) -> Optional[List[Lead]]:
        """Get cached results if available and valid"""
        cache = LeadCache.query.filter_by(
            domain=domain,
            domain_type=domain_type
        ).first()
        
        if cache and cache.is_valid():
            # Parse JSON and convert to Lead objects
            leads_data = json.loads(cache.leads_data)
            return [Lead(**lead_dict) for lead_dict in leads_data]
        
        return None
    
    def _save_to_cache(self, domain: str, domain_type: str, leads: List[Lead], provider: str):
        """Save results to cache (7 day expiry)"""
        # Convert Lead objects to dicts
        leads_data = [
            {
                'name': lead.name,
                'email': lead.email,
                'title': lead.title,
                'linkedin': lead.linkedin,
                'confidence': lead.confidence
            }
            for lead in leads
        ]
        
        cache = LeadCache(
            domain=domain,
            domain_type=domain_type,
            leads_data=json.dumps(leads_data),
            lead_count=len(leads),
            provider=provider,
            expires_at=datetime.utcnow() + timedelta(days=7)
        )
        
        db.session.add(cache)
        db.session.commit()
    
    def _is_rate_limited(self, user_id: int, provider: str, window_hours: int = 24) -> bool:
        """
        Check if user has exceeded rate limit for provider
        Limit: 10 calls per provider per 24 hours
        """
        since = datetime.utcnow() - timedelta(hours=window_hours)
        
        call_count = APICallLog.query.filter(
            APICallLog.user_id == user_id,
            APICallLog.provider == provider,
            APICallLog.created_at >= since,
            APICallLog.success == True
        ).count()
        
        return call_count >= 10
    
    def _log_api_call(self, user_id: int, provider: str, domain: str, success: bool):
        """Log API call for rate limiting"""
        log = APICallLog(
            user_id=user_id,
            provider=provider,
            domain=domain,
            success=success
        )
        db.session.add(log)
        db.session.commit()
    
    def _fetch_from_provider(self, provider: str, domain: str, domain_type: str, config: Dict) -> List[Lead]:
        """Fetch leads from specific provider using provided config"""
        if provider == 'hunter':
            return self._fetch_hunter(domain, domain_type, config)
        elif provider == 'apollo':
            return self._fetch_apollo(domain, domain_type, config)
        elif provider == 'snov':
            return self._fetch_snov(domain, domain_type, config)
        elif provider == 'findthatlead':
            return self._fetch_findthatlead(domain, domain_type, config)
        else:
            return []
    
    def _fetch_hunter(self, domain: str, domain_type: str, config: Dict) -> List[Lead]:
        """Fetch from Hunter.io"""
        api_key = config['api_key']
        
        url = f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={api_key}"
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        emails = data.get('data', {}).get('emails', [])
        
        leads = []
        for email_data in emails:
            lead = Lead(
                name=f"{email_data.get('first_name', '')} {email_data.get('last_name', '')}".strip(),
                email=email_data.get('value'),
                title=email_data.get('position'),
                linkedin=email_data.get('linkedin'),
                confidence=email_data.get('confidence', 0) / 100  # Convert to 0-1
            )
            leads.append(lead)
        
        return leads
    
    def _fetch_apollo(self, domain: str, domain_type: str, config: Dict) -> List[Lead]:
        """Fetch from Apollo.io"""
        api_key = config['api_key']
        
        url = "https://api.apollo.io/v1/mixed_people/search"
        headers = {"X-Api-Key": api_key}
        
        payload = {
            "organization_domains": [domain],
            "page": 1,
            "per_page": 25
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        people = data.get('people', [])
        
        leads = []
        for person in people:
            lead = Lead(
                name=person.get('name'),
                email=person.get('email'),
                title=person.get('title'),
                linkedin=person.get('linkedin_url'),
                confidence=0.8  # Apollo doesn't provide confidence
            )
            leads.append(lead)
        
        return leads
    
    def _fetch_snov(self, domain: str, domain_type: str, config: Dict) -> List[Lead]:
        """Fetch from Snov.io"""
        api_key = config['api_key']
        client_secret = config['client_secret']
        
        # First, get access token
        auth_url = "https://api.snov.io/v1/get-access-token"
        auth_data = {
            "client_id": api_key,
            "client_secret": client_secret,
            "grant_type": "client_credentials"
        }
        
        auth_response = requests.post(auth_url, json=auth_data, timeout=30)
        auth_response.raise_for_status()
        access_token = auth_response.json().get('access_token')
        
        # Now search for emails
        search_url = "https://api.snov.io/v1/get-domain-emails-with-info"
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {"domain": domain, "limit": 25}
        
        response = requests.get(search_url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        
        emails = response.json().get('emails', [])
        
        leads = []
        for email_data in emails:
            lead = Lead(
                name=f"{email_data.get('firstName', '')} {email_data.get('lastName', '')}".strip(),
                email=email_data.get('email'),
                title=email_data.get('position'),
                linkedin=email_data.get('socialUrl'),
                confidence=0.8
            )
            leads.append(lead)
        
        return leads
    
    def _fetch_findthatlead(self, domain: str, domain_type: str, config: Dict) -> List[Lead]:
        """Fetch from FindThatLead"""
        api_key = config['api_key']
        
        url = f"https://api.findthatlead.com/v1/domains/{domain}/emails"
        headers = {"Authorization": f"Bearer {api_key}"}
        
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        emails = data.get('data', [])
        
        leads = []
        for email_data in emails:
            lead = Lead(
                name=f"{email_data.get('first_name', '')} {email_data.get('last_name', '')}".strip(),
                email=email_data.get('email'),
                title=email_data.get('position'),
                linkedin=email_data.get('linkedin'),
                confidence=0.8
            )
            leads.append(lead)
        
        return leads
    
    def get_provider_status(self, user: 'User') -> Dict:
        """Get status of all providers for a specific user"""
        status = {}
        providers = self.get_user_providers(user)
        
        for provider_name, config in providers.items():
            provider_status = {
                'enabled': config['enabled'],
                'credits_per_month': config['credits_per_month']
            }
            
            # Get user's calls in last 24 hours
            since = datetime.utcnow() - timedelta(hours=24)
            calls_today = APICallLog.query.filter(
                APICallLog.user_id == user.id,
                APICallLog.provider == provider_name,
                APICallLog.created_at >= since,
                APICallLog.success == True
            ).count()
            
            provider_status['calls_today'] = calls_today
            provider_status['remaining_today'] = max(0, 10 - calls_today)
            provider_status['rate_limited'] = calls_today >= 10
            
            status[provider_name] = provider_status
        
        return status
    
    def get_enabled_providers(self, user: 'User') -> List[str]:
        """Get list of enabled provider names for a user"""
        providers = self.get_user_providers(user)
        return [name for name, config in providers.items() if config['enabled']]


# Singleton instance
email_finder = MultiProviderEmailFinder()
