const { chromium } = require('playwright-core');
(async () => { const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--no-sandbox'] });
const p = await b.newPage({ viewport: { width: 2560, height: 1440 } }); await p.goto('file://' + __dirname + '/banner.html'); await p.waitForTimeout(300);
await p.screenshot({ path: __dirname + '/banner.jpg', type: 'jpeg', quality: 92 });
await p.screenshot({ path: '/tmp/banner-mobile.png', clip: { x: 507, y: 509, width: 1546, height: 423 } }); await b.close(); })();
