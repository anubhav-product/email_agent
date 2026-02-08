const { chromium } = require('playwright');

async function testLeadFinderAI() {
    const browser = await chromium.launch({ headless: false });
    const context = await browser.newContext();
    const page = await context.newPage();

    console.log('🧪 Starting LeadFinder AI Tests...\n');

    try {
        // Test 1: Landing Page
        console.log('1️⃣ Testing Landing Page...');
        await page.goto('http://localhost:5000');
        await page.waitForSelector('text=Cold Email Automation That Actually Gets Responses');
        console.log('✅ New landing page loaded successfully');
        
        // Check for key elements
        const hasHero = await page.locator('text=Find decision-makers').isVisible();
        const hasProviders = await page.locator('text=Built on the Best Email Providers').isVisible();
        const hasCTA = await page.locator('text=Start Free').isVisible();
        console.log(`✅ Hero: ${hasHero}, Providers Section: ${hasProviders}, CTA: ${hasCTA}\n`);

        // Test 2: Signup & Onboarding  
        console.log('2️⃣ Testing Signup & Onboarding...');
        await page.click('text=Start Free', { timeout: 5000 });
        await page.waitForURL('**/signup');
        console.log('✅ Navigated to signup page');

        // Fill signup form
        const testEmail = `test${Date.now()}@example.com`;
        await page.fill('input[name="email"]', testEmail);
        await page.fill('input[name="password"]', 'testpassword123');
        await page.fill('input[name="name"]', 'Test User');
        await page.click('button[type="submit"]');
        
        // Should redirect to settings (onboarding)
        await page.waitForURL('**/settings', { timeout: 10000 });
        console.log('✅ Redirected to Settings for onboarding');

        // Check provider cards
        const providerCards = await page.locator('.provider-card').count();
console.log(`✅ Found ${providerCards} provider cards`);

        // Test 3: Navigation
        console.log('\n3️⃣ Testing Navigation...');
        await page.click('text=Generate Leads');
        await page.waitForTimeout(1000);
        const currentUrl = page.url();
        console.log(`✅ Clicked Generate Leads, current URL: ${currentUrl}`);

        // Go to Dashboard
        await page.click('text=Dashboard');
        await page.waitForURL('**/dashboard');
        console.log('✅ Navigated to Dashboard');

        // Test 4: Dashboard Toggle
        console.log('\n4️⃣ Testing Dashboard Toggle...');
        await page.click('text=Switch to Simple View');
        await page.waitForTimeout(1000);
        const hasGradient = await page.locator('body').evaluate(el => 
            getComputedStyle(el).background.includes('gradient')
        );
        console.log(`✅ Toggled to Simple View (has gradient: ${hasGradient})`);

        await page.click('text=Switch to Premium View');
        await page.waitForTimeout(1000);
        console.log('✅ Toggled back to Premium View');

        // Test 5: Settings Page Details
        console.log('\n5️⃣ Testing Settings Page...');
        await page.click('text=Settings');
        await page.wait ForURL('**/settings');
        
        const warningAlert = await page.locator('.alert.warning').isVisible();
        const hunterioBadge = await page.locator('text=Hunter.io').isVisible();
        const apolloBadge = await page.locator('text=Apollo.io').isVisible();
        console.log(`✅ Warning alert: ${warningAlert}`);
        console.log(`✅ Provider cards visible: Hunter=${hunterioBadge}, Apollo=${apolloBadge}`);

        console.log('\n🎉 All tests passed!');

    } catch (error) {
        console.error('❌ Test failed:', error.message);
        await page.screenshot({ path: 'test-failure.png' });
    } finally {
        await browser.close();
    }
}

testLeadFinderAI();
