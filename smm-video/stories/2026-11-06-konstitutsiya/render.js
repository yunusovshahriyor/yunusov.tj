// node render.js frames|stills
const { chromium } = require('playwright-core');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--no-sandbox'] });
  const mode = process.argv[2];
  if (mode === 'stills') {
    let p = await b.newPage({ viewport: { width: 540, height: 960 }, deviceScaleFactor: 2 });
    await p.goto('file://' + __dirname + '/card.html'); await p.waitForTimeout(300);
    await p.screenshot({ path: __dirname + '/story.jpg', type: 'jpeg', quality: 92 });
    p = await b.newPage({ viewport: { width: 540, height: 675 }, deviceScaleFactor: 2 });
    await p.goto('file://' + __dirname + '/card.html#post'); await p.waitForTimeout(300);
    await p.screenshot({ path: __dirname + '/post.jpg', type: 'jpeg', quality: 92 });
  } else {
    const out = process.argv[3]; const p = await b.newPage({ viewport: { width: 540, height: 960 }, deviceScaleFactor: 2 });
    await p.goto('file://' + __dirname + '/card.html'); await p.waitForTimeout(300);
    for (let i = 0; i < 16 * 30; i++) { await p.evaluate(t => window.frame(t), i / 30); await p.screenshot({ path: `${out}/f${String(i).padStart(4, '0')}.jpg`, type: 'jpeg', quality: 90 }); }
  }
  await b.close();
})();
