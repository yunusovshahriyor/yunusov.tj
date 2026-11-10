const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ args: ['--no-sandbox'] });
  for (let i = 1; i <= 8; i++) {
    const p = await b.newPage({ viewport: { width: 540, height: 960 }, deviceScaleFactor: 2 });
    await p.goto('file://' + __dirname + '/f' + i + '.html');
    await p.screenshot({ path: `frame-${i}.png` });
    await p.close();
  }
  await b.close();
})();
