const { chromium } = require('playwright-core');
(async () => { const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--no-sandbox'] });
const p = await b.newPage({ viewport: { width: 1280, height: 720 } }); await p.goto('file://' + __dirname + '/thumb.html'); await p.waitForTimeout(300);
await p.screenshot({ path: __dirname + '/../thumbnail.jpg', type: 'jpeg', quality: 92 }); await b.close(); })();
