"""Simple synchronous test to find issues"""

import requests
import time

BASE_URL = "http://127.0.0.1:5000"
session = requests.Session()
issues = []
suggestions = []

print("=" * 70)
print("🔍 SIMPLE AUTOMATED TESTING")
print("=" * 70)

# Test 1: Homepage
print("\n1. Testing Homepage...")
try:
    resp = session.get(BASE_URL, timeout=5)
    print(f"   Status: {resp.status_code}")
    if resp.status_code == 200:
        if "LeadFinder" in resp.text or "Lead" in resp.text:
            print("   ✅ Homepage loaded successfully")
        else:
            print("   ⚠️ Homepage loaded but content looks unusual")
    else:
        issues.append(f"Homepage returned {resp.status_code}")
except Exception as e:
    issues.append(f"Homepage failed: {e}")
    print(f"   ❌ Error: {e}")

time.sleep(0.5)

# Test 2: Signup page
print("\n2. Testing Signup Page...")
try:
    resp = session.get(f"{BASE_URL}/signup", timeout=5)
    print(f"   Status: {resp.status_code}")
    if resp.status_code == 200:
        print("   ✅ Signup page accessible")
    else:
        issues.append(f"Signup page returned {resp.status_code}")
except Exception as e:
    issues.append(f"Signup page failed: {e}")
    print(f"   ❌ Error: {e}")

time.sleep(0.5)

# Test 3: Create account
print("\n3. Testing Account Creation...")
test_email = f"test_{int(time.time())}@example.com"
try:
    signup_data = {
        'name': 'Test User',
        'email': test_email,
        'password': 'testpass123',
        'confirm_password': 'testpass123'
    }
    resp = session.post(f"{BASE_URL}/signup", data=signup_data, allow_redirects=True, timeout=5)
    print(f"   Status: {resp.status_code}")
    if resp.status_code == 200:
        if '/settings' in resp.url:
            print(f"   ✅ Account created, redirected to Settings")
        else:
            print(f"   ✅ Account created, redirected to {resp.url}")
    else:
        issues.append(f"Signup failed: {resp.status_code}")
except Exception as e:
    issues.append(f"Signup failed: {e}")
    print(f"   ❌ Error: {e}")

time.sleep(0.5)

# Test 4: Settings page
print("\n4. Testing Settings Page...")
try:
    resp = session.get(f"{BASE_URL}/settings", timeout=5)
    print(f"   Status: {resp.status_code}")
    if resp.status_code == 200:
        # Check for providers
        providers_found = []
        if "Hunter" in resp.text:
            providers_found.append("Hunter")
        if "Apollo" in resp.text:
            providers_found.append("Apollo")
        if "Snov" in resp.text:
            providers_found.append("Snov")
        if "FindThatLead" in resp.text:
            providers_found.append("FindThatLead")
        if "Gmail" in resp.text:
            providers_found.append("Gmail")
        if "OpenAI" in resp.text:
            providers_found.append("OpenAI")
        
        print(f"   ✅ Settings loaded")
        print(f"   📋 Providers found: {', '.join(providers_found)}")
        
        if len(providers_found) < 4:
            suggestions.append(f"Only {len(providers_found)} providers found in settings")
    else:
        issues.append(f"Settings page returned {resp.status_code}")
except Exception as e:
    issues.append(f"Settings page failed: {e}")
    print(f"   ❌ Error: {e}")

time.sleep(0.5)

# Test 5: Save API key
print("\n5. Testing API Key Save...")
try:
    api_data = {
        'hunter_api_key': 'test_key_hunter_123'
    }
    resp = session.post(f"{BASE_URL}/save-api-keys", data=api_data, allow_redirects=True, timeout=5)
    print(f"   Status: {resp.status_code}")
    if resp.status_code == 200:
        print("   ✅ API key saved")
        if "success" in resp.text.lower() or "configured" in resp.text.lower():
            print("   ✅ Success message shown")
        else:
            suggestions.append("Add clear success message after saving API keys")
    else:
        issues.append(f"Save API keys failed: {resp.status_code}")
except Exception as e:
    issues.append(f"Save API keys failed: {e}")
    print(f"   ❌ Error: {e}")

time.sleep(0.5)

# Test 6: Dashboard
print("\n6. Testing Dashboard...")
try:
    resp = session.get(f"{BASE_URL}/app", timeout=5)
    print(f"   Status: {resp.status_code}")
    if resp.status_code == 200:
        print("   ✅ Dashboard accessible")
        if "Generate" in resp.text or "Lead" in resp.text:
            print("   ✅ Lead generation interface present")
        else:
            issues.append("Dashboard missing lead generation interface")
    else:
        issues.append(f"Dashboard returned {resp.status_code}")
except Exception as e:
    issues.append(f"Dashboard failed: {e}")
    print(f"   ❌ Error: {e}")

time.sleep(0.5)

# Test 7: Batch page
print("\n7. Testing Batch Generation...")
try:
    resp = session.get(f"{BASE_URL}/batch", timeout=5)
    print(f"   Status: {resp.status_code}")
    if resp.status_code == 200:
        print("   ✅ Batch page accessible")
    else:
        issues.append(f"Batch page returned {resp.status_code}")
except Exception as e:
    issues.append(f"Batch page failed: {e}")
    print(f"   ❌ Error: {e}")

time.sleep(0.5)

# Test 8: Gmail connect
print("\n8. Testing Gmail Connect...")
try:
    resp = session.get(f"{BASE_URL}/connect-gmail", timeout=5, allow_redirects=False)
    print(f"   Status: {resp.status_code}")
    if resp.status_code in [200, 302]:
        print("   ✅ Gmail connect route exists")
    else:
        issues.append(f"Gmail connect returned {resp.status_code}")
except Exception as e:
    issues.append(f"Gmail connect failed: {e}")
    print(f"   ❌ Error: {e}")

time.sleep(0.5)

# Test 9: Provider status API
print("\n9. Testing Provider Status API...")
try:
    resp = session.get(f"{BASE_URL}/api/provider-status", timeout=5)
    print(f"   Status: {resp.status_code}")
    if resp.status_code == 200:
        try:
            data = resp.json()
            print(f"   ✅ API working, {len(data)} providers")
        except:
            issues.append("Provider API didn't return valid JSON")
    else:
        print(f"   ℹ️ API status: {resp.status_code}")
except Exception as e:
    print(f"   ℹ️ API: {e}")

# === REPORT ===
print("\n" + "=" * 70)
print("📊 TEST RESULTS")
print("=" * 70)

print(f"\n❌ ISSUES FOUND: {len(issues)}")
if issues:
    for i, issue in enumerate(issues, 1):
        print(f"   {i}. {issue}")
else:
    print("   None - All tests passed!")

print(f"\n💡 SUGGESTIONS: {len(suggestions)}")
if suggestions:
    for i, sug in enumerate(suggestions, 1):
        print(f"   {i}. {sug}")
else:
    print("   None - App looks good!")

print("\n" + "=" * 70)
print("🎯 RECOMMENDED FEATURES TO ADD:")
print("=" * 70)
recommendations = [
    "✨ Email template builder - Let users create custom email templates",
    "📊 Analytics dashboard - Show API usage, success rates, conversion metrics",
    "🔄 Auto-export to CRM - Integrate with Salesforce, HubSpot, Pipedrive",
    "👥 Team collaboration - Share leads and templates with team members",
    "📧 Email scheduler - Schedule follow-up sequences automatically",
    "🎯 Lead scoring - Rank leads by title match, company size, etc.",
    "📱 Mobile app - iOS/Android companion for on-the-go lead generation",
    "🔔 Webhook notifications - Real-time alerts when leads are found",
    "🌐 LinkedIn integration - Enrich leads with LinkedIn profiles",
    "📈 A/B testing - Test different email templates and track performance"
]

for i, rec in enumerate(recommendations[:5], 1):
    print(f"   {i}. {rec}")

print("\n" + "=" * 70)
print("✅ TESTING COMPLETE")
print("=" * 70)
