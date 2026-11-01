// node shot.js <in.html> <out.jpg>
const { chromium } = require('playwright-core');
(async () => { const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1243/chrome-linux64/chrome', args: ['--no-sandbox'] });
const p = await b.newPage({ viewport: { width: 1280, height: 720 } }); await p.goto('file://' + __dirname + '/' + process.argv[2]); await p.waitForTimeout(400);
await p.screenshot({ path: __dirname + '/' + process.argv[3], type: 'jpeg', quality: 92 }); await b.close(); })();
