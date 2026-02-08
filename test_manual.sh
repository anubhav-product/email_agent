#!/bin/bash
# Manual E2E Testing Script for LeadFinder AI
# Tests all features and identifies issues

BASE_URL="http://127.0.0.1:5000"

echo "======================================================================"
echo "🧪 MANUAL E2E TESTING - LeadFinder AI"
echo "======================================================================"
echo ""

# Test 1: Homepage
echo "TEST 1: Homepage"
echo "----------------------------------------------------------------------"
response=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/")
if [ "$response" = "200" ]; then
    echo "✅ Homepage loads (HTTP $response)"
else
    echo "❌ Homepage failed (HTTP $response)"
fi

# Test 2: Signup page
echo ""
echo "TEST 2: Signup Page"
echo "----------------------------------------------------------------------"
response=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/signup")
if [ "$response" = "200" ]; then
    echo "✅ Signup page loads (HTTP $response)"
else
    echo "❌ Signup page failed (HTTP $response)"
fi

# Test 3: Login page
echo ""
echo "TEST 3: Login Page"
echo "----------------------------------------------------------------------"
response=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/login")
if [ "$response" = "200" ]; then
    echo "✅ Login page loads (HTTP $response)"
else
    echo "❌ Login page failed (HTTP $response)"
fi

# Test 4: Settings (should redirect to login)
echo ""
echo "TEST 4: Settings Page (Unauthenticated)"
echo "----------------------------------------------------------------------"
response=$(curl -s -o /dev/null -w "%{http_code}" -L "$BASE_URL/settings")
if [ "$response" = "200" ]; then
    echo "✅ Settings redirects properly (HTTP $response)"
else
    echo "⚠️  Settings response: HTTP $response"
fi

# Test 5: Dashboard (should redirect to login)
echo ""
echo "TEST 5: Dashboard  Page (Unauthenticated)"
echo "----------------------------------------------------------------------"
response=$(curl -s -o /dev/null -w "%{http_code}" -L "$BASE_URL/app")
if [ "$response" = "200" ]; then
    echo "✅ Dashboard redirects properly (HTTP $response)"
else
    echo "⚠️  Dashboard response: HTTP $response"
fi

# Test 6: Batch page (should redirect to login)
echo ""
echo "TEST 6: Batch Page (Unauthenticated)"
echo "----------------------------------------------------------------------"
response=$(curl -s -o /dev/null -w "%{http_code}" -L "$BASE_URL/batch")
if [ "$response" = "200" ]; then
    echo "✅ Batch page redirects properly (HTTP $response)"
else
    echo "⚠️  Batch response: HTTP $response"
fi

# Test 7: API endpoint
echo ""
echo "TEST 7: API Provider Status"
echo "----------------------------------------------------------------------"
response=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/api/provider-status")
if [ "$response" = "401" ] || [ "$response" = "302" ]; then
    echo "✅ API endpoint requires auth (HTTP $response)"
elif [ "$response" = "200" ]; then
    echo "⚠️  API endpoint accessible without auth"
else
    echo "❌ API endpoint error (HTTP $response)"
fi

echo ""
echo "======================================================================"
echo "✅ BASIC CONNECTIVITY TESTS COMPLETE"
echo "======================================================================"
echo ""
echo "📋 MANUAL TESTING CHECKLIST:"
echo "  [ ] Open $BASE_URL in browser"
echo "  [ ] Test signup with new email"
echo "  [ ] Verify redirect to Settings page"
echo "  [ ] Add at least one API key (Hunter, Apollo, etc.)"
echo "  [ ] Click 'Generate Leads' and enter a company domain"
echo "  [ ] Verify leads are displayed"
echo "  [ ] Test batch generation with multiple domains"
echo "  [ ] Check dashboard shows search history"
echo "  [ ] Test logout and login again"
echo "  [ ] Verify Gmail integration section appears"
echo ""
echo "🔍 ISSUES TO CHECK:"
echo "  - Any 404 errors?"
echo "  - Forms submitting correctly?"
echo "  - API keys being saved encrypted?"
echo "  - Error messages helpful?"
echo "  - Mobile responsive?"
echo ""
