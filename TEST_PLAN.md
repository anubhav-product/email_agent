# LeadFinder AI - Test Plan

## User Flow Testing with Playwright

### Test 1: Landing Page
- Visit http://localhost:5000
- Verify new cold email landing page loads
- Check for: Hero section, features, providers, CTA buttons
- Click "Start Free" button → should go to /signup

### Test 2: Signup & Onboarding
- Fill signup form with test email/password
- Submit
- Should redirect to /settings (onboarding)
- Verify warning about no providers configured
- Verify all 4 provider cards shown (none enabled)
- Verify clear instructions on how to add API keys

### Test 3: Navigation
- Click Dashboard link → should show dashboard
- Click Settings link → should show settings page
- Click Generate Leads link → should check for providers first
- If no providers, redirect to settings with warning message

### Test 4: Dashboard Toggle
- Go to dashboard
- Click "Switch to Simple View"
- Verify dashboard changes to gradient design
- Click "Switch to Premium View"  
- Verify dashboard changes back to white cards

### Test 5: Provider Status Indicator
- Go to main app (/app)
- Should see provider status badge at top:
  - Red if 0 providers
  - Orange if 1-2 providers
  - Green if 3-4 providers
- Badge should link to Settings

### Test 6: Error Handling
- Try to generate leads without providers
- Should redirect to Settings
- Should show helpful message about adding API keys
- NOT a technical error message

## Expected Results

✅ Professional cold email landing page
✅ Guided onboarding flow (signup → settings)
✅ Clear provider status everywhere
✅ Settings page with instructions
✅ Dashboard toggle works
✅ No confusing errors, only helpful guidance
✅ All navigation links work
✅ Responsive design

## Screenshots to Capture
1. Landing page hero
2. Settings page with provider cards
3. Main app with provider status
4. Dashboard (both views)
5. Error message example
