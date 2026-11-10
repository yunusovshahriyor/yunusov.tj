const { chromium } = require('playwright');
(async () => {
  const times = process.argv.slice(3).map(Number), out = process.argv[2];
  const b = await chromium.launch({ args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 540, height: 960 }, deviceScaleFactor: 1 });
  await p.goto('file://' + __dirname + '/reel.html');
  await p.evaluate(() => document.getAnimations().forEach(a => a.pause()));
  for (let i = 0; i < times.length; i++) {
    await p.evaluate(t => document.getAnimations().forEach(a => { a.currentTime = t; }), times[i] * 1000);
    await p.screenshot({ path: `${out}/p${String(i).padStart(2, '0')}.png` });
  }
  await b.close();
})();
