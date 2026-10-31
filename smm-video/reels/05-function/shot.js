const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 540, height: 960 }, deviceScaleFactor: 2 });
  await p.goto('file://' + __dirname + '/cover.html');
  await p.screenshot({ path: 'cover.jpg', type: 'jpeg', quality: 92 });
  await b.close();
})();
