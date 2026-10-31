const { chromium } = require('playwright-core');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 320, height: 320 }, deviceScaleFactor: 2 });
  await p.goto('file://' + __dirname + '/avatar.html');
  await p.screenshot({ path: __dirname + '/avatar.png' });
  await b.close();
})();
