// Детерминированный движок кадра: window.frame(t) приводит страницу (IDE + слайды + оверлеи) к моменту t.
(function () {
  "use strict";
  var TL = window.TL, $ = function (s) { return document.querySelector(s); };
  var clamp = function (x) { return x < 0 ? 0 : x > 1 ? 1 : x; };
  var easeOut = function (p) { return 1 - Math.pow(1 - p, 3); };
  var easeIO = function (p) { return p < .5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2; };
  var back = function (p) { var c = 1.7, c3 = c + 1; return 1 + c3 * Math.pow(p - 1, 3) + c * Math.pow(p - 1, 2); };

  /* ---------- слайды ---------- */
  var animEls = [].slice.call(document.querySelectorAll("[data-a]")).map(function (el) {
    var a = el.dataset.a.split(";"); return { el: el, k: a[0], t: +a[1], o: el.dataset.o != null ? +el.dataset.o : null, ok: el.dataset.ok || "fade" };
  });
  function animate(t) {
    animEls.forEach(function (A) {
      var p = clamp((t - A.t) / (A.k === "stamp" ? .35 : A.k === "drop" ? .6 : .5)), op = clamp(p * 2.5), tr = "";
      if (A.k === "up") tr = "translateY(" + (1 - easeOut(p)) * 40 + "px)";
      else if (A.k === "down") tr = "translateY(" + -(1 - easeOut(p)) * 40 + "px)";
      else if (A.k === "left") tr = "translateX(" + -(1 - easeOut(p)) * 80 + "px)";
      else if (A.k === "right") tr = "translateX(" + (1 - easeOut(p)) * 80 + "px)";
      else if (A.k === "pop") tr = "scale(" + (p ? back(p) : 0) + ")";
      else if (A.k === "stamp") { tr = "scale(" + (2.2 - 1.2 * easeOut(p)) + ") rotate(" + (-4 * (1 - p)) + "deg)"; op = clamp(p * 3); }
      else if (A.k === "drop") { var d = p < .7 ? -260 * (1 - easeOut(p / .7)) : 14 * Math.sin((p - .7) / .3 * Math.PI) * (1 - p) * 3; tr = "translateY(" + d + "px)"; op = clamp(p * 6); }
      if (A.o != null && t >= A.o) {
        var q = clamp((t - A.o) / .45);
        if (A.ok === "flyout") tr += " translateY(" + -easeIO(q) * 300 + "px) rotate(" + q * 25 + "deg)";
        if (A.ok === "shrink") tr += " scale(" + (1 - q) + ")";
        op *= 1 - q;
      }
      A.el.style.opacity = op; A.el.style.transform = tr;
    });
    document.querySelectorAll("[data-cnt]").forEach(function (el) {
      var c = el.dataset.cnt.split(";"), a = +c[0], b = +c[1], p = easeIO(clamp((t - +c[2]) / +c[3]));
      el.textContent = Math.round(a + (b - a) * p).toLocaleString("ru-RU");
    });
    document.querySelectorAll("[data-tw]").forEach(function (el) {
      var c = el.dataset.tw.split(";"), s = el.dataset.text, n = Math.floor(s.length * clamp((t - +c[0]) / +c[1]));
      el.textContent = s.slice(0, n); el.classList.toggle("typing", n > 0 && n < s.length);
    });
  }
  function scenes(t) {
    TL.scenes.forEach(function (S) {
      var el = document.getElementById(S.id); if (!el) return;
      var op = Math.min(clamp((t - S.t0) / .35), 1 - clamp((t - S.t1) / .35));
      el.style.opacity = op; el.style.visibility = op > 0 ? "visible" : "hidden";
      el.style.transform = "scale(" + (1 + .025 * clamp((t - S.t0) / (S.t1 - S.t0))) + ")";
    });
  }
  function inIde(t) { return TL.scenes.some(function (S) { return S.id === "ide" && t >= S.t0 && t < S.t1; }); }

  /* ---------- редактор ---------- */
  var ta = document.getElementById("ta"), hl = document.getElementById("hl");
  var FILES = ["html", "css", "js"], cache = {}, dirty = false;
  function stateAt(f, t) {
    var op = null;
    TL.ide.forEach(function (o) { if ((o.op === "set" || o.op === "type") && (o.file || "js") === f && o.t <= t) op = o; });
    if (!op) return { code: null };
    if (op.op === "set") return { code: op.code, caret: null };
    var A = op.from, B = op.to, pre = 0; while (pre < A.length && pre < B.length && A[pre] === B[pre]) pre++;
    var suf = 0; while (suf < A.length - pre && suf < B.length - pre && A[A.length - 1 - suf] === B[B.length - 1 - suf]) suf++;
    var mA = A.slice(pre, A.length - suf), mB = B.slice(pre, B.length - suf);
    var p = clamp((t - op.t) / op.dur), del = mA.length ? Math.min(.35, mA.length * .06 / op.dur) : 0, mid;
    if (p < del) mid = mA.slice(0, Math.ceil(mA.length * (1 - p / del)));
    else mid = mB.slice(0, Math.floor(mB.length * clamp((p - del) / (1 - del))));
    return { end: pre + mB.length, code: A.slice(0, pre) + mid + A.slice(A.length - suf), caret: t < op.t + op.dur + 1.2 ? pre + mid.length : null, opT: op.t, opDur: op.dur };
  }
  function applyCode(t) {
    var changed = false, cs = { code: null }, cur = window.__ide.cur();
    FILES.forEach(function (f) {
      var s = stateAt(f, t);
      if (s.code != null && cache[f] !== s.code) { cache[f] = s.code; window.__ide.setFileCode(f, s.code); changed = true; }
      if (f === cur) cs = s;
    });
    if (changed) dirty = true;
    return { cs: cs, changed: changed };
  }
  function lastChange(t) {
    var m = -1; TL.ide.forEach(function (o) { if ((o.op === "set" || o.op === "type") && o.t <= t) m = Math.max(m, o.op === "type" ? Math.min(t, o.t + o.dur) : o.t); });
    return m;
  }
  // прямоугольник символов [c0, c1) строки line в подсвеченном коде
  function charRect(line, c0, c1) {
    var lines = ta.value.split("\n"), off = 0;
    for (var i = 0; i < line; i++) { if (lines[i] === undefined) return null; off += lines[i].length + 1; }
    var a = off + c0, b = off + c1, w = document.createTreeWalker(hl, NodeFilter.SHOW_TEXT), n, pos = 0, r = document.createRange(), sa = 0, sb = 0;
    while ((n = w.nextNode())) {
      var L = n.nodeValue.length;
      if (!sa && a <= pos + L) { r.setStart(n, a - pos); sa = 1; }
      if (!sb && b <= pos + L) { r.setEnd(n, b - pos); sb = 1; break; }
      pos += L;
    }
    if (!sa || !sb) return null;
    var rs = r.getClientRects(); if (!rs.length) return null;
    var R = { left: 1e9, top: 1e9, right: -1e9, bottom: -1e9 };
    [].forEach.call(rs, function (q) { R.left = Math.min(R.left, q.left); R.top = Math.min(R.top, q.top); R.right = Math.max(R.right, q.right); R.bottom = Math.max(R.bottom, q.bottom); });
    return R;
  }
  var gut = document.getElementById("gut"), codewrap = ta.parentNode, G = { key: null, acc: [] };
  ta.setAttribute("wrap", "soft");
  // каретка с учётом переноса строк и прокрутки
  function caretRect(idx) {
    var all = ta.value.split("\n"), v = ta.value.slice(0, idx).split("\n"), line = v.length - 1, col = v[line].length, r = null;
    if (col > 0) { r = charRect(line, col - 1, col); if (r) return { x: r.right, y: r.top, h: r.bottom - r.top }; }
    else if (all[line] && all[line].length) { r = charRect(line, 0, 1); if (r) return { x: r.left, y: r.top, h: r.bottom - r.top }; }
    var cs = getComputedStyle(hl), lh = parseFloat(cs.lineHeight), hr = hl.getBoundingClientRect(), z = hr.width / hl.offsetWidth;
    var rb = G.acc[line] != null ? G.acc[line] : line * lh;
    return { x: hr.left + parseFloat(cs.paddingLeft) * z, y: hr.top + (parseFloat(cs.paddingTop) + rb - hl.scrollTop) * z, h: lh * z };
  }
  // номери сатрҳо бо назардошти «ба сатри нав гузаштан» + прокрутка то каретка
  function layoutEditor(cs) {
    hl.scrollTop = 0; ta.scrollTop = 0; gut.scrollTop = 0;
    var lines = ta.value.split("\n"), lh = parseFloat(getComputedStyle(hl).lineHeight), hr = hl.getBoundingClientRect(), z = hr.width / hl.offsetWidth || 1;
    var key = ta.value + "|" + Math.round(hr.width / z);
    if (G.key !== key || !gut.firstElementChild) {
      var acc = [], a = 0, html = "";
      for (var i = 0; i < lines.length; i++) {
        var h = lh, r = lines[i].length ? charRect(i, 0, lines[i].length) : null;
        if (r) h = Math.max(lh, Math.round((r.bottom - r.top) / z / lh) * lh);
        acc.push(a); a += h; html += '<div style="height:' + h + 'px">' + (i + 1) + "</div>";
      }
      gut.innerHTML = html; G.key = key; G.acc = acc;
    }
    var idx = cs.caret != null ? cs.caret : (cs.end != null ? cs.end : 0);
    var cr = caretRect(idx), pt = (cr.y - hr.top) / z, ch = cr.h / z, H = codewrap.clientHeight;
    var target = Math.max(0, pt + ch + 30 - H); if (target > 0) target = 14 + Math.ceil((target - 14) / lh) * lh;
    hl.scrollTop = target; ta.scrollTop = target; gut.scrollTop = target;
  }

  /* ---------- оверлеи ---------- */
  var ov = document.getElementById("ovl");
  function pool(cls, n) { var a = []; for (var i = 0; i < n; i++) { var d = document.createElement("div"); d.className = cls; ov.appendChild(d); a.push(d); } return a; }
  var markEls = pool("mk", 6), ringEls = pool("rg", 4), chipEls = pool("chip", 3);
  var caret = pool("caret", 1)[0], ptr = document.getElementById("ptr"), rip = document.getElementById("rip");
  function elRect(sel) { var e = document.querySelector(sel); return e ? e.getBoundingClientRect() : null; }
  function overlays(t, cs, ide) {
    var mi = 0;
    if (ide) TL.marks.forEach(function (m) {
      if (t < m.t0 || t > m.t1 + .3 || mi >= markEls.length) return;
      var r = charRect(m.line, m.c0, m.c1); if (!r) return;
      var cw = codewrap.getBoundingClientRect(); if (r.bottom > cw.bottom + 2 || r.top < cw.top - 2) return;
      var el = markEls[mi++], p = clamp((t - m.t0) / .4), q = clamp((t - m.t1) / .3);
      el.className = "mk " + (m.color || "y") + (m.pos === "below" ? " below" : "");
      el.innerHTML = m.text ? '<b style="transform:scale(' + (p ? back(p) : 0) + ')"><i>' + m.text + "</i></b>" : "";
      el.style.cssText = "display:block;left:" + (r.left - 6) + "px;top:" + (r.top - 4) + "px;width:" + (r.right - r.left + 12) + "px;height:" + (r.bottom - r.top + 8) + "px;opacity:" + clamp(p * 2) * (1 - q);
    });
    for (; mi < markEls.length; mi++) markEls[mi].style.display = "none";
    var ri = 0;
    if (ide) TL.rings.forEach(function (g) {
      if (t < g.t0 || t > g.t1 + .3 || ri >= ringEls.length) return;
      var r = elRect(g.sel); if (!r || !r.width) return;
      var el = ringEls[ri++], p = clamp((t - g.t0) / .35), q = clamp((t - g.t1) / .3), pad = g.pad != null ? g.pad : 6;
      el.className = "rg " + (g.color || "y");
      el.innerHTML = g.text ? "<b><i>" + g.text + "</i></b>" : "";
      if (g.text && r.top < 150) el.classList.add("below");
      if (r.left > 640) el.classList.add("rt"); if (r.width > 800 || g.sel === "#task" || g.sel === "#checks") el.classList.add("in");
      el.style.cssText = "display:block;left:" + (r.left - pad) + "px;top:" + (r.top - pad) + "px;width:" + (r.width + 2 * pad) + "px;height:" + (r.height + 2 * pad) + "px;opacity:" + p * (1 - q) + ";transform:scale(" + (1.15 - .15 * easeOut(p)) + ")";
    });
    for (; ri < ringEls.length; ri++) ringEls[ri].style.display = "none";
    var ci = 0;
    TL.chips.forEach(function (c) {
      if (t < c.t0 || t > c.t1 + .3 || ci >= chipEls.length) return;
      var el = chipEls[ci++], p = clamp((t - c.t0) / .45), q = clamp((t - c.t1) / .3);
      el.className = "chip " + (c.cls || ""); el.innerHTML = c.html;
      el.style.cssText = "display:flex;opacity:" + clamp(p * 2) * (1 - q) + ";transform:translate(-50%,-50%) scale(" + (p ? back(p) : 0) * (1 - .1 * q) + ")" + (c.style ? ";" + c.style : "");
    });
    for (; ci < chipEls.length; ci++) chipEls[ci].style.display = "none";
    // каретка
    if (ide && cs.caret != null) { var cr = caretRect(cs.caret); caret.style.cssText = "display:block;left:" + cr.x + "px;top:" + cr.y + "px;height:" + cr.h + "px;opacity:" + (Math.floor(t * 2.2) % 2 && cs.typingDone ? 0 : 1); }
    else caret.style.display = "none";
    // указатель
    var P = TL.ptr, k = -1; for (var i = 0; i < P.length; i++) if (P[i].t - .7 <= t) k = i;
    var pp = window.__pvPtr;
    if (ide && pp && t >= pp.t && (k < 0 || pp.t > P[k].t)) {
      ptr.style.cssText = "display:block;left:" + pp.x + "px;top:" + pp.y + "px";
      var q = clamp((t - pp.t) / .5);
      if (q < 1 && !pp.hover) rip.style.cssText = "display:block;left:" + pp.x + "px;top:" + pp.y + "px;opacity:" + (1 - q) + ";transform:translate(-50%,-50%) scale(" + (.3 + q * 1.4) + ")"; else rip.style.display = "none";
      return;
    }
    if (!ide || k < 0 || !P[k].sel) { ptr.style.display = "none"; rip.style.display = "none"; return; }
    function ctr(sel) { var r = elRect(sel); return r ? { x: r.left + r.width / 2, y: r.top + r.height / 2 } : { x: 640, y: 360 }; }
    var to = ctr(P[k].sel), pos = to;
    if (t < P[k].t && k > 0 && P[k - 1].sel) { var fr = ctr(P[k - 1].sel), e = easeIO(clamp((t - (P[k].t - .7)) / .7)); pos = { x: fr.x + (to.x - fr.x) * e, y: fr.y + (to.y - fr.y) * e }; }
    else if (t < P[k].t) { var e2 = easeOut(clamp((t - (P[k].t - .7)) / .7)); pos = { x: to.x + 120 * (1 - e2), y: to.y + 160 * (1 - e2) }; }
    ptr.style.cssText = "display:block;left:" + pos.x + "px;top:" + pos.y + "px";
    var cl = null; TL.ide.forEach(function (o) { if (o.sel && o.t <= t && t < o.t + .5) cl = o; });
    if (cl) { var rp = clamp((t - cl.t) / .5); rip.style.cssText = "display:block;left:" + pos.x + "px;top:" + pos.y + "px;opacity:" + (1 - rp) + ";transform:translate(-50%,-50%) scale(" + (.3 + rp * 1.4) + ")"; }
    else rip.style.display = "none";
  }

  /* ---------- камера (зум в IDE) ---------- */
  var app = document.querySelector(".app");
  function camera(t) {
    var s = 1, x = 640, y = 360;
    TL.zooms.forEach(function (z) {
      if (t < z.t0 - .7 || t > z.t1 + .7) return;
      var p = t < z.t0 ? easeIO(clamp((t - z.t0 + .7) / .7)) : t > z.t1 ? 1 - easeIO(clamp((t - z.t1) / .7)) : 1;
      s = 1 + (z.s - 1) * p; x = 640 + (z.x - 640) * p; y = 360 + (z.y - 360) * p;
    });
    // фокус (x,y) переходит в центр кадра, края не выходят за экран
    var tx = Math.min(0, Math.max(1280 - 1280 * s, 640 - x * s)), ty = Math.min(0, Math.max(720 - 720 * s, 360 - y * s));
    app.style.transform = "translate(" + tx + "px," + ty + "px) scale(" + s + ")";
  }

  /* ---------- реальные действия в IDE ---------- */
  var done = 0, real = TL.ide.filter(function (o) { return o.op === "run" || o.op === "check" || o.op === "click" || o.op === "goto" || o.op === "clear" || o.op === "file"; });
  var sleep = function (ms) { return new Promise(function (r) { setTimeout(r, ms); }); };
  window.frame = async function (t) {
    while (done < real.length && real[done].t <= t) {
      var o = real[done++]; applyCode(o.t);
      if (o.op === "goto") window.__ide.goto(o.lesson, o.i || 0);
      else if (o.op === "run") document.getElementById("run").click();
      else if (o.op === "check") document.getElementById("check").click();
      else if (o.op === "clear") document.getElementById("out").innerHTML = "";
      else if (o.op === "click") document.querySelector(o.sel).click();
      else if (o.op === "file") window.__ide.setFile(o.file);
      await sleep(o.op === "goto" ? 120 : (o.wait || 260));
    }
    var ide = inIde(t), ac = applyCode(t), cs = ac.cs;
    var needRender = dirty; dirty = false;
    if (needRender) await new Promise(function (r) { var d = 0, f = function () { if (!d) { d = 1; r(); } }; window.__ide.renderPreview(f); setTimeout(f, 1500); });
    var last = null; TL.ide.forEach(function (o) { if (o.op === "type" && o.t <= t && (o.file || "js") === window.__ide.cur()) last = o; });
    cs.typingDone = !last || t > last.t + last.dur;
    if (ide) layoutEditor(cs);
    scenes(t); animate(t); camera(t); overlays(t, cs, ide);
    document.body.classList.toggle("noide", !ide);
    return { reloaded: needRender, tc: lastChange(t) };
  };
})();
