const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 600, height: 314 }, deviceScaleFactor: 2 });
  await p.goto('file://' + __dirname + '/quiz-royhat-banner.html');
  await p.screenshot({ path: __dirname + '/quiz-royhat-banner.jpg', type: 'jpeg', quality: 92 });
  await b.close();
})();
