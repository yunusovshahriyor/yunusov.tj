# Ролик «Рӯйхат (array)». Тайминги — из timelineA.json (точная разметка ElevenLabs v4).
import json, re
TL = json.load(open('timelineA.json')); SN = TL['sentences']; PRE = TL['pre']
TOTAL = TL['total']; END = round(TOTAL + 1.2, 2)
T = [s['start'] for s in SN]; E = [s['end'] for s in SN]
V = set("аеёиоуэюяӣӯ")
def norm(w): return re.sub(r'[^\w-]', '', w).lower()
def WT(i, prefix, nth=0):
    m = [w for w in SN[i]['words'] if norm(w['w']).startswith(prefix.lower())]
    return m[nth]['t0']
f = lambda x: f"{x:.2f}s"
def S(a, b=None): return f"--a:{a:.2f}s;--b:{(b if b is not None else END + 5):.2f}s"

KW = {"рӯйхат", "рӯйхат!", "array", "сифр", "шумора", "тағйирёбанда", "қуттӣ", "давр", "i", "fruits"}
def syl(w):
    n = sum(c in V for c in w.lower())
    return max(1, n if n else len(re.sub(r'\W', '', w)) // 3 or 1)
capw = []
for s in PRE + SN:
    if s['text'] == s['tts']:
        capw += [(w['w'], w['t0'], w['t1'], s['i']) for w in s['words']]
    else:
        ws = s['text'].split(); n = [syl(w) for w in ws]; N = sum(n); c = 0
        for k, w in enumerate(ws):
            a = s['start'] + (s['end'] - s['start']) * c / N; c += n[k]
            b = s['start'] + (s['end'] - s['start']) * c / N
            capw.append((w, a, b, s['i']))
chunks = []; cur = []
for x in capw:
    if cur and cur[-1][3] != x[3]:
        chunks.append(cur); cur = []
    cur.append(x); txt = " ".join(y[0] for y in cur)
    if len(cur) >= 3 or len(txt) >= 17 or re.search(r'[,.:!?—»…]$', x[0]):
        chunks.append(cur); cur = []
if cur: chunks.append(cur)
cap_html = []
for k, ch in enumerate(chunks):
    a = ch[0][1]; nxt = chunks[k + 1][0][1] if k + 1 < len(chunks) else END
    b = nxt if (k + 1 < len(chunks) and chunks[k + 1][0][3] == ch[0][3]) else min(nxt, ch[-1][2] + 0.25)
    words = []
    for w, wa, *_ in ch:
        w2 = w.replace("«", "").replace("»", "").replace("<", "&lt;")
        kw = " kwd" if norm(w2) in KW or norm(w2).split("-")[0] in KW or w2.lower().strip('.,:!?') in KW else ""
        words.append(f'<span class="w{kw}" style="--w:{wa:.2f}s">{w2}</span>')
    cap_html.append(f'<div class="cap" style="--a:{a:.2f}s;--b:{max(b, a + 0.3):.2f}s">{" ".join(words)}</div>')

SFX = []
def sfx(name, at, gain=1.0): SFX.append(dict(name=name, t=round(at, 3), gain=gain))
TYPE_CPS = 18.0
def typing(at, txt):
    for k, ch in enumerate(txt):
        if ch != " ": sfx("key", at + k / TYPE_CPS)
    return len(txt) / TYPE_CPS

PUNCH = [0.02, T[0], WT(8, "сифр"), WT(12, "анор"), WT(18, "санҷиш")]
SHAKE = [0.05, T[8]]
FLASH = [0.0, T[0], WT(18, "санҷиш")]
cam_anim = ", ".join([f"punch .4s ease-out {f(x)} 1" for x in PUNCH] + [f"shakecam .35s ease-in-out {f(x)} 1" for x in SHAKE])
flash_html = "".join(f'<div class="flash" style="animation:flash .35s ease-out {f(x)} forwards"></div>' for x in FLASH)

titles = [
    (0, T[0], "1 рӯйхат", "ба ҷои 100 тағйирёбанда", None),
    (T[0], T[3], "Рӯйхат", "рӯйхати харид", T[1]),
    (T[3], T[5], "array", "якчанд қимат дар як ҷой", None),
    (T[5], T[7], "let fruits", "тағйирёбанда аз дарси 1", None),
    (T[7], T[10], "Шумора", "аз 0 оғоз мешавад!", None),
    (T[10], T[13], ".length ва .push", "чанд қимат / илова кардан", None),
    (T[13], T[16], "Рӯйхат + давр", "алоқаманд ҳастанд", None),
    (T[16], T[17], "Дар ҳаёт", "рӯйхатҳо ҳама ҷо", None),
    (T[17], T[18], "Хулоса", "қимат + шумора аз 0", None),
    (T[18], T[22], "Санҷиш", "«тухм» — шумораи чанд?", None),
    (T[22], T[23], "Шпаргалка бепул", "дар шарҳ: РӮЙХАТ", None),
    (T[23], END + 5, "Дарси оянда", "функсия", None),
]
title_html = []
for k, (a, b, l1, l2, l2at) in enumerate(titles):
    title_html.append(f'<div class="ttl sc" style="{S(a, b - 0.05)}"><div class="t1">{l1}</div><div class="t2 sc" style="{S(l2at or a + 0.2)}">{l2}</div></div>')
    if k: sfx("whoosh", a - 0.08, 0.45)

H = []
# 0: хук — 100 переменных → один список
p0, p1 = PRE
def PW(p, pre): return [w for w in p['words'] if norm(w['w']).startswith(pre)][0]['t0']
t_sad = PW(p0, 'сад'); t_one = PW(p0, 'рӯйхат')
grid = "".join(f'<i style="--a:{t_sad + k * 0.011:.2f}s;--o:{t_one:.2f}s"></i>' for k in range(100))
H.append(f'''<div class="sc" style="{S(0, T[0] - 0.12)}">
 <div class="chip pop" style="--a:{f(0.1)};position:absolute;left:0;right:0;margin:auto;width:max-content;top:195px;background:#1F3F44;color:#F4EFE6;font:700 14px 'JetBrains Mono',monospace;letter-spacing:3px;padding:6px 12px;border-radius:6px">ДАРСИ 4 / 12</div>
 <div class="hookgrid">{grid}</div>
 <div class="cntlab sc" style="{S(t_sad)};top:490px;color:#1F3F44;font-size:26px">100 тағйирёбанда 😵</div>
 <div class="listbar pop" style="--a:{f(t_one + 0.2)}"><span>[</span><span class="emo">🍞🥛🥚🍎🍐</span><span>]</span></div>
 <div class="cntlab sc" style="{S(t_one + 0.3)};top:420px;color:#B4472E;font-size:30px">1 рӯйхат ✅</div>
 <div class="bubble ink-bg pop" style="--a:{f(p1['start'])};left:175px;top:520px;font-size:30px">Чӣ тавр? 🤔</div>
</div>''')
sfx("hit", 0.0, 0.9)
for k in range(14): sfx("tick", t_sad + k * 0.09, 0.4)
sfx("thump", t_one + 0.2, 0.9); sfx("chime", t_one + 0.4, 0.8); sfx("pop", p1['start'], 0.8)

# A: «Рӯйхат!» + рӯйхати харид
names = [("🍞", "нон", "нон"), ("🥛", "шир", "шир"), ("🥚", "тухм", "тухм"), ("🍎", "себ", "себ"), ("🍐", "нок", "нок")]
items = "".join(f'<div class="pi pop" style="--a:{f(WT(1, k))}"><span class="emo">{e}</span>{n}</div>' for e, n, k in names)
H.append(f'''<div class="sc" style="{S(T[0] - 0.1, T[3] - 0.1)}">
 <div class="slam" style="--a:{f(T[0])};top:215px;font-size:82px;letter-spacing:1px">РӮЙХАТ!</div>
 <div class="paper pop" style="--a:{f(T[1])};top:320px;left:70px;right:70px"><h4>РӮЙХАТИ ХАРИД</h4>{items}</div>
 <div class="bubble ok-bg pop" style="--a:{f(T[2])};left:300px;top:250px;font-size:24px">5 чиз = 1 рӯйхат</div>
</div>''')
sfx("hit", T[0], 0.8); sfx("pop", T[1], 0.7)
for _, _, k in names: sfx("pop", WT(1, k), 0.7)
sfx("chime", T[2], 0.7)

# P: массив-ячейки (держатся с T[3] до T[16])
cells = [("себ", WT(9, "сифр")), ("нок", WT(9, "як")), ("ангур", WT(9, "ду"))]
t_val = T[6]
cell_html = ""
for k, (v, ti_) in enumerate(cells):
    cell_html += f'<div class="cellbox pop" style="--a:{f(T[3] + 0.15 + k * 0.12)};--ix:{f(ti_)};--l:{f(WT(15, v))}"><i class="ix">{k}</i><span class="cv pop" style="--a:{f(t_val + k * 0.25)}">{v}</span></div>'
t_anor = WT(12, "анор")
cell_html += f'<div class="cellbox" style="--ix:{f(t_anor + 0.4)};--l:{f(WT(15, "анор"))};background:transparent;border:3px dashed #C8975A;box-shadow:none"><i class="ix">3</i><span class="cv pop" style="--a:{f(t_anor + 0.1)};position:absolute">анор</span></div>'
H.append(f'''<div class="sc" style="{S(T[3] - 0.05, T[16] - 0.1)}">
 <div class="cellrow" style="top:200px">{cell_html}</div>
 <div class="stamp" style="--a:{f(T[4] + 0.3)};left:330px;top:322px;font-size:28px">array</div>
 <div class="sticker pop" style="--a:{f(WT(5, 'қуттӣ'))};left:30px;top:326px">ДАРСИ 1 · тағйирёбанда = қуттӣ</div>
 <div class="banner" style="--a:{f(T[8])};top:520px;font-size:30px;letter-spacing:2px;left:30px;right:30px;animation:slam .45s cubic-bezier(.2,1.3,.4,1) {f(T[8])} forwards,hide2 .25s linear {f(T[10] - 0.1)} forwards">ДИҚҚАТ: АЗ 0!</div>
</div>''')
sfx("pop", T[3] + 0.15, 0.7); sfx("pop", T[3] + 0.27, 0.7); sfx("pop", T[3] + 0.39, 0.7); sfx("thump", T[4] + 0.3, 0.8)
for k in range(3): sfx("pop", t_val + k * 0.25, 0.8)
sfx("riser", T[8] - 0.6, 0.5); sfx("hit", T[8], 0.9)
for _, ti_ in cells: sfx("ding", ti_ + 0.05, 0.6)

# T1: let fruits
L1 = 'let fruits = ["себ", "нок", "ангур"];'
d1 = typing(T[5], L1)
H.append(f'''<div class="sc" style="{S(T[5] - 0.05, T[10] - 0.1)}">
 <div class="term2" style="inset:405px 20px auto 20px"><div class="bar"><i></i><i></i><i></i><span>royhat.js</span></div><div class="code2" style="font-size:18px"><div class="ln"><div class="type" style="--a:{T[5]:.2f}s;--d:{d1:.2f}s;--n:{len(L1)}"><span class="kw">let</span> <span class="nm">fruits</span> = [<span class="str">"себ"</span>, <span class="str">"нок"</span>, <span class="str">"ангур"</span>];</div></div></div></div>
</div>''')

# T2: length / push
L2 = 'console.log(fruits.length);'; L3 = 'fruits.push("анор");'
t_len = WT(10, "чанд"); 
d2 = typing(T[10], L2); d3 = typing(T[12], L3)
H.append(f'''<div class="sc" style="{S(T[10] - 0.05, T[13] - 0.1)}">
 <div class="term2" style="inset:405px 20px auto 20px"><div class="bar"><i></i><i></i><i></i><span>royhat.js</span></div><div class="code2" style="font-size:17px">
  <div class="ln"><div class="type" style="--a:{T[10]:.2f}s;--d:{d2:.2f}s;--n:{len(L2)}"><span class="fn">console</span>.log(<span class="nm">fruits</span>.length);</div></div>
  <div class="ln"><div class="type" style="--a:{T[12]:.2f}s;--d:{d3:.2f}s;--n:{len(L3)}"><span class="nm">fruits</span>.push(<span class="str">"анор"</span>);</div></div></div></div>
 <div class="bubble ok-bg pop" style="--a:{f(WT(10, 'се'))};left:60px;top:560px;font-size:26px">length = 3</div>
 <div class="bubble rust no-bg pop" style="--a:{f(t_anor + 0.5)};left:290px;top:560px;font-size:26px">length = 4</div>
</div>''')
sfx("chime", WT(10, "се"), 0.7); sfx("pop", t_anor, 0.9); sfx("thud", t_anor + 0.4, 0.8); sfx("pop", t_anor + 0.5, 0.7)

# T3: for + highlight
L4 = 'for (let i = 0; i < fruits.length; i++) {'; L5 = '  console.log(fruits[i]);'
t4 = T[14]; d4 = typing(t4, L4); d5 = typing(t4 + d4 + 0.1, L5)
outs = [("себ", WT(15, "себ"), 0), ("нок", WT(15, "нок"), 1), ("ангур", WT(15, "ангур"), 2), ("анор", WT(15, "анор"), 3)]
lines = "".join(f'<div class="out2 pop" style="--a:{f(t_)}">▶ {v}</div>' for v, t_, _ in outs)
ptr = "".join(f'<div class="iptr" style="--a:{f(t_ - 0.05)};--b:{f(t_ + 0.65)};left:{(42 + k * 122):.0f}px">i = {k}</div>' for _, t_, k in outs)
H.append(f'''<div class="sc" style="{S(T[13] - 0.05, T[16] - 0.1)}">
 {ptr}
 <div class="term2" style="inset:405px 20px auto 20px"><div class="bar"><i></i><i></i><i></i><span>royhat.js</span></div><div class="code2" style="font-size:16px">
  <div class="ln"><div class="type" style="--a:{t4:.2f}s;--d:{d4:.2f}s;--n:{len(L4)}"><span class="kw">for</span> (<span class="kw">let</span> <span class="nm">i</span> = <span class="v">0</span>; <span class="nm">i</span> &lt; <span class="nm">fruits</span>.length; <span class="nm">i</span>++) {{</div></div>
  <div class="ln"><div class="type" style="--a:{t4 + d4 + 0.1:.2f}s;--d:{d5:.2f}s;--n:{len(L5)}">  <span class="fn">console</span>.log(<span class="nm">fruits</span>[<span class="nm">i</span>]);</div></div></div></div>
 <div class="outbox" style="top:545px">{lines}</div>
</div>''')
for _, t_, _ in outs: sfx("tick2", t_, 0.7); sfx("pop", t_, 0.5)

# G: в жизни
tm, tg, tf = WT(16, "мусиқӣ"), WT(16, "суратҳо"), WT(16, "обуначиёни")
H.append(f'''<div class="sc life" style="{S(T[16], T[17] - 0.1)}">
 <div class="card pop" style="--a:{f(tm)}"><div class="ic" style="background:#B4472E">🎵</div><div class="ct">Рӯйхати мусиқӣ</div></div>
 <div class="card pop" style="--a:{f(tg)}"><div class="ic" style="background:#E9B949">🖼️</div><div class="ct">Суратҳо дар галерея</div></div>
 <div class="card pop" style="--a:{f(tf)}"><div class="ic" style="background:#1F3F44">👥</div><div class="ct">Обуначиёни Instagram</div></div>
</div>''')
for x in (tm, tg, tf): sfx("pop", x, 0.8)

# H: итог
tq, ts_, tz = WT(17, "якчанд"), WT(17, "шумора"), WT(17, "сифр")
H.append(f'''<div class="sc" style="{S(T[17], T[18] - 0.1)}">
 <div class="formula" style="top:290px;flex-wrap:wrap;row-gap:14px"><div class="ftile dark pop" style="--a:{f(T[17])}">РӮЙХАТ</div><div class="fop pop" style="--a:{f(T[17] + 0.2)}">=</div>
  <div class="ftile pop" style="--a:{f(tq)};border-color:#3E7C59">якчанд қимат</div><div class="fop pop" style="--a:{f(tq + 0.3)}">+</div>
  <div class="ftile pop" style="--a:{f(ts_)};border-color:#E9B949">шумора аз 0</div></div>
</div>''')
for x in (T[17], tq, ts_): sfx("pop", x, 0.7)

# I: квиз — рӯйхати харид с номерами
t_sj = WT(18, "санҷиш"); t_q = T[19]
qitems = [("🍞", "нон", 0), ("🥛", "шир", 1), ("🥚", "тухм", None), ("🍎", "себ", 3), ("🍐", "нок", 4)]
qh = "".join(f'<div class="pi pop {"hot" if ix is None else ""}" style="--a:{f(WT(18, n) + 0.1)}"><span class="emo">{e}</span>{n}<span class="ix" style="{"background:#B4472E;color:#fff" if ix is None else ""}">{"?" if ix is None else ix}</span></div>' for e, n, ix in qitems)
H.append(f'''<div class="sc" style="{S(T[18] - 0.05, T[22] - 0.1)}">
 <div class="banner" style="--a:{f(t_sj)};top:215px">САНҶИШ</div>
 <div class="paper pop" style="--a:{f(WT(18, 'нон'))};top:320px;left:60px;right:60px"><h4>РӮЙХАТИ ХАРИД</h4>{qh}</div>
 <div class="bubble ink-bg pop" style="--a:{f(T[20])};left:90px;top:592px;font-size:21px">☝ шумора аз 0 оғоз мешавад</div>
</div>''')
sfx("riser", t_sj - 1.0, 0.6); sfx("hit", t_sj, 1.0)
for _, n, _ in qitems: sfx("pop", WT(18, n) + 0.1, 0.5)
for k in range(int((T[22] - t_q) / 0.5)): sfx("tick", t_q + k * 0.5, 0.8)
sfx("pop", T[20], 0.7)

# K: CTA — кодовое слово «РӮЙХАТ»
t_kw = WT(22, "рӯйхат"); t_pdf = WT(22, "шпаргалкаи"); t_dm = WT(22, "директ")
H.append(f'''<div class="sc" style="{S(T[22] - 0.05, T[23] - 0.1)}">
 <div class="pwd" style="top:215px;left:60px;right:60px;height:74px;animation:scin .35s ease-out {f(T[22])} both"><span class="emo" style="position:static;font-size:28px">💬</span><div class="type" style="--a:{f(t_kw)};--d:.5s;--n:6;font-size:30px;color:#B4472E">РӮЙХАТ</div><span class="res2 ink-bg pop" style="--a:{f(t_kw + 0.6)};right:14px">➤</span></div>
 <svg style="position:absolute;left:0;top:0" width="540" height="640"><path class="draw" pathLength="100" d="M270 300 L270 345" stroke="#1F3F44" stroke-width="6" style="--len:101;--a:{f(t_pdf - 0.3)};--d:.25s"/></svg>
 <div class="pop" style="--a:{f(t_pdf)};position:absolute;left:45px;right:45px;top:350px;height:236px;border-radius:16px;overflow:hidden;box-shadow:0 16px 34px rgba(31,63,68,.3);background:url(banner-h.jpg) center/cover"></div>
 <div class="bubble ok-bg pop" style="--a:{f(t_dm)};left:300px;top:560px;font-size:22px">📩 ба Direct</div>
</div>''')
sfx("pop", T[22], 0.7)
for k in range(6): sfx("key", t_kw + k * 0.08)
sfx("click", t_kw + 0.6, 0.8); sfx("whoosh", t_pdf - 0.1, 0.6); sfx("chime", t_pdf, 0.8); sfx("pop", t_dm, 0.8)

# J: следующий урок и подписка
t_sub = WT(24, "обуна"); T_CLICK = t_sub + 0.8
H.append(f'''<div class="sc" style="{S(T[23])}">
 <div class="lesson pop" style="--a:{f(T[23] + 0.05)}"><small>ДАРСИ 5</small><b>Функсия</b><code>function ( )</code></div>
 <div class="sub pop" style="--a:{f(t_sub)}"><span class="b1" style="--a:{f(T_CLICK)}">Обуна шавед</span><span class="b2" style="--a:{f(T_CLICK)}">Обуна шудед ✓</span><i class="press" style="--a:{f(T_CLICK)}"></i></div>
 <svg class="cursor" style="--a:{f(t_sub + 0.1)};--c:{f(T_CLICK)}" width="34" height="40" viewBox="0 0 24 28"><path d="M2 2l19 11-8.5 1.8L17 24l-3.6 1.6-4.4-9.2L2 22z" fill="#1F3F44" stroke="#fff" stroke-width="1.5"/></svg>
</div>''')
sfx("whoosh", T[23], 0.8); sfx("pop", t_sub, 0.8); sfx("click", T_CLICK, 1.2); sfx("chime", T_CLICK + 0.1, 0.9)

css = open('style.css').read()
css += '''
.paper{position:absolute;background:#FFFDF8;border:2px solid #E3D9C7;border-radius:16px;padding:14px 18px;box-shadow:0 14px 30px rgba(31,63,68,.12)}
.paper h4{font:800 13px "JetBrains Mono",monospace;color:#B4472E;letter-spacing:2px;margin-bottom:6px}
.pi{height:46px;display:flex;align-items:center;gap:12px;font-size:26px;font-weight:800;border-bottom:1.5px solid #EFE7DA;border-radius:8px;padding:0 6px}
.pi .emo{position:static;font-size:26px}
.pi .ix{margin-left:auto;font:900 20px "JetBrains Mono",monospace;min-width:34px;height:32px;border-radius:9px;background:#E9B949;color:#1F3F44;display:flex;align-items:center;justify-content:center}
.pi.hot{background:rgba(180,71,46,.12)}
.cellrow{position:absolute;left:14px;right:14px;display:flex;gap:8px;justify-content:center}
.cellbox{position:relative;width:114px;height:104px;border-radius:16px;background:#C8975A;display:flex;align-items:center;justify-content:center;box-shadow:0 8px 18px rgba(0,0,0,.18)}
.cellbox .cv{background:#fff;color:#1F3F44;border-radius:9px;padding:7px 10px;font-size:19px;font-weight:900;opacity:0}
.cellbox .ix{position:absolute;top:-17px;left:50%;translate:-50% 0;background:#E9B949;color:#1F3F44;font:900 18px "JetBrains Mono",monospace;min-width:36px;height:30px;border-radius:9px;display:flex;align-items:center;justify-content:center;opacity:0;font-style:normal;animation:popin .4s cubic-bezier(.3,1.6,.5,1) var(--ix) forwards}
.cellbox{animation:popin .45s cubic-bezier(.3,1.6,.5,1) var(--a, 0s) both, cellhl .6s ease-in-out var(--l) 1}
@keyframes cellhl{40%{scale:1.12;filter:brightness(1.15) drop-shadow(0 0 14px rgba(180,71,46,.7))}}
.hookgrid{position:absolute;left:70px;top:250px;width:400px;display:grid;grid-template-columns:repeat(10,1fr);gap:5px}
.hookgrid i{aspect-ratio:1;border-radius:4px;background:#C8975A;opacity:0;animation:popin .2s ease-out var(--a) forwards,hgout .5s ease-in var(--o) forwards}
@keyframes hgout{to{opacity:0;scale:.2}}
.listbar{position:absolute;left:40px;right:40px;top:290px;height:84px;border-radius:16px;background:#1F3F44;display:flex;align-items:center;justify-content:center;gap:10px;color:#fff;font:800 36px "JetBrains Mono",monospace}
.iptr{position:absolute;top:314px;background:#B4472E;color:#fff;font:900 16px "JetBrains Mono",monospace;padding:5px 9px;border-radius:9px;opacity:0;animation:ptr .3s ease-out var(--a) forwards,hide2 .2s linear var(--b) forwards;z-index:5}
@keyframes ptr{from{opacity:0;translate:0 -10px}to{opacity:1;translate:0 0}}
@keyframes hide2{to{opacity:0}}
.outbox{position:absolute;left:30px;right:30px;top:520px;display:flex;gap:8px;flex-wrap:wrap}
.out2{background:#10191B;color:#7FD49A;font:700 20px "JetBrains Mono",monospace;padding:8px 14px;border-radius:10px}
'''
body = f'''<div class="cam" style="animation:{cam_anim}">
<div class="hdr"><span>ШАҲРИЁР ЮНУСОВ</span><span>ДАРСИ 04 / 12</span></div>
{"".join(title_html)}
{"".join(H)}
{"".join(cap_html)}
</div>
{flash_html}
<div class="prog" style="--d:{END:.2f}s"></div>'''
open('reel.html', 'w').write(f'<!doctype html><html lang="tg"><head><meta charset="utf-8"><style>{css}</style></head><body>{body}</body></html>')
json.dump(dict(end=END, sfx=SFX), open('sfx.json', 'w'), indent=0)
print(END, len(SFX), len(chunks))
