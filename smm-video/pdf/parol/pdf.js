// node pdf.js <preview-dir> — PDF + превью страниц
const { chromium } = require('playwright-core');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 600, height: 900 } });
  await p.goto('file://' + __dirname + '/parol.html'); await p.waitForTimeout(400);
  await p.pdf({ path: __dirname + '/7-qoidai-paroli-bekhatar.pdf', width: '600px', height: '900px', printBackground: true, preferCSSPageSize: true });
  const els = await p.$$('.page');
  for (let i = 0; i < els.length; i++) await els[i].screenshot({ path: `${process.argv[2]}/pp-${i + 1}.png` });
  await b.close();
})();
