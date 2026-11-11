// node render.js <from_s> <to_s> <outdir> [fps|list:t1,t2,...]  — кадры 1920×1080 (реҷаи web: се файл + пешнамоиш)
const { chromium } = require('playwright-core');
(async () => {
  const [from, to, out, mode] = [parseFloat(process.argv[2]), parseFloat(process.argv[3]), process.argv[4], process.argv[5] || '30'];
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1243/chrome-linux64/chrome', args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 1.5 });
  p.on('pageerror', e => console.error('PAGEERR', e.message));
  p.on('dialog', d => d.dismiss());
  await p.goto('file://' + __dirname + '/video.html#web');
  await p.waitForTimeout(500);
  const TL = await p.evaluate(() => window.TL), pvOps = TL.pv || [];
  const list = mode.startsWith('list:') ? mode.slice(5).split(',').map(Number) : null;
  const fps = list ? 0 : parseFloat(mode);
  const times = list || Array.from({ length: Math.round((to - from) * fps) }, (_, i) => from + i / fps);
  let k = list ? 0 : Math.round(from * fps); const applied = new Set();
  const SC = 1.2;   // масштаби iframe (transform: scale) — бояд бо video.css мувофиқ бошад
  const doPv = async (op) => {
    const fr = p.frames().find(f => f !== p.mainFrame()); if (!fr) return;
    const loc = fr.locator(op.sel).first();
    try {
      if (op.kind === 'unhover') { await p.mouse.move(5, 700); await p.evaluate(() => { window.__pvPtr = null; }); await p.waitForTimeout(60); return; }
      if (op.kind === 'fill') { await loc.fill(op.value, { timeout: 2000 }); await p.waitForTimeout(90); return; }
      // координаты на странице: прямоугольник iframe + (прямоугольник элемента × масштаб)
      let er = await loc.evaluate(e => { const q = e.getBoundingClientRect(); return [q.x, q.y, q.width, q.height, innerHeight]; }, { timeout: 2000 });
      if (er[1] + er[3] > er[4] || er[1] < 0) { await loc.evaluate(e => e.scrollIntoView({ block: 'center' })); er = await loc.evaluate(e => { const q = e.getBoundingClientRect(); return [q.x, q.y, q.width, q.height, innerHeight]; }); }
      const ir = await p.evaluate(() => { const f = document.getElementById('pvf'), q = f.getBoundingClientRect(); return [q.x, q.y, q.width / f.offsetWidth]; });
      const SCe = ir[2] || SC;   // реальный масштаб (с учётом камеры)
      const cx = ir[0] + (er[0] + er[2] / 2) * SCe, cy = ir[1] + (er[1] + er[3] / 2) * SCe;
      await p.mouse.move(cx, cy);
      if (op.kind === 'click') { await p.mouse.click(cx, cy); await p.evaluate(([x, y, t]) => { window.__pvPtr = { x, y, t }; }, [cx, cy, op.t]); }
      if (op.kind === 'hover') await p.evaluate(([x, y, t]) => { window.__pvPtr = { x, y, t, hover: true }; }, [cx, cy, op.t]);
    } catch (e) { console.error('PV', op.kind, op.sel, String(e.message).split('\n')[0]); }
    await p.waitForTimeout(90);
  };
  for (const t of times) {
    const r = await p.evaluate(t => window.frame(t), t);
    if (r.reloaded) applied.clear();
    for (let i = 0; i < pvOps.length; i++) { const op = pvOps[i]; if (!applied.has(i) && op.t <= t && op.t >= r.tc - 1e-6) { applied.add(i); await doPv(op); } }
    const name = list ? `t${t.toFixed(1)}` : `f${String(k).padStart(5, '0')}`;
    await p.screenshot({ path: `${out}/${name}.jpg`, type: 'jpeg', quality: 88 });
    k++;
  }
  await b.close();
})();
