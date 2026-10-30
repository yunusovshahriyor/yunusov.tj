const { chromium } = require('playwright-core');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 600, height: 900 }, deviceScaleFactor: 1 });
  await p.goto('file://' + __dirname + '/cheatsheet.html');
  await p.pdf({ path: __dirname + '/shpargalka-darsho-1-4.pdf', width: '600px', height: '900px', printBackground: true, preferCSSPageSize: true });
  // превью страниц для проверки вёрстки
  const n = await p.$$eval('.page', (els) => els.length);
  for (let i = 0; i < n; i++) {
    const el = (await p.$$('.page'))[i];
    await el.screenshot({ path: `/tmp/pdfprev-${i + 1}.png` });
  }
  await b.close();
})();
