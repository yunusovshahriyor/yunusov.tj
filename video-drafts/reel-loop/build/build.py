# Ролик «Давр: loop». Тайминги — из timeline.json (точная разметка ElevenLabs v4).
import json, re
TL = json.load(open('timeline.json')); SN = TL['sentences']
TOTAL = TL['total']; END = round(TOTAL + 1.2, 2)
T = [s['start'] for s in SN]; E = [s['end'] for s in SN]
V = set("аеёиоуэюяӣӯ")
def norm(w): return re.sub(r'[^\w-]', '', w).lower()
def WT(i, prefix, nth=0):
    m = [w for w in SN[i]['words'] if norm(w['w']).startswith(prefix.lower())]
    return m[nth]['t0']
f = lambda x: f"{x:.2f}s"
def S(a, b=None): return f"--a:{a:.2f}s;--b:{(b if b is not None else END + 5):.2f}s"

KW = {"давр", "давр?", "for", "шарт", "қадам", "оғоз", "i", "array", "қуттӣ", "тағйирёбанда"}
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
    if len(cur) >= 3 or len(txt) >= 17 or re.search(r'[,.:!?—»…]$', x[0]):
        chunks.append(cur); cur = []
if cur: chunks.append(cur)
cap_html = []
for k, ch in enumerate(chunks):
    a = ch[0][1]; nxt = chunks[k + 1][0][1] if k + 1 < len(chunks) else END
    b = nxt if (k + 1 < len(chunks) and chunks[k + 1][0][3] == ch[0][3]) else min(nxt, ch[-1][2] + 0.25)
    words = []
    for w, *_ in ch:
        w2 = w.replace("«", "").replace("»", "").replace("<", "&lt;")
        words.append(f'<span class="kwd">{w2}</span>' if norm(w2) in KW or w2.lower().strip('.,:!?') in KW else w2)
    cap_html.append(f'<div class="cap" style="--a:{a:.2f}s;--b:{max(b, a + 0.3):.2f}s">{" ".join(words)}</div>')

SFX = []
def sfx(name, at, gain=1.0): SFX.append(dict(name=name, t=round(at, 3), gain=gain))
TYPE_CPS = 18.0
def typing(at, txt):
    for k, ch in enumerate(txt):
        if ch != " ": sfx("key", at + k / TYPE_CPS)
    return len(txt) / TYPE_CPS

t_hazor = WT(17, "ҳазор")
PUNCH = [0.02, WT(6, "давр"), WT(12, "қуттӣ"), t_hazor, WT(20, "санҷиш")]
SHAKE = [0.05, WT(16, "хотима")]
FLASH = [0.0, WT(20, "санҷиш")]
cam_anim = ", ".join([f"punch .4s ease-out {f(x)} 1" for x in PUNCH] + [f"shakecam .35s ease-in-out {f(x)} 1" for x in SHAKE])
flash_html = "".join(f'<div class="flash" style="animation:flash .35s ease-out {f(x)} forwards"></div>' for x in FLASH)

titles = [
    (0, T[4], "Давр", "такрор бе хастагӣ", T[1]),
    (T[4], T[7], "Дар варзиш", "10 бор нишаст-хез", None),
    (T[7], T[12], "for", "се қисм", None),
    (T[12], T[14], "i = қуттӣ", "аз дарси 1", None),
    (T[14], T[17], "i &lt;= 10", "шарт аз дарси 2", None),
    (T[17], T[18], "Ҳазор бор?", "камтар аз 1 сония", None),
    (T[18], T[19], "Дар ҳаёт", "даврҳо ҳама ҷо", None),
    (T[19], T[20], "Хулоса", "оғоз + шарт + қадам", None),
    (T[20], T[22], "Санҷиш", "чанд бор «Салом»?", None),
    (T[22], END + 5, "Дарси оянда", "рӯйхат: array", None),
]
title_html = []
for k, (a, b, l1, l2, l2at) in enumerate(titles):
    title_html.append(f'<div class="ttl sc" style="{S(a, b - 0.05)}"><div class="t1">{l1}</div><div class="t2 sc" style="{S(l2at or a + 0.2)}">{l2}</div></div>')
    if k: sfx("whoosh", a - 0.08, 0.45)

H = []
# A: хук — сто раз «Салом», устал / не устал
t_sad = WT(1, "сад"); t_tired = T[2]; t_pc = T[3]
H.append(f'''<div class="sc" style="{S(0, T[4] - 0.1)}">
 <div class="slam" style="--a:0s;top:205px;font-size:92px">ДАВР?</div>
 <div class="emo pop spin" style="--a:{f(0.3)};left:410px;top:420px;font-size:56px">🔁</div>
 <div class="bigcnt anim" style="--a:{f(t_sad)};--d:{T[2] - t_sad:.2f}s;--from:0;--to:100;top:330px;font-size:96px"></div>
 <div class="cntlab sc" style="{S(t_sad)};top:450px">× «Салом»</div>
 <div class="bubble no-bg pop" style="--a:{f(t_tired)};left:50px;top:520px">😮‍💨 Шумо — хаста</div>
 <div class="bubble ok-bg pop" style="--a:{f(t_pc)};left:280px;top:575px">⚡ Компютер — не</div>
</div>''')
sfx("hit", 0.0, 1.0); sfx("pop", 0.3, 0.6)
for k in range(14): sfx("tick", t_sad + k * (T[2] - t_sad) / 14, 0.35)
sfx("buzz", t_tired, 0.4); sfx("chime", t_pc, 0.8)

# B: спорт 1..10
t1 = WT(5, "як"); t2 = WT(5, "ду"); t3 = WT(5, "се"); t10 = WT(5, "даҳ")
H.append(f'''<div class="sc" style="{S(T[4], T[7] - 0.1)}">
 <div class="emo pop" style="--a:{f(T[4])};left:225px;top:200px;font-size:90px">🏋️</div>
 <div class="bigcnt" style="--n:0;top:320px;animation:count .01s linear {f(t1)} both, c2 .01s linear {f(t2)} forwards, c3 .01s linear {f(t3)} forwards, c10 {t10 - t3 - 0.1:.2f}s steps(7,end) {f(t3 + 0.1)} forwards;--from:1;--to:1"></div>
 <div class="cntlab sc" style="{S(t1)};top:470px">нишаст-хез</div>
 <div class="stamp" style="--a:{f(WT(6, "давр"))};left:160px;top:520px">ДАВР!</div>
</div>''')
sfx("pop", T[4], 0.7)
for x in (t1, t2, t3): sfx("tick2", x, 0.7)
for k in range(7): sfx("tick", t3 + 0.1 + k * (t10 - t3 - 0.1) / 7, 0.5)
sfx("ding", t10, 0.7); sfx("thump", WT(6, "давр"), 1.0)

# C: for — три части
t_for = WT(7, "фор"); t_line = T[8]; t_init = WT(9, "ай"); t_cond = T[10]; t_step = WT(11, "қадам")
L1 = 'for (let i = 1; i <= 10; i++) {'; L2 = '  console.log("Нишаст-хез " + i);'
d1 = typing(t_line, L1); d2 = typing(t_line + d1 + 0.1, L2)
code = (f'<div class="ln"><div class="type" style="--a:{t_line:.2f}s;--d:{d1:.2f}s;--n:{len(L1)}"><span class="kw">for</span> (<span class="hl1" style="--h:{t_init:.2f}s"><span class="kw">let</span> <span class="nm">i</span> = <span class="v">1</span></span>; <span class="hl1" style="--h:{t_cond:.2f}s"><span class="nm">i</span> <span class="op">&lt;=</span> <span class="v">10</span></span>; <span class="hl1" style="--h:{t_step:.2f}s"><span class="nm">i</span>++</span>) {{</div></div>'
        f'<div class="ln"><div class="type" style="--a:{t_line + d1 + 0.1:.2f}s;--d:{d2:.2f}s;--n:{len(L2)}">  console.log(<span class="str">"Нишаст-хез "</span> + <span class="nm">i</span>);</div></div>'
        f'<div class="ln"><div class="type" style="--a:{t_line + d1 + d2 + 0.2:.2f}s;--d:.1s;--n:1">}}</div></div>')
H.append(f'''<div class="sc" style="{S(T[7], T[12] - 0.1)}">
 <div class="pill pop" style="--a:{f(T[7] + 0.3)};top:205px">давр = <code style="font:800 26px 'JetBrains Mono',monospace;color:#B4472E">for</code> <span class="emo" style="position:static;font-size:24px">🔁</span></div>
 <div class="term2 sc" style="{S(t_line - 0.2)};inset:280px 28px auto 28px"><div class="bar"><i></i><i></i><i></i><span>davr.js</span></div><div class="code2" style="font-size:19px">{code}</div></div>
 <div class="qpill c1 pop" style="--a:{f(t_init)};left:40px;top:470px">1 · ОҒОЗ: i = 1</div>
 <div class="qpill c2 pop" style="--a:{f(t_cond)};left:210px;top:520px">2 · ШАРТ: i &lt;= 10</div>
 <div class="qpill c3 pop" style="--a:{f(t_step)};left:330px;top:470px">3 · ҚАДАМ: i++</div>
</div>''')
sfx("hit", t_for, 0.6)
for x in (t_init, t_cond, t_step): sfx("pop", x, 0.8)

# D: i — коробка из урока 1
ta = WT(13, "як"); tb = WT(13, "ду"); tc = WT(13, "се")
H.append(f'''<div class="sc" style="{S(T[12], T[14] - 0.1)}">
 <div class="stage pop" style="--a:{f(T[12])};top:215px">
  <div class="flap l"></div><div class="flap r"></div><div class="back"></div>
  <div class="num" style="animation:dropin .5s cubic-bezier(.4,1.5,.6,1) {f(ta - 0.1)} forwards, flyout .3s ease-in {f(tb - 0.2)} forwards">1</div>
  <div class="num" style="animation:dropin .5s cubic-bezier(.4,1.5,.6,1) {f(tb - 0.1)} forwards, flyout .3s ease-in {f(tc - 0.2)} forwards">2</div>
  <div class="num" style="animation:dropin .5s cubic-bezier(.4,1.5,.6,1) {f(tc - 0.1)} forwards">3</div>
  <div class="front"><div class="tag">i</div></div>
 </div>
 <div class="sticker pop" style="--a:{f(T[12] + 0.4)};left:345px;top:240px">ДАРСИ 1</div>
 <div class="pill pop" style="--a:{f(T[13])};top:520px">ҳар давр: <b style="color:#B4472E">i</b> = 1 → 2 → 3 …</div>
</div>''')
sfx("whoosh", T[12], 0.6); sfx("pop", T[12] + 0.05)
for x in (ta, tb, tc): sfx("thud", x + 0.3, 0.8)

# E: условие из урока 2
t_ok = T[15]; t_end = WT(16, "хотима")
H.append(f'''<div class="sc" style="{S(T[14], T[17] - 0.1)}">
 <div class="val flip" style="--a:{f(T[14])};--b:{f(t_end - 0.4)}">i = <span style="color:#3E7C59">3</span></div>
 <div class="val flipin" style="--a:{f(t_end - 0.15)}">i = <span style="color:#B4472E">11</span></div>
 <div class="diamond pop scan" style="--a:{f(T[14] + 0.3)}"><svg viewBox="0 0 200 120"><polygon points="100,4 196,60 100,116 4,60" fill="#1F3F44"/></svg><span>i &lt;= 10 ?</span></div>
 <svg style="position:absolute;left:0;top:0" width="540" height="640">
  <path class="draw" pathLength="100" d="M200 400 Q150 440 140 480" stroke="#3E7C59" stroke-width="8" style="--len:101;--a:{f(t_ok)};--d:.3s"/>
  <path class="draw" pathLength="100" d="M340 400 Q390 440 400 480" stroke="#B4472E" stroke-width="8" style="--len:101;--a:{f(t_end)};--d:.3s"/>
 </svg>
 <div class="res lit-ok" style="--a0:{f(T[14] + 0.6)};--a:{f(t_ok + 0.25)};left:35px;top:485px">↻ Боз давр</div>
 <div class="res lit-no" style="--a0:{f(T[14] + 0.75)};--a:{f(t_end + 0.25)};left:295px;top:485px">■ Бас</div>
 <div class="sticker pop" style="--a:{f(T[14] + 0.4)};left:380px;top:225px">ДАРСИ 2</div>
</div>''')
sfx("pop", T[14] + 0.3, 0.8); sfx("chime", t_ok + 0.25, 0.9); sfx("buzz", t_end + 0.25, 0.8)

# F: тысяча раз
H.append(f'''<div class="sc" style="{S(T[17], T[18] - 0.1)}">
 <div class="bigcnt anim" style="--a:{f(t_hazor)};--d:1.1s;--from:10;--to:1000;top:250px;color:#B4472E"></div>
 <div class="cntlab sc" style="{S(t_hazor)};top:400px;color:#1F3F44">такрор</div>
 <div class="bubble ink-bg pop" style="--a:{f(WT(17, "камтар"))};left:150px;top:470px;font-size:26px">⚡ &lt; 1 сония</div>
</div>''')
for k in range(16): sfx("tick", t_hazor + k * 0.07, 0.4)
sfx("ding", t_hazor + 1.15, 0.8); sfx("pop", WT(17, "камтар"), 0.7)

# G: в жизни
t_feed = WT(18, "лентаи"); t_game = WT(18, "бозӣ")
cols = ["#E9B949", "#B4472E", "#3E7C59", "#1F3F44", "#E9B949", "#B4472E"]
feed = "".join(f'<i style="background:{c}"></i>' for c in cols * 2)
H.append(f'''<div class="sc" style="{S(T[18], T[19] - 0.1)}">
 <div class="phone3 pop" style="--a:{f(t_feed)}"><div class="feed" style="--a:{f(t_feed)}">{feed}</div></div>
 <div class="game pop" style="--a:{f(t_game)}"><span class="emo">🎮</span>60 кадр / сония</div>
</div>''')
sfx("pop", t_feed, 0.7); sfx("whoosh", t_feed + 0.3, 0.4); sfx("pop", t_game, 0.7)

# H: итог
t_og = WT(19, "оғоз"); t_sh = WT(19, "шарт"); t_qd = WT(19, "қадам")
H.append(f'''<div class="sc" style="{S(T[19], T[20] - 0.1)}">
 <div class="formula" style="top:290px;flex-wrap:wrap;row-gap:14px"><div class="ftile dark pop" style="--a:{f(T[19])}">ДАВР</div><div class="fop pop" style="--a:{f(T[19] + 0.2)}">=</div>
  <div class="ftile pop" style="--a:{f(t_og)};border-color:#3E7C59">оғоз</div><div class="fop pop" style="--a:{f(t_og + 0.2)}">+</div>
  <div class="ftile pop" style="--a:{f(t_sh)};border-color:#E9B949">шарт</div><div class="fop pop" style="--a:{f(t_sh + 0.2)}">+</div>
  <div class="ftile pop" style="--a:{f(t_qd)};border-color:#B4472E">қадам</div></div>
</div>''')
for x in (T[19], t_og, t_sh, t_qd): sfx("pop", x, 0.7)

# I: квиз
t_sj = WT(20, "санҷиш"); t_q = WT(20, "чанд")
QL = 'for (let i = 0; i < 3; i++) {'
H.append(f'''<div class="sc" style="{S(T[20] - 0.05, T[22] - 0.1)}">
 <div class="banner" style="--a:{f(t_sj)}">САНҶИШ</div>
 <div class="term2 pop" style="--a:{f(WT(20, "сифр"))};top:320px;left:28px;right:180px"><div class="bar"><i></i><i></i><i></i></div><div class="code2" style="font-size:15px"><div class="ln"><span class="kw">for</span> (<span class="kw">let</span> <span class="nm">i</span> = <span class="v">0</span>; <span class="nm">i</span> &lt; <span class="v">3</span>; <span class="nm">i</span>++) {{</div><div class="ln">  console.log(<span class="str">"Салом"</span>);</div><div class="ln">}}</div></div></div>
 <div class="quizq pop" style="--a:{f(t_q)};left:350px;top:320px;transform:scale(.85)"><svg width="170" height="170"><circle cx="85" cy="85" r="70" fill="#FFFDF8" stroke="#E3D9C7" stroke-width="10"/><circle class="cring" cx="85" cy="85" r="70" fill="none" stroke="#B4472E" stroke-width="10" style="--a:{f(t_q)};--d:{E[21] - t_q:.2f}s"/></svg><b>?</b></div>
 <div class="bubble ink-bg pop" style="--a:{f(T[21])};left:110px;top:540px;font-size:20px">💬 Ҷавоб дар шарҳ <span class="dots"><i></i><i></i><i></i></span></div>
</div>''')
sfx("riser", t_sj - 1.0, 0.6); sfx("hit", t_sj, 1.0); sfx("pop", WT(20, "сифр"), 0.6)
for k in range(int((E[21] - t_q) / 0.5)): sfx("tick", t_q + k * 0.5, 0.8)
sfx("pop", T[21], 0.7)

# J: следующий урок и подписка
t_sub = WT(23, "обуна"); T_CLICK = t_sub + 0.8
H.append(f'''<div class="sc" style="{S(T[22])}">
 <div class="lesson pop" style="--a:{f(T[22] + 0.05)}"><small>ДАРСИ 4</small><b>Рӯйхат</b><code>array [ ]</code></div>
 <div class="sub pop" style="--a:{f(t_sub)}"><span class="b1" style="--a:{f(T_CLICK)}">Обуна шавед</span><span class="b2" style="--a:{f(T_CLICK)}">Обуна шудед ✓</span><i class="press" style="--a:{f(T_CLICK)}"></i></div>
 <svg class="cursor" style="--a:{f(t_sub + 0.1)};--c:{f(T_CLICK)}" width="34" height="40" viewBox="0 0 24 28"><path d="M2 2l19 11-8.5 1.8L17 24l-3.6 1.6-4.4-9.2L2 22z" fill="#1F3F44" stroke="#fff" stroke-width="1.5"/></svg>
</div>''')
sfx("whoosh", T[22], 0.8); sfx("pop", t_sub, 0.8); sfx("click", T_CLICK, 1.2); sfx("chime", T_CLICK + 0.1, 0.9)

css = open('style.css').read() + "@keyframes c2 { to { --n:2; } } @keyframes c3 { to { --n:3; } } @keyframes c10 { from { --n:3; } to { --n:10; } }"
body = f'''<div class="cam" style="animation:{cam_anim}">
<div class="hdr"><span>ШАҲРИЁР ЮНУСОВ</span><span>03 / БАРНОМАСОЗӢ</span></div>
{"".join(title_html)}
{"".join(H)}
{"".join(cap_html)}
</div>
{flash_html}
<div class="prog" style="--d:{END:.2f}s"></div>'''
open('reel.html', 'w').write(f'<!doctype html><html lang="tg"><head><meta charset="utf-8"><style>{css}</style></head><body>{body}</body></html>')
json.dump(dict(end=END, sfx=SFX), open('sfx.json', 'w'), indent=0)
print(END, len(SFX), len(chunks))
