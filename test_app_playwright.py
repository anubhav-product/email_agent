"""
Playwright tests for LeadFinder AI SaaS Application
Tests all features and identifies issues
"""

import time
from playwright.sync_api import sync_playwright, expect

BASE_URL = "http://127.0.0.1:5000"

def test_homepage():
    """Test landing page loads correctly"""
    print("\n🧪 TEST 1: Homepage / Landing Page")
    print("=" * 60)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            page.goto(BASE_URL, timeout=10000)
            print(f"✅ Page loaded: {page.title()}")
            
            # Check for key elements
            if "LeadFinder" in page.title():
                print("✅ Page title contains 'LeadFinder'")
            else:
                print(f"⚠️  Unexpected title: {page.title()}")
            
            # Check for signup/login links
            if page.locator("text=Sign Up").count() > 0:
                print("✅ 'Sign Up' link found")
            else:
                print("❌ 'Sign Up' link NOT found")
            
            if (page.locator("text=Login").count() > 0 or
                page.locator("text=Log in").count() > 0 or
                page.locator("text=Sign In").count() > 0):
                print("✅ 'Login' link found")
            else:
                print("⚠️  'Login' link NOT found")
                
            # Screenshot
            page.screenshot(path="/tmp/homepage.png")
            print("📸 Screenshot saved: /tmp/homepage.png")
            
        except Exception as e:
            print(f"❌ ERROR: {e}")
        finally:
            browser.close()


def test_signup_flow():
    """Test user signup process"""
    print("\n🧪 TEST 2: Signup Flow")
    print("=" * 60)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            # Go to signup page
            page.goto(f"{BASE_URL}/signup", timeout=10000)
            print(f"✅ Signup page loaded: {page.title()}")
            
            # Check for form fields
            name_field = page.locator('input[name="name"]')
            email_field = page.locator('input[name="email"]')
            password_field = page.locator('input[name="password"]')
            
            if name_field.count() > 0:
                print("✅ Name field found")
            else:
                print("❌ Name field NOT found")
                
            if email_field.count() > 0:
                print("✅ Email field found")
            else:
                print("❌ Email field NOT found")
                
            if password_field.count() > 0:
                print("✅ Password field found")
            else:
                print("❌ Password field NOT found")
            
            # Try to create account
            test_email = f"test_{int(time.time())}@example.com"
            name_field.fill("Test User")
            email_field.fill(test_email)
            password_field.fill("testpass123")
            
            confirm_field = page.locator('input[name="confirm_password"]')
            if confirm_field.count() > 0:
                confirm_field.fill("testpass123")
                print("✅ Confirm password field found and filled")
            
            page.screenshot(path="/tmp/signup_filled.png")
            print("📸 Screenshot saved: /tmp/signup_filled.png")
            
            # Submit form
            page.locator('button[type="submit"]').click()
            page.wait_for_load_state("networkidle", timeout=5000)
            
            current_url = page.url
            print(f"✅ Form submitted, redirected to: {current_url}")
            
            if "/settings" in current_url or "/app" in current_url:
                print("✅ Successfully redirected after signup")
            else:
                print(f"⚠️  Unexpected redirect: {current_url}")

            # Check cold email options page
            if page.locator("text=Cold Email").count() > 0:
                page.locator("text=Cold Email").first.click()
                page.wait_for_url("**/cold-email-options", timeout=5000)
                has_general = page.locator("text=General Outreach").count() > 0
                has_job = page.locator("text=Job Seeker Outreach").count() > 0
                print(f"✅ Cold Email options visible: General={has_general}, Job={has_job}")
            
            page.screenshot(path="/tmp/after_signup.png")
            print("📸 Screenshot saved: /tmp/after_signup.png")
            
        except Exception as e:
            print(f"❌ ERROR: {e}")
            page.screenshot(path="/tmp/signup_error.png")
        finally:
            browser.close()


def test_login_flow():
    """Test login functionality"""
    print("\n🧪 TEST 3: Login Flow")
    print("=" * 60)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            page.goto(f"{BASE_URL}/login", timeout=10000)
            print(f"✅ Login page loaded: {page.title()}")
            
            # Check form fields
            email_field = page.locator('input[name="email"]')
            password_field = page.locator('input[name="password"]')
            
            if email_field.count() > 0 and password_field.count() > 0:
                print("✅ Login form fields found")
            else:
                print("❌ Login form incomplete")
            
            page.screenshot(path="/tmp/login_page.png")
            print("📸 Screenshot saved: /tmp/login_page.png")
            
        except Exception as e:
            print(f"❌ ERROR: {e}")
        finally:
            browser.close()


def test_settings_page():
    """Test settings page (requires auth)"""
    print("\n🧪 TEST 4: Settings Page (Unauthenticated)")
    print("=" * 60)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            page.goto(f"{BASE_URL}/settings", timeout=10000)
            
            # Should redirect to login if not authenticated
            current_url = page.url
            print(f"Current URL: {current_url}")
            
            if "/login" in current_url:
                print("✅ Correctly redirects to login when not authenticated")
            elif "/settings" in current_url:
                print("⚠️  Settings page accessible without auth (potential security issue)")
            
            page.screenshot(path="/tmp/settings_unauth.png")
            
        except Exception as e:
            print(f"❌ ERROR: {e}")
        finally:
            browser.close()


def test_dashboard_page():
    """Test dashboard page"""
    print("\n🧪 TEST 5: Dashboard Page")
    print("=" * 60)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            page.goto(f"{BASE_URL}/app", timeout=10000)
            current_url = page.url
            
            if "/login" in current_url:
                print("✅ Dashboard requires authentication (redirect to login)")
            else:
                print(f"Current URL: {current_url}")
            
            page.screenshot(path="/tmp/dashboard.png")
            
        except Exception as e:
            print(f"❌ ERROR: {e}")
        finally:
            browser.close()


def check_page_errors():
    """Check for JavaScript errors and console warnings"""
    print("\n🧪 TEST 6: Check for Page Errors")
    print("=" * 60)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        errors = []
        warnings = []
        
        # Capture console messages
        page.on("console", lambda msg: 
            errors.append(msg.text) if msg.type == "error" else 
            warnings.append(msg.text) if msg.type == "warning" else None
        )
        
        # Capture page errors
        page.on("pageerror", lambda exc: errors.append(str(exc)))
        
        try:
            # Test multiple pages
            pages_to_test = ["/", "/signup", "/login"]
            
            for path in pages_to_test:
                print(f"\n  Testing: {BASE_URL}{path}")
                page.goto(f"{BASE_URL}{path}", timeout=10000, wait_until="networkidle")
                time.sleep(1)  # Wait for any delayed errors
                
            if errors:
                print(f"\n❌ Found {len(errors)} JavaScript errors:")
                for err in errors[:5]:  # Show first 5
                    print(f"   • {err[:100]}")
            else:
                print("\n✅ No JavaScript errors found")
                
            if warnings:
                print(f"\n⚠️  Found {len(warnings)} warnings:")
                for warn in warnings[:3]:
                    print(f"   • {warn[:100]}")
            else:
                print("✅ No console warnings")
                
        except Exception as e:
            print(f"❌ ERROR: {e}")
        finally:
            browser.close()


def run_all_tests():
    """Run all tests in sequence"""
    print("\n" + "=" * 70)
    print("🎭 PLAYWRIGHT E2E TESTING - LeadFinder AI")
    print("=" * 70)
    
    tests = [
        test_homepage,
        test_signup_flow,
        test_login_flow,
        test_settings_page,
        test_dashboard_page,
        check_page_errors
    ]
    
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"\n❌ Test failed with exception: {e}")
        time.sleep(0.5)
    
    print("\n" + "=" * 70)
    print("✅ TESTING COMPLETE")
    print("=" * 70)
    print("\n📋 SUMMARY & RECOMMENDATIONS:")
    print("  1. Check screenshots in /tmp/ folder for visual verification")
    print("  2. Review any errors or warnings above")
    print("  3. Test authenticated features (settings, dashboard) manually")
    print("  4. Add automated tests for lead generation flow")
    print("  5. Test API key validation and error handling")
    print("\n")


if __name__ == "__main__":
    run_all_tests()
