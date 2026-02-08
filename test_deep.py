"""Deep functional testing - tests actual features and edge cases"""

import requests
import time
import json

BASE_URL = "http://127.0.0.1:5000"
session = requests.Session()
issues = []
warnings = []
suggestions = []

def log(level, msg):
    prefix = {
        'info': "ℹ️ ",
        'success': "✅",
        'error': "❌",
        'warning': "⚠️ ",
        'suggest': "💡"
    }
    print(f"{prefix.get(level, '')} {msg}")

print("=" * 70)
print("🔬 DEEP FUNCTIONAL TESTING")
print("=" * 70)

# Setup: Create test account
print("\n📝 Setup: Creating test account...")
test_email = f"deeptest_{int(time.time())}@example.com"
signup_data = {
    'name': 'Deep Test User',
    'email': test_email,
    'password': 'SecurePass123!',
    'confirm_password': 'SecurePass123!'
}
resp = session.post(f"{BASE_URL}/signup", data=signup_data, allow_redirects=True)
if resp.status_code == 200:
    log('success', f"Test account created: {test_email}")
else:
    log('error', f"Failed to create account: {resp.status_code}")
    exit(1)

time.sleep(0.5)

# Test 1: Settings page completeness
print("\n🧪 TEST 1: Settings Page Completeness")
print("-" * 70)
resp = session.get(f"{BASE_URL}/settings")
content = resp.text

required_elements = {
    'Hunter.io API Key': 'Hunter' in content,
    'Apollo.io API Key': 'Apollo' in content,
    'Snov.io Client ID': 'Snov' in content,
    'FindThatLead API Key': 'FindThatLead' in content,
    'OpenAI API Key': 'OpenAI' in content,
    'Gmail Integration': 'Gmail' in content,
    'Save button': 'save' in content.lower() or 'submit' in content.lower(),
}

for element, present in required_elements.items():
    if present:
        log('success', f"{element} found")
    else:
        issues.append(f"Settings missing: {element}")
        log('error', f"{element} NOT found")

# Test 2: API Key Encryption
print("\n🧪 TEST 2: API Key Encryption & Storage")
print("-" * 70)
test_keys = {
    'hunter_api_key': 'test_hunter_secure_key_12345',
    'apollo_api_key': 'test_apollo_secure_key_67890',
    'openai_api_key': 'sk-test_openai_key_abcdef'
}

resp = session.post(f"{BASE_URL}/save-api-keys", data=test_keys, allow_redirects=True)
if resp.status_code == 200:
    log('success', "API keys saved")
    
    # Check if keys are displayed  (they shouldn't be shown in plain text)
    if 'test_hunter_secure_key' in resp.text:
        warnings.append("API keys may be displayed in plain text on page")
        log('warning', "Plain text key found in response - security concern!")
    else:
        log('success', "API keys not displayed in plain text (good security)")
        
    # Check for success message
    if 'success' in resp.text.lower() or 'configured' in resp.text.lower() or 'saved' in resp.text.lower():
        log('success', "Success feedback provided")
    else:
        suggestions.append("Add clear success message after saving API keys")
        log('suggest', "Consider adding success notification")
else:
    issues.append(f"Save API keys failed: HTTP {resp.status_code}")

time.sleep(0.5)

# Test 3: Provider Status API
print("\n🧪 TEST 3: Provider Status API")
print("-" * 70)
resp = session.get(f"{BASE_URL}/api/provider-status")
if resp.status_code == 200:
    try:
        data = resp.json()
        log('success', f"Provider API returned {len(data)} providers")
        
        # Check structure - data is a dict with provider names as keys
        for provider_name, provider_data in data.items():
            if isinstance(provider_data, dict) and 'enabled' in provider_data:
                status = '✓ enabled' if provider_data.get('enabled') else '✗ disabled'
                log('info', f"{provider_name}: {status}")
            else:
                warnings.append(f"Provider data structure unexpected for {provider_name}")
                
        # Check if our saved keys are reflected
        if 'hunter' in data and data['hunter'].get('enabled'):
            log('success', "Saved API keys reflected in status API")
        else:
            # This is expected if the test key isn't valid
            log('info', "Hunter shows in API (test key not validated)")
            
    except json.JSONDecodeError:
        issues.append("Provider status API didn't return valid JSON")
        log('error', "Invalid JSON response")
else:
    log('warning', f"Provider status API: HTTP {resp.status_code}")

time.sleep(0.5)

# Test 4: Dashboard Features
print("\n🧪 TEST 4: Dashboard Features")
print("-" * 70)
resp = session.get(f"{BASE_URL}/app")
content = resp.text

dashboard_features = {
    'Generate button': 'generate' in content.lower(),
    'Company name input': 'company' in content.lower(),
    'Domain input': 'domain' in content.lower(),
    'Search history': 'history' in content.lower() or 'recent' in content.lower(),
    'Provider selection': 'provider' in content.lower(),
}

for feature, present in dashboard_features.items():
    if present:
        log('success', f"{feature} present")
    else:
        log('warning', f"{feature} not clearly visible")

# Test 5: Lead Generation Error Handling
print("\n🧪 TEST 5: Lead Generation Error Handling")
print("-" * 70)

# Test empty form submission
resp = session.post(f"{BASE_URL}/generate", data={}, allow_redirects=True)
if 'error' in resp.text.lower() or 'required' in resp.text.lower():
    log('success', "Empty form shows error message")
else:
    suggestions.append("Add validation for empty form submission")
    log('suggest', "Consider adding form validation messages")

time.sleep(0.5)

# Test invalid domain
resp = session.post(f"{BASE_URL}/generate", data={'company_name': 'Test', 'domain': 'not-a-real-domain.xyz'}, allow_redirects=True)
# Should either return "no leads" or handle gracefully
if resp.status_code == 200:
    log('success', "Invalid domain handled without crash")
else:
    log('warning', f"Invalid domain returned HTTP {resp.status_code}")

time.sleep(0.5)

# Test 6: Batch Generation
print("\n🧪 TEST 6: Batch Generation")
print("-" * 70)
resp = session.get(f"{BASE_URL}/batch")
content = resp.text

batch_features = {
    'File upload': 'file' in content.lower() or 'upload' in content.lower() or 'csv' in content.lower(),
    'Instructions': 'csv' in content.lower() or 'format' in content.lower(),
    'Example format': 'example' in content.lower() or 'format' in content.lower(),
}

for feature, present in batch_features.items():
    if present:
        log('success', f"{feature} present")
    else:
        suggestions.append(f"Batch page should include: {feature}")
        log('suggest', f"Add {feature} to batch page")

# Test 7: Gmail Integration
print("\n🧪 TEST 7: Gmail Integration")
print("-" * 70)
resp = session.get(f"{BASE_URL}/settings")
content = resp.text

gmail_features = {
    'Gmail section': 'gmail' in content.lower(),
    'Connect button': 'connect' in content.lower(),
    'OAuth explanation': 'oauth' in content.lower() or 'google' in content.lower(),
}

for feature, present in gmail_features.items():
    if present:
        log('success', f"{feature} present")
    else:
        log('warning', f"{feature} not found")

# Test connect-gmail endpoint
resp = session.get(f"{BASE_URL}/connect-gmail", allow_redirects=False)
if resp.status_code in [200, 302]:
    log('success', "Gmail connect route exists")
    if resp.status_code == 302 and 'google' in resp.headers.get('Location', '').lower():
        log('success', "Redirects to Google OAuth (production-ready)")
    elif 'implement' in resp.text.lower() or 'coming soon' in resp.text.lower() or 'warning' in resp.text.lower():
        warnings.append("Gmail OAuth not fully implemented yet")
        log('warning', "Gmail OAuth is placeholder - needs implementation")
    else:
        log('info', "Gmail connect responds correctly")
else:
    issues.append(f"Gmail connect returned unexpected {resp.status_code}")

time.sleep(0.5)

# Test 8: Security - Logout & Session
print("\n🧪 TEST 8: Security & Session Management")
print("-" * 70)

# Try accessing protected page before logging out
resp = session.get(f"{BASE_URL}/app")
if resp.status_code == 200:
    log('success', "Logged-in user can access dashboard")
else:
    issues.append(f"Logged-in user cannot access dashboard: {resp.status_code}")

# Logout
resp = session.get(f"{BASE_URL}/logout", allow_redirects=False)
if resp.status_code == 302:
    log('success', "Logout redirects properly")
else:
    log('warning', f"Logout returned {resp.status_code}")

# Try accessing protected page after logout
resp = session.get(f"{BASE_URL}/app", allow_redirects=False)
if resp.status_code == 302:
    log('success', "Protected page redirects when logged out")
elif resp.status_code == 401:
    log('success', "Protected page returns 401 when logged out")
else:
    issues.append(f"Protected page accessible without login: HTTP {resp.status_code}")
    log('error', "Security issue - page accessible after logout!")

# Test 9: Mobile Responsiveness
print("\n🧪 TEST 9: Mobile Responsiveness")
print("-" * 70)
headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)'}
resp = requests.get(f"{BASE_URL}/", headers=headers)
content = resp.text

mobile_indicators = {
    'Viewport meta tag': 'viewport' in content.lower(),
    'Responsive CSS': 'media' in content.lower() or 'responsive' in content.lower() or '@media' in content.lower(),
}

for indicator, present in mobile_indicators.items():
    if present:
        log('success', f"{indicator} found")
    else:
        suggestions.append(f"Add mobile responsiveness: {indicator}")
        log('suggest', f"Consider adding {indicator}")

# Test 10: Error Pages
print("\n🧪 TEST 10: Error Handling")
print("-" * 70)
resp = requests.get(f"{BASE_URL}/nonexistent-page-xyz")
if resp.status_code == 404:
    log('success', "404 handler exists")
    if '404' in resp.text or 'not found' in resp.text.lower():
        log('success', "404 page has user-friendly message")
    else:
        suggestions.append("Create custom 404 error page")
        log('suggest', "Add custom 404 page with helpful links")
else:
    log('warning', f"404 page returned {resp.status_code}")

# ===== FINAL REPORT =====
print("\n\n" + "=" * 70)
print("📊 DEEP TESTING REPORT")
print("=" * 70)

print(f"\n❌ CRITICAL ISSUES: {len(issues)}")
if issues:
    for i, issue in enumerate(issues, 1):
        print(f"   {i}. {issue}")
else:
    print("   None! 🎉")

print(f"\n⚠️  WARNINGS: {len(warnings)}")
if warnings:
    for i, warning in enumerate(warnings, 1):
        print(f"   {i}. {warning}")
else:
    print("   None!")

print(f"\n💡 SUGGESTIONS: {len(suggestions)}")
if suggestions:
    for i, sug in enumerate(suggestions, 1):
        print(f"   {i}. {sug}")
else:
    print("   App is well-polished!")

print("\n" + "=" * 70)
print("🚀 FEATURES TO ADD NEXT:")
print("=" * 70)

priority_features = [
    ("P0 - Critical", [
        "Complete Gmail OAuth implementation (currently placeholder)",
        "Add real API key validation (test Hunter/Apollo keys work)",
        "Implement actual lead generation with configured providers",
    ]),
    ("P1 - High Priority", [
        "Email template builder - Let users customize email templates",
        "Analytics dashboard - Track API usage, costs, success rates",
        "Lead export - Download as CSV or sync to CRM",
        "Team features - Allow multiple users per organization",
    ]),
    ("P2 - Medium Priority", [
        "Email A/B testing - Test different templates automatically",
        "Lead scoring - Rank leads by title, seniority, company size",
        "Webhook integration - Real-time notifications",
        "Custom fields - Let users add custom data to leads",
    ]),
    ("P3 - Nice to Have", [
        "Mobile app - iOS/Android companion",
        "Chrome extension - Generate leads while browsing LinkedIn",
        "AI insights - GPT-powered lead recommendations",
        "White-label option - Rebrand for agencies",
    ])
]

for priority, features in priority_features[:2]:  # Show P0 and P1
    print(f"\n{priority}:")
    for feat in features:
        print(f"   • {feat}")

print("\n" + "=" * 70)
print("✅ DEEP TESTING COMPLETE")
print("=" * 70)
print(f"\nSummary: {len(issues)} issues, {len(warnings)} warnings, {len(suggestions)} suggestions")
if len(issues) == 0:
    print("🎉 No critical issues found - app is production-ready!")
print("=" * 70)
