const { chromium } = require('playwright-core');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--no-sandbox'] });
  for (const [f, w, h] of JSON.parse(process.argv[2])) {
    const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 2 });
    await p.goto('file://' + __dirname + '/' + f + '.html');
    await p.screenshot({ path: __dirname + '/' + f + '.png' });
    await p.close();
  }
  await b.close();
})();
