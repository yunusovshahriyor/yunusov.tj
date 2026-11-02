const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 560, height: 740 }, deviceScaleFactor: 2 });
  await p.goto('file://' + __dirname + '/character.html');
  await p.screenshot({ path: __dirname + '/../character.png' });
  await b.close();
})();
