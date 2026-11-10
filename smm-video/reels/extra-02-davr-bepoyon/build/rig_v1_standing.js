// Одамак — скелет (FK/IK) бо тарҷумаи пайдарпайи калидҳо. Ҳар кадр аз вақт t ҳисоб мешавад.
(function () {
const GY = 700, Ls = { torso: 54, thigh: 46, shin: 44, ua: 34, fa: 33 };
const STAND = GY - Ls.thigh - Ls.shin + 2, KNEEL = GY - Ls.thigh;
const SK = '#F2C7A0', SK2 = '#DDA97C', HAIR = '#2A2233', HOOD = '#8A63E0', HOOD2 = '#6A47C4', JEANS = '#34416A', JEANS2 = '#27325A';
const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
const ss = x => { x = clamp(x, 0, 1); return x * x * (3 - 2 * x); };
const lerp = (a, b, u) => a + (b - a) * u;
const rad = d => d * Math.PI / 180;

// ---------- калидҳо ----------
const LX = 299;                       // ҷойи ноутбук рӯи замин
const base = () => ({ x: 235, y: KNEEL, torso: 24, tilt: 8, look: 3, hL: 0, kL: -90, hR: 0, kR: -90,
  aL: [LX - 14, GY - 8], aR: [LX + 10, GY - 8], bL: -1, bR: -1, lx: LX, ly: GY, lrot: 0, heat: 0 });
const head = p => { const s = shoulder(p); const a = rad(p.torso); return [s[0] + Math.sin(a) * 30, s[1] - Math.cos(a) * 30]; };
function shoulder(p) { const a = rad(p.torso); return [p.x + Math.sin(a) * Ls.torso, p.y - Math.cos(a) * Ls.torso]; }
const KEYS = [];
function K(t, o) { const prev = KEYS.length ? KEYS[KEYS.length - 1].raw : base(); const raw = Object.assign({}, prev, o); KEYS.push({ t, raw }); return raw; }
const hx = p => head(p), carry = (x, y) => ({ lx: x + 50, ly: y + 8, aL: [x + 26, y - 6], aR: [x + 72, y - 8], bL: 1, bR: 1 });
// 0.2–2.7 қадамзанӣ бо ноутбук
K(0.2, Object.assign({ x: -90, y: STAND, torso: 8, tilt: 0, look: 3, hL: 0, kL: -6, hR: 0, kR: -6 }, carry(-90, STAND)));
K(2.7, Object.assign({ x: 235, y: STAND, torso: 8 }, carry(235, STAND)));
// 3.5 зону мезанад ва ноутбукро мемонад
K(3.5, { x: 235, y: KNEEL, torso: 24, tilt: 8, look: 3, hL: 0, kL: -90, hR: 0, kR: -90, lx: LX, ly: GY, aL: [LX - 14, GY - 8], aR: [LX + 10, GY - 8], bL: -1, bR: -1 });
K(7.1, { torso: 22, tilt: 6 });
K(7.9, { torso: 12, tilt: -6, look: 5, aL: [LX - 14, GY - 36], aR: [LX + 10, GY - 36] });      // «Осон!» — лабханд
K(8.0, { aR: [LX + 10, GY - 32] });
K(8.11, { aR: [LX + 10, GY - 5] });                                                            // Enter
K(8.3, { aR: [LX + 10, GY - 30] });
K(8.9, { torso: 6, tilt: 5, look: 6, aL: [235 + 8, KNEEL + 26], aR: [235 + 14, KNEEL + 30], bL: -1, bR: -1 });   // тамошо
K(10.0, { torso: 2, tilt: 6, look: 7, heat: 0.55 });
K(10.9, { torso: -2, tilt: 8, look: 8, heat: 0.75, aR: p => [hx(p)[0] + 14, hx(p)[1] + 26], bR: 1 });             // даст ба гардан
K(11.35, { torso: -4, heat: 0.85 });
K(11.6, { x: 225, y: STAND - 62, torso: -12, tilt: 0, look: 0, hL: 22, kL: -36, hR: -16, kR: -22, heat: 0.9, aL: p => [p.x - 50, p.y - 150], aR: p => [p.x + 46, p.y - 150], bL: 1, bR: -1 });   // ҷаҳиш
K(12.0, { x: 212, y: STAND + 8, torso: -8, hL: 14, kL: -34, hR: -10, kR: -26 });                                // фуромадан
K(12.5, { x: 205, y: STAND, torso: -8, hL: 4, kL: -8, hR: -4, kR: -8, aL: p => [hx(p)[0] - 30, hx(p)[1] + 4], aR: p => [hx(p)[0] + 30, hx(p)[1] + 4], bL: 1, bR: -1, heat: 0.95 });   // сарро мегирад
K(14.4, { torso: -12, x: 202 });
K(15.2, { x: 238, y: STAND + 16, torso: 32, tilt: 10, hL: 24, kL: -40, hR: -10, kR: -52, look: 7, aL: [LX - 16, GY - 54], aR: [LX + 12, GY - 54], bL: -1, bR: -1, heat: 1 });   // ноутбукро медорад
K(15.9, { heat: 1 });
K(16.15, { x: 226, y: STAND + 2, torso: -18, tilt: 0, hL: 10, kL: -6, hR: 4, kR: -6, aL: p => [p.x - 44, p.y - 150], aR: p => [p.x + 40, p.y - 150], bL: 1, bR: -1, ly: GY, lx: LX });   // ноутбук парид
K(16.9, { x: 188, y: GY - 14, torso: -88, tilt: 6, look: 0, hL: 86, kL: 0, hR: 80, kR: 4, aL: p => [shoulder(p)[0] + 40, shoulder(p)[1] + 4], aR: p => [shoulder(p)[0] + 8, shoulder(p)[1] - 78], bL: -1, bR: 1 });   // афтод
K(19.0, {});
K(19.5, { y: GY - 16 });
K(20.3, { x: 205, y: GY - 28, torso: 6, tilt: 4, hL: 74, kL: -96, hR: 62, kR: -90, aL: p => [p.x + 40, p.y + 6], aR: p => [p.x + 30, p.y + 10], bL: -1, bR: -1, heat: 0 });   // менишинад
K(21.0, { x: 235, y: KNEEL, torso: 14, tilt: 4, look: 4, hL: 0, kL: -90, hR: 0, kR: -90, aL: [LX - 14, GY - 8], aR: p => [hx(p)[0] + 12, hx(p)[1] + 28], bL: -1, bR: 1 });   // фикр
K(23.2, {});
K(23.45, { torso: 20, aR: [LX + 10, GY - 8], bR: -1 });
K(24.4, { torso: 24, tilt: 8, look: 3 });
K(30.4, { torso: 22 });
K(30.55, { aR: [LX + 10, GY - 32] });
K(30.68, { aR: [LX + 10, GY - 5] });                                                           // Enter-и дуюм
K(30.9, { aR: [LX + 10, GY - 30], torso: 14, look: 6 });
K(31.5, { torso: 6, tilt: 4, aL: [235 + 8, KNEEL + 26], aR: [235 + 14, KNEEL + 30] });
K(33.0, { torso: 2 });
K(33.45, { x: 235, y: STAND + 10, torso: 6, hL: 14, kL: -38, hR: 10, kR: -30, aL: p => [p.x - 40, p.y - 40], aR: p => [p.x + 40, p.y - 40], bL: 1, bR: -1 });   // хез мекунад
K(33.9, { y: STAND - 8, torso: 0, hL: 0, kL: -4, hR: 0, kR: -4, aL: p => [p.x - 50, p.y - 150], aR: p => [p.x + 48, p.y - 150] });
K(34.3, { y: STAND - 66, hL: 38, kL: -66, hR: 28, kR: -58 });                                  // ҷаҳиш
K(34.75, { y: STAND + 8, hL: 16, kL: -34, hR: 12, kR: -30 });
K(35.2, { y: STAND, hL: 0, kL: -4, hR: 0, kR: -4 });
K(37.6, { y: STAND, torso: 2 });
K(38.1, { x: 235, y: STAND, torso: 4, tilt: 12, look: 4, hL: 0, kL: -4, hR: 0, kR: -4, aL: p => [p.x - 24, p.y - 10], aR: p => [hx(p)[0] + 6, hx(p)[1] - 20], bL: -1, bR: 1 });   // сарро харошидан
K(42.8, {});
K(43.4, { torso: 0, tilt: 0, look: 3, aL: p => [p.x - 22, p.y + 34], aR: p => [p.x + 62, p.y - 150], bL: -1, bR: 1 });   // салом
K(47.5, {});

function evalKeys(t) {
  let i = 0; while (i < KEYS.length - 1 && KEYS[i + 1].t <= t) i++;
  const A = KEYS[i], B = KEYS[Math.min(i + 1, KEYS.length - 1)];
  const u = A === B ? 0 : ss((t - A.t) / (B.t - A.t));
  const pa = Object.assign({}, A.raw), pb = Object.assign({}, B.raw);
  const fix = (p) => { const q = Object.assign({}, p); ['aL', 'aR'].forEach(k => { if (typeof q[k] === 'function') q[k] = q[k](q); }); return q; };
  const a = fix(pa), b = fix(pb), o = {};
  for (const k in a) o[k] = Array.isArray(a[k]) ? [lerp(a[k][0], b[k][0], u), lerp(a[k][1], b[k][1], u)] : (typeof a[k] === 'number' ? lerp(a[k], b[k], u) : (u < .5 ? a[k] : b[k]));
  return o;
}

// ---------- мӯда: сатҳи иловагӣ ----------
function mood(t) {
  if (t < 10) return 'type'; if (t < 11.6) return 'help'; if (t < 16.2) return 'shock'; if (t < 20.3) return 'help';
  if (t < 30.6) return 'type'; if (t < 38) return 'happy'; if (t < 43.2) return 'help'; return 'happy';
}
function procedural(p, t) {
  const o = Object.assign({}, p, { aL: p.aL.slice(), aR: p.aR.slice() });
  // қадамзанӣ
  const w = ss((t - 0.2) / 0.2) * (1 - ss((t - 2.55) / 0.3));
  if (w > 0) {
    const ph = o.x / 88 * 2 * Math.PI;
    o.hL = lerp(o.hL, 30 * Math.sin(ph), w); o.hR = lerp(o.hR, -30 * Math.sin(ph), w);
    o.kL = lerp(o.kL, -8 - 34 * Math.max(0, Math.cos(ph)), w); o.kR = lerp(o.kR, -8 - 34 * Math.max(0, -Math.cos(ph)), w);
    const bob = -4 * Math.abs(Math.sin(ph)) * w; o.y += bob; o.aL[1] += bob; o.aR[1] += bob; o.ly += bob;
  }
  // навиштан: зарбаи ангуштон
  [[3.8, 7.1, 1], [24.5, 30.4, 1.35]].forEach(([a, b, e]) => {
    const f = ss((t - a) / 0.2) * (1 - ss((t - (b - .15)) / 0.15));
    if (f > 0) {
      const k1 = Math.max(0, Math.sin(2 * Math.PI * 6.3 * t) + 0.6 * Math.sin(2 * Math.PI * 9.1 * t + 1)) * 5 * e;
      const k2 = Math.max(0, Math.sin(2 * Math.PI * 7.2 * t + 2) + 0.5 * Math.sin(2 * Math.PI * 4.7 * t)) * 5 * e;
      o.aL[1] -= k1 * f; o.aR[1] -= k2 * f; o.tilt += 1.6 * Math.sin(2 * Math.PI * 3.2 * t) * f; o.torso += 1.2 * Math.sin(2 * Math.PI * 1.6 * t) * f;
    }
  });
  // ларзиш
  const jit = (a, b, amp) => { const f = ss((t - a) / 0.2) * (1 - ss((t - b) / 0.2)); return amp * f; };
  const ja = jit(10.2, 11.5, 0.8) + jit(12.5, 16.2, 2.2) + jit(16.3, 19.2, 1.4);
  if (ja) { const n = Math.sin(t * 91) * ja, m = Math.cos(t * 83) * ja; o.x += n; o.y += m; o.aL[0] += n; o.aR[0] += n; o.aL[1] += m; o.aR[1] += m; }
  // ноутбук меларзад
  const lj = jit(13.2, 15.9, 3.5) + jit(10.2, 13.2, 1.2);
  o.lx += Math.sin(t * 77) * lj; o.ly += Math.cos(t * 69) * lj * 0.6; o.lrot += Math.sin(t * 63) * lj * 1.5;
  // ноутбук парвоз мекунад ва бармегардад
  if (t >= 15.9 && t < 18.7) { const u = (t - 15.9) / 2.8; o.ly = GY - 760 * Math.pow(u, 1.6) - 40 * u; o.lx = LX + 60 * u; o.lrot = 1080 * Math.pow(u, 1.3); }
  if (t >= 18.7 && t < 19.5) { const u = (t - 18.7) / 0.8, e = u * u; o.ly = lerp(-170, GY, Math.min(1, e)); o.lx = LX; o.lrot = lerp(-220, 0, ss(u)); o.heat = 0; }
  if (t >= 19.5 && t < 19.8) o.ly = GY - 8 * Math.sin((t - 19.5) / 0.3 * Math.PI);
  // даст меҷунбонад
  const wv = (a, b, key, amp) => { const f = ss((t - a) / 0.2) * (1 - ss((t - b) / 0.2)); if (f > 0) { o[key][0] += Math.sin(t * 13) * amp * f; o[key][1] += Math.cos(t * 7) * 6 * f; } };
  wv(17.0, 19.4, 'aR', 16); wv(43.6, 47.6, 'aR', 22);
  // харошидан
  const sc = ss((t - 38.6) / 0.2) * (1 - ss((t - 42.8) / 0.2)); if (sc > 0) { o.aR[0] += Math.sin(t * 15) * 5 * sc; o.aR[1] += Math.cos(t * 12) * 4 * sc; }
  // ҷаҳиши шодӣ
  const ch = ss((t - 35.4) / 0.3) * (1 - ss((t - 37.5) / 0.3)); if (ch > 0) { const b = -10 * Math.abs(Math.sin(t * 7)) * ch; o.y += b; o.aL[1] += b; o.aR[1] += b; }
  // нафаскашӣ
  o.torso += 0.8 * Math.sin(t * 2.4);
  return o;
}

// ---------- IK / FK ----------
function ik(P, T, a, b, bend) {
  let dx = T[0] - P[0], dy = T[1] - P[1], d = Math.hypot(dx, dy);
  const max = a + b - 0.5, min = Math.abs(a - b) + 1; const dc = clamp(d, min, max);
  const base = Math.atan2(dy, dx); const cosA = clamp((a * a + dc * dc - b * b) / (2 * a * dc), -1, 1), A = Math.acos(cosA);
  const ea = base + bend * A; const E = [P[0] + a * Math.cos(ea), P[1] + a * Math.sin(ea)];
  const H = d <= max ? T : [P[0] + dx / d * max, P[1] + dy / d * max];
  return [E, H];
}
const dir = (a) => [Math.sin(rad(a)), Math.cos(rad(a))];
function seg(pts, w, c) { return `<path d="M${pts.map(p => p[0].toFixed(1) + ',' + p[1].toFixed(1)).join(' L')}" fill="none" stroke="${c}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round"/>`; }
function leg(H, h, k, front, off) {
  const d1 = dir(h), K = [H[0] + d1[0] * Ls.thigh, H[1] + d1[1] * Ls.thigh], d2 = dir(h + k), F = [K[0] + d2[0] * Ls.shin, K[1] + d2[1] * Ls.shin];
  const ang = h + k;
  const shoe = `<g transform="translate(${F[0].toFixed(1)},${F[1].toFixed(1)}) rotate(${ang.toFixed(1)})"><ellipse cx="7" cy="3" rx="12.5" ry="6.2" fill="#F5F5F7" stroke="#C9C9D2" stroke-width="1.5"/><rect x="-5" y="7" width="24" height="2.6" rx="1" fill="#BD93F9"/></g>`;
  return seg([H, K, F], 15, front ? JEANS : JEANS2) + shoe;
}
function arm(S, T, bend, front) {
  const [E, Hd] = ik(S, T, Ls.ua, Ls.fa, bend);
  return seg([S, E, Hd], 13.5, front ? HOOD : HOOD2) + `<circle cx="${Hd[0].toFixed(1)}" cy="${Hd[1].toFixed(1)}" r="7" fill="${SK}"/>`;
}
function torsoPath(Hp, Sp) {
  const dx = Sp[0] - Hp[0], dy = Sp[1] - Hp[1], L = Math.hypot(dx, dy), nx = dy / L, ny = -dx / L;     // перпендикуляр
  const hw = 17, sw = 21;
  const hl = [Hp[0] - nx * hw, Hp[1] - ny * hw], hr = [Hp[0] + nx * hw, Hp[1] + ny * hw];
  const sl = [Sp[0] - nx * sw, Sp[1] - ny * sw], sr = [Sp[0] + nx * sw, Sp[1] + ny * sw];
  const f = p => p[0].toFixed(1) + ',' + p[1].toFixed(1);
  const mid = [(hl[0] + hr[0]) / 2 - dx / L * -8, (hl[1] + hr[1]) / 2 - dy / L * -8];
  return `<path d="M${f(sl)} L${f(sr)} L${f(hr)} Q${f([Hp[0] - dx / L * -9, Hp[1] - dy / L * -9])} ${f(hl)} Z" fill="url(#hood)"/>` +
         `<path d="M${(Sp[0] - nx * 11 - dx / L * 4).toFixed(1)},${(Sp[1] - ny * 11 - dy / L * 4).toFixed(1)} Q${(Sp[0] - dx / L * 14).toFixed(1)},${(Sp[1] - dy / L * 14).toFixed(1)} ${(Sp[0] + nx * 11 - dx / L * 4).toFixed(1)},${(Sp[1] + ny * 11 - dy / L * 4).toFixed(1)}" fill="none" stroke="${HOOD2}" stroke-width="5" stroke-linecap="round"/>`;
}
function faceSvg(m, look, t) {
  const blink = ((t * 1000) % 3300) < 110;
  const eye = (dx, wide, happy) => {
    const x = dx + look * 0.5;
    if (happy) return `<path d="M${x - 6},-1 Q${x},-9 ${x + 6},-1" fill="none" stroke="#2A2233" stroke-width="2.6" stroke-linecap="round"/>`;
    if (blink && !wide) return `<path d="M${x - 5},-3 L${x + 5},-3" stroke="#2A2233" stroke-width="2.6" stroke-linecap="round"/>`;
    const r = wide ? 6.5 : 5;
    return `<ellipse cx="${x}" cy="-3" rx="${r}" ry="${r + 1}" fill="#fff"/><circle cx="${x + look * 0.18 + (dx < 0 ? 0.6 : -0.6)}" cy="-3" r="${wide ? 2.4 : 3}" fill="#2A2233"/>`;
  };
  const nose = `<path d="M${look * 0.5},1 Q${3 + look * 0.5},7 ${look * 0.5},8" fill="none" stroke="${SK2}" stroke-width="2" stroke-linecap="round"/>`;
  if (m === 'type') return eye(-9) + eye(9) + nose + `<path d="M-14,-13 Q-9,-16 -4,-13 M4,-13 Q9,-16 14,-13" fill="none" stroke="${HAIR}" stroke-width="2.6" stroke-linecap="round"/><path d="M-8,13 Q0,19 8,13" fill="none" stroke="#7a3b3b" stroke-width="2.6" stroke-linecap="round"/>`;
  if (m === 'shock') return eye(-9, true) + eye(9, true) + nose + `<path d="M-16,-18 L-3,-13 M16,-18 L3,-13" stroke="${HAIR}" stroke-width="2.8" stroke-linecap="round"/><ellipse cx="0" cy="15" rx="6" ry="8" fill="#5a1f2b"/><ellipse cx="0" cy="18" rx="3.5" ry="3" fill="#E36F7B"/>`;
  if (m === 'happy') return eye(-9, false, true) + eye(9, false, true) + nose + `<path d="M-12,9 Q0,25 12,9 Z" fill="#5a1f2b"/><path d="M-9,10 Q0,14 9,10" fill="#fff"/><ellipse cx="-15" cy="8" rx="4" ry="2.6" fill="#F59BA4" opacity=".6"/><ellipse cx="15" cy="8" rx="4" ry="2.6" fill="#F59BA4" opacity=".6"/>`;
  return eye(-9) + eye(9) + nose + `<path d="M-15,-12 L-4,-15 M15,-12 L4,-15" stroke="${HAIR}" stroke-width="2.8" stroke-linecap="round"/><path d="M-8,16 Q0,10 8,16" fill="none" stroke="#7a3b3b" stroke-width="2.6" stroke-linecap="round"/>`;
}
function headSvg(Cx, Cy, rot, m, look, t) {
  const ears = [-1, 1].map(s => `<ellipse cx="${s * 25}" cy="3" rx="5.5" ry="8" fill="${SK2}"/><ellipse cx="${s * 25}" cy="3" rx="2.6" ry="4.5" fill="#C98F66"/>`).join('');
  const hair = `<path d="M-26,-2 Q-30,-38 0,-34 Q30,-38 26,-2 Q22,-18 6,-21 Q-10,-14 -26,-2 Z" fill="${HAIR}"/><path d="M-4,-32 Q14,-44 20,-30" fill="none" stroke="${HAIR}" stroke-width="7" stroke-linecap="round"/>`;
  return `<g transform="translate(${Cx.toFixed(1)},${Cy.toFixed(1)}) rotate(${rot.toFixed(1)}) scale(.88)"><rect x="-6" y="22" width="12" height="16" rx="5" fill="${SK2}"/>${ears}<ellipse cx="0" cy="0" rx="25" ry="28" fill="url(#skin)"/>${hair}${faceSvg(m, look, t)}</g>`;
}
function laptopSide(p) {
  const col = p.heat < .5 ? mixc('#BD93F9', '#FFB86C', p.heat / .5) : mixc('#FFB86C', '#F48771', (p.heat - .5) / .5);
  let keys = ''; for (let i = 0; i < 9; i++) keys += `<rect x="${-30 + i * 6.4}" y="-8" width="4.4" height="2.4" rx="1" fill="#5a5a66"/>`;
  return `<g transform="translate(${p.lx.toFixed(1)},${p.ly.toFixed(1)}) rotate(${p.lrot.toFixed(1)})">` +
    `<polygon points="30,-5 37,-5 50,-64 43,-64" fill="#33333b" stroke="#16161a" stroke-width="1.2"/>` +
    `<polygon points="30,-5 32,-5 45,-62 43,-62" fill="${col}" opacity=".95" filter="url(#glow)"/>` +
    `<rect x="-36" y="-6" width="72" height="7" rx="2.5" fill="#4a4a54" stroke="#2a2a30" stroke-width="1.2"/>${keys}</g>`;
}
function laptopSvg(p) {
  if (p.side) return laptopSide(p);
  const col = p.heat < .5 ? mixc('#BD93F9', '#FFB86C', p.heat / .5) : mixc('#FFB86C', '#F48771', (p.heat - .5) / .5);
  const cols = ['#569CD6', '#CE9178', '#B5CEA8', '#DCDCAA', '#9CDCFE'];
  let lines = ''; for (let i = 0; i < 5; i++) lines += `<rect x="${-26}" y="${-52 + i * 8}" width="${20 + ((i * 13) % 30)}" height="4" rx="2" fill="${cols[i]}"/>`;
  const fl = p.heat > 0.8 ? `<text x="0" y="-18" font-size="24" text-anchor="middle">🔥</text>` : '';
  return `<g transform="translate(${p.lx.toFixed(1)},${p.ly.toFixed(1)}) rotate(${p.lrot.toFixed(1)})"><path d="M-40,0 L40,0 L50,10 L-50,10 Z" fill="#3a3a40" stroke="#555" stroke-width="2"/><rect x="-33" y="-58" width="66" height="56" rx="5" fill="#1E1E1E" stroke="${col}" stroke-width="3.2" filter="url(#glow)"/>${lines}${fl}</g>`;
}
function mixc(a, b, u) { const pa = [1, 3, 5].map(i => parseInt(a.substr(i, 2), 16)), pb = [1, 3, 5].map(i => parseInt(b.substr(i, 2), 16)); return '#' + pa.map((v, i) => Math.round(lerp(v, pb[i], clamp(u, 0, 1))).toString(16).padStart(2, '0')).join(''); }

function render(t) {
  const p = procedural(evalKeys(t), t), m = mood(t);
  const Hp = [p.x, p.y], Sp = shoulder(p), hd = head(p), hRot = p.torso * 0.5 + p.tilt;
  const hipL = [Hp[0] - 4, Hp[1]], hipR = [Hp[0] + 4, Hp[1]];
  let s = '';
  s += leg(hipL, p.hL, p.kL, false) ;
  s += arm([Sp[0] - 6, Sp[1] + 4], p.aL, p.bL, false);
  s += leg(hipR, p.hR, p.kR, true);
  s += torsoPath(Hp, Sp);
  s += headSvg(hd[0], hd[1], hRot, m, p.look, t);
  s += laptopSvg(p);
  s += arm([Sp[0] + 6, Sp[1] + 4], p.aR, p.bR, true);
  const lap = '';
  // ноутбук пеш аз дастҳо дар ҳолати навиштан; дар бозуҳо баъд
  let extra = '';
  if (t >= 10.2 && t < 11.6) extra += `<path d="M${hd[0] + 26},${hd[1] - 20} q-5,9 0,12 q5,-3 0,-12z" fill="#4FC1FF"/>`;
  if (t >= 12 && t < 16) extra += `<path d="M${hd[0] - 40},${hd[1] - 10} q-5,9 0,12 q5,-3 0,-12z M${hd[0] + 42},${hd[1] - 2} q-5,9 0,12 q5,-3 0,-12z" fill="#4FC1FF"/>`;
  if (t >= 19.8 && t < 31) extra += `<text x="${hd[0] - 14}" y="${hd[1] - 46}" font-size="28">💡</text>`;
  if (t >= 33.4 && t < 37.6) extra += `<text x="${hd[0] - 78}" y="${hd[1] - 20}" font-size="24">✨</text><text x="${hd[0] + 52}" y="${hd[1] - 4}" font-size="24">✨</text>`;
  if (t >= 38.3 && t < 42.9) extra += `<text x="${hd[0] + 22}" y="${hd[1] - 36}" font-size="30" font-weight="900" fill="#FF79C6">?</text><text x="${hd[0] - 34}" y="${hd[1] - 26}" font-size="22" font-weight="900" fill="#BD93F9">?</text>`;
  document.getElementById('rig').innerHTML = s.replace('', '') + lap + extra;
}

function chairSvg(cx, top) {
  const c = '#3a3a44', c2 = '#2a2a33', ac = '#BD93F9';
  return `<g><rect x="${cx - 34}" y="${top - 70}" width="12" height="74" rx="5" fill="${c2}"/><rect x="${cx - 34}" y="${top - 74}" width="12" height="8" rx="4" fill="${ac}"/>` +
         `<rect x="${cx - 34}" y="${top}" width="74" height="12" rx="6" fill="${c}"/><rect x="${cx - 34}" y="${top + 10}" width="74" height="3" fill="${ac}" opacity=".6"/>` +
         `<rect x="${cx - 28}" y="${top + 12}" width="8" height="${GY - top - 12}" rx="3" fill="${c2}"/><rect x="${cx + 28}" y="${top + 12}" width="8" height="${GY - top - 12}" rx="3" fill="${c2}"/></g>`;
}
function drawPose(p, m, t, chair) {
  const Hp = [p.x, p.y], Sp = shoulder(p), hd = head(p), hRot = p.torso * 0.5 + p.tilt;
  let s = chair ? chairSvg(chair.cx, chair.top) : '';
  s += leg([Hp[0] - 4, Hp[1]], p.hL, p.kL, false);
  s += arm([Sp[0] - 6, Sp[1] + 4], p.aL, p.bL, false);
  s += leg([Hp[0] + 4, Hp[1]], p.hR, p.kR, true);
  s += torsoPath(Hp, Sp);
  s += headSvg(hd[0], hd[1], hRot, m, p.look, t);
  s += laptopSvg(p);
  s += arm([Sp[0] + 6, Sp[1] + 4], p.aR, p.bR, true);
  return s;
}
window.__drawPose = drawPose; window.__STAND = STAND; window.__GY = GY;
window.__setT = render;
render(0);
})();
