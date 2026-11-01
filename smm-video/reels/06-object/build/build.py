# Ролик «Объект» — стили «VS Code Dark + бунафш». Тайминг: timelineA.json.
import json, re
TL = json.load(open('timelineA.json')); SN = TL['sentences']; PRE = TL['pre']
TOTAL = TL['total']; END = round(TOTAL + 1.2, 2)
T = [s['start'] for s in SN]
V = set("аеёиоуэюяӣӯ")
def norm(w): return re.sub(r'[^\w-]', '', w).lower()
def WT(i, prefix, nth=0, src=None):
    ws = (src or SN[i])['words']
    return [w for w in ws if norm(w['w']).startswith(prefix.lower())][nth]['t0']
f = lambda x: f"{x:.2f}s"
def S(a, b=None): return f"--a:{a:.2f}s;--b:{(b if b is not None else END + 5):.2f}s"

# ---------- субтитры ----------
KW = {"объект", "объект!", "ном", "қимат", "person", "шиноснома", "санҷиш", "age", "name"}
def syl(w):
    n = sum(c in V for c in w.lower()); return max(1, n if n else len(re.sub(r'\W', '', w)) // 3 or 1)
capw = []
for s in PRE + SN:
    sid = s['i'] if s in SN else -1 - PRE.index(s)
    if s['text'] == s['tts']:
        capw += [(w['w'], w['t0'], w['t1'], sid) for w in s['words']]
    else:
        ws = s['text'].split(); n = [syl(w) for w in ws]; Nn = sum(n); c = 0
        for k, w in enumerate(ws):
            a = s['start'] + (s['end'] - s['start']) * c / Nn; c += n[k]
            b = s['start'] + (s['end'] - s['start']) * c / Nn
            capw.append((w, a, b, sid))
chunks = []; cur = []
for x in capw:
    if cur and cur[-1][3] != x[3]: chunks.append(cur); cur = []
    cur.append(x); txt = " ".join(y[0] for y in cur)
    if len(cur) >= 3 or len(txt) >= 17 or re.search(r'[,.:!?—»…]$', x[0]): chunks.append(cur); cur = []
if cur: chunks.append(cur)
cap_html = []
for k, ch in enumerate(chunks):
    a = ch[0][1]; nxt = chunks[k + 1][0][1] if k + 1 < len(chunks) else END
    b = nxt if (k + 1 < len(chunks) and chunks[k + 1][0][3] == ch[0][3]) else min(nxt, ch[-1][2] + 0.25)
    words = []
    for j, (w, wa, wb, _) in enumerate(ch):
        w2 = w.replace("«", "").replace("»", "").replace("<", "&lt;")
        kw = " kwd" if norm(w2).strip('!?') in KW else ""
        w1 = ch[j + 1][1] if j + 1 < len(ch) else b
        words.append(f'<span class="w{kw}" style="--w:{wa:.2f}s;--w1:{w1:.2f}s">{w2}</span>')
    cap_html.append(f'<div class="cap" style="--a:{a:.2f}s;--b:{max(b, a + 0.05):.2f}s"><span>{" ".join(words)}</span></div>')

# ---------- звук ----------
SFX = []
def sfx(name, at, gain=1.0): SFX.append(dict(name=name, t=round(at, 3), gain=gain))
def typing(at, dur, raw, gain=0.5):
    n = len(raw); step = dur / max(1, n)
    for k, ch in enumerate(raw):
        if ch != " ": sfx("key", at + k * step, gain)
def TYP(at, dur, html, raw):
    typing(at, dur, raw)
    return f'<span class="type" style="--a:{at:.2f}s;--d:{dur:.2f}s;--n:{len(raw)}">{html}</span>'
H = []
def scene(a, b, body, whoosh=True):
    H.append(f'<div class="sc" style="{S(a, b)}">{body}</div>')
    if whoosh: sfx("whoosh", a - 0.05, 0.45)

# ===== ХУК: 10 тағйирёбанда → як объект =====
p0, p1 = PRE
t_one = WT(0, "як", 1, p0)
names = ["name", "age", "city", "job", "phone", "email", "height", "weight", "hobby", "id"]
vals = ['"Алӣ"', '25', '"Душанбе"', '"IT"', '"+992…"', '"ali@…"', '178', '70', '"футбол"', '1']
rows = ""; step = (t_one - 0.8) / 10
for k in range(10):
    rows += f'<div class="ln fade" style="--a:{0.3 + k * step:.2f}s"><span class="k">let</span> <span class="p">{names[k]}</span> = <span class="{"n" if not vals[k].startswith(chr(34)) else "s"}">{vals[k]}</span>;</div>'
    sfx("key", 0.3 + k * step, 0.5)
    if k % 2 == 0: sfx("tick", 0.3 + k * step, 0.5)
obj_code = ('<div class="ln"><span class="k">let</span> <span class="p">person</span> = {</div>'
            '<div class="ln">  <span class="p">name</span>: <span class="s">"Алӣ"</span>,</div>'
            '<div class="ln">  <span class="p">age</span>: <span class="n">25</span>,</div>'
            '<div class="ln">  <span class="p">city</span>: <span class="s">"Душанбе"</span></div>'
            '<div class="ln">};</div>')
scene(0, T[0] - 0.1, f'''
<div class="kicker" style="top:100px">ДАРСИ 6 · ОБЪЕКТ</div>
<div class="ide gone" style="--g:{t_one - 0.05:.2f}s;top:135px"><div class="bar"><i></i><i></i><i></i><span>odam.js</span></div><div class="code" style="font-size:13.5px;line-height:1.5;padding-top:8px"><div style="line-height:1.5">{rows}</div></div></div>
<div class="pill err fade gone" style="--a:0.6s;--g:{t_one - 0.05:.2f}s;top:520px">10 тағйирёбанда 😵</div>
<div class="ide pop" style="--a:{t_one + 0.05:.2f}s;top:135px"><div class="bar"><i></i><i></i><i></i><span>object.js</span></div><div class="code" style="font-size:16px">{obj_code}</div></div>
<div class="pill ok pop" style="--a:{t_one + 0.2:.2f}s;top:360px">1 объект ✅</div>
<div class="pill acc2 pop" style="--a:{p1['start']:.2f}s;top:470px;font-size:22px;padding:11px 26px">Чӣ тавр? 🤔</div>''', whoosh=False)
sfx("hit", 0.0, 0.8); sfx("chime", t_one + 0.1, 0.8); sfx("thump", t_one + 0.05, 0.6); sfx("pop", p1['start'], 0.8)

# ===== ШИНОСНОМА (T0..T2) =====
t_nom, t_sin, t_sha, t_kor = WT(1, "ном"), WT(1, "синну"), WT(1, "шаҳр"), WT(1, "корт", 0)
scene(T[0] - 0.1, T[2] - 0.1, f'''
<div class="slam acc" style="--a:{T[0]:.2f}s;top:100px;font-size:62px">ОБЪЕКТ!</div>
<div class="idc pop" style="--a:{T[1] + 0.2:.2f}s;top:230px"><div class="hd">ШИНОСНОМА</div>
 <div class="bd"><div class="av">🙂</div><div style="flex:1">
  <div class="row fade" style="--a:{t_nom:.2f}s"><small>НОМ</small><b>Алӣ</b></div>
  <div class="row fade" style="--a:{t_sin:.2f}s"><small>СИННУ СОЛ</small><b>25</b></div>
  <div class="row fade" style="--a:{t_sha:.2f}s"><small>ШАҲР</small><b>Душанбе</b></div></div></div></div>
<div class="pill ok pop" style="--a:{t_kor:.2f}s;top:480px">ҳама дар як корт 🪪</div>''')
sfx("hit", T[0], 0.9); sfx("pop", T[1] + 0.2, 0.7)
for t_ in (t_nom, t_sin, t_sha): sfx("pop", t_, 0.6)
sfx("chime", t_kor, 0.6)

# ===== ДАР БАРНОМАСОЗӢ: калид + қимат (T2..T4) =====
t_q = WT(3, "қимат"); t_n = WT(3, "ном")
scene(T[2] - 0.1, T[4] - 0.1, f'''
<div class="kicker" style="top:140px">ДАР БАРНОМАСОЗӢ ҲАМ</div>
<div class="card pop" style="--a:{T[2] + 0.1:.2f}s;left:50px;right:50px;top:190px;text-align:center;padding:24px">
 <div style="font:600 26px/1.6 var(--mono)"><span style="color:var(--purple)">{{</span><br>
 <span class="p hlt" style="--a:{t_n + 0.1:.2f}s;--b:{END + 5:.2f}s">name</span>: <span class="s hlt" style="--a:{t_q + 0.1:.2f}s;--b:{END + 5:.2f}s">"Алӣ"</span><br><span style="color:var(--purple)">}}</span></div></div>
<div class="pill pop" style="--a:{t_n + 0.1:.2f}s;top:420px;border-color:var(--par);color:var(--par)">name = ном (калид)</div>
<div class="pill pop" style="--a:{t_q + 0.1:.2f}s;top:475px;border-color:var(--str);color:var(--str)">"Алӣ" = қимат</div>
<div class="pill acc2 pop" style="--a:{t_n + 0.45:.2f}s;top:530px">ҳар қимат — бо ном</div>''')
sfx("pop", T[2] + 0.1, 0.7); sfx("pop", t_n + 0.1, 0.7); sfx("pop", t_q + 0.1, 0.7); sfx("chime", t_n + 0.5, 0.6)

# ===== КОД + РӮЙХАТ vs ОБЪЕКТ + НУҚТА + ИВАЗ (T4..T11) =====
t_nm, t_ag, t_ci = WT(4, "нейм"), WT(4, "эйдж"), WT(4, "сити")
r1 = 'let person = {'; r2 = '  name: "Алӣ",'; r3 = '  age: 25,'; r4 = '  city: "Душанбе"'; r5 = '};'
h1 = '<span class="k">let</span> <span class="p">person</span> = {'
t_n8 = WT(8, "нейм"); t_a9 = WT(9, "эйдж"); t_a10 = WT(10, "эйдж"); t_sh = WT(10, "шаш")
t_alii = WT(8, "алӣ"); t_25 = WT(9, "бисту")
h2 = f'  <span class="p hlt" style="--a:{t_n8:.2f}s;--b:{t_a9 - 0.1:.2f}s">name</span>: <span class="s">"Алӣ"</span>,'
h3 = f'  <span class="p hlt" style="--a:{t_a9:.2f}s;--b:{T[10] - 0.1:.2f}s">age</span>: <span class="n hlt" style="--a:{T[10] + 0.1:.2f}s;--b:{END + 5:.2f}s">25</span>,'
h4 = '  <span class="p">city</span>: <span class="s">"Душанбе"</span>'
code_html = (f'<div class="ln">{TYP(T[4] + 0.05, max(0.6, t_nm - T[4] - 0.4), h1, r1)}</div>'
             f'<div class="ln">{TYP(t_nm, 0.5, h2, r2)}</div>'
             f'<div class="ln">{TYP(t_ag, 0.4, h3, r3)}</div>'
             f'<div class="ln">{TYP(t_ci, 0.6, h4, r4)}</div>'
             f'<div class="ln">{TYP(t_ci + 0.7, 0.15, "};", r5)}</div>')
term = (f'<div class="term abs" style="left:20px;right:20px;top:332px;border-radius:12px;border:1px solid var(--line);animation:fadein .2s var(--a) both,gone .2s var(--g) forwards;--a:{T[8]:.2f}s;--g:{T[10] - 0.05:.2f}s">'
        f'<div class="ln"><span class="pr">$ </span>{TYP(T[8] + 0.05, max(0.5, t_alii - T[8] - 0.5), "<span class=p>person</span>.<span class=p>name</span>", "person.name")}</div><span class="out" style="--a:{t_alii:.2f}s">Алӣ</span>'
        f'<div class="ln"><span class="pr">$ </span>{TYP(T[9] + 0.05, max(0.5, t_25 - T[9] - 0.4), "<span class=p>person</span>.<span class=p>age</span>", "person.age")}</div><span class="out" style="--a:{t_25 + 0.2:.2f}s">25</span></div>')
sfx("ding", t_alii + 0.05, 0.6); sfx("ding", t_25 + 0.25, 0.6)
cmp_ = (f'<div class="card" style="animation:popin .45s cubic-bezier(.3,1.6,.5,1) {f(T[5])} both,gone .25s ease-in {f(T[8] - 0.05)} forwards;left:20px;width:250px;top:345px;text-align:center"><div style="font:800 11px var(--mono);letter-spacing:2px;color:var(--muted)">РӮЙХАТ</div><div style="font:700 17px var(--mono);margin:8px 0;color:var(--kw)">[0] [1] [2]</div><div style="font:700 15px Inter;color:var(--white)">бо шумора</div></div>'
        f'<div class="card" style="animation:popin .45s cubic-bezier(.3,1.6,.5,1) {f(T[7] + 0.3)} both,gone .25s ease-in {f(T[8] - 0.05)} forwards;right:20px;width:250px;top:345px;text-align:center;border-color:var(--purple)"><div style="font:800 11px var(--mono);letter-spacing:2px;color:var(--purple)">ОБЪЕКТ</div><div style="font:700 17px var(--mono);margin:8px 0;color:var(--par)">name age city</div><div style="font:700 15px Inter;color:var(--white)">бо ном</div></div>')
sfx("pop", T[5], 0.7); sfx("pop", T[7] + 0.3, 0.8)
edit = (f'<div class="box pop" style="--a:{T[10]:.2f}s;left:210px;top:350px"><div class="tag">age</div>'
        f'<div class="num" style="position:relative;height:40px;width:100px;text-align:center"><span class="abs" style="left:0;right:0;animation:gone .2s ease-in {f(t_sh)} forwards">25</span><span class="abs pop" style="left:0;right:0;--a:{t_sh + 0.05:.2f}s;color:#7a2d00">26</span></div></div>'
        f'<div class="pill pop" style="--a:{T[10] + 0.3:.2f}s;top:490px;font:700 17px var(--mono)"><span class="p">person</span>.<span class="p">age</span> = <span class="n">26</span></div>')
sfx("pop", T[10], 0.8); sfx("ding", t_sh + 0.05, 0.8); sfx("chime", t_sh + 0.1, 0.6)
scene(T[4] - 0.1, T[11] - 0.1, f'''
<div class="kicker" style="top:100px">ОБЪЕКТ</div>
<div class="ide" style="top:135px"><div class="bar"><i></i><i></i><i></i><span>object.js</span></div><div class="code" style="font-size:16px">{code_html}</div></div>
{cmp_}{term}{edit}''')

# ===== ДАР ҲАЁТ (T11..T12) =====
items = [("📸", "профили Instagram", "profile = { name, posts }", WT(11, "профили")), ("🚗", "мошин", "car = { brand, year }", WT(11, "мошин")), ("🛒", "мағоза", "shop = { name, items }", WT(11, "мағоза"))]
cards = ""
for k, (e, n, c, ti) in enumerate(items):
    cards += f'<div class="card pop" style="--a:{ti:.2f}s;left:40px;right:40px;top:{190 + k * 115}px;display:flex;align-items:center;gap:18px"><span class="emo" style="font-size:42px">{e}</span><div><div style="font:800 21px Inter;color:var(--white)">{n}</div><div style="font:700 13px var(--mono);color:var(--par);margin-top:4px">{c}</div></div></div>'
    sfx("pop", ti, 0.7)
scene(T[11] - 0.1, T[12] - 0.1, f'<div class="kicker" style="top:138px">ОБЪЕКТ ҲАМА ҶО ҲАСТ</div>{cards}')

# ===== ХУЛОСА (T12..T13) =====
scene(T[12] - 0.1, T[13] - 0.1, f'''
<div class="kicker" style="top:170px">ХУЛОСА</div>
<div class="h1 pop" style="--a:{T[12] + 0.05:.2f}s;top:215px;font-size:50px">ОБЪЕКТ</div>
<div class="h1 acc pop" style="--a:{WT(12, 'маълумот'):.2f}s;top:285px;font-size:40px">= ном + қимат</div>
<div class="card pop" style="--a:{WT(12, 'шиноснома'):.2f}s;left:50px;right:50px;top:390px;text-align:center;font:700 20px Inter;color:var(--white)">🪪 шиноснома барои барнома</div>
<div class="card pop" style="--a:{WT(12, 'ном', 0):.2f}s;left:50px;right:50px;top:465px;text-align:center;font:700 18px Inter;color:var(--white)">маълумот бо ном ва қимат</div>''')
sfx("hit", T[12] + 0.05, 0.7); sfx("pop", WT(12, 'маълумот'), 0.7); sfx("pop", WT(12, 'шиноснома'), 0.6); sfx("chime", WT(12, 'ном', 0) + .3, 0.6)

# ===== САНҶИШ (T13..T17) =====
t_c = WT(15, "чӣ")
q1 = 'let person = { name: "Алӣ", age: 25 };'; q2 = 'person.age = 30;'; q3 = 'console.log(person.name, person.age);'
hq1 = '<span class="k">let</span> <span class="p">person</span> = { <span class="p">name</span>: <span class="s">"Алӣ"</span>, <span class="p">age</span>: <span class="n">25</span> };'
hq2 = '<span class="p">person</span>.<span class="p">age</span> = <span class="n">30</span>;'
hq3 = '<span class="f">console</span>.<span class="f">log</span>(<span class="p">person</span>.<span class="p">name</span>, <span class="p">person</span>.<span class="p">age</span>);'
scene(T[13] - 0.1, T[17] - 0.1, f'''
<div class="kicker" style="top:140px">САНҶИШ</div>
<div class="h1 pop" style="--a:{T[13] + 0.05:.2f}s;top:175px;font-size:40px">чӣ чоп мешавад?</div>
<div class="ide" style="top:250px;left:12px;right:12px"><div class="bar"><i></i><i></i><i></i><span>test.js</span></div>
<div class="code" style="font-size:16px"><div class="ln">{TYP(T[13] + 0.1, 2.4, hq1, q1)}</div><div class="ln">{TYP(T[14] + 0.05, 1.6, hq2, q2)}</div><div class="ln">{TYP(T[15] + 0.05, 3.0, hq3, q3)}</div></div></div>
<div class="h1 acc pop" style="--a:{t_c:.2f}s;top:420px;font-size:110px">?</div>
<div class="pill ok pop" style="--a:{T[16]:.2f}s;top:600px">💬 ҷавобро дар шарҳ нависед</div>''')
sfx("hit", T[13] + 0.05, 0.7); sfx("pop", t_c, 0.8); sfx("tick2", t_c, 0.5); sfx("pop", T[16], 0.6)

# ===== ДАЪВАТ БА ШАРҲ (T17..T18) =====
t_vid = WT(17, "видео"); t_dir = WT(17, "директ")
kw_raw = "ОБЪЕКТ"
scene(T[17] - 0.1, T[18] - 0.1, f'''
<div class="kicker" style="top:140px">ШАРҲ → DIRECT</div>
<div class="card pop" style="--a:{T[17] + 0.05:.2f}s;left:40px;right:40px;top:190px;display:flex;align-items:center;gap:14px">
 <div style="width:38px;height:38px;border-radius:50%;background:var(--accent)"></div>
 <div style="flex:1;background:#1E1E1E;border:1px solid var(--line);border-radius:999px;padding:11px 16px;font:700 17px var(--mono);color:var(--white)">{TYP(T[17] + 0.15, 1.0, kw_raw, kw_raw)}</div>
 <div style="font-weight:800;color:var(--purple)">➤</div></div>
<div class="card pop" style="--a:{t_vid:.2f}s;left:40px;right:40px;top:300px;padding:0;overflow:hidden">
 <div style="height:170px;background:linear-gradient(135deg,#2a1f45,#1E1E1E);display:flex;align-items:center;justify-content:center"><div style="width:68px;height:48px;border-radius:12px;background:#F4443C;color:#fff;font-size:24px;line-height:48px;text-align:center">▶</div></div>
 <div style="padding:12px 18px"><div style="font:800 18px Inter;color:var(--white)">Дарси 6: Объект</div><div style="font:600 13px Inter;color:var(--muted);margin-top:3px">видеои пурраи дарс · YouTube</div></div></div>
<div class="pill acc2 pop" style="--a:{t_dir:.2f}s;top:520px">✉ ба Direct мефиристам</div>''')
sfx("pop", T[17] + 0.05, 0.7); sfx("pop", t_vid, 0.7); sfx("chime", t_dir, 0.8); sfx("ding", t_dir + 0.1, 0.5)

# ===== ДАРСИ ОЯНДА (T18..END) =====
t_sub = SN[19]['start'] + 0.1
scene(T[18] - 0.1, END + 5, f'''
<div class="kicker" style="top:140px">ДАРСИ ОЯНДА</div>
<div class="h1 pop" style="--a:{T[18] + 0.05:.2f}s;top:180px;font-size:58px">7 · <span class="acc">Хатогӣ</span></div>
<div class="ide pop" style="--a:{WT(18, 'хатогиҳоро'):.2f}s;top:290px"><div class="bar"><i></i><i></i><i></i><span>bug.js</span></div>
<div class="code" style="font-size:15px"><div class="ln"><span class="k">let</span> <span class="p">age</span> = <span class="s">"25"</span> + <span class="n">1</span>;</div><div class="ln"><span class="f">console</span>.<span class="f">log</span>(<span class="p">age</span>); <span class="cm">// 251 😱</span></div></div></div>
<div class="pill acc2 pop" style="--a:{t_sub:.2f}s;top:470px;font-size:20px;padding:12px 30px">🔔 Обуна шавед</div>''')
sfx("hit", T[18] + 0.05, 0.7); sfx("pop", WT(18, 'хатогиҳоро'), 0.7); sfx("pop", t_sub, 0.8); sfx("ding", t_sub + 0.1, 0.6)

html = f'''<!doctype html><html lang="tg"><head><meta charset="utf-8"><link rel="stylesheet" href="style.css"></head><body>
{"".join(H)}
{"".join(cap_html)}
</body></html>'''
open('reel.html', 'w', encoding='utf-8').write(html)
json.dump(dict(end=END, sfx=SFX), open('sfx.json', 'w'))
print('END', END, 'sfx', len(SFX), 'captions', len(cap_html))
