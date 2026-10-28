# Ролик «Тағйирёбанда» v3: стиль «бумага + терминал», субтитры по словам, события для звуковых эффектов.
# Вход: timeline.json (предложения), gaps.txt (паузы). Выход: reel.html, sfx.json, END.
import json, re
TL = json.load(open('timeline.json'))
gaps = [tuple(map(float, l.split())) for l in open('gaps.txt')]
t = [o['start'] for o in TL]; e = [o['end'] for o in TL]
TOTAL = e[-1]; END = round(TOTAL + 0.6, 2)
V = set("аеёиоуэюяӣӯ")
SPOKEN = {"«age»,": 1, "«age»": 1, "age": 1, "let": 1, "=": 3, "25.": 3, "Instagram.": 3, "«if/else».": 2}

def syl(w):
    if w in SPOKEN: return SPOKEN[w]
    return max(1, sum(c in V for c in w.lower()))

# --- время каждого слова: пропорционально слогам по «речевому» времени внутри предложения
words = []  # (sent, idx, text, start, end)
for i, o in enumerate(TL):
    ws = o['text'].split()
    s0, s1 = o['start'], o['end']
    segs = []; p = s0
    for a, b in gaps:
        if a >= s0 and b <= s1:
            if a > p: segs.append((p, a))
            p = b
    if p < s1: segs.append((p, s1))
    tot = sum(b - a for a, b in segs)
    def wall(x):
        for a, b in segs:
            if x <= b - a + 1e-9: return a + x
            x -= b - a
        return s1
    n = [syl(w) for w in ws]; N = sum(n); c = 0
    for k, w in enumerate(ws):
        ws0 = wall(tot * c / N); c += n[k]; ws1 = wall(tot * c / N)
        words.append((i, k, w, round(ws0, 3), round(ws1, 3)))

def W(i, prefix, nth=0):
    """Время начала слова в предложении i, начинающегося с prefix (nth-е совпадение)."""
    m = [x for x in words if x[0] == i and x[2].strip('«»,.:!?—').lower().startswith(prefix.lower())]
    return m[nth][3]

# --- субтитры: куски до 3 слов / 20 символов, разрыв после знаков препинания
chunks = []
for i, o in enumerate(TL):
    ws = [x for x in words if x[0] == i]
    cur = []
    for x in ws:
        cur.append(x)
        txt = " ".join(y[2] for y in cur)
        if len(cur) >= 3 or len(txt) >= 18 or re.search(r'[,.:!?—]$', x[2]):
            chunks.append((txt, cur[0][3], cur[-1][4], i)); cur = []
    if cur: chunks.append((" ".join(y[2] for y in cur), cur[0][3], cur[-1][4], i))
cap_html = []
for k, (txt, a, b, i) in enumerate(chunks):
    nxt = chunks[k + 1][1] if k + 1 < len(chunks) else END
    b2 = nxt if (k + 1 < len(chunks) and chunks[k + 1][3] == i) else min(nxt, b + 0.25)
    txt = txt.replace("«", "").replace("»", "")
    cap_html.append(f'<div class="cap" style="--a:{a:.2f}s;--b:{max(b2, a + 0.3):.2f}s">{txt}</div>')

# --- звуковые события
SFX = []
def sfx(name, at, **kw): SFX.append(dict(name=name, t=round(at, 3), **kw))

def S(**kw): return "--a:{:.2f}s;--b:{:.2f}s".format(kw['a'], kw.get('b', END + 5))

# ключевые моменты
T_STAMP1 = W(1, "оддӣ")
T_AGE = W(5, "age")
T_25 = W(6, "бисту")
T_LET = W(7, "let")
T_HL_AGE = W(8, "қуттии"); T_HL_25 = W(8, "қимати")
T_DEL = W(10, "нест"); T_26 = W(10, "бисту")
T_NOM = W(11, "ном")
T_STAMP2 = W(13, "тағйир", 0)
T_C1 = W(15, "холи"); T_C2 = W(15, "бақияи"); T_C3 = W(15, "шумораи")
T_COUNT = t[16]
T_Q2 = W(20, "номаш")
T_TYPE = t[21]
T_NEXT = t[22]; T_SUB = t[23]
CODE1 = "let age = 25;"; CODE2 = "age = 26;"
TYPE_CPS = 13.0
CMT = "price = 100"

# заголовки разделов
titles = [
    (0, t[3], "Тағйирёбанда", "хеле оддӣ аст", T_STAMP1),
    (t[3], t[6], "Тасаввур кунед", "як қуттӣ", None),
    (t[6], t[9], "Дар дохили қуттӣ", "қимат", None),
    (t[9], t[11], "Як сол мегузарад", "қимат иваз мешавад", None),
    (t[11], t[14], "Қуттӣ ҳамон", "танҳо қимат нав", None),
    (t[14], t[17], "Дар ҳаёт", "ҳамааш тағйирёбанда", None),
    (t[17], t[20], "Хулоса", "ном ва қимат", None),
    (t[20], t[22], "Савол", "барои шумо", None),
    (t[22], END + 5, "Дарси оянда", "шарт: if / else", None),
]
title_html = []
for k, (a, b, l1, l2, l2at) in enumerate(titles):
    a2 = l2at if l2at else a + 0.25
    title_html.append(f'<div class="ttl sc" style="{S(a=a, b=b - 0.05)}"><div class="t1">{l1}</div><div class="t2 sc" style="{S(a=a2)}">{l2}</div></div>')
    if k: sfx("whoosh", a - 0.05, gain=0.5)

# сцена 1: слово + штамп + секундомер
sfx("whoosh", 0.05, gain=0.7)
sfx("thump", T_STAMP1 + 0.05); sfx("pop", t[2] + 0.05)
for k in range(int((t[3] - t[2]) / 0.5)): sfx("tick", t[2] + 0.3 + k * 0.5, gain=0.6)
# сцена 2: коробка
sfx("pop", t[3] + 0.05, gain=1.0); sfx("click", T_AGE + 0.05); sfx("pop", T_AGE + 0.08, gain=0.6)
sfx("whoosh", T_25 - 0.1, gain=0.6); sfx("thud", T_25 + 0.45)
sfx("pop", t[7] + 0.05, gain=0.7)
for k, ch in enumerate(CODE1):
    if ch != " ": sfx("key", T_LET + k / TYPE_CPS)
sfx("ding", T_HL_AGE + 0.05, gain=0.6); sfx("ding", T_HL_25 + 0.05, gain=0.8)
sfx("pop", t[9] + 0.05)
sfx("thump", T_DEL + 0.05, gain=0.6); sfx("whoosh", T_DEL + 0.45, gain=0.7)
sfx("whoosh", T_26 - 0.1, gain=0.5); sfx("thud", T_26 + 0.45)
for k, ch in enumerate(CODE2):
    if ch != " ": sfx("key", T_26 + 0.1 + k / TYPE_CPS)
sfx("tick2", t[11] + 0.1); sfx("tick2", T_NOM + 0.05); sfx("pop", t[12] + 0.05)
sfx("thump", T_STAMP2 + 0.05)
# сцена 3: жизнь
for x in (T_C1, T_C2, T_C3): sfx("pop", x + 0.05, gain=0.8)
for k in range(3):
    for j in range(10): sfx("tick", T_COUNT + k * 0.25 + j * 0.08, gain=0.35)
# сцена 4: итог
for x in (t[17], t[18], t[19]): sfx("tick2", x + 0.1)
sfx("ding", t[19] + 0.6, gain=0.7)
# сцена 5: чат
sfx("pop", t[20] + 0.1, gain=0.8); sfx("pop", T_Q2 + 0.05, gain=0.8)
for k, ch in enumerate(CMT):
    if ch != " ": sfx("key", T_TYPE + 0.15 + k / TYPE_CPS)
T_SENT = T_TYPE + 0.15 + len(CMT) / TYPE_CPS + 0.1
sfx("click", T_SENT); sfx("pop", T_SENT + 0.05, gain=0.7)
sfx("whoosh", T_NEXT + 0.05, gain=0.8)
T_CLICK = T_SUB + 0.75
sfx("click", T_CLICK, gain=1.2); sfx("ding", T_CLICK + 0.1, gain=0.9)

def typed(txt, a, cls=""):
    n = len(txt); d = n / TYPE_CPS
    return f'<div class="type {cls}" style="--a:{a:.2f}s;--d:{d:.2f}s;--n:{n}">{txt}</div>'

code1 = (f'<div class="type" style="--a:{T_LET:.2f}s;--d:{len(CODE1) / TYPE_CPS:.2f}s;--n:{len(CODE1)}">'
         f'<span class="kw">let</span> <span class="nm hl" style="--h:{T_HL_AGE:.2f}s">age</span> = '
         f'<span class="v hl" style="--h:{T_HL_25:.2f}s">25</span>;</div>')
code2 = f'<div class="type" style="--a:{T_26 + 0.1:.2f}s;--d:{len(CODE2) / TYPE_CPS:.2f}s;--n:{len(CODE2)}"><span class="nm">age</span> = <span class="v">26</span>;</div>'
cmt = f'<div class="type" style="--a:{T_TYPE + 0.15:.2f}s;--d:{len(CMT) / TYPE_CPS:.2f}s;--n:{len(CMT)}">{CMT}</div>'

css = open('style.css').read()
body = f"""
<div class="hdr"><span>ШАҲРИЁР ЮНУСОВ</span><span>01 / БАРНОМАСОЗӢ</span></div>
{''.join(title_html)}

<!-- сцена 1 -->
<div class="sc" style="{S(a=0.1, b=t[3] - 0.1)}">
  <div class="word shake" style="--a:{t[1]:.2f}s"><div class="wl">ТАҒЙИРЁБАНДА</div><div class="ws">variable</div></div>
  <div class="stamp" style="--a:{T_STAMP1:.2f}s;left:300px;top:360px">ОДДӢ!</div>
  <div class="watch pop" style="--a:{t[2]:.2f}s"><svg viewBox="0 0 120 120" width="120" height="120"><circle cx="60" cy="64" r="44" fill="#FFFDF8" stroke="#1F3F44" stroke-width="8"/><rect x="52" y="6" width="16" height="12" rx="3" fill="#1F3F44"/><circle class="ring" cx="60" cy="64" r="32" fill="none" stroke="#B4472E" stroke-width="12" style="--a:{t[2]:.2f}s;--d:{t[3] - t[2]:.2f}s"/></svg><b>1:00</b></div>
</div>

<!-- сцена 2: коробка -->
<div class="sc" style="{S(a=t[3], b=t[14] - 0.1)}">
  <div class="stage pop glow" style="--a:{t[3]:.2f}s;--g:{T_STAMP2:.2f}s">
    <div class="flap l"></div><div class="flap r"></div><div class="back"></div>
    <div class="num drop flyout" style="--a:{T_25:.2f}s;--o:{T_DEL + 0.4:.2f}s">25<i class="x xs" style="--a:{T_DEL:.2f}s"></i></div>
    <div class="num drop" style="--a:{T_26:.2f}s">26</div>
    <div class="front"><div class="tag pop hlt" style="--a:{T_AGE:.2f}s;--h:{T_HL_AGE:.2f}s">age</div></div>
  </div>
  <div class="year pop popout" style="--a:{t[9]:.2f}s;--b:{t[10] + 0.6:.2f}s">+1 сол</div>
  <div class="term sc" style="{S(a=t[7], b=t[11])}"><div class="bar"><i></i><i></i><i></i><span>code.js</span></div>
    <div class="code">{code1}{code2}</div></div>
  <div class="checks sc" style="{S(a=t[11] + 0.05)}">
    <div class="row pop" style="--a:{t[11] + 0.1:.2f}s"><b class="ok">✓</b> Қуттӣ ҳамон</div>
    <div class="row pop" style="--a:{T_NOM:.2f}s"><b class="ok">✓</b> Ном ҳамон</div>
    <div class="row pop hot" style="--a:{t[12]:.2f}s"><b>↻</b> Қимат: 25 → 26</div>
  </div>
  <div class="stamp big" style="--a:{T_STAMP2:.2f}s;left:70px;top:330px">ТАҒЙИР МЕЁБАД</div>
</div>

<!-- сцена 3: жизнь -->
<div class="sc life" style="{S(a=t[14], b=t[17] - 0.1)}">
  <div class="card pop" style="--a:{T_C1:.2f}s"><div class="ic" style="background:#E9B949">★</div><div class="ct">Холи бозӣ</div><div class="cnt" style="--a:{T_COUNT:.2f}s;--from:120;--to:150"></div></div>
  <div class="card pop" style="--a:{T_C2:.2f}s"><div class="ic" style="background:#1F3F44">◼</div><div class="ct">Бақияи ҳисоб</div><div class="cnt" style="--a:{T_COUNT + 0.25:.2f}s;--from:500;--to:350"></div></div>
  <div class="card pop" style="--a:{T_C3:.2f}s"><div class="ic" style="background:#B4472E">♥</div><div class="ct">Пайравон</div><div class="cnt" style="--a:{T_COUNT + 0.5:.2f}s;--from:1443;--to:1500"></div></div>
</div>

<!-- сцена 4: итог -->
<div class="sc sum" style="{S(a=t[17], b=t[20] - 0.1)}">
  <div class="sumh">Тағйирёбанда =</div>
  <div class="row pop" style="--a:{t[17] + 0.05:.2f}s"><b class="ok">✓</b> <span class="k">Ном</span> — болои қуттӣ</div>
  <div class="row pop" style="--a:{t[18] + 0.05:.2f}s"><b class="ok">✓</b> <span class="k">Қимат</span> — дохили қуттӣ</div>
  <div class="row pop hot" style="--a:{t[19] + 0.05:.2f}s"><b>↻</b> Қимат тағйир меёбад</div>
</div>

<!-- сцена 5: чат и подписка -->
<div class="sc chat" style="{S(a=t[20], b=t[22] - 0.1)}">
  <div class="bar"><i></i><i></i><i></i><span>шарҳҳо</span></div>
  <div class="msg pop" style="--a:{t[20] + 0.1:.2f}s"><b class="av">Ш</b><span>Номи қуттии шумо чӣ мебуд?</span></div>
  <div class="msg pop" style="--a:{T_Q2:.2f}s"><b class="av">Ш</b><span>Дар дохилаш чӣ мегузоштед?</span></div>
  <div class="msg me pop" style="--a:{T_SENT:.2f}s"><span>price = 100 😄</span></div>
  <div class="input sc" style="{S(a=t[21] - 0.1, b=T_SENT)}">{cmt}<i class="caret"></i></div>
</div>
<div class="sc next" style="{S(a=T_NEXT)}">
  <div class="lesson pop" style="--a:{T_NEXT + 0.05:.2f}s"><small>ДАРСИ 2</small><b>Шарт</b><code>if / else</code></div>
  <div class="sub pop" style="--a:{T_SUB:.2f}s"><span class="b1" style="--a:{T_CLICK:.2f}s">Обуна шавед</span><span class="b2" style="--a:{T_CLICK:.2f}s">Обуна шудед ✓</span><i class="press" style="--a:{T_CLICK:.2f}s"></i></div>
  <svg class="cursor" style="--a:{T_SUB + 0.1:.2f}s;--c:{T_CLICK:.2f}s" width="34" height="40" viewBox="0 0 24 28"><path d="M2 2l19 11-8.5 1.8L17 24l-3.6 1.6-4.4-9.2L2 22z" fill="#1F3F44" stroke="#fff" stroke-width="1.5"/></svg>
</div>

{''.join(cap_html)}
<div class="prog" style="--d:{END:.2f}s"></div>
"""
html = f'<!doctype html><html lang="tg"><head><meta charset="utf-8"><style>{css}</style></head><body>{body}</body></html>'
open('reel.html', 'w').write(html)
json.dump(dict(end=END, sfx=SFX, music_end=END), open('sfx.json', 'w'), indent=0)
json.dump(words, open('words.json', 'w'), ensure_ascii=False)
print(END, len(SFX), len(chunks))
