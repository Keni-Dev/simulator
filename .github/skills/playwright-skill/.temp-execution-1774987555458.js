const { chromium } = require('playwright');

const TARGET_URL = 'http://localhost:3000';

(async () => {
  const browser = await chromium.launch({ headless: false, slowMo: 100 });
  const context = await browser.newContext({
    permissions: ['camera'], // Grant camera permission
  });
  const page = await context.newPage();
  
  await page.setViewportSize({ width: 1920, height: 1080 });
  await page.goto(TARGET_URL, { waitUntil: 'networkidle', timeout: 30000 });
  
  // Wait longer for the HUD and 3D scene to render
  console.log('Waiting for scene to initialize...');
  await page.waitForTimeout(6000);
  
  console.log('Page loaded:', await page.title());
  
  await page.screenshot({ 
    path: '/tmp/hud-redesigned.png', 
    fullPage: true 
  });
  console.log('📸 Screenshot saved to /tmp/hud-redesigned.png');
  
  await browser.close();
})();
