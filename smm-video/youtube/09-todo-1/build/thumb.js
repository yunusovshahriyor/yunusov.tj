const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--no-sandbox'] });
const p = await b.newPage({ viewport: { width: 1280, height: 720 } }); await p.goto('file://' + __dirname + '/thumb6.html'); await p.waitForTimeout(400);
await p.screenshot({ path: __dirname + '/../thumbnail.jpg', type: 'jpeg', quality: 92 }); await b.close(); })();
