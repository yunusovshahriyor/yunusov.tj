# Ролик «Шарт: if / else». Тайминги — из timeline.json (точная разметка ElevenLabs).
import json, re
TL = json.load(open('timeline.json')); SN = TL['sentences']
TOTAL = TL['total']; END = round(TOTAL + 1.2, 2)
T = [s['start'] for s in SN]; E = [s['end'] for s in SN]
V = set("аеёиоуэюяӣӯ")
def norm(w): return re.sub(r'[^\w-]', '', w).lower()
def WT(i, prefix, nth=0):
    m = [w for w in SN[i]['words'] if norm(w['w']).startswith(prefix.lower())]
    return m[nth]['t0']
def WE(i, prefix, nth=0):
    m = [w for w in SN[i]['words'] if norm(w['w']).startswith(prefix.lower())]
    return m[nth]['t1']
f = lambda x: f"{x:.2f}s"
def S(a, b=None): return f"--a:{a:.2f}s;--b:{(b if b is not None else END + 5):.2f}s"

# ---- субтитры: если текст совпадает с TTS — точное время слов, иначе пропорционально слогам
KW = {"if", "else", "агар", "вагарна", "шарт", "шарт?", "дуруст", "нодуруст", "санҷиш", "loop", "давр"}
def syl(w):
    n = sum(c in V for c in w.lower())
    return max(1, n if n else len(re.sub(r'\W', '', w)) // 3 or 1)
capw = []
for s in SN:
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
    if len(cur) >= 3 or len(txt) >= 17 or re.search(r'[,.:!?—»]$', x[0]):
        chunks.append(cur); cur = []
if cur: chunks.append(cur)
cap_html = []
for k, ch in enumerate(chunks):
    a = ch[0][1]; nxt = chunks[k + 1][0][1] if k + 1 < len(chunks) else END
    b = nxt if (k + 1 < len(chunks) and chunks[k + 1][0][3] == ch[0][3]) else min(nxt, ch[-1][2] + 0.25)
    words = []
    for w, *_ in ch:
        w2 = w.replace("«", "").replace("»", "")
        words.append(f'<span class="kwd">{w2}</span>' if norm(w2) in KW or w2.lower().strip('.,:!?') in KW else w2)
    cap_html.append(f'<div class="cap" style="--a:{a:.2f}s;--b:{max(b, a + 0.3):.2f}s">{" ".join(words)}</div>')

# ---- звук
SFX = []
def sfx(name, at, gain=1.0): SFX.append(dict(name=name, t=round(at, 3), gain=gain))
TYPE_CPS = 16.0
def typing(at, txt):
    for k, ch in enumerate(txt):
        if ch != " ": sfx("key", at + k / TYPE_CPS)
    return len(txt) / TYPE_CPS

# ---- камера: акценты и тряска
PUNCH = [0.02, WT(6, "шарт"), WT(10, "хуш"), WT(15, "ҳамагӣ"), WT(21, "санҷиш")]
SHAKE = [0.05, WT(14, "нодуруст"), WT(17, "нодуруст")]
FLASH = [0.0, WT(21, "санҷиш")]
cam_anim = ", ".join([f"punch .4s ease-out {f(x)} 1" for x in PUNCH] + [f"shakecam .35s ease-in-out {f(x)} 1" for x in SHAKE])
flash_html = "".join(f'<div class="flash" style="animation:flash .35s ease-out {f(x)} forwards"></div>' for x in FLASH)

# ---- заголовки
titles = [
    (0, T[3], "Шарт", "чӣ тавр қарор мекунад?", T[1]),
    (T[3], T[7], "Ҳар субҳ", "борон меборад?", None),
    (T[7], T[8], "if / else", "агар / вагарна", None),
    (T[8], T[10], "Қуттии age", "аз дарси гузашта", None),
    (T[10], T[12], "Код", "if (age >= 18)", None),
    (T[12], T[16], "Компютер месанҷад", "дуруст ё нодуруст", None),
    (T[16], T[18], "Дар ҳаёт", "шартҳо дар ҳама ҷо", None),
    (T[18], T[21], "Хулоса", "савол + ду роҳ", None),
    (T[21], T[23], "Санҷиш", "age = 15 → ?", None),
    (T[23], END + 5, "Дарси оянда", "давр: loop", None),
]
title_html = []
for k, (a, b, l1, l2, l2at) in enumerate(titles):
    title_html.append(f'<div class="ttl sc" style="{S(a, b - 0.05)}"><div class="t1">{l1}</div><div class="t2 sc" style="{S(l2at or a + 0.2)}">{l2}</div></div>')
    if k: sfx("whoosh", a - 0.08, 0.45)

H = []  # html сцен
# A: хук
sfx("hit", 0.0, 1.0); sfx("whoosh", T[1] - 0.1, 0.5)
H.append(f'''<div class="sc" style="{S(0, T[3] - 0.1)}">
 <div class="slam" style="--a:0s;top:215px;font-size:92px;letter-spacing:2px">ШАРТ?</div>
 <svg style="position:absolute;left:0;top:0" width="540" height="640">
  <path class="draw" pathLength="100" d="M270 610 L270 500" stroke="#1F3F44" stroke-width="10" style="--len:101;--a:{f(T[1])};--d:.35s"/>
  <path class="draw" pathLength="100" d="M270 500 Q270 450 150 410" stroke="#3E7C59" stroke-width="10" style="--len:101;--a:{f(T[1] + 0.35)};--d:.4s"/>
  <path class="draw" pathLength="100" d="M270 500 Q270 450 390 410" stroke="#B4472E" stroke-width="10" style="--len:101;--a:{f(T[1] + 0.55)};--d:.4s"/>
 </svg>
 <div class="bubble ok-bg pop" style="--a:{f(T[1] + 0.75)};left:70px;top:350px">✓ ҲА</div>
 <div class="bubble no-bg pop" style="--a:{f(T[1] + 0.95)};left:360px;top:350px">✗ НЕ</div>
 <div class="pill pop" style="--a:{f(WT(2, "субҳ"))};top:540px"><span class="emo" style="position:static;font-size:26px">🌅</span> ҳар субҳ</div>
</div>''')
sfx("pop", T[1] + 0.75, 0.7); sfx("pop", T[1] + 0.95, 0.7); sfx("pop", WT(2, "субҳ"), 0.6)

# B: утро — чатр / айнак
tq = WT(4, "агар"); ty = WT(4, "чатр"); tn = WT(5, "айнаки"); ts = WT(6, "шарт")
H.append(f'''<div class="sc" style="{S(T[3], T[7] - 0.1)}">
 <div class="emo pop" style="--a:{f(T[3])};left:236px;top:205px;font-size:68px">🚪</div>
 <div class="pill pop" style="--a:{f(tq)};top:290px"><span class="emo" style="position:static;font-size:26px">🌧️</span> Борон меборад?</div>
 <svg style="position:absolute;left:0;top:0" width="540" height="640">
  <path class="draw" pathLength="100" d="M230 345 Q170 365 150 400" stroke="#3E7C59" stroke-width="7" style="--len:101;--a:{f(ty - 0.2)}"/>
  <path class="draw" pathLength="100" d="M310 345 Q370 365 390 400" stroke="#B4472E" stroke-width="7" style="--len:101;--a:{f(tn - 0.2)}"/>
 </svg>
 <div class="choice yes pop" style="--a:{f(ty)};left:45px;top:405px"><span class="emo">☂️</span>Чатр<small class="ok-bg">ҲА</small></div>
 <div class="choice no pop" style="--a:{f(tn)};left:295px;top:405px"><span class="emo">😎</span>Айнак<small class="no-bg">НЕ</small></div>
 <div class="stamp" style="--a:{f(ts)};left:175px;top:440px">ШАРТ!</div>
</div>''')
sfx("pop", T[3], 0.8); sfx("pop", tq, 0.8); sfx("chime", ty, 0.6); sfx("pop", tn, 0.8); sfx("thump", ts, 1.0)

# C: if = агар, else = вагарна
t_ie = WT(7, "иф-элс"); t_ag = WT(7, "агар"); t_vg = WT(7, "вагарна")
H.append(f'''<div class="sc" style="{S(T[7], T[8] - 0.1)}">
 <div class="slam" style="--a:{f(t_ie)};top:225px;font:900 64px 'JetBrains Mono',monospace;color:#B4472E">if / else</div>
 <div class="dict pop" style="--a:{f(t_ag)};top:345px"><code>if</code><span class="eq">=</span>агар</div>
 <div class="dict pop" style="--a:{f(t_vg)};top:455px"><code>else</code><span class="eq">=</span>вагарна</div>
</div>''')
sfx("hit", t_ie, 0.7); sfx("pop", t_ag, 0.8); sfx("pop", t_vg, 0.8)

# D: коробка из урока 1
t25 = WT(8, "бисту")
H.append(f'''<div class="sc" style="{S(T[8], T[10] - 0.1)}">
 <div class="stage pop" style="--a:{f(T[8])};top:215px">
  <div class="flap l"></div><div class="flap r"></div><div class="back"></div>
  <div class="num" style="animation:dropin .6s cubic-bezier(.4,1.5,.6,1) {f(t25)} forwards">25</div>
  <div class="front"><div class="tag">age</div></div>
 </div>
 <div class="sticker pop" style="--a:{f(T[8] + 0.4)};left:345px;top:240px">ДАРСИ 1</div>
 <div class="pill pop" style="--a:{f(T[9])};top:510px">Акнун — <b style="color:#B4472E">қарор</b> 🤔</div>
</div>''')
sfx("whoosh", T[8], 0.6); sfx("pop", T[8] + 0.05); sfx("thud", t25 + 0.45); sfx("pop", T[9], 0.6)

# E: код
t_if = WT(10, "иф"); t_cond = WT(10, "агар"); t_br = WT(10, "барнома"); t_hush = WT(10, "хуш")
t_else = WT(11, "элс"); t_han = WT(11, "ҳанӯз")
L1 = 'if (age >= 18) {'; L2 = '  console.log("Хуш омадед!");'; L3 = '} else {'; L4 = '  console.log("Ҳанӯз барвақт");'
def tl(at, txt, html):
    d = typing(at, txt)
    return f'<div class="ln"><div class="type" style="--a:{at:.2f}s;--d:{d:.2f}s;--n:{len(txt)}">{html}</div></div>'
code = (f'<div class="ln"><span class="kw">let</span> <span class="nm">age</span> = <span class="v">25</span>;</div>'
        + tl(t_if, L1, f'<span class="kw">if</span> (<span class="condhl" style="--h:{t_cond:.2f}s"><span class="nm">age</span> <span class="op">&gt;=</span> <span class="v">18</span></span>) {{')
        + tl(t_br, L2, '  console.log(<span class="str">"Хуш омадед!"</span>);')
        + tl(t_else, L3, '} <span class="kw">else</span> {')
        + tl(t_han - 0.1, L4, '  console.log(<span class="str">"Ҳанӯз барвақт"</span>);')
        + tl(E[11] - 0.1, '}', '}'))
H.append(f'''<div class="sc" style="{S(T[10] - 0.1, T[12] - 0.1)}">
 <div class="term2"><div class="bar"><i></i><i></i><i></i><span>shart.js</span></div><div class="code2">{code}</div></div>
 <div class="out pop" style="--a:{f(t_hush)}"><b>▶</b> Хуш омадед! <span class="emo" style="position:static;font-size:24px">🎉</span></div>
</div>''')
sfx("ding", t_cond, 0.5); sfx("chime", t_hush, 1.0); sfx("pop", t_hush, 0.6)

# F: компютер проверяет
t_chk = WT(12, "месанҷад"); t_ok = WT(13, "дуруст"); t_no = WT(14, "нодуруст"); t_all = WT(15, "ҳамагӣ")
H.append(f'''<div class="sc" style="{S(T[12], T[16] - 0.1)}">
 <div class="val flip" style="--a:{f(T[12])};--b:{f(t_no - 0.15)}"><span class="nm" style="color:#1F3F44">age</span> = <span style="color:#3E7C59">25</span></div>
 <div class="val flipin" style="--a:{f(t_no + 0.1)}">age = <span style="color:#B4472E">12</span></div>
 <div class="diamond pop scan" style="--a:{f(T[12] + 0.3)}"><svg viewBox="0 0 200 120"><polygon points="100,4 196,60 100,116 4,60" fill="#1F3F44"/></svg><span>age &gt;= 18 ?</span></div>
 <svg style="position:absolute;left:0;top:0" width="540" height="640">
  <path class="draw" pathLength="100" d="M200 400 Q150 440 140 480" stroke="#3E7C59" stroke-width="8" style="--len:101;--a:{f(t_ok)};--d:.3s"/>
  <path class="draw" pathLength="100" d="M340 400 Q390 440 400 480" stroke="#B4472E" stroke-width="8" style="--len:101;--a:{f(t_no + 0.15)};--d:.3s"/>
 </svg>
 <div class="res lit-ok" style="--a0:{f(T[12] + 0.6)};--a:{f(t_ok + 0.25)};left:35px;top:485px">✓ Хуш омадед!</div>
 <div class="res lit-no" style="--a0:{f(T[12] + 0.75)};--a:{f(t_no + 0.4)};left:295px;top:485px">✗ Ҳанӯз барвақт</div>
 <div class="stamp" style="--a:{f(t_all)};left:175px;top:228px">ОДДӢ!</div>
</div>''')
sfx("pop", T[12] + 0.3, 0.8); sfx("tick", t_chk, 0.6); sfx("tick", t_chk + 0.5, 0.6); sfx("tick", t_chk + 1.0, 0.6)
sfx("chime", t_ok + 0.25, 0.9); sfx("whoosh", t_no, 0.4); sfx("buzz", t_no + 0.4, 0.8); sfx("thump", t_all, 1.0)

# G: жизнь — светофор и пароль
t_g = WT(16, "сабз"); t_r = WT(16, "сурх"); t_pw_ok = WT(17, "дуруст"); t_pw_no = WT(17, "нодуруст")
pw_type = T[17] - 0.05
H.append(f'''<div class="sc" style="{S(T[16], T[18] - 0.1)}">
 <div class="tlight pop" style="--a:{f(T[16] + 0.1)}"><i class="lamp" style="--c:#E0534A;--a:{f(t_r)};--b:{f(END + 5)}"></i><i></i><i class="lamp" style="--c:#4CC26E;--a:{f(t_g)};--b:{f(t_r)}"></i></div>
 <div class="tl-lab ok-bg pop" style="--a:{f(t_g + 0.1)};top:395px">🚶 мегузарем</div>
 <div class="tl-lab no-bg pop" style="--a:{f(t_r + 0.1)};top:220px">✋ меистем</div>
 <div class="pwd state" style="--a0:{f(T[17] - 0.15)};--a:{f(t_pw_ok)};--b:{f(t_pw_no)}"><span class="emo" style="position:static;font-size:30px">🔑</span><div class="type" style="--a:{f(pw_type)};--d:.6s;--n:8">••••••••</div>
  <span class="res2 ok-bg" style="animation:popin .4s cubic-bezier(.3,1.6,.5,1) {f(t_pw_ok + 0.1)} both, fadeo .2s linear {f(t_pw_no)} forwards">✓ ворид</span></div>
 <div class="bubble no-bg pop" style="--a:{f(t_pw_no + 0.15)};left:330px;top:610px;font-size:20px">✗ хато!</div>
</div>''')
sfx("pop", T[16] + 0.1, 0.7); sfx("ding", t_g, 0.7); sfx("buzz", t_r, 0.6)
for k in range(8): sfx("key", pw_type + k * 0.075)
sfx("chime", t_pw_ok + 0.1, 0.8); sfx("buzz", t_pw_no + 0.1, 0.9)

# H: итог
t_sv = WT(18, "савол"); t_du = WT(18, "ду")
H.append(f'''<div class="sc" style="{S(T[18], T[21] - 0.1)}">
 <div class="formula"><div class="ftile dark pop" style="--a:{f(T[18])}">ШАРТ</div><div class="fop pop" style="--a:{f(T[18] + 0.25)}">=</div>
  <div class="ftile pop" style="--a:{f(t_sv)}">❓ савол</div><div class="fop pop" style="--a:{f(t_sv + 0.3)}">+</div><div class="ftile pop" style="--a:{f(t_du)}">2 роҳ</div></div>
 <div class="path ok-bg pop" style="--a:{f(T[19])};top:345px">✓ ҲА <span style="opacity:.7">→</span> як кор</div>
 <div class="path no-bg pop" style="--a:{f(T[20])};top:440px">✗ НЕ <span style="opacity:.7">→</span> кори дигар</div>
</div>''')
for x in (T[18], t_sv, t_du): sfx("pop", x, 0.7)
sfx("chime", T[19], 0.6); sfx("tick2", T[20], 0.8)

# I: санҷиш
t_sj = WT(21, "санҷиш"); t_15 = WT(21, "понздаҳ"); t_q = WT(21, "чӣ")
H.append(f'''<div class="sc" style="{S(T[21] - 0.05, T[23] - 0.1)}">
 <div class="banner" style="--a:{f(t_sj)}">САНҶИШ</div>
 <div class="stage pop" style="--a:{f(t_sj + 0.3)};left:40px;top:300px;transform:scale(.8)">
  <div class="flap l"></div><div class="flap r"></div><div class="back"></div>
  <div class="num" style="animation:dropin .6s cubic-bezier(.4,1.5,.6,1) {f(t_15)} forwards">15</div>
  <div class="front"><div class="tag">age</div></div></div>
 <div class="quizq pop" style="--a:{f(t_q)}"><svg width="170" height="170"><circle cx="85" cy="85" r="70" fill="#FFFDF8" stroke="#E3D9C7" stroke-width="10"/><circle class="cring" cx="85" cy="85" r="70" fill="none" stroke="#B4472E" stroke-width="10" style="--a:{f(t_q)};--d:{E[22] - t_q:.2f}s"/></svg><b>?</b></div>
 <div class="bubble ink-bg pop" style="--a:{f(T[22])};left:110px;top:560px;font-size:20px">💬 Ҷавоб дар шарҳ <span class="dots"><i></i><i></i><i></i></span></div>
</div>''')
sfx("riser", t_sj - 1.0, 0.6); sfx("hit", t_sj, 1.0); sfx("thud", t_15 + 0.45)
n = int((E[22] - t_q) / 0.5)
for k in range(n): sfx("tick", t_q + k * 0.5, 0.8)
sfx("pop", T[22], 0.7)

# J: следующий урок и подписка
t_sub = WT(24, "обуна"); T_CLICK = t_sub + 0.8
H.append(f'''<div class="sc" style="{S(T[23])}">
 <div class="lesson pop" style="--a:{f(T[23] + 0.05)}"><small>ДАРСИ 3</small><b>Давр <span class="emo spin" style="position:static;font-size:38px">🔁</span></b><code>loop</code></div>
 <div class="sub pop" style="--a:{f(t_sub)}"><span class="b1" style="--a:{f(T_CLICK)}">Обуна шавед</span><span class="b2" style="--a:{f(T_CLICK)}">Обуна шудед ✓</span><i class="press" style="--a:{f(T_CLICK)}"></i></div>
 <svg class="cursor" style="--a:{f(t_sub + 0.1)};--c:{f(T_CLICK)}" width="34" height="40" viewBox="0 0 24 28"><path d="M2 2l19 11-8.5 1.8L17 24l-3.6 1.6-4.4-9.2L2 22z" fill="#1F3F44" stroke="#fff" stroke-width="1.5"/></svg>
</div>''')
sfx("whoosh", T[23], 0.8); sfx("pop", t_sub, 0.8); sfx("click", T_CLICK, 1.2); sfx("chime", T_CLICK + 0.1, 0.9)

css = open('style.css').read()
body = f'''<div class="cam" style="animation:{cam_anim}">
<div class="hdr"><span>ШАҲРИЁР ЮНУСОВ</span><span>02 / БАРНОМАСОЗӢ</span></div>
{"".join(title_html)}
{"".join(H)}
{"".join(cap_html)}
</div>
{flash_html}
<div class="prog" style="--d:{END:.2f}s"></div>'''
open('reel.html', 'w').write(f'<!doctype html><html lang="tg"><head><meta charset="utf-8"><style>{css}</style></head><body>{body}</body></html>')
json.dump(dict(end=END, sfx=SFX), open('sfx.json', 'w'), indent=0)
print(END, len(SFX), len(chunks))
