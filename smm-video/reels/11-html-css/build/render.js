const { chromium } = require('playwright');
(async () => {
  const END = parseFloat(process.argv[2]), out = process.argv[3], fps = 30;
  const b = await chromium.launch({ args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 540, height: 960 }, deviceScaleFactor: 2 });
  await p.goto('file://' + __dirname + '/reel.html');
  await p.evaluate(() => document.getAnimations().forEach(a => a.pause()));
  for (let i = 0; i < Math.round(fps * END); i++) {
    await p.evaluate(t => document.getAnimations().forEach(a => { a.currentTime = t; }), (i / fps) * 1000);
    await p.screenshot({ path: `${out}/f${String(i).padStart(4, '0')}.jpg`, type: 'jpeg', quality: 90 });
  }
  await b.close();
})();
