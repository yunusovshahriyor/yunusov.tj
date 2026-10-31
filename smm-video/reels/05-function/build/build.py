# Ролик «Функсия» — стили «VS Code Dark + бунафш». Тайминг: timeline.json (ElevenLabs with-timestamps → prep.py).
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

# ---------- субтитры (калима ба калима) ----------
KW = {"функсия", "функсия!", "мошин", "return", "тугма", "name", "age", "birthday", "санҷиш", "либос", "код"}
def syl(w):
    n = sum(c in V for c in w.lower()); return max(1, n if n else len(re.sub(r'\W', '', w)) // 3 or 1)
capw = []
for s in PRE + SN:
    if s['text'] == s['tts']:
        capw += [(w['w'], w['t0'], w['t1'], s['i'] if s in SN else -1 - PRE.index(s)) for w in s['words']]
    else:
        ws = s['text'].split(); n = [syl(w) for w in ws]; Nn = sum(n); c = 0
        sid = s['i'] if s in SN else -1 - PRE.index(s)
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
# заголовок (шапка)
hdr = '<div class="hdr"><span>ШАҲРИЁР ЮНУСОВ · <b>05</b> / БАРНОМАСОЗӢ</span><span>ДАРСИ <b>5</b> / 12</span></div>'

def scene(a, b, body, whoosh=True):
    H.append(f'<div class="sc" style="{S(a, b)}">{body}</div>')
    if whoosh: sfx("whoosh", a - 0.05, 0.45)

# ===== ХУК: 10 маротиба навиштан → як функсия =====
p0, p1 = PRE
t_one = WT(0, "як", 1, p0); t_use = WT(0, "истифода", 0, p0)
LINE = '<span class="f">console</span>.<span class="f">log</span>(<span class="s">"Салом, Алӣ!"</span>);'
rows = ""; step = (t_one - 0.7) / 10
for k in range(10):
    rows += f'<div class="ln fade" style="--a:{0.3 + k * step:.2f}s">{LINE}</div>'
    sfx("key", 0.3 + k * step, 0.5)
    if k % 2 == 0: sfx("tick", 0.3 + k * step, 0.5)
fn_code = ('<div class="ln"><span class="k">function</span> <span class="f">greet</span>(<span class="p">name</span>) {</div>'
           '<div class="ln">  <span class="f">console</span>.<span class="f">log</span>(<span class="s">"Салом, "</span> + <span class="p">name</span>);</div>'
           '<div class="ln">}</div>')
chips = "".join(f'<div class="abs pop" style="--a:{t_use + 0.05 + k * 0.1:.2f}s;left:{20 + (k % 5) * 100}px;top:{455 + (k // 5) * 44}px;width:92px;text-align:center;background:var(--panel2);border:1px solid var(--line);border-radius:10px;padding:7px 0;font:700 13px var(--mono);color:var(--fn)">greet()</div>' for k in range(10))
for k in range(10): sfx("pop", t_use + 0.05 + k * 0.1, 0.45)
scene(0, T[0] - 0.1, f'''{hdr}
<div class="kicker" style="top:104px">ДАРСИ 5 · ФУНКСИЯ</div>
<div class="ide gone" style="--g:{t_one - 0.05:.2f}s;top:140px"><div class="bar"><i></i><i></i><i></i><span>takror.js</span></div><div class="code" style="font-size:14.5px;padding-top:10px">{rows}</div></div>
<div class="pill err fade gone" style="--a:{0.5:.2f}s;--g:{t_one - 0.05:.2f}s;top:520px">× 10 — аз нав ва аз нав 😵</div>
<div class="ide pop" style="--a:{t_one + 0.05:.2f}s;top:140px"><div class="bar"><i></i><i></i><i></i><span>function.js</span></div><div class="code" style="font-size:15px">{fn_code}</div></div>
<div class="pill ok pop" style="--a:{t_one + 0.15:.2f}s;top:290px">1 бор менависем ✍</div>
{chips}
<div class="pill acc2 pop" style="--a:{p1['start']:.2f}s;top:570px;font-size:22px;padding:11px 26px">Чӣ тавр? 🤔</div>''', whoosh=False)
sfx("hit", 0.0, 0.8); sfx("chime", t_one + 0.1, 0.8); sfx("pop", p1['start'], 0.8)

# ===== МОШИНИ ЛИБОСШӮЙӢ (T0..T5) =====
t_cloth = WT(2, "либос"); t_in = WT(2, "мегузор"); t_press = WT(2, "пахш"); t_wash = WT(2, "мешӯ")
t_q = T[3]; t_btn = T[4]
mach = f'''<div class="mach" style="left:195px;top:300px"><div class="top"><i></i><i></i><i></i></div>
  <div class="win idle"></div><div class="win run fade" style="--a:{t_wash:.2f}s"></div>
  <div class="abs fade" style="--a:{t_q + 0.1:.2f}s;left:25px;top:48px;width:100px;height:100px;border-radius:50%;background:rgba(30,30,30,.88);color:var(--purple);font:900 54px/100px var(--mono);text-align:center">?</div>
</div>
<div class="btn press" style="--a:{t_press:.2f}s;left:248px;top:466px">▶</div>
<div class="btn press" style="--a:{t_btn:.2f}s;left:248px;top:466px"></div><div class="btn press" style="--a:{t_btn + 0.6:.2f}s;left:248px;top:466px"></div>'''
cloth_in = f'<div class="abs emo pop" style="--a:{t_cloth:.2f}s;left:50px;top:360px;font-size:62px;animation:popin .45s cubic-bezier(.3,1.6,.5,1) {f(t_cloth)} both,slidein .5s ease-in {f(t_in)} forwards">👕</div>'
clean = f'<div class="abs emo pop" style="--a:{t_wash + 1.0:.2f}s;left:370px;top:360px;font-size:62px">✨👕</div>'
scene(T[0] - 0.1, T[5] - 0.1, f'''{hdr}
<div class="slam acc" style="--a:{T[0]:.2f}s;top:110px;font-size:62px">ФУНКСИЯ!</div>
{cloth_in}{mach}{clean}
<div class="pill pop" style="--a:{t_cloth:.2f}s;top:560px;font-size:14px;left:-300px;right:0;margin:0 0 0 40px;width:max-content;background:transparent;border:0;color:var(--muted)">👕 либос</div>
<div class="pill fade" style="--a:{t_q + 0.15:.2f}s;top:560px;border-color:var(--purple);color:var(--white)">🙈 дарунаш чӣ — донистан лозим нест</div>
<div class="pill ok fade" style="--a:{t_btn:.2f}s;top:610px">ҳар дафъа — ҳамон як тугма</div>''')
H.insert(0, '<style>@keyframes slidein{to{translate:140px 0;opacity:0;scale:.5}}</style>')
sfx("hit", T[0], 0.9); sfx("pop", t_cloth, 0.7); sfx("whoosh", t_in, 0.5); sfx("click", t_press, 0.9); sfx("pop", t_press, 0.5)
sfx("riser", t_wash - 0.2, 0.3); sfx("ding", t_wash + 1.0, 0.7); sfx("buzz", t_q + 0.1, 0.5)
sfx("click", t_btn, 0.7); sfx("click", t_btn + 0.6, 0.7)

# ===== ДАР БАРНОМАСОЗӢ ҲАМ ҲАМИН ТАВР (T5..T7) =====
t_name = WT(6, "ном")
scene(T[5] - 0.1, T[7] - 0.1, f'''{hdr}
<div class="kicker" style="top:140px">ДАР БАРНОМАСОЗӢ ҲАМ</div>
<div class="card pop" style="--a:{T[5] + 0.1:.2f}s;left:50px;right:50px;top:200px;text-align:center;padding:26px">
 <div style="font:900 34px var(--mono);color:var(--fn)">greet</div>
 <div style="font:600 14px var(--mono);color:var(--muted);margin:2px 0 14px">← ном</div>
 <div style="font:600 24px/1.6 var(--mono);color:var(--text)"><span style="color:var(--purple)">{{</span><br><span class="cm">  якчанд сатри код</span><br><span style="color:var(--purple)">}}</span></div></div>
<div class="pill acc2 pop" style="--a:{t_name:.2f}s;top:490px;font-size:18px">функсия = код + ном</div>''')
sfx("pop", T[5] + 0.1, 0.7); sfx("pop", t_name, 0.7); sfx("chime", t_name + 0.2, 0.6)

# ===== КОД: function greet (T7..T14) =====
r1 = 'function greet(name) {'
d1 = max(0.9, T[8] - T[7] - 0.5)
html1 = f'<span class="k">function</span> <span class="f">greet</span>(<span class="p hlm" style="--a:{T[13] + 0.1:.2f}s">name</span>) {{'
t1 = TYP(T[7] + 0.05, d1, html1, r1)
r2 = '  console.log("Салом, " + name);'
d2 = max(0.9, T[9] - T[8] - 0.5)
html2 = '  <span class="f">console</span>.<span class="f">log</span>(<span class="s">"Салом, "</span> + <span class="p">name</span>);'
t2 = TYP(T[8] + 0.05, d2, html2, r2)
t3 = TYP(T[9] + 0.05, 0.2, '}', '}')
r4 = 'greet("Алӣ")'; r5 = 'greet("Мариям")'
d4 = max(0.6, WT(10, "салом") - T[10] - 0.7); d5 = max(0.6, WT(11, "салом") - T[11] - 0.5)
html4 = '<span class="f">greet</span>(<span class="s">"Алӣ"</span>)'; html5 = '<span class="f">greet</span>(<span class="s">"Мариям"</span>)'
t4 = TYP(WT(10, "грит"), d4, html4, r4)
t5 = TYP(WT(11, "грит") + 0.0, d5, html5, r5)
o1 = WT(10, "салом"); o2 = WT(11, "салом")
sfx("ding", o1 + 0.05, 0.6); sfx("ding", o2 + 0.05, 0.6)
scene(T[7] - 0.1, T[14] - 0.1, f'''{hdr}
<div class="kicker" style="top:108px">ДАР IDE</div>
<div class="ide" style="top:140px"><div class="bar"><i></i><i></i><i></i><span>function.js</span></div>
<div class="code"><div class="ln">{t1}</div><div class="ln">{t2}</div><div class="ln">{t3}</div></div>
<div class="term"><div class="ln"><span class="pr">$ </span>{t4}</div><span class="out" style="--a:{o1:.2f}s">Салом, Алӣ!</span>
<div class="ln"><span class="pr">$ </span>{t5}</div><span class="out" style="--a:{o2:.2f}s">Салом, Мариям!</span></div></div>
<div class="pill pop" style="--a:{T[9] + 0.25:.2f}s;top:440px;border-color:var(--str)">⏸ сохта шуд — ҳанӯз иҷро нашудааст</div>
<div class="pill ok pop" style="--a:{WT(10, 'даъват'):.2f}s;top:500px">▶ даъват = иҷро</div>
<div class="pill acc2 pop" style="--a:{T[12] + 0.05:.2f}s;top:560px">1 функсия · 2 натиҷаи гуногун</div>
<div class="pill pop" style="--a:{T[13] + 0.1:.2f}s;top:620px;border-color:var(--purple)"><span class="p">name</span> = 👕 либос (ҷузъи хом)</div>''')
sfx("pop", T[9] + 0.25, 0.6); sfx("pop", T[12] + 0.05, 0.7); sfx("chime", T[12] + 0.1, 0.6); sfx("pop", T[13] + 0.1, 0.7); sfx("pop", WT(10, 'даъват'), 0.6)

# ===== RETURN + қуттии age (T14..T20) =====
t_ret = WT(15, "ритёрн"); t_box = T[16]; t_sw = WT(19, "шаш")
r6 = 'function birthday(age) {'; r7 = '  return age + 1;'; r8 = '}'; r9 = 'let age = 25;'; r10 = 'age = birthday(age);'
d6 = max(0.8, T[18] - T[17] - 1.2)
h6 = '<span class="k">function</span> <span class="f">birthday</span>(<span class="p">age</span>) {'
h7 = '  <span class="c">return</span> <span class="p">age</span> + <span class="n">1</span>;'
h9 = '<span class="k">let</span> <span class="p">age</span> = <span class="n">25</span>;'
h10 = '<span class="p">age</span> = <span class="f">birthday</span>(<span class="p">age</span>);'
tt6 = TYP(T[17] + 0.05, d6 * 0.5, h6, r6); tt7 = TYP(T[17] + 0.05 + d6 * 0.55, d6 * 0.45, h7, r7)
tt8 = TYP(T[17] + 0.05 + d6 + 0.05, 0.15, '}', r8)
tt9 = TYP(T[18] + 0.1, max(0.5, T[19] - T[18] - 0.9), h9, r9)
d10 = max(0.8, t_sw - T[19] - 0.5); tt10 = TYP(T[19] + 0.05, d10, h10, r10)
scene(T[14] - 0.1, T[20] - 0.1, f'''{hdr}
<div class="slam" style="--a:{t_ret:.2f}s;top:110px;font-size:50px;color:var(--ctrl)">return</div>
<div class="pill fade" style="--a:{T[14] + 0.1:.2f}s;top:175px;border-color:var(--ctrl)">функсия натиҷа бармегардонад ↩</div>
<div class="box pop" style="--a:{t_box:.2f}s;left:210px;top:225px"><div class="tag">age</div>
  <div class="num" style="position:relative;height:40px;width:100px;text-align:center"><span class="abs" style="left:0;right:0;animation:gone .2s ease-in {f(t_sw)} forwards">25</span><span class="abs pop" style="left:0;right:0;--a:{t_sw + 0.05:.2f}s;color:#7a2d00">26</span></div></div>
<div class="ide fade" style="--a:{T[17]:.2f}s;top:350px"><div class="bar"><i></i><i></i><i></i><span>birthday.js</span></div>
<div class="code"><div class="ln">{tt6}</div><div class="ln">{tt7}</div><div class="ln">{tt8}</div><div class="ln"> </div><div class="ln">{tt9}</div><div class="ln">{tt10}</div></div></div>
<div class="pill ok pop" style="--a:{t_sw + 0.1:.2f}s;top:610px">25 → 26 🎂</div>''')
sfx("hit", t_ret, 0.8); sfx("pop", t_box, 0.8); sfx("ding", t_sw + 0.05, 0.8); sfx("chime", t_sw + 0.1, 0.7)

# ===== ДАР ҲАЁТ (T20..T21) =====
items = [("👍", "лайк", "like()", WT(20, "лайк")), ("🔐", "воридшавӣ", "login()", WT(20, "ворид")), ("🛒", "ҳисоби нарх", "price()", WT(20, "нарх"))]
cards = ""
for k, (e, n, c, ti) in enumerate(items):
    cards += f'<div class="card pop" style="--a:{ti:.2f}s;left:40px;right:40px;top:{190 + k * 120}px;display:flex;align-items:center;gap:18px"><span class="emo" style="font-size:44px">{e}</span><div><div style="font:800 22px Inter;color:var(--white)">{n}</div><div style="font:700 15px var(--mono);color:var(--fn);margin-top:4px">{c}</div></div></div>'
    sfx("pop", ti, 0.7)
scene(T[20] - 0.1, T[21] - 0.1, f'<div>{hdr}</div><div class="kicker" style="top:138px">ФУНКСИЯ ҲАМА ҶО ҲАСТ</div>{cards}')

# ===== ХУЛОСА (T21..T22) =====
scene(T[21] - 0.1, T[22] - 0.1, f'''{hdr}
<div class="kicker" style="top:170px">ХУЛОСА</div>
<div class="h1 pop" style="--a:{T[21] + 0.05:.2f}s;top:215px;font-size:50px">ФУНКСИЯ</div>
<div class="h1 acc pop" style="--a:{WT(21, 'код'):.2f}s;top:285px;font-size:42px">= код бо ном</div>
<div class="card pop" style="--a:{WT(21, 'як'):.2f}s;left:50px;right:50px;top:395px;text-align:center;font:700 20px Inter;color:var(--white)">✍ як бор менависӣ</div>
<div class="card pop" style="--a:{WT(21, 'борҳо'):.2f}s;left:50px;right:50px;top:470px;text-align:center;font:700 20px Inter;color:var(--white)">▶ борҳо истифода мебарӣ</div>''')
sfx("hit", T[21] + 0.05, 0.7); sfx("pop", WT(21, 'код'), 0.7); sfx("pop", WT(21, 'як'), 0.6); sfx("pop", WT(21, 'борҳо'), 0.6); sfx("chime", WT(21, 'борҳо') + .3, 0.6)

# ===== САНҶИШ (T22..T26) =====
t_in2 = WT(24, "дохил")
scene(T[22] - 0.1, T[26] - 0.1, f'''{hdr}
<div class="kicker" style="top:150px">САНҶИШ</div>
<div class="h1 pop" style="--a:{T[22] + 0.05:.2f}s;top:185px;font-size:44px">чанд мешавад?</div>
<div class="ide pop" style="--a:{WT(23, 'аз'):.2f}s;top:270px"><div class="bar"><i></i><i></i><i></i><span>test.js</span></div>
<div class="code" style="font-size:19px;text-align:center"><span class="f">birthday</span>(<span class="hlm" style="--a:{t_in2:.2f}s"><span class="f">birthday</span>(<span class="n">25</span>)</span>)</div></div>
<div class="h1 acc pop" style="--a:{WT(23, 'чанд'):.2f}s;top:390px;font-size:110px">?</div>
<div class="pill pop" style="--a:{T[24] + 0.1:.2f}s;top:560px;border-color:var(--purple)">💡 аввал дохилӣ иҷро мешавад</div>
<div class="pill ok pop" style="--a:{T[25]:.2f}s;top:615px">💬 ҷавобро дар шарҳ нависед</div>''')
sfx("hit", T[22] + 0.05, 0.7); sfx("pop", WT(23, 'аз'), 0.6); sfx("pop", WT(23, 'чанд'), 0.8); sfx("tick2", t_in2, 0.6); sfx("pop", T[24] + 0.1, 0.6); sfx("pop", T[25], 0.6)

# ===== ДАЪВАТ БА ШАРҲ (T26..T27) =====
t_vid = WT(26, "видео"); t_dir = WT(26, "директ")
kw_raw = "ФУНКСИЯ"
scene(T[26] - 0.1, T[27] - 0.1, f'''{hdr}
<div class="kicker" style="top:140px">ШАРҲ → DIRECT</div>
<div class="card pop" style="--a:{T[26] + 0.05:.2f}s;left:40px;right:40px;top:190px;display:flex;align-items:center;gap:14px">
 <div style="width:38px;height:38px;border-radius:50%;background:var(--accent)"></div>
 <div style="flex:1;background:#1E1E1E;border:1px solid var(--line);border-radius:999px;padding:11px 16px;font:700 17px var(--mono);color:var(--white)">{TYP(T[26] + 0.15, 1.0, kw_raw, kw_raw)}</div>
 <div style="font-weight:800;color:var(--purple)">➤</div></div>
<div class="card pop" style="--a:{t_vid:.2f}s;left:40px;right:40px;top:300px;padding:0;overflow:hidden">
 <div style="height:170px;background:linear-gradient(135deg,#2a1f45,#1E1E1E);display:flex;align-items:center;justify-content:center"><div style="width:68px;height:48px;border-radius:12px;background:#F4443C;color:#fff;font-size:24px;line-height:48px;text-align:center">▶</div></div>
 <div style="padding:12px 18px"><div style="font:800 18px Inter;color:var(--white)">Дарси 5: Функсия</div><div style="font:600 13px Inter;color:var(--muted);margin-top:3px">видеои пурраи дарс · YouTube</div></div></div>
<div class="pill acc2 pop" style="--a:{t_dir:.2f}s;top:520px">✉ ба Direct мефиристам</div>''')
sfx("pop", T[26] + 0.05, 0.7); sfx("pop", t_vid, 0.7); sfx("chime", t_dir, 0.8); sfx("ding", t_dir + 0.1, 0.5)

# ===== ДАРСИ ОЯНДА (T27..END) =====
t_sub = SN[28]['start'] + 0.1
scene(T[27] - 0.1, END + 5, f'''{hdr}
<div class="kicker" style="top:140px">ДАРСИ ОЯНДА</div>
<div class="h1 pop" style="--a:{T[27] + 0.05:.2f}s;top:180px;font-size:58px">6 · <span class="acc">Объект</span></div>
<div class="ide pop" style="--a:{WT(27, 'шиноснома'):.2f}s;top:290px"><div class="bar"><i></i><i></i><i></i><span>object.js</span></div>
<div class="code" style="font-size:15.5px"><span class="k">let</span> <span class="p">cat</span> = {{
  <span class="p">name</span>: <span class="s">"Мурка"</span>,
  <span class="p">age</span>: <span class="n">3</span>
}};</div></div>
<div class="pill acc2 pop" style="--a:{t_sub:.2f}s;top:560px;font-size:20px;padding:12px 30px">🔔 Обуна шавед</div>''')
sfx("hit", T[27] + 0.05, 0.7); sfx("pop", WT(27, 'шиноснома'), 0.7); sfx("pop", t_sub, 0.8); sfx("ding", t_sub + 0.1, 0.6)

html = f'''<!doctype html><html lang="tg"><head><meta charset="utf-8"><link rel="stylesheet" href="style.css"></head><body>
{"".join(H)}
{"".join(cap_html)}
</body></html>'''
open('reel.html', 'w', encoding='utf-8').write(html)
json.dump(dict(end=END, sfx=SFX), open('sfx.json', 'w'))
print('END', END, 'sfx', len(SFX), 'captions', len(cap_html))
