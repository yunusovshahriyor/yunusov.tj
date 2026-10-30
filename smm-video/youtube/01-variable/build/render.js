// node render.js <from_s> <to_s> <outdir> [fps|list:t1,t2,...]  — кадры 1920×1080
const { chromium } = require('playwright-core');
(async () => {
  const [from, to, out, mode] = [parseFloat(process.argv[2]), parseFloat(process.argv[3]), process.argv[4], process.argv[5] || '30'];
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 1.5 });
  p.on('pageerror', e => console.error('PAGEERR', e.message));
  p.on('dialog', d => d.dismiss());
  await p.goto('file://' + __dirname + '/video.html#free');
  await p.waitForTimeout(400);
  const list = mode.startsWith('list:') ? mode.slice(5).split(',').map(Number) : null;
  const fps = list ? 0 : parseFloat(mode);
  const times = list || Array.from({ length: Math.round((to - from) * fps) }, (_, i) => from + i / fps);
  let k = list ? 0 : Math.round(from * fps);
  for (const t of times) {
    await p.evaluate(t => window.frame(t), t);
    const name = list ? `t${t.toFixed(1)}` : `f${String(k).padStart(5, '0')}`;
    await p.screenshot({ path: `${out}/${name}.jpg`, type: 'jpeg', quality: 88 });
    k++;
  }
  await b.close();
})();
