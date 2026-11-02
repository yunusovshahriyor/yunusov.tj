const { chromium } = require('playwright');
(async () => {
  const END = parseFloat(process.argv[2]), out = process.argv[3], fps = parseInt(process.argv[4] || '30');
  const b = await chromium.launch({ args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 540, height: 960 }, deviceScaleFactor: 2 });
  await p.goto('file://' + __dirname + '/reel.html');
  await p.evaluate(() => document.getAnimations().forEach(a => a.pause()));
  const i0 = parseInt(process.argv[5] || '0'), i1 = parseInt(process.argv[6] || String(Math.round(fps * END)));
  for (let i = i0; i < i1; i++) {
    await p.evaluate(t => { if (window.__setT) window.__setT(t / 1000); document.getAnimations().forEach(a => { a.currentTime = t; }); }, (i / fps) * 1000);
    await p.screenshot({ path: `${out}/f${String(i).padStart(4, '0')}.jpg`, type: 'jpeg', quality: 90 });
  }
  await b.close();
})();
