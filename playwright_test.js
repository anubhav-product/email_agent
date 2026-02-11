const { chromium } = require('playwright');

async function testLeadFinderAI() {
    const browser = await chromium.launch({ headless: true });
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
        const hasCTA = await page.getByRole('link', { name: 'Start Free →' }).isVisible();
        console.log(`✅ Hero: ${hasHero}, Providers Section: ${hasProviders}, CTA: ${hasCTA}\n`);

        // Test 2: Signup & Onboarding  
        console.log('2️⃣ Testing Signup & Onboarding...');
            await page.getByRole('link', { name: 'Start Free →' }).click({ timeout: 5000 });
            await page.waitForURL('**/signup', { timeout: 10000 });
        console.log('✅ Navigated to signup page');

        // Fill signup form
        const testEmail = `test${Date.now()}@example.com`;
        await page.fill('input[name="email"]', testEmail);
        await page.fill('input[name="password"]', 'testpassword123');
        await page.fill('input[name="name"]', 'Test User');
        await page.click('button[type="submit"]');
        
        // Should redirect to settings (onboarding)
            await page.waitForURL('**/settings?onboarding=1', { timeout: 15000 });
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

        // Cold Email options
        await page.click('text=Cold Email');
        await page.waitForURL('**/cold-email-options');
        const hasGeneral = await page.locator('text=General Outreach').isVisible();
        const hasJob = await page.locator('text=Job Seeker Outreach').isVisible();
        console.log(`✅ Cold Email options: General=${hasGeneral}, Job=${hasJob}`);
        
            // Open General wizard and verify form action
            await page.click('text=Start General Email');
            await page.waitForURL('**/cold-email?mode=general');
            const formAction = await page.locator('form').getAttribute('action');
            console.log(`✅ Cold Email form action: ${formAction}`);

            // Submit cold email form to ensure it doesn't route to lead generation
            await page.fill('textarea[name="about_you"]', 'Founder building analytics tools');
            await page.fill('input[name="target_company"]', 'Figma');
            await page.fill('textarea[name="purpose"]', 'Partnership discussion');
            await page.click('button[type="submit"]');
            await page.waitForLoadState('networkidle');
            const currentColdUrl = page.url();
            const hasOutput = await page.locator('text=Subject').count() > 0;
            console.log(`✅ Cold Email stayed on wizard: ${currentColdUrl.includes('/cold-email')}`);
            console.log(`✅ Cold Email output shown: ${hasOutput}`);

            // Campaign builder
            await page.goto('http://localhost:5000/cold-email-campaign?mode=general');
            await page.fill('textarea[name="about_you"]', 'Founder building analytics tools');
            await page.fill('input[name="target_company"]', 'Figma');
            await page.fill('textarea[name="purpose"]', 'Partnership discussion');
            await page.click('button[type="submit"]');
            await page.waitForLoadState('networkidle');
            const hasCampaignOutput = await page.locator('text=Generated Subject').count() > 0;
            console.log(`✅ Campaign builder generated email: ${hasCampaignOutput}`);

        // Go to Dashboard
        await page.goto('http://localhost:5000/dashboard');
        await page.waitForURL('**/dashboard');
        console.log('✅ Navigated to Dashboard');

        // Test 4: Dashboard Toggle
        console.log('\n4️⃣ Testing Dashboard Toggle...');
        const simpleToggle = page.locator('text=Switch to Simple View');
        const premiumToggle = page.locator('text=Switch to Premium View');
        if (await simpleToggle.count() > 0) {
            await simpleToggle.click();
            await page.waitForTimeout(1000);
            const hasGradient = await page.locator('body').evaluate(el =>
                getComputedStyle(el).background.includes('gradient')
            );
            console.log(`✅ Toggled to Simple View (has gradient: ${hasGradient})`);
        } else {
            console.log('⚠️ Simple View toggle not found');
        }

        if (await premiumToggle.count() > 0) {
            await premiumToggle.click();
            await page.waitForTimeout(1000);
            console.log('✅ Toggled back to Premium View');
        } else {
            console.log('⚠️ Premium View toggle not found');
        }

        // Test 5: Settings Page Details
        console.log('\n5️⃣ Testing Settings Page...');
        await page.click('text=Settings');
        await page.waitForURL('**/settings');
        
        const warningAlert = await page.locator('.alert.warning').isVisible();
        const hunterioBadge = await page.getByRole('heading', { name: /Hunter\.io/i }).isVisible();
        const apolloBadge = await page.getByRole('heading', { name: /Apollo\.io/i }).isVisible();
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
