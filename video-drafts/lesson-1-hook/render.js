const { chromium } = require('playwright-core');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 1280, height: 720 } });
  await p.goto('file://' + __dirname + '/hook.html');
  const fps = 30, total = 16.9;
  await p.evaluate(() => document.getAnimations().forEach(a => a.pause()));
  for (let i = 0; i < Math.round(fps * total); i++) {
    await p.evaluate(t => document.getAnimations().forEach(a => { a.currentTime = t; }), (i / fps) * 1000);
    await p.screenshot({ path: `/tmp/fr/f${String(i).padStart(4, '0')}.jpg`, type: 'jpeg', quality: 92 });
  }
  await b.close();
})();
