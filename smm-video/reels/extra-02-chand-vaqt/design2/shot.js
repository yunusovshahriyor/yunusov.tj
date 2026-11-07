const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ args: ['--no-sandbox'] });
  for (let i = 1; i <= 10; i++) {
    const p = await b.newPage({ viewport: { width: 540, height: 960 }, deviceScaleFactor: 2 });
    await p.goto('file://' + __dirname + '/g' + i + '.html');
    await p.screenshot({ path: `glass-${i}.png` });
    await p.close();
  }
  await b.close();
})();
