"""
Comprehensive automated testing using requests library
Simulates full user journey and identifies issues
"""

import requests
import time
import json

BASE_URL = "http://127.0.0.1:5000"

class TestSession:
    def __init__(self):
        self.session = requests.Session()
        self.test_email = f"test_{int(time.time())}@example.com"
        self.test_password = "testpass123"
        self.issues_found = []
        self.suggestions = []
        
    def log(self, emoji, message):
        print(f"{emoji} {message}")
        
    def add_issue(self, issue):
        self.issues_found.append(issue)
        self.log("❌", f"ISSUE: {issue}")
        
    def add_suggestion(self, suggestion):
        self.suggestions.append(suggestion)
        self.log("💡", f"SUGGESTION: {suggestion}")
        
    def test_homepage(self):
        self.log("\n🧪", "TEST 1: Homepage & Navigation")
        print("=" * 70)
        
        try:
            resp = self.session.get(BASE_URL)
            self.log("✅", f"Homepage loads: {resp.status_code}")
            
            if "LeadFinder" not in resp.text:
                self.add_issue("Homepage doesn't contain 'LeadFinder' branding")
            
            if "Sign Up" not in resp.text and "signup" not in resp.text.lower():
                self.add_issue("No clear 'Sign Up' call-to-action on homepage")
            else:
                self.log("✅", "Sign Up link found")
                
            if resp.status_code != 200:
                self.add_issue(f"Homepage returned HTTP {resp.status_code}")
                
        except Exception as e:
            self.add_issue(f"Homepage failed to load: {e}")
            
    def test_signup(self):
        self.log("\n🧪", "TEST 2: User Signup Flow")
        print("=" * 70)
        
        try:
            # Get signup page first
            resp = self.session.get(f"{BASE_URL}/signup")
            if resp.status_code != 200:
                self.add_issue(f"Signup page returned HTTP {resp.status_code}")
                return False
            
            self.log("✅", "Signup page accessible")
            
            # Submit signup form
            signup_data = {
                'name': 'Test User',
                'email': self.test_email,
                'password': self.test_password,
                'confirm_password': self.test_password
            }
            
            resp = self.session.post(f"{BASE_URL}/signup", data=signup_data, allow_redirects=True)
            
            if resp.status_code == 200:
                self.log("✅", f"Signup successful, redirected to: {resp.url}")
                
                if '/settings' in resp.url:
                    self.log("✅", "Correctly redirected to Settings page")
                elif '/app' in resp.url or '/dashboard' in resp.url:
                    self.add_suggestion("Consider redirecting new users to Settings first to add API keys")
                    
                return True
            else:
                self.add_issue(f"Signup failed with HTTP {resp.status_code}")
                return False
                
        except Exception as e:
            self.add_issue(f"Signup test failed: {e}")
            return False
            
    def test_settings_page(self):
        self.log("\n🧪", "TEST 3: Settings Page & API Key Management")
        print("=" * 70)
        
        try:
            resp = self.session.get(f"{BASE_URL}/settings")
            
            if resp.status_code != 200:
                self.add_issue(f"Settings page returned HTTP {resp.status_code}")
                return
            
            self.log("✅", "Settings page accessible")
            
            # Check for provider forms
            providers = ['Hunter', 'Apollo', 'Snov', 'FindThatLead']
            for provider in providers:
                if provider in resp.text:
                    self.log("✅", f"{provider} provider form found")
                else:
                    self.add_issue(f"{provider} provider form NOT found in settings")
            
            # Check for Gmail integration
            if 'Gmail' in resp.text:
                self.log("✅", "Gmail integration section found")
            else:
                self.add_suggestion("Add Gmail integration for creating drafts")
                
            # Check for OpenAI
            if 'OpenAI' in resp.text:
                self.log("✅", "OpenAI configuration section found")
            else:
                self.add_suggestion("Add OpenAI API key configuration")
                
            # Test saving API key
            api_key_data = {
                'hunter_api_key': 'test_hunter_key_12345',
                'apollo_api_key': 'test_apollo_key_67890'
            }
            
            resp = self.session.post(f"{BASE_URL}/save-api-keys", data=api_key_data, allow_redirects=True)
            
            if resp.status_code == 200:
                self.log("✅", "API keys saved successfully")
                
                if 'Success' in resp.text or 'configured' in resp.text.lower():
                    self.log("✅", "Success message displayed")
                else:
                    self.add_suggestion("Add clear success message when API keys are saved")
            else:
                self.add_issue(f"Saving API keys failed: HTTP {resp.status_code}")
                
        except Exception as e:
            self.add_issue(f"Settings test failed: {e}")
            
    def test_dashboard(self):
        self.log("\n🧪", "TEST 4: Dashboard & Search History")
        print("=" * 70)
        
        try:
            resp = self.session.get(f"{BASE_URL}/app")
            
            if resp.status_code == 200:
                self.log("✅", "Dashboard accessible")
                
                if 'Generate Leads' in resp.text or 'Lead' in resp.text:
                    self.log("✅", "Lead generation interface present")
                else:
                    self.add_issue("Dashboard missing lead generation interface")
                    
            else:
                self.add_issue(f"Dashboard returned HTTP {resp.status_code}")
                
        except Exception as e:
            self.add_issue(f"Dashboard test failed: {e}")
            
    def test_lead_generation(self):
        self.log("\n🧪", "TEST 5: Lead Generation Flow")
        print("=" * 70)
        
        try:
            # Note: This will fail without real API keys configured
            lead_data = {
                'domain': 'stripe.com',
                'domain_type': 'pm',
                'company_name': 'Stripe'
            }
            
            resp = self.session.post(f"{BASE_URL}/generate", data=lead_data, allow_redirects=True)
            
            if resp.status_code == 200:
                if 'No leads found' in resp.text or 'provider' in resp.text.lower():
                    self.log("⚠️", "Lead generation requires valid API keys (expected)")
                elif 'lead' in resp.text.lower():
                    self.log("✅", "Lead generation interface working")
                else:
                    self.add_suggestion("Improve error messages when API keys are not valid")
            else:
                self.log("⚠️", f"Generate endpoint: HTTP {resp.status_code}")
                
        except Exception as e:
            self.log("⚠️", f"Lead generation (expected without real keys): {e}")
            
    def test_batch_page(self):
        self.log("\n🧪", "TEST 6: Batch Generation Feature")
        print("=" * 70)
        
        try:
            resp = self.session.get(f"{BASE_URL}/batch")
            
            if resp.status_code == 200:
                self.log("✅", "Batch page accessible")
                
                if 'multiple' in resp.text.lower() or 'domains' in resp.text.lower():
                    self.log("✅", "Batch interface explains multi-domain feature")
                else:
                    self.add_suggestion("Add clear instructions for batch processing")
            else:
                self.add_issue(f"Batch page returned HTTP {resp.status_code}")
                
        except Exception as e:
            self.add_issue(f"Batch test failed: {e}")
            
    def test_api_endpoints(self):
        self.log("\n🧪", "TEST 7: API Endpoints")
        print("=" * 70)
        
        try:
            resp = self.session.get(f"{BASE_URL}/api/provider-status")
            
            if resp.status_code == 200:
                try:
                    data = resp.json()
                    self.log("✅", f"Provider status API working: {len(data)} providers")
                except:
                    self.add_issue("Provider status API didn't return valid JSON")
            else:
                self.log("ℹ️", f"Provider status API: HTTP {resp.status_code}")
                
        except Exception as e:
            self.log("⚠️", f"API test: {e}")
            
    def test_logout(self):
        self.log("\n🧪", "TEST 8: Logout Functionality")
        print("=" * 70)
        
        try:
            resp = self.session.get(f"{BASE_URL}/logout", allow_redirects=True)
            
            if '/login' in resp.url or resp.url == BASE_URL + '/':
                self.log("✅", "Logout successful, redirected to login/home")
            else:
                self.add_issue(f"Logout redirected to unexpected page: {resp.url}")
                
        except Exception as e:
            self.add_issue(f"Logout test failed: {e}")
            
    def generate_report(self):
        print("\n\n" + "=" * 70)
        print("📊 COMPREHENSIVE TEST REPORT")
        print("=" * 70)
        
        print(f"\n✅ Total Issues Found: {len(self.issues_found)}")
        if self.issues_found:
            for i, issue in enumerate(self.issues_found, 1):
                print(f"   {i}. {issue}")
        else:
            print("   No critical issues found!")
            
        print(f"\n💡 Suggestions for Improvement: {len(self.suggestions)}")
        if self.suggestions:
            for i, suggestion in enumerate(self.suggestions, 1):
                print(f"   {i}. {suggestion}")
        else:
            print("   No suggestions - app looks great!")
            
        print("\n" + "=" * 70)
        print("🎯 RECOMMENDED FEATURES TO ADD:")
        print("=" * 70)
        recommendations = [
            "Email templates management - Let users create custom email templates",
            "Lead scoring system - Rank leads by match quality",
            "Export to CRM - Integrate with Salesforce, HubSpot, etc.",
            "Team collaboration - Share leads with team members",
            "Analytics dashboard - Show API usage, success rates, etc.",
            "Webhook notifications - Alert when leads are found",
            "Custom fields - Let users add custom data to leads",
            "Lead enrichment - Add company info, social profiles",
            "Follow-up scheduler - Schedule email sequences",
            "Mobile app - iOS/Android companion apps"
        ]
        for i, rec in enumerate(recommendations[:5], 1):
            print(f"   {i}. {rec}")
        
        print("\n" + "=" * 70)
        print("✅ TESTING COMPLETE - Check issues and suggestions above")
        print("=" * 70)
        

def main():
    print("\n" + "=" * 70)
    print("🎭 COMPREHENSIVE AUTOMATED E2E TESTING")
    print("=" * 70)
    
    tester = TestSession()
    
    # Run all tests in sequence
    tests = [
        tester.test_homepage,
        tester.test_signup,
        tester.test_settings_page,
        tester.test_dashboard,
        tester.test_lead_generation,
        tester.test_batch_page,
        tester.test_api_endpoints,
        tester.test_logout
    ]
    
    for test in tests:
        try:
            test()
            time.sleep(0.3)  # Brief pause between tests
        except Exception as e:
            tester.add_issue(f"Test execution error: {e}")
    
    tester.generate_report()


if __name__ == "__main__":
    main()
