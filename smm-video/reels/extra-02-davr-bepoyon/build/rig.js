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
const CHX = 170, SEAT = GY - 46, SX = CHX + 4, HIPY = SEAT - 14;        // курсӣ ва ҷойи нишастан
const LAPX = SX + 36, LAPY = HIPY - 8;                                     // ноутбук рӯи зону
const FLX = SX + 92;                                                       // ноутбук рӯи замин
const base = () => ({ x: SX, y: HIPY, torso: 10, tilt: 8, look: 9, hL: 90, kL: -90, hR: 88, kR: -90, aL: [LAPX - 24, LAPY - 11], aR: [LAPX - 4, LAPY - 11],
  bL: 1, bR: 1, lx: LAPX, ly: LAPY, lrot: 0, heat: 0, side: 1, curl: 16 });
const head = p => { const s = shoulder(p); const a = rad(p.torso); return [s[0] + Math.sin(a) * 30, s[1] - Math.cos(a) * 30]; };
function shoulderJoint(p, side) { const S = shoulder(p), a = rad(p.torso); return [S[0] - Math.sin(a) * 11 + Math.cos(a) * 3 * side, S[1] + Math.cos(a) * 11 + Math.sin(a) * 3 * side]; }
function shoulder(p) { const a = rad(p.torso); return [p.x + Math.sin(a) * Ls.torso, p.y - Math.cos(a) * Ls.torso]; }
const KEYS = [];
function K(t, o) { const prev = KEYS.length ? KEYS[KEYS.length - 1].raw : base(); const raw = Object.assign({}, prev, o); KEYS.push({ t, raw }); return raw; }
const hx = p => head(p);
const carry = (x, y) => ({ lx: x + 64, ly: y - 26, aL: [x + 34, y - 22], aR: [x + 58, y - 36], bL: 1, bR: 1 });
const onLap = { lx: LAPX, ly: LAPY, lrot: 0, aL: [LAPX - 24, LAPY - 11], aR: [LAPX - 4, LAPY - 11], bL: 1, bR: 1 };
const seated = { x: SX, y: HIPY, hL: 90, kL: -90, hR: 88, kR: -90 };
// 0.2–2.6 қадамзанӣ бо ноутбук дар даст
K(0.2, Object.assign({ x: -90, y: STAND, torso: 4, tilt: 5, look: 9, hL: 6, kL: -6, hR: -6, kR: -8 }, carry(-90, STAND)));
K(2.55, Object.assign({ x: 140, y: STAND, torso: 4 }, carry(140, STAND)));
K(3.0, Object.assign({ x: 156, y: STAND + 22, torso: 14, tilt: 6, hL: 52, kL: -64, hR: 48, kR: -58 }, carry(156, STAND + 22)));        // менишинад
K(3.55, Object.assign({}, seated, onLap, { torso: 10, tilt: 8 }));
K(7.1, { torso: 9 });
K(7.9, { torso: 3, tilt: -4, aL: [LAPX - 24, LAPY - 44], aR: [LAPX - 4, LAPY - 44], curl: 28 });                // «Осон!»
K(8.0, { aR: [LAPX - 4, LAPY - 40] });
K(8.11, { aR: [LAPX - 4, LAPY - 10], curl: 40 });                                                          // Enter
K(8.3, { aR: [LAPX - 4, LAPY - 34], curl: 20 });
K(8.9, { torso: 2, tilt: 5, aL: [LAPX - 28, LAPY - 16], aR: [LAPX + 4, LAPY - 18], curl: 14 });             // тамошо
K(10.0, { torso: -1, tilt: 6, heat: 0.55 });
K(10.9, { torso: -4, tilt: 8, heat: 0.75, aR: p => [hx(p)[0] + 14, hx(p)[1] + 26], bR: 1 });                // даст ба гардан
K(11.3, { torso: -6, heat: 0.85, aR: [LAPX - 4, LAPY - 20] });
K(11.65, Object.assign({}, { x: SX + 26, y: STAND - 52, torso: -14, tilt: 0, look: 0, hL: 26, kL: -40, hR: -16, kR: -30, heat: 0.9,
  lx: SX + 70, ly: GY - 150, lrot: -4, aL: p => [p.x - 50, p.y - 150], aR: p => [p.x + 46, p.y - 150], bL: 1, bR: -1 }));       // ҷаҳиш аз курсӣ
K(11.95, { x: SX + 52, y: STAND + 8, torso: -8, hL: 14, kL: -34, hR: -10, kR: -26, lx: FLX, ly: GY, lrot: -3 });
K(12.5, { x: SX + 62, y: STAND, torso: -8, hL: 4, kL: -8, hR: -4, kR: -8, aL: p => [hx(p)[0] - 30, hx(p)[1] + 4], aR: p => [hx(p)[0] + 30, hx(p)[1] + 4], bL: 1, bR: -1, heat: 0.95 });
K(14.4, { torso: -12, x: SX + 60 });
K(15.2, { x: SX + 78, y: STAND + 18, torso: 32, tilt: 10, hL: 24, kL: -40, hR: -10, kR: -52, look: 9, aL: [FLX + 10, GY - 56], aR: [FLX + 34, GY - 48], bL: 1, bR: 1, heat: 1 });
K(15.9, { heat: 1 });
K(16.15, { x: SX + 70, y: STAND + 2, torso: -18, tilt: 0, hL: 10, kL: -6, hR: 4, kR: -6, aL: p => [p.x - 44, p.y - 150], aR: p => [p.x + 40, p.y - 150], bL: 1, bR: -1 });
K(16.9, { x: SX + 20, y: GY - 14, torso: -88, tilt: 6, look: 0, hL: 86, kL: 0, hR: 80, kR: 4, aL: p => [shoulder(p)[0] + 40, shoulder(p)[1] + 4], aR: p => [shoulder(p)[0] + 8, shoulder(p)[1] - 78], bL: 1, bR: 1 });
K(19.0, {});
K(19.5, { y: GY - 16 });
K(20.2, { x: SX + 30, y: GY - 26, torso: -30, tilt: 4, look: 6, hL: 80, kL: -70, hR: 70, kR: -60, aL: p => [p.x + 30, p.y + 10], aR: p => [p.x + 40, p.y + 6], bL: 1, bR: 1, heat: 0 });       // менишинад
K(20.9, { x: SX + 52, y: STAND, torso: 6, tilt: 4, hL: 4, kL: -6, hR: -4, kR: -8, aL: p => [p.x - 14, p.y - 6], aR: p => [hx(p)[0] + 6, hx(p)[1] - 12], bL: 1, bR: 1 });            // хез мекунад, сар мехорад
K(21.4, { x: SX + 74, y: STAND + 20, torso: 30, tilt: 8, hL: 20, kL: -34, hR: -10, kR: -48, aL: [FLX + 6, GY - 28], aR: [FLX + 28, GY - 30] });                            // ноутбукро мегирад
K(21.9, Object.assign({ x: SX + 40, y: STAND, torso: 6, tilt: 6, hL: 4, kL: -6, hR: -6, kR: -8, lrot: 0 }, carry(SX + 40, STAND)));
K(22.5, Object.assign({}, seated, onLap, { torso: 12, tilt: 6, curl: 16 }));
K(23.1, { torso: 10, aR: p => [hx(p)[0] + 12, hx(p)[1] + 28], bR: 1 });                                 // фикр: даст ба манаҳ
K(23.4, { aR: p => [hx(p)[0] + 12, hx(p)[1] + 28] });
K(23.7, { aR: [LAPX - 4, LAPY - 11] });
K(24.4, { torso: 10, tilt: 8 });
K(30.4, { torso: 9 });
K(30.55, { aR: [LAPX - 4, LAPY - 38], curl: 28 });
K(30.68, { aR: [LAPX - 4, LAPY - 10], curl: 40 });
K(30.9, { aR: [LAPX - 4, LAPY - 34], torso: 3, look: 9 });
K(31.5, { torso: 0, tilt: 4, aL: [LAPX - 28, LAPY - 16], aR: [LAPX + 4, LAPY - 18], curl: 14 });
K(33.0, { torso: -2 });
K(33.45, { x: SX + 20, y: STAND + 14, torso: 8, hL: 34, kL: -50, hR: 28, kR: -44, lx: CHX + 6, ly: SEAT - 8, aL: p => [p.x - 40, p.y - 40], aR: p => [p.x + 40, p.y - 40], bL: 1, bR: -1 });   // хез мекунад
K(33.9, { x: SX + 46, y: STAND - 8, torso: 0, hL: 0, kL: -4, hR: 0, kR: -4, lx: CHX + 6, ly: SEAT - 8, aL: p => [p.x - 50, p.y - 150], aR: p => [p.x + 48, p.y - 150] });
K(34.3, { y: STAND - 66, hL: 38, kL: -66, hR: 28, kR: -58 });
K(34.75, { y: STAND + 8, hL: 16, kL: -34, hR: 12, kR: -30 });
K(35.2, { y: STAND, hL: 0, kL: -4, hR: 0, kR: -4 });
K(37.6, { y: STAND, torso: 2 });
K(38.1, { x: SX + 60, y: STAND, torso: 4, tilt: 12, look: 6, hL: 0, kL: -4, hR: 0, kR: -4, aL: p => [p.x - 24, p.y - 10], aR: p => [hx(p)[0] + 6, hx(p)[1] - 20], bL: 1, bR: 1 });
K(42.8, {});
K(43.4, { torso: 0, tilt: 0, look: 5, aL: p => [p.x - 22, p.y + 34], aR: p => [p.x + 62, p.y - 150], bL: 1, bR: 1, curl: 4 });
K(47.5, {});

function herm(p0, p1, m0, m1, u) { const u2 = u * u, u3 = u2 * u; return (2 * u3 - 3 * u2 + 1) * p0 + (u3 - 2 * u2 + u) * m0 + (-2 * u3 + 3 * u2) * p1 + (u3 - u2) * m1; }
const fixP = (p) => { const q = Object.assign({}, p); ['aL', 'aR'].forEach(k => { if (typeof q[k] === 'function') q[k] = q[k](q); }); return q; };
let KF = null;
function evalKeys(t) {
  if (!KF) KF = KEYS.map(k => ({ t: k.t, v: fixP(k.raw) }));
  let i = 0; while (i < KF.length - 1 && KF[i + 1].t <= t) i++;
  const A = KF[i], B = KF[Math.min(i + 1, KF.length - 1)], P = KF[i - 1], N = KF[i + 2];
  const dt = B.t - A.t, u = dt > 0 ? clamp((t - A.t) / dt, 0, 1) : 0;
  const one = (v0, v1, vm, vp) => {
    if (v0 === v1) return v0;
    const m0 = P ? (v1 - vm) / (B.t - P.t) * dt : (v1 - v0);
    const m1 = N ? (vp - v0) / (N.t - A.t) * dt : (v1 - v0);
    return herm(v0, v1, m0 * 0.9, m1 * 0.9, u);
  };
  const o = {};
  for (const k in A.v) {
    const a = A.v[k], b = B.v[k];
    if (Array.isArray(a)) o[k] = [0, 1].map(c => one(a[c], b[c], P ? P.v[k][c] : a[c], N ? N.v[k][c] : b[c]));
    else if (typeof a === 'number') o[k] = one(a, b, P ? P.v[k] : a, N ? N.v[k] : b);
    else o[k] = u < .5 ? a : b;
  }
  o.ly = Math.min(o.ly, GY); o.y = Math.min(o.y, GY - 8);
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
  const w = ss((t - 0.2) / 0.2) * (1 - ss((t - 2.45) / 0.25));
  if (w > 0) {
    const ph = o.x / 88 * 2 * Math.PI;
    o.hL = lerp(o.hL, 30 * Math.sin(ph), w); o.hR = lerp(o.hR, -30 * Math.sin(ph), w);
    o.kL = lerp(o.kL, -8 - 34 * Math.max(0, Math.cos(ph)), w); o.kR = lerp(o.kR, -8 - 34 * Math.max(0, -Math.cos(ph)), w);
    const bob = -4 * Math.abs(Math.sin(ph)) * w; o.y += bob; o.aL[1] += bob; o.aR[1] += bob; o.ly += bob;
  }
  // навиштан: пайдарпайии зарбаҳо (burst) + ҳаракати ангуштон
  o.tL = 0; o.tR = 0;
  [[3.8, 7.1, 1], [24.5, 30.4, 1.25]].forEach(([a, b, e]) => {
    const f = ss((t - a) / 0.25) * (1 - ss((t - (b - .2)) / 0.2));
    if (f > 0) {
      const burst = clamp((Math.sin(2 * Math.PI * 0.62 * t) + 0.55) * 1.6, 0, 1);               // тез-тез навишта, таваққуфҳо
      const burst2 = clamp((Math.sin(2 * Math.PI * 0.62 * t + 0.9) + 0.5) * 1.6, 0, 1);
      o.tL = f * burst * e; o.tR = f * burst2 * e;
      const k1 = Math.max(0, Math.sin(2 * Math.PI * 7.4 * t) + 0.5 * Math.sin(2 * Math.PI * 11 * t + 1)) * 1.8 * o.tL;
      const k2 = Math.max(0, Math.sin(2 * Math.PI * 8.1 * t + 2) + 0.5 * Math.sin(2 * Math.PI * 5.3 * t)) * 1.8 * o.tR;
      o.aL[1] -= k1; o.aR[1] -= k2;
      o.tilt += (1.2 * Math.sin(2 * Math.PI * 1.7 * t) + 2.2 * (burst - 0.5)) * f; o.torso += 0.8 * Math.sin(2 * Math.PI * 1.1 * t) * f;
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
  if (t >= 15.9 && t < 18.7) { const u = (t - 15.9) / 2.8; o.ly = GY - 760 * Math.pow(u, 1.6) - 40 * u; o.lx = FLX + 60 * u; o.lrot = 1080 * Math.pow(u, 1.3); }
  if (t >= 18.7 && t < 19.5) { const u = (t - 18.7) / 0.8, e = u * u; o.ly = lerp(-170, GY, Math.min(1, e)); o.lx = FLX; o.lrot = lerp(-220, 0, ss(u)); o.heat = 0; }
  if (t >= 19.5 && t < 19.8) o.ly = GY - 8 * Math.sin((t - 19.5) / 0.3 * Math.PI);
  if (t >= 19.8 && t < 21.3) { o.lx = FLX; o.ly = GY; o.lrot = 0; o.heat = 0; }
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
function handSvg(Hd, ang, curl, typ, t, ph) {
  // кафи даст + чор ангуш (ду банд) + нарм шудани ангуштон ҳангоми навиштан
  const d = [Math.cos(ang), Math.sin(ang)], pp = [-d[1], d[0]], deg = 180 / Math.PI;
  let g = `<ellipse cx="${Hd[0].toFixed(1)}" cy="${Hd[1].toFixed(1)}" rx="7.6" ry="6.6" transform="rotate(${(ang * deg).toFixed(1)} ${Hd[0].toFixed(1)} ${Hd[1].toFixed(1)})" fill="${SK}"/>`;
  for (let i = 0; i < 4; i++) {
    const off = (i - 1.5) * 3.5, len1 = 5.6 - Math.abs(i - 1.5) * 0.6, len2 = 4.6 - Math.abs(i - 1.5) * 0.5;
    const tap = typ * Math.max(0, Math.sin(2 * Math.PI * (6.5 + i * 1.1) * t + ph + i * 1.7)) * 34;
    const f1 = rad(curl * 0.55 + tap * 0.7), f2 = rad(curl * 0.7 + tap);
    const P0 = [Hd[0] + d[0] * 5.4 + pp[0] * off, Hd[1] + d[1] * 5.4 + pp[1] * off];
    const a1 = ang + f1, P1 = [P0[0] + Math.cos(a1) * len1, P0[1] + Math.sin(a1) * len1];
    const a2 = a1 + f2, P2 = [P1[0] + Math.cos(a2) * len2, P1[1] + Math.sin(a2) * len2];
    g += seg([P0, P1, P2], 3.3, SK);
  }
  // ангуштони бузург
  const T0 = [Hd[0] + d[0] * 1 - pp[0] * 5, Hd[1] + d[1] * 1 - pp[1] * 5], a3 = ang - rad(40 - curl * 0.4);
  g += seg([T0, [T0[0] + Math.cos(a3) * 6, T0[1] + Math.sin(a3) * 6]], 3.6, SK);
  return g;
}
function arm(S, T, bend, front, o, t, side) {
  const [E, Hd] = ik(S, T, Ls.ua, Ls.fa, bend);
  const fx = Hd[0] - E[0], fy = Hd[1] - E[1];
  let ang = Math.atan2(fy, fx);
  const typ = side === 'L' ? (o.tL || 0) : (o.tR || 0);
  ang += rad(10 + 12 * typ);                                                              // кафи даст каме поён
  const L = Math.hypot(fx, fy) || 1, cuffStart = [Hd[0] - fx / L * 9, Hd[1] - fy / L * 9];
  const col = front ? HOOD : HOOD2, cuffc = front ? '#5B3BB0' : '#4B2F96';
  // оринҷ ва китф — кулоҳи ҷома, то даст ба бадан часпида бошад
  const sleeve = seg([S, E, Hd], 13.5, col) + `<circle cx="${S[0].toFixed(1)}" cy="${S[1].toFixed(1)}" r="9.5" fill="${col}"/><circle cx="${E[0].toFixed(1)}" cy="${E[1].toFixed(1)}" r="6.9" fill="${col}"/>`;
  const cuff = seg([cuffStart, [Hd[0] - fx / L * 3, Hd[1] - fy / L * 3]], 14.5, cuffc);
  return sleeve + cuff + handSvg([Hd[0] + fx / L * 3, Hd[1] + fy / L * 3], ang, o.curl, typ, t, side === 'L' ? 0 : 2.1);
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
const MOODS = { type: { eo: 1, ha: 0, sm: .35, op: 0, br: 0, wo: 0, ch: 0 }, help: { eo: .95, ha: 0, sm: -.5, op: 0, br: .1, wo: 1, ch: 0 },
  shock: { eo: 1.4, ha: 0, sm: 0, op: 1, br: 1, wo: .3, ch: 0 }, happy: { eo: 0, ha: 1, sm: 1, op: .85, br: .3, wo: 0, ch: 1 } };
const MOOD_T = [[0, 'type'], [10, 'help'], [11.6, 'shock'], [16.2, 'help'], [20.3, 'type'], [30.6, 'happy'], [38, 'help'], [43.2, 'happy']];
function moodP(t) {
  let i = 0; while (i < MOOD_T.length - 1 && MOOD_T[i + 1][0] <= t) i++;
  const cur = MOODS[MOOD_T[i][1]], prev = MOODS[MOOD_T[Math.max(0, i - 1)][1]], w = i === 0 ? 1 : ss((t - MOOD_T[i][0]) / 0.22), o = {};
  for (const k in cur) o[k] = lerp(prev[k], cur[k], w);
  return o;
}
function faceSvg(M, look, t, gz) {
  const bt = (t * 1000) % 3300, blink = bt < 130 ? Math.sin(bt / 130 * Math.PI) : 0, open = M.eo * (1 - 0.92 * blink);
  const eye = (dx) => {
    const ex = dx + look * 0.3, ry = Math.max(0.5, 6.2 * open), rx = 5.1;
    let g = '';
    if (M.ha < 0.98) g += `<g opacity="${(1 - M.ha).toFixed(2)}"><ellipse cx="${ex}" cy="-3" rx="${rx}" ry="${ry.toFixed(2)}" fill="#fff"/><ellipse cx="${(ex + gz[0]).toFixed(1)}" cy="${(-3 + gz[1]).toFixed(1)}" rx="3" ry="${Math.min(3.1, ry * 0.9).toFixed(2)}" fill="#2A2233"/><circle cx="${(ex + gz[0] + 1).toFixed(1)}" cy="${(-4 + gz[1]).toFixed(1)}" r="0.9" fill="#fff" opacity="${Math.min(1, open)}"/><path d="M${ex - rx - .5},${-3 - ry * .2} Q${ex},${-3 - ry - 1.4} ${ex + rx + .5},${-3 - ry * .2}" fill="none" stroke="${SK2}" stroke-width="1.6" stroke-linecap="round"/></g>`;
    if (M.ha > 0.02) g += `<path opacity="${M.ha.toFixed(2)}" d="M${ex - 6},-1 Q${ex},-9 ${ex + 6},-1" fill="none" stroke="#2A2233" stroke-width="2.6" stroke-linecap="round"/>`;
    return g;
  };
  const nose = `<path d="M${look * 0.4},1 Q${3 + look * 0.4},7 ${look * 0.4},8" fill="none" stroke="${SK2}" stroke-width="2" stroke-linecap="round"/>`;
  const yo = -12 - M.br * 5, yi = yo - M.wo * 3.2 + (M.wo > 0.5 ? 0 : 0);
  const brow = s => `<path d="M${s * 15},${yo + M.wo * 1.5 + M.br * 0} Q${s * 9.5},${(yo + yi) / 2 - 2.6} ${s * 4},${yi - (M.wo * 2.4)}" fill="none" stroke="${HAIR}" stroke-width="2.7" stroke-linecap="round"/>`;
  const w = 8 + M.op * 3, y0 = 13 - M.op * 1;
  let mouth;
  if (M.op < 0.12) mouth = `<path d="M${-w},${y0} Q0,${y0 + M.sm * 7} ${w},${y0}" fill="none" stroke="#7a3b3b" stroke-width="2.6" stroke-linecap="round"/>`;
  else mouth = `<path d="M${-w},${y0} Q0,${y0 + M.sm * 4} ${w},${y0} Q0,${y0 + M.op * 17 + 4} ${-w},${y0} Z" fill="#5a1f2b"/>` + (M.sm > 0.6 ? `<path d="M${-w + 2},${y0 + .6} Q0,${y0 + M.sm * 3 + .6} ${w - 2},${y0 + .6} L${w - 3},${y0 + 3.4} Q0,${y0 + M.sm * 3 + 3.4} ${-w + 3},${y0 + 3.4} Z" fill="#fff"/>` : `<ellipse cx="0" cy="${y0 + M.op * 11 + 2}" rx="3.5" ry="${2 + M.op}" fill="#E36F7B"/>`);
  const cheeks = `<ellipse cx="-15" cy="8" rx="4" ry="2.6" fill="#F59BA4" opacity="${(M.ch * .6).toFixed(2)}"/><ellipse cx="15" cy="8" rx="4" ry="2.6" fill="#F59BA4" opacity="${(M.ch * .6).toFixed(2)}"/>`;
  return eye(-9) + eye(9) + nose + brow(-1) + brow(1) + mouth + cheeks;
}
function headSvg(Cx, Cy, rot, m, look, t, lag, gz) {
  const M = typeof m === 'string' ? MOODS[m] : m;
  const ears = [-1, 1].map(s => `<ellipse cx="${s * 25}" cy="3" rx="5.5" ry="8" fill="${SK2}"/><ellipse cx="${s * 25}" cy="3" rx="2.6" ry="4.5" fill="#C98F66"/>`).join('');
  const L = lag || 0;
  const hair = `<path d="M-26,-2 Q-30,-38 0,-34 Q30,-38 26,-2 Q22,-18 6,-21 Q-10,-14 -26,-2 Z" fill="${HAIR}"/><path d="M-4,-32 Q${14 + L * .8},${-44 + Math.abs(L) * .3} ${20 + L * 1.4},${-30 + L * .4}" fill="none" stroke="${HAIR}" stroke-width="7" stroke-linecap="round"/><path d="M-14,-26 Q-4,-33 8,-30" fill="none" stroke="#4a3d5c" stroke-width="2" stroke-linecap="round" opacity=".7"/>`;
  const shade = `<ellipse cx="3" cy="14" rx="20" ry="13" fill="url(#cheek)" opacity=".5"/>`;
  return `<g transform="translate(${Cx.toFixed(1)},${Cy.toFixed(1)}) rotate(${rot.toFixed(1)}) scale(.88)"><rect x="-6" y="22" width="12" height="16" rx="5" fill="${SK2}"/>${ears}<ellipse cx="0" cy="0" rx="25" ry="28" fill="url(#skin)"/>${shade}${hair}${faceSvg(M, look, t, gz || [0, 0])}</g>`;
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

function footPos(H, h, k) { const d1 = dir(h), K = [H[0] + d1[0] * Ls.thigh, H[1] + d1[1] * Ls.thigh], d2 = dir(h + k); return [K[0] + d2[0] * Ls.shin, K[1] + d2[1] * Ls.shin]; }
function render(t) {
  const p = procedural(evalKeys(t), t), M = moodP(t);
  const Hp = [p.x, p.y], Sp = shoulder(p), hd = head(p);
  const prev = evalKeys(Math.max(0, t - 0.07)), lag = clamp((prev.torso - p.torso) * 0.55 + (prev.y - p.y) * 0.04, -9, 9);
  const hRot = p.torso * 0.5 + p.tilt + lag * 0.5;
  // нигоҳ: ба ноутбук, гоҳ ба код
  let gz = [p.look * 0.18, 0];
  const seatedTyping = (t > 3.6 && t < 8.6) || (t > 22.6 && t < 31.5);
  if (seatedTyping) { const c = t % 2.7; gz = (c > 2.15 && c < 2.55) ? [-1, -2.8] : [2.4, 1.8]; }
  else if (t >= 11.6 && t < 16) gz = [0, -1.5 * Math.sin(t * 9)];
  const hipL = [Hp[0] - 4, Hp[1]], hipR = [Hp[0] + 4, Hp[1]];
  const fL = footPos(hipL, p.hL, p.kL), fR = footPos(hipR, p.hR, p.kR);
  const lowest = Math.max(fL[1], fR[1], Hp[1]), air = clamp(GY - 6 - lowest, 0, 120), sx = (fL[0] + fR[0]) / 2;
  let s = `<ellipse cx="${CHX + 4}" cy="${GY + 5}" rx="54" ry="7" fill="#000" opacity=".38"/>`;
  s += `<ellipse cx="${sx.toFixed(1)}" cy="${GY + 5}" rx="${(50 - air * 0.18).toFixed(1)}" ry="${(7 - air * 0.03).toFixed(1)}" fill="#000" opacity="${(0.4 * (1 - air / 130)).toFixed(2)}"/>`;
  if (p.ly > GY - 4) s += `<ellipse cx="${p.lx.toFixed(1)}" cy="${GY + 6}" rx="42" ry="5" fill="#000" opacity=".42"/>`;
  s += chairSvg(CHX, SEAT);
  s += leg(hipL, p.hL, p.kL, false);
  s += arm(shoulderJoint(p, -1), p.aL, p.bL, false, p, t, 'L');
  s += leg(hipR, p.hR, p.kR, true);
  s += torsoPath(Hp, Sp);
  s += headSvg(hd[0], hd[1], hRot, M, p.look, t, lag, gz);
  s += laptopSvg(p);
  s += arm(shoulderJoint(p, 1), p.aR, p.bR, true, p, t, 'R');
  // рӯшноии экран (ба рӯй ва дастҳо мерасад)
  const gc = p.heat < .5 ? mixc('#BD93F9', '#FFB86C', p.heat / .5) : mixc('#FFB86C', '#F48771', (p.heat - .5) / .5);
  if (p.ly < GY + 30) s += `<circle cx="${(p.lx + 34).toFixed(1)}" cy="${(p.ly - 34).toFixed(1)}" r="120" fill="${gc}" opacity="${(0.12 + 0.1 * p.heat).toFixed(2)}" style="mix-blend-mode:screen" filter="url(#soft)"/>`;
  let extra = '';
  if (t >= 10.2 && t < 11.6) extra += `<path d="M${hd[0] + 26},${hd[1] - 20} q-5,9 0,12 q5,-3 0,-12z" fill="#4FC1FF"/>`;
  if (t >= 12 && t < 16) extra += `<path d="M${hd[0] - 40},${hd[1] - 10} q-5,9 0,12 q5,-3 0,-12z M${hd[0] + 42},${hd[1] - 2} q-5,9 0,12 q5,-3 0,-12z" fill="#4FC1FF"/>`;
  if (t >= 22.6 && t < 31) extra += `<text x="${hd[0] - 14}" y="${hd[1] - 46}" font-size="28">💡</text>`;
  if (t >= 33.4 && t < 37.6) extra += `<text x="${hd[0] - 78}" y="${hd[1] - 20}" font-size="24">✨</text><text x="${hd[0] + 52}" y="${hd[1] - 4}" font-size="24">✨</text>`;
  if (t >= 38.3 && t < 42.9) extra += `<text x="${hd[0] + 22}" y="${hd[1] - 36}" font-size="30" font-weight="900" fill="#FF79C6">?</text><text x="${hd[0] - 34}" y="${hd[1] - 26}" font-size="22" font-weight="900" fill="#BD93F9">?</text>`;
  document.getElementById('rig').innerHTML = s + extra;
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
  s += arm(shoulderJoint(p, -1), p.aL, p.bL, false, p, t, 'L');
  s += leg([Hp[0] + 4, Hp[1]], p.hR, p.kR, true);
  s += torsoPath(Hp, Sp);
  s += headSvg(hd[0], hd[1], hRot, m, p.look, t, 0, [2.4, 1.8]);
  s += laptopSvg(p);
  s += arm(shoulderJoint(p, 1), p.aR, p.bR, true, p, t, 'R');
  return s;
}
window.__drawPose = drawPose; window.__STAND = STAND; window.__GY = GY;
window.__setT = render;
render(0);
})();
