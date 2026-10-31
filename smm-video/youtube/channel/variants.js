const { chromium } = require('playwright-core');
(async () => { const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--no-sandbox'] });
const p = await b.newPage({ viewport: { width: 2560, height: 1440 } });
for (const v of ['vs','teal','neon','mix']) { await p.goto('file://' + __dirname + '/banner.html#' + v); await p.reload(); await p.waitForTimeout(300);
  await p.screenshot({ path: `${__dirname}/variants/banner-${v}.jpg`, type: 'jpeg', quality: 92 }); }
await b.close(); })();
