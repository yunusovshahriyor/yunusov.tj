# «Даври бепоён» v2 — анимацияи беовоз ва БЕ ШАРҲ. Одамак бо ноутбук; код дар ҳаво менависад.
# Матн танҳо: код, «Салом»-ҳо, рақамҳо ва калимаи «ДАВР» дар охир.
import json, random
import character as C
END = 47.5
f = lambda x: f"{x:.2f}s"
R = random.Random(11)
SFX = []
def sfx(name, at, gain=1.0): SFX.append(dict(name=name, t=round(at, 3), gain=gain))
def typing(at, dur, raw, gain=0.55):
    n = len(raw); step = dur / max(1, n)
    for k, ch in enumerate(raw):
        if ch != " ": sfx("key", at + k * step, gain)
def TYP(at, dur, html, raw):
    typing(at, dur, raw)
    return f'<span class="type" style="--a:{at:.2f}s;--d:{dur:.2f}s;--n:{len(raw)}">{html}</span>'
H = []
def S(a, b=None): return f"--a:{a:.2f}s;--b:{(b if b is not None else END + 5):.2f}s"
def scene(a, b, body, whoosh=False):
    H.append(f'<div class="sc" style="{S(a, b)}">{body}</div>')
    if whoosh: sfx("whoosh", a - 0.05, 0.4)
LOGH = '  <span class=f>console</span>.<span class=f>log</span>(<span class=s>"Салом"</span>);'
LOGR = '  console.log("Салом");'

# ---------- ҳолатҳои Одамак ----------
def tap(s): return f'<g class="tap">{s}</g>'
def P_type(scr="#BD93F9", mood="type", sweat=False, extra=""):
    sw = '<path d="M130,40 q-5,9 0,12 q5,-3 0,-12z" fill="#4FC1FF"/><path d="M84,52 q-5,9 0,12 q5,-3 0,-12z" fill="#4FC1FF"/>' if sweat else ""
    return (C.leg((104,170),(150,192),(116,214),False) + C.leg((104,170),(64,194),(104,216),True,-1)
            + C.arm((112,114),(138,150),(160,178),False) + C.torso((90,112),(126,112),(88,172),(120,172)) + C.head(108,76,mood)
            + C.laptop(142,124,scr,64,50) + tap(C.arm((92,116),(124,152),(148,178))) + sw + extra)
def P_walk(ph):
    a = ((124,214,112,250),(146,214,160,250)) if ph == 0 else ((130,210,146,250),(140,212,122,250))
    (k1x, k1y, f1x, f1y), (k2x, k2y, f2x, f2y) = a
    return (C.leg((126,170),(k1x,k1y),(f1x,f1y),False,-1) + C.leg((146,170),(k2x,k2y),(f2x,f2y))
            + C.torso((112,112),(158,112),(116,172),(154,172)) + C.head(135,68,"type") + C.arm((118,112),(120,148),(150,150),False)
            + C.laptop(138,116,"#BD93F9",44,34) + C.arm((152,114),(158,146),(146,150)))
def P_shock():
    drops = '<path d="M58,40 q-5,9 0,12 q5,-3 0,-12z M208,52 q-5,9 0,12 q5,-3 0,-12z" fill="#4FC1FF"/>'
    return (C.leg((126,170),(108,214),(96,250),False,-1) + C.leg((146,170),(164,214),(178,250)) + C.arm((152,112),(178,84),(190,48),False)
            + C.torso((112,112),(158,112),(116,172),(154,172)) + C.head(135,68,"shock") + C.arm((118,112),(92,84),(80,48)) + drops
            + C.laptop(188,196,"#F48771",60,44,'<text x="30" y="30" font-size="22" text-anchor="middle">🔥</text>'))
def P_buried(): return C.arm((168,172),(192,130),(208,90),False).replace('<path','<path class="wave"',1) + C.head(135,128,"help")
def P_happy():
    return (C.leg((126,170),(108,214),(96,250),False,-1) + C.leg((146,170),(164,214),(178,250)) + C.arm((152,112),(184,78),(194,40),False)
            + C.torso((112,112),(158,112),(116,172),(154,172)) + C.head(135,68,"happy") + C.arm((118,112),(86,78),(76,40))
            + '<text x="52" y="64" font-size="22">✨</text><text x="205" y="74" font-size="22">✨</text>'
            + C.laptop(190,198,"#4EC9B0",60,44,'<text x="30" y="30" font-size="22" font-weight="900" fill="#4EC9B0" text-anchor="middle">✓</text>'))
def P_wave():
    return (C.leg((126,170),(108,214),(96,250),False,-1) + C.leg((146,170),(164,214),(178,250)) + C.arm((152,112),(176,86),(194,50),False).replace('<path','<path class="wave"',1)
            + C.torso((112,112),(158,112),(116,172),(154,172)) + C.head(135,68,"happy") + C.arm((118,112),(120,150),(124,184)))
def pose(a, b, inner, cls="bob"):
    H.append(f'<div class="pose {cls}" style="--a:{a:.2f}s;--b:{b:.2f}s">{C.svg(inner)}</div>')

# ---------- 0–3: қадамзанӣ ----------
def _ss(x): x = max(0, min(1, x)); return x * x * (3 - 2 * x)
import math
_prev = None
for _i in range(0, 2600):
    _t = 0.2 + _i * 0.001
    _x = -90 + 325 * _ss((_t - 0.2) / 2.5)
    _c = math.floor(_x / 88 * 2)       # ҳар нимтаи давр — як қадам
    if _prev is not None and _c != _prev: sfx("tick", _t, 0.45)
    _prev = _c
sfx("thud", 2.9, 0.4)

# ---------- 3–8: фикр (се «Салом») + код дар ҳаво ----------
bub = ''.join(f'<div style="border-radius:11px;background:{c};width:58px;height:22px;font:800 12px/22px Inter;text-align:center;color:#1E1E1E">Салом</div>' for c in ("#BD93F9", "#FF79C6", "#BD93F9"))
H.append(f'<div class="bubble" style="--a:3.0s;--g:8.0s;left:90px;top:332px;flex-direction:column;gap:5px;padding:9px 11px;border-radius:22px">{bub}</div>')
H.append('<div class="bub-dot pop" style="--a:3.0s;left:196px;top:470px;width:14px;height:14px"></div><div class="bub-dot pop" style="--a:3.0s;left:186px;top:448px;width:9px;height:9px"></div>')
sfx("pop", 3.0, 0.6)
l1 = TYP(3.6, 1.2, "<span class=c>while</span> (<span class=k>true</span>) {", "while (true) {")
l2 = TYP(4.9, 1.7, LOGH, LOGR)
l3 = TYP(6.7, 0.2, "}", "}")
CUR = '<i class="cur"></i>'
H.append(f'<div class="fcode" style="top:150px;--v:19.0s;animation:gone .25s ease-in 19.0s forwards"><div class="ln">{l1}{CUR}</div><div class="ln">{l2}</div><div class="ln">{l3}</div></div>')
# Enter / Run
sfx("click", 8.0, 0.9); sfx("ding", 8.05, 0.6)
H.append(f'<div class="fl" style="--a:8.0s;left:340px;top:560px;font-size:30px;color:#4EC9B0;animation:popin .3s var(--a) both,gone .2s 8.9s forwards">▶</div>')

# ---------- 8.4–15.9: «Салом»-ҳо мепаранд ----------
N = 70; LX, LY = 330, 590
for i in range(N):
    p = i / N
    ta = 8.4 + (p ** 1.7) * 7.2
    x = R.randint(20, 470); y = 705 - R.random() * (36 + 190 * p)
    r = R.randint(-25, 25); c = "#BD93F9" if i % 2 else "#FF79C6"
    H.append(f'<div class="fly" style="--a:{ta:.2f}s;--c:19.0s;--sx:{LX - 29}px;--sy:{LY}px;--x:{x}px;--y:{y:.0f}px;--r:{r}deg;--d:{0.55 + R.random() * .3:.2f}s;z-index:5"><div class="pillx" style="background:{c}">Салом</div></div>')
    if i % 3 == 0: sfx("pop", ta, 0.28)
for k in range(5): H.append(f'<div class="steam" style="--a:{10.4 + k * .27:.2f}s;left:{300 + k * 14}px;top:540px;--sx:{(k - 2) * 12}px"></div>')
sfx("riser", 8.4, 0.5); sfx("fan", 9.4, 0.5); sfx("buzz", 11.4, 0.7); sfx("riser", 12.8, 0.5); sfx("boing", 9.6, 0.5)
sfx("hit", 15.9, 0.9); sfx("whoosh", 16.0, 0.7); sfx("riser", 16.1, 0.6)
sfx("thud", 19.05, 0.8)

# ---------- 19–23: код бармегардад, true ♾️ ✅ ----------
code3 = (f'<div class="ln"><span class="c">while</span> (<span class="hlt" style="--a:19.8s;--b:{END + 5:.2f}s;color:#fff"><span class="k">true</span></span>) {{</div>'
         f'<div class="ln">{LOGH.replace("class=", "class=")}</div><div class="ln">}}</div>')
H.append(f'<div class="fcode" style="top:150px;opacity:0;animation:fadein .3s 19.2s both,gone .25s ease-in 23.6s forwards">{code3}</div>')
H.append('<div class="fl" style="--a:19.9s;left:410px;top:150px;font-size:56px;animation:popin .4s var(--a) both,spin 1.6s linear 20.3s infinite,gone .2s 23.6s forwards">♾️</div>')
for k in range(5):
    H.append(f'<div class="fl" style="--a:{20.4 + k * 0.45:.2f}s;left:{120 + k * 56}px;top:290px;animation:popin .4s var(--a) both,gone .2s 23.6s forwards">✅</div>')
    sfx("pop", 20.4 + k * 0.45, 0.55)
sfx("chime", 19.8, 0.5); sfx("tick2", 19.9, 0.4)

# ---------- 23–30.5: for — вайрон ва нав ----------
H.append(f'<div class="sel fcode" style="--a:23.4s;top:150px;left:60px;right:60px;opacity:0;animation:fadein .01s 23.4s both,selin .12s 23.4s both,gone .2s 24.0s forwards;color:transparent;text-shadow:none"><div class="ln">while (true) {{</div><div class="ln">  console.log("Салом");</div><div class="ln">}}</div></div>')
sfx("click", 23.4, 0.7); sfx("whoosh", 24.0, 0.5)
ta_, tb_, tc_ = 28.0, 28.9, 29.8
col1, col2, col3 = "#4EC9B0", "#DCDCAA", "#FF79C6"
h_for = (f'<span class="c">for</span> (<span class="k">let</span> <span class="part" style="--a:{ta_}s;--col:{col1}"><span class="p">i</span> = <span class="n">0</span><b>1</b></span>; '
         f'<span class="part" style="--a:{tb_}s;--col:{col2}"><span class="p">i</span> &lt; <span class="n">3</span><b>2</b></span>; '
         f'<span class="part" style="--a:{tc_}s;--col:{col3}"><span class="p">i</span>++<b>3</b></span>) {{')
r_for = "for (let i = 0; i < 3; i++) {"
for t_ in (ta_, tb_, tc_): sfx("pop", t_, 0.7); sfx("chime", t_ + 0.05, 0.4)
H.append(f'<div class="fcode" style="top:150px;--v:38.0s;animation:gone .25s ease-in 37.6s forwards"><div class="ln">{TYP(24.4, 3.0, h_for, r_for)}{CUR}</div><div class="ln">{TYP(27.6, 1.4, LOGH, LOGR)}</div><div class="ln">{TYP(29.1, 0.2, "}", "}")}</div></div>')

# ---------- 30.6–33: иҷро: i = 0,1,2,3 ----------
sfx("click", 30.6, 0.9); sfx("ding", 30.65, 0.6)
ibox = (f'<div class="ibox" style="--a:30.7s;animation:popin .45s cubic-bezier(.3,1.6,.5,1) 30.7s both,gone .2s 37.6s forwards"><small>i</small><b><span style="--a:30.8s;--b:31.6s">0</span><span style="--a:31.6s;--b:32.4s">1</span><span style="--a:32.4s;--b:33.2s">2</span><span style="--a:33.2s;--b:37.6s">3</span></b></div>')
H.append(ibox)
for k, tt in enumerate((31.0, 31.8, 32.6)):
    H.append(f'<div class="fly" style="--a:{tt:.2f}s;--c:37.6s;--sx:{LX - 29}px;--sy:{LY}px;--x:{110 + k * 78}px;--y:690px;--r:{(-6, 4, -3)[k]}deg;--d:.6s;z-index:5"><div class="pillx" style="background:{"#BD93F9" if k % 2 == 0 else "#FF79C6"}">Салом</div></div>')
    sfx("pop", tt, 0.7); sfx("ding", tt + 0.03, 0.4)
for tt in (30.8, 31.6, 32.4): sfx("tick2", tt, 0.4)
H.append('<div class="fcode" style="top:300px;left:300px;right:0;text-align:left;font-size:22px;opacity:0;animation:fadein .2s 33.3s both,gone .2s 37.6s forwards;color:var(--err)">3 &lt; 3</div>')
H.append('<div class="xmark" style="--a:33.4s;--b:35.5s;left:400px;top:360px;font-size:70px">✖</div>')
sfx("buzz", 33.3, 0.5); sfx("hit", 33.4, 0.8); sfx("chime", 33.9, 0.8); sfx("ding", 34.0, 0.6)

# ---------- 37.6–43: санҷиш ----------
q = (f'<div class="ln">{TYP(37.9, 2.0, "<span class=c>for</span> (<span class=k>let</span> <span class=p>i</span> = <span class=n>0</span>; <span class=p>i</span> &lt; <span class=n>3</span>; ", "for (let i = 0; i < 3; ")}'
     f'<span class="hle" style="--a:40.0s;border:2px dashed var(--err);padding:0 8px;animation:fadein .2s 40.0s both,hle .25s 40.0s forwards">?</span>) {{</div>'
     f'<div class="ln">{TYP(40.3, 0.9, LOGH, LOGR)}</div><div class="ln">}}</div>')
H.append(f'<div class="fcode" style="top:150px;opacity:0;animation:fadein .2s 37.9s both,gone .25s ease-in 43.0s forwards">{q}</div>')
for k, (lab, sub) in enumerate([("3", ""), ("0", ""), ("♾️", "")]):
    H.append(f'<div class="card" style="animation:popin .45s cubic-bezier(.3,1.6,.5,1) {40.2 + k * 0.4:.2f}s both,gone .2s 43.0s forwards;left:{30 + k * 165}px;width:150px;top:300px;text-align:center;padding:16px 0;z-index:3"><div style="font:900 40px var(--mono);color:var(--purple)">{lab}</div></div>')
    sfx("pop", 40.2 + k * 0.4, 0.7)
sfx("tick2", 40.0, 0.5)

# ---------- 43–47.5: даъват ----------
H.append(f'''<div class="sc" style="{S(43.0)}">
<div class="card pop" style="--a:43.2s;left:40px;right:40px;top:130px;display:flex;align-items:center;gap:14px;padding:8px 16px">
 <div style="width:34px;height:34px;border-radius:50%;background:var(--accent)"></div>
 <div style="flex:1;background:#1E1E1E;border:1px solid var(--line);border-radius:999px;padding:9px 16px;font:700 16px var(--mono);color:var(--white)">{TYP(43.4, 0.7, "ДАВР", "ДАВР")}</div>
 <div style="font-weight:800;color:var(--purple)">➤</div></div>
<div class="card pop" style="--a:44.4s;left:40px;right:40px;top:196px;padding:0;overflow:hidden">
 <div style="height:100px;background:linear-gradient(135deg,#2a1f45,#1E1E1E);display:flex;align-items:center;justify-content:center"><div style="width:62px;height:44px;border-radius:12px;background:#F4443C;color:#fff;font-size:22px;line-height:44px;text-align:center">▶</div></div>
 <div style="padding:8px 18px"><div style="font:800 15px Inter;color:var(--white)">Давр (for) аз сифр</div></div></div>
<div class="pill acc2 pop" style="--a:45.5s;top:350px;font-size:17px;padding:8px 24px">🔔</div></div>''')
sfx("pop", 43.2, 0.6); sfx("pop", 44.4, 0.7); sfx("chime", 44.6, 0.6); sfx("ding", 45.5, 0.6)

RIG = open('rig.js', encoding='utf-8').read()
STAGE = '<svg id="stage" viewBox="0 0 540 960" width="540" height="960" style="position:absolute;left:0;top:0;z-index:2;overflow:visible">' + C.DEFS + '<g id="rig"></g></svg>'
html = f'''<!doctype html><html lang="tg"><head><meta charset="utf-8"><link rel="stylesheet" href="style.css"></head><body>
{STAGE}{"".join(H)}<script>{RIG}</script>
</body></html>'''
open('reel.html', 'w', encoding='utf-8').write(html)
json.dump(dict(end=END, sfx=SFX), open('sfx.json', 'w'))
print('END', END, 'sfx', len(SFX))
