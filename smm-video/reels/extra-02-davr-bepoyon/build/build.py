# «Даври бепоён» — анимацияи беовоз (Одамак). Таймингҳо дастӣ; садо: клавиатура + эффектҳо.
import json, random
import character as C
END = 47.0
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
def scene(a, b, body, whoosh=True):
    H.append(f'<div class="sc" style="{S(a, b)}">{body}</div>')
    if whoosh: sfx("whoosh", a - 0.05, 0.4)
def cap(a, b, txt, big=False):
    H.append(f'<div class="cap{" big" if big else ""}" style="--a:{a:.2f}s;--b:{b:.2f}s"><span>{txt}</span></div>')

LOGH = '  <span class=f>console</span>.<span class=f>log</span>(<span class=s>"Салом"</span>);'
LOGR = '  console.log("Салом");'
# ---------- ҳолатҳои Одамак ----------
def tap(s): return f'<g class="tap">{s}</g>'
def P_type(scr="#BD93F9", mood="type", sweat=False, extra=""):
    sw = '<path d="M130,40 q-5,9 0,12 q5,-3 0,-12z" fill="#4FC1FF"/><path d="M84,52 q-5,9 0,12 q5,-3 0,-12z" fill="#4FC1FF"/>' if sweat else ""
    return (C.leg((104,170),(150,192),(116,214),False) + C.leg((104,170),(64,194),(104,216),True,-1)
            + C.arm((112,114),(138,150),(160,178),False) + C.torso((90,112),(126,112),(88,172),(120,172)) + C.head(108,76,mood)
            + C.laptop(142,124,scr,64,50) + tap(C.arm((92,116),(124,152),(148,178))) + sw + extra)
def P_shock():
    drops = '<path d="M58,40 q-5,9 0,12 q5,-3 0,-12z M208,52 q-5,9 0,12 q5,-3 0,-12z" fill="#4FC1FF"/>'
    return (C.leg((126,170),(108,214),(96,250),False,-1) + C.leg((146,170),(164,214),(178,250)) + C.arm((152,112),(178,84),(190,48),False)
            + C.torso((112,112),(158,112),(116,172),(154,172)) + C.head(135,68,"shock") + C.arm((118,112),(92,84),(80,48)) + drops
            + C.laptop(188,196,"#F48771",60,44,'<text x="30" y="30" font-size="22" text-anchor="middle">🔥</text>'))
def P_buried():
    return C.arm((168,172),(192,130),(208,90),False).replace('<path','<path class="wave"',1) + C.head(135,128,"help")
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

# 8 ҳолат дар як стейҷ
pose(0, 11.0, P_type())
pose(11.0, 12.6, P_type("#FFB86C", "help", True), "jit")
pose(12.6, 16.9, P_shock(), "jit")
pose(16.9, 20.0, P_buried(), "jit")
pose(20.0, 31.4, P_type("#BD93F9", "type", False, '<text x="96" y="26" font-size="26">💡</text>'))
pose(31.4, 35.0, P_happy())
pose(35.0, 41.0, P_type("#BD93F9", "help", False, '<text x="128" y="30" font-size="30" font-weight="900" fill="#FF79C6">?</text><text x="84" y="40" font-size="22" font-weight="900" fill="#BD93F9">?</text>'))
pose(41.0, END + 5, P_wave())

# ---------- сарлавҳа ----------
scene(0, 3.2, '<div class="slam acc" style="--a:0.2s;top:160px;font-size:50px">ДАВРИ БЕПОЁН</div><div class="pill ok pop" style="--a:.8s;top:230px;font-size:17px">♾️ чаро давр ист намекунад?</div>', whoosh=False)
sfx("hit", 0.2, 0.7); sfx("pop", 0.8, 0.6)

# ===== САҲНАИ 1: навиштани while(true) (0..10) =====
t_c, t_w, t_l, t_e = 0.9, 3.4, 5.0, 6.8
code1 = (f'<div class="ln">{TYP(t_c, 1.6, "<span class=cm>// се бор «Салом»</span>", "// се бор «Салом»")}</div>'
         f'<div class="ln">{TYP(t_w, 1.3, "<span class=c>while</span> (<span class=k>true</span>) {", "while (true) {")}</div>'
         f'<div class="ln">{TYP(t_l, 1.5, LOGH, LOGR)}</div>'
         f'<div class="ln">{TYP(t_e, 0.2, "}", "}")}</div>')
runbtn = f'<div class="abs" style="right:14px;top:6px;font:800 11px var(--mono);color:#1E1E1E;background:var(--ok);border-radius:999px;padding:3px 10px;animation:fadein .2s {f(6.9)} both,press .5s ease-out {f(8.1)} both">▶ RUN</div>'
term_lines = "".join(f'<span class="out" style="--a:{8.3 + k * 0.18:.2f}s">Салом</span>' for k in range(5))
scene(0.1, 17.2, f'''
<div class="ide" style="top:112px"><div class="bar"><i></i><i></i><i></i><span>salom.js</span>{runbtn}</div><div class="code" style="font-size:16px">{code1}</div>
<div class="term" style="min-height:72px;padding-top:6px"><span class="pr" style="color:var(--muted)">▸ натиҷа</span>{term_lines}</div></div>
<div class="chipx" style="animation:popin .45s cubic-bezier(.3,1.6,.5,1) 7.30s both,gone .2s ease-in 9.9s forwards;left:300px;top:395px;background:var(--panel2);border:1px solid var(--purple);color:#fff;font-family:Inter;font-weight:800">Осон! 😎</div>''', whoosh=False)
sfx("ding", 8.1, 0.6); sfx("click", 8.1, 0.9)
for k in range(5): sfx("tick", 8.3 + k * 0.18, 0.5)
sfx("pop", 7.3, 0.6)
cap(0.3, 3.4, "Одамак мехоҳад: компютер <em>се бор</em> «Салом» гӯяд")
cap(3.4, 7.6, "Ӯ менависад: <em>while (true)</em> — «то даме ки ҳақиқат аст»")
cap(7.6, 10.0, "Иҷро ▶")

# ===== САҲНАИ 2: «Салом»-ҳо мепаранд (10..17) =====
N = 70
LX, LY = 330, 590   # ҷойи ноутбук
for i in range(N):
    p = i / N
    ta = 10.0 + (p ** 1.7) * 6.4
    x = R.randint(20, 470); y = 705 - R.random() * (36 + 190 * p)
    r = R.randint(-25, 25); c = "#BD93F9" if i % 2 else "#FF79C6"
    H.append(f'<div class="fly" style="--a:{ta:.2f}s;--c:20.0s;--sx:{LX - 29}px;--sy:{LY}px;--x:{x}px;--y:{y:.0f}px;--r:{r}deg;--d:{0.55 + R.random() * .3:.2f}s;z-index:5"><div class="pillx" style="background:{c}">Салом</div></div>')
    if i % 3 == 0: sfx("pop", ta, 0.28)
# ҳисобкунак
for v, t0, t1 in [("1", 10.0, 10.8), ("10", 10.8, 11.6), ("100", 11.6, 12.5), ("1 000", 12.5, 13.5), ("10 000", 13.5, 14.6), ("100 000", 14.6, 15.8), ("1 000 000", 15.8, 17.2)]:
    H.append(f'<div class="counter" style="--a:{t0:.2f}s;--b:{t1:.2f}s;z-index:6">{v}×</div>')
    sfx("tick2", t0, 0.35)
for k in range(5): H.append(f'<div class="steam" style="--a:{12.0 + k * .27:.2f}s;left:{300 + k * 14}px;top:{540}px;--sx:{(k - 2) * 12}px"></div>')
sfx("riser", 10.0, 0.5); sfx("fan", 11.0, 0.5); sfx("buzz", 12.6, 0.7); sfx("riser", 14.0, 0.5); sfx("boing", 11.0, 0.5)
cap(10.0, 13.5, "Компютер «Салом» мегӯяд… ва мегӯяд… ва мегӯяд…")
cap(13.5, 17.0, "Ист намекунад! 😱", True)
# ноутбук парвоз мекунад
lap_svg = '<svg viewBox="0 0 90 70" width="130" height="100">' + C.DEFS + C.laptop(10, 6, "#F48771", 64, 44, '<text x="32" y="30" font-size="20" text-anchor="middle">🔥</text>') + '</svg>'
H.append(f'<div class="lfly" style="--a:16.9s;z-index:7">{lap_svg}</div>')
sfx("hit", 16.9, 0.9); sfx("whoosh", 17.0, 0.7); sfx("riser", 17.1, 0.6)

# ===== САҲНАИ 3: чаро? true (17..24) =====
code3 = f'<div class="ln"><span class="c">while</span> (<span class="hlt" style="--a:18.0s;--b:{END + 5:.2f}s;color:#fff"><span class="k">true</span></span>) {{</div><div class="ln">  <span class="f">console</span>.<span class="f">log</span>(<span class="s">"Салом"</span>);</div><div class="ln">}}</div>'
ticks = "".join(f'<span class="emo pop" style="--a:{20.4 + k * 0.45:.2f}s;font-size:34px;margin:0 6px">✅</span>' for k in range(5))
for k in range(5): sfx("pop", 20.4 + k * 0.45, 0.6)
scene(17.6, 24.0, f'''
<div class="ide" style="top:112px"><div class="bar"><i></i><i></i><i></i><span>salom.js</span></div><div class="code" style="font-size:16px">{code3}</div></div>
<div class="card pop" style="--a:20.2s;left:40px;right:40px;top:290px;text-align:center"><div style="font:800 13px var(--mono);color:var(--muted);letter-spacing:2px">ШАРТ ҲАР ДАФЪА:</div><div style="margin-top:6px"><b style="font:900 26px var(--mono);color:var(--ok)">true</b> {ticks}</div></div>
<div class="pill err pop" style="--a:22.6s;top:400px;font-size:17px">🚪✖ роҳи баромад нест</div>''')
cap(17.0, 20.0, "Чаро? Шарт ҳамеша <em>true</em> аст")
cap(20.0, 24.0, "Шарт ҳеҷ гоҳ «не» намешавад — давр <em>охир надорад</em>")
sfx("thud", 20.1, 0.8); sfx("chime", 18.0, 0.5); sfx("buzz", 22.6, 0.6)
lap_fall = '<svg viewBox="0 0 90 70" width="130" height="100">' + C.DEFS + C.laptop(10, 6, "#BD93F9", 64, 44) + '</svg>'
H.append(f'<div class="lfall" style="--a:19.9s;z-index:7">{lap_fall}</div>')

# ===== САҲНАИ 4: for — оғоз, шарт, қадам (24..35) =====
ta, tb, tc = 29.0, 30.0, 31.0
code4 = (f'<div class="ln">{TYP(24.2, 2.6, "<span class=c>for</span> (<span class=k>let</span> <span class=p hlt style=--a:%ss;--b:36.2s>i = 0</span>; <span class=p hlt style=--a:%ss;--b:36.2s>i &lt; 3</span>; <span class=p hlt style=--a:%ss;--b:36.2s>i++</span>) {" % (ta, tb, tc), "for (let i = 0; i < 3; i++) {")}</div>'
         f'<div class="ln">{TYP(27.0, 1.5, LOGH, LOGR)}</div>'
         f'<div class="ln">{TYP(28.6, 0.2, "}", "}")}</div>')
outs = "".join(f'<span class="out" style="--a:{t0:.2f}s">Салом</span>' for t0 in (31.7, 32.4, 33.1))
chips = (f'<div class="chipx" style="--a:{ta:.2f}s;left:8px;top:392px;font-size:13px;padding:6px 10px;background:rgba(78,201,176,.15);border:1.5px solid var(--ok);color:var(--ok)">1 · оғоз: i = 0</div>'
         f'<div class="chipx" style="--a:{tb:.2f}s;left:8px;top:430px;font-size:13px;padding:6px 10px;background:rgba(220,220,170,.12);border:1.5px solid var(--fn);color:var(--fn)">2 · шарт: i &lt; 3</div>'
         f'<div class="chipx" style="--a:{tc:.2f}s;left:8px;top:468px;font-size:13px;padding:6px 10px;background:rgba(255,121,198,.15);border:1.5px solid var(--pink);color:var(--pink)">3 · қадам: i++</div>')
for t_ in (ta, tb, tc): sfx("pop", t_, 0.7); sfx("chime", t_ + 0.05, 0.4)
ibox = (f'<div class="ibox" style="--a:31.3s"><small>i</small><b><span style="--a:31.4s;--b:32.1s">0</span><span style="--a:32.1s;--b:32.8s">1</span><span style="--a:32.8s;--b:33.5s">2</span><span style="--a:33.5s;--b:36s">3</span></b></div>'
        f'<div class="pill err pop" style="--a:33.6s;left:370px;right:auto;margin:0;top:572px;font-size:15px;font-family:var(--mono)">3 &lt; 3 ✖</div>'
        f'<div class="stop" style="--a:33.7s;--b:35.0s">БАС!</div>')
for t_ in (31.7, 32.4, 33.1): sfx("pop", t_, 0.6); sfx("ding", t_ + 0.02, 0.4)
sfx("tick2", 31.4, 0.4); sfx("tick2", 32.1, 0.4); sfx("tick2", 32.8, 0.4); sfx("buzz", 33.5, 0.5); sfx("hit", 33.7, 0.8); sfx("chime", 34.1, 0.7)
scene(24.0, 35.0, f'''
<div class="ide" style="top:112px"><div class="bar"><i></i><i></i><i></i><span>davr.js</span></div><div class="code" style="font-size:16px">{code4}</div>
<div class="term" style="min-height:62px;padding-top:6px"><span class="pr" style="color:var(--muted)">▸ натиҷа</span>{outs}</div></div>
{chips}{ibox}''')
cap(24.0, 29.0, "Ҳал: давр аз <em>се қисм</em> иборат аст")
cap(29.0, 31.4, "Давр = <em>оғоз</em> + <em>шарт</em> + <em>қадам</em>")
cap(31.4, 35.0, "Се бор — ва <em>бас</em>! ✅", True)

# ===== САҲНАИ 5: санҷиш (35..41) =====
code5 = (f'<div class="ln">{TYP(35.2, 2.0, "<span class=c>for</span> (<span class=k>let</span> <span class=p>i</span> = <span class=n>0</span>; <span class=p>i</span> &lt; <span class=n>3</span>; <span class=hle style=--a:37.4s>&nbsp;?&nbsp;</span>) {", "for (let i = 0; i < 3;  ?  ) {")}</div>'
         f'<div class="ln">  <span class="f">console</span>.<span class="f">log</span>(<span class="s">"Салом"</span>);</div><div class="ln">}}</div>')
qcards = "".join(f'<div class="card pop" style="--a:{37.0 + k * 0.4:.2f}s;left:{30 + k * 165}px;width:150px;top:300px;text-align:center;padding:14px 0"><div style="font:900 34px var(--mono);color:var(--purple)">{lab}</div><div style="font:700 13px Inter;color:var(--text);margin-top:4px">{sub}</div></div>' for k, (lab, sub) in enumerate([("3", "бор"), ("0", "ҳеҷ чиз"), ("♾️", "бепоён")]))
for k in range(3): sfx("pop", 37.0 + k * 0.4, 0.7)
scene(35.0, 41.0, f'''
<div class="ide" style="top:112px"><div class="bar"><i></i><i></i><i></i><span>test.js</span></div><div class="code" style="font-size:16px">{code5}</div></div>{qcards}
<div class="pill ok pop" style="--a:39.0s;top:400px">💬 ҷавобро дар шарҳ нависед</div>''')
cap(35.0, 41.0, "Агар <em>i++</em> набошад, чӣ мешавад?", True)
sfx("hit", 35.1, 0.6); sfx("tick2", 37.4, 0.4); sfx("pop", 39.0, 0.6)

# ===== САҲНАИ 6: даъват (41..END) =====
scene(41.0, END + 5, f'''
<div class="kicker" style="top:104px">ШАРҲ → DIRECT</div>
<div class="card pop" style="--a:41.2s;left:40px;right:40px;top:126px;display:flex;align-items:center;gap:14px;padding:8px 16px">
 <div style="width:34px;height:34px;border-radius:50%;background:var(--accent)"></div>
 <div style="flex:1;background:#1E1E1E;border:1px solid var(--line);border-radius:999px;padding:9px 16px;font:700 16px var(--mono);color:var(--white)">{TYP(41.4, 0.7, "ДАВР", "ДАВР")}</div>
 <div style="font-weight:800;color:var(--purple)">➤</div></div>
<div class="card pop" style="--a:42.4s;left:40px;right:40px;top:188px;padding:0;overflow:hidden">
 <div style="height:96px;background:linear-gradient(135deg,#2a1f45,#1E1E1E);display:flex;align-items:center;justify-content:center"><div style="width:62px;height:44px;border-radius:12px;background:#F4443C;color:#fff;font-size:22px;line-height:44px;text-align:center">▶</div></div>
 <div style="padding:10px 18px"><div style="font:800 17px Inter;color:var(--white)">Давр (for) аз сифр</div><div style="font:600 12px Inter;color:var(--muted);margin-top:3px">видеои пурраи дарс · YouTube</div></div></div>
<div class="pill acc2 pop" style="--a:43.4s;top:356px;font-size:15px">✉ ба Direct мефиристам</div>
<div class="pill acc2 pop" style="--a:44.6s;top:398px;font-size:17px;padding:8px 24px">🔔 Обуна шавед</div>''')
cap(41.0, 44.2, "Калимаи <em>«ДАВР»</em> → видеои пурра дар Direct")
cap(44.2, END, "Обуна шавед — ҳар ҳафта дарси нав 🚀")
sfx("pop", 41.2, 0.6); sfx("pop", 42.4, 0.7); sfx("chime", 43.4, 0.7); sfx("ding", 44.6, 0.6)

html = f'''<!doctype html><html lang="tg"><head><meta charset="utf-8"><link rel="stylesheet" href="style.css"><style>@keyframes slidein{{to{{translate:140px 0;opacity:0}}}}</style></head><body>
{"".join(H)}
</body></html>'''
open('reel.html', 'w', encoding='utf-8').write(html)
json.dump(dict(end=END, sfx=SFX), open('sfx.json', 'w'))
print('END', END, 'sfx', len(SFX))
