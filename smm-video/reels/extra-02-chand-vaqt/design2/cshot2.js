const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ args: ['--no-sandbox'] });
  for (const n of ['A', 'B']) {
    const p = await b.newPage({ viewport: { width: 540, height: 960 }, deviceScaleFactor: 2 });
    await p.goto('file://' + __dirname + '/cover' + n + '.html');
    await p.screenshot({ path: `../cover-${n}.jpg`, type: 'jpeg', quality: 93 });
    await p.close();
  }
  await b.close();
})();
