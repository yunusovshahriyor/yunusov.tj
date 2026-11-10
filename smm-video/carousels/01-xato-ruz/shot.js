const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ args: ['--no-sandbox'] });
  for (let i = 1; i <= 5; i++) {
    const p = await b.newPage({ viewport: { width: 540, height: 675 }, deviceScaleFactor: 2 });
    await p.goto('file://' + __dirname + '/slide-' + i + '.html');
    await p.screenshot({ path: `slide-${i}.jpg`, type: 'jpeg', quality: 92 });
    await p.close();
  }
  await b.close();
})();
