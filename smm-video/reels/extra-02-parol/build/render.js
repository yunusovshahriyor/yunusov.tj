// node render.js <from> <to> <outdir> [fps|list:t1,t2]  — кадрҳо 1080×1920
const { chromium } = require('playwright-core');
(async () => {
  const [from, to, out, mode] = [parseFloat(process.argv[2]), parseFloat(process.argv[3]), process.argv[4], process.argv[5] || '30'];
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 540, height: 960 }, deviceScaleFactor: 2 });
  p.on('pageerror', e => console.error('PAGEERR', e.message));
  await p.goto('file://' + __dirname + '/reel.html'); await p.waitForTimeout(300);
  const list = mode.startsWith('list:') ? mode.slice(5).split(',').map(Number) : null, fps = list ? 0 : +mode;
  const times = list || Array.from({ length: Math.round((to - from) * fps) }, (_, i) => from + i / fps);
  let k = list ? 0 : Math.round(from * fps);
  for (const t of times) { await p.evaluate(t => window.frame(t), t); await p.screenshot({ path: `${out}/${list ? 't' + t.toFixed(1) : 'f' + String(k).padStart(5, '0')}.jpg`, type: 'jpeg', quality: 88 }); k++; }
  await b.close();
})();
