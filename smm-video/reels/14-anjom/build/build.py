# Ролик «Силсила тамом шуд — калкулятор» — стили «VS Code Dark + бунафш». Тайминг: timelineA.json.
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
KW = {"дарс", "калкулятор", "лоиҳа", "функсия", "шарт", "хато", "саҳифа", "амал", "дебаг", "алифбо"}
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

# ===== A: ХУК (0..PRE[2]) =====

KICK = lambda txt, top=104: f'<div class="kicker" style="top:{top}px">{txt}</div>'
p0, p1, p2 = PRE
# ===== A: ХУК =====
scene(0, p2['start'] - 0.1, f'''{KICK("БАРНОМАСОЗӢ АЗ СИФР")}
<div class="slam" style="--a:{p0['start'] + 0.1:.2f}s;top:200px;font-size:150px;color:var(--white)">13</div>
<div class="h1 acc pop" style="--a:{p0['start'] + 0.5:.2f}s;top:370px;font-size:44px">дарс — тамом!</div>
<div class="fl" style="--a:{p0['start'] + 1.0:.2f}s;left:222px;top:450px;font-size:90px">🎓</div>
<div class="pill ok pop" style="--a:{p1['start'] + 0.3:.2f}s;top:590px;font-size:20px;padding:11px 26px">силсила тамом шуд ✅</div>''', whoosh=False)
sfx("hit", p0['start'] + 0.1, 0.9); sfx("pop", p0['start'] + 0.5, 0.6); sfx("chime", p0['start'] + 1.0, 0.7); sfx("ding", p1['start'] + 0.3, 0.7)
scene(p2['start'] - 0.1, T[0] - 0.1, f'''<div class="slam" style="--a:{p2['start']:.2f}s;top:230px;font-size:46px;color:var(--white)">ШУМО ЧӢ<br><span class="acc">ОМӮХТЕД?</span></div>
<div class="fl" style="--a:{p2['start'] + 0.3:.2f}s;left:222px;top:420px;font-size:90px">🎒</div>''')
sfx("hit", p2['start'], 0.8)

# ===== B: ЧӢ ОМӮХТЕД (T0..T5) =====
chips = [("let", "тағйирёбанда", 0, 'k'), ("if", "шарт", 0, 'c'), ("for", "давр", 0, 'c'), ("[ ]", "рӯйхат", 0, 'n'),
         ("function", "функсия", 0, 'f'), ("{ }", "объект", 0, 's'),
         ("🐞", "дебаг", 1, 'e'), ("📝", "лоиҳа", 2, 'e'), ("&lt;/&gt;", "эйч", 3, 'k'), ("🎨", "си-эс", 3, 'e'), ("🌐", "сайт", 3, 'e'), ("🤖", "зеҳни", 4, 'e')]
labels = ["тағйирёбанда", "шарт", "давр", "рӯйхат", "функсия", "объект", "дебаг", "лоиҳа", "HTML", "CSS", "сайт", "зеҳни сунъӣ"]
cc = ""
for k, (sym, pre, si, cls) in enumerate(chips):
    ti = WT(si, pre)
    col, row = k % 3, k // 3
    inner = f'<span class="emo" style="font-size:30px">{sym}</span>' if cls == 'e' else f'<span class="{cls}" style="font:800 20px var(--mono)">{sym}</span>'
    cc += (f'<div class="fcd pop" style="--a:{ti:.2f}s;left:{20 + col * 170}px;top:{150 + row * 108}px;width:155px;padding:12px 6px">{inner}<b style="font-size:13px">{labels[k]}</b></div>')
    sfx("pop", ti, 0.55)
scene(T[0] - 0.1, T[5] - 0.1, f'{KICK("13 ДАРС")}{cc}')

# ===== C: ИН КАМ НЕСТ (T5..T7) =====
scene(T[5] - 0.1, T[7] - 0.1, f'''{KICK("ИН КАМ НЕСТ!")}
<div class="card pop" style="--a:{WT(6, 'код'):.2f}s;left:40px;right:40px;top:170px;font:800 20px Inter;color:var(--white)">💻 код менависед <span style="color:var(--ok)">✓</span></div>
<div class="card pop" style="--a:{WT(6, 'хатоҳоро'):.2f}s;left:40px;right:40px;top:260px;font:800 20px Inter;color:var(--white)">🐞 хатоҳоро меёбед <span style="color:var(--ok)">✓</span></div>
<div class="card pop" style="--a:{WT(6, 'барномаи'):.2f}s;left:40px;right:40px;top:350px;font:800 20px Inter;color:var(--white)">📱 барномаи хурд месозед <span style="color:var(--ok)">✓</span></div>''')
sfx("hit", T[5], 0.7)
for w_ in ('код', 'хатоҳоро', 'барномаи'): sfx("pop", WT(6, w_), 0.7); sfx("chime", WT(6, w_) + 0.05, 0.4)

# ===== D: ВАҚТИ АМАЛ (T7..T10) =====
scene(T[7] - 0.1, T[10] - 0.1, f'''<div class="slam" style="--a:{T[7]:.2f}s;top:200px;font-size:46px;color:var(--white)">ВАҚТИ<br><span class="acc">АМАЛ!</span></div>
<div class="fl" style="--a:{T[7] + 0.3:.2f}s;left:222px;top:400px;font-size:90px">⚡</div>
<div class="pill pop" style="--a:{WT(8, 'кор'):.2f}s;top:530px;font-size:18px;border-color:var(--purple);color:var(--purple)">барномасозӣ = кор</div>
<div class="card pop" style="--a:{WT(9, 'лоиҳаи'):.2f}s;left:70px;right:70px;top:600px;text-align:center;font:900 22px Inter;color:var(--white)">📦 як лоиҳаи ҳақиқӣ</div>''')
sfx("hit", T[7], 0.9); sfx("chime", T[7] + 0.3, 0.6); sfx("pop", WT(8, 'кор'), 0.6); sfx("pop", WT(9, 'лоиҳаи'), 0.7)

# ===== E: КАЛКУЛЯТОР (T10..T13) =====
keys = "789÷456×123−0.=+"
kb = "".join(f'<div style="height:38px;border-radius:10px;background:{"var(--accent)" if k in "÷×−+=" else "#34343A"};color:{"#1E1E1E" if k in "÷×−+=" else "#fff"};font:800 18px var(--mono);text-align:center;line-height:38px">{k}</div>' for k in keys)
calc = (f'<div class="card pop" style="--a:{T[10] + 0.1:.2f}s;left:130px;width:280px;top:140px;padding:14px"><div style="background:#16161a;border-radius:10px;padding:8px 12px;text-align:right;font:800 28px var(--mono);color:var(--ok);margin-bottom:10px">12 × 5 = 60</div>'
        f'<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px">{kb}</div></div>')
steps = [("1", "функсияҳо", "функсияҳо"), ("2", "шарт ва хатоҳо", "шарт"), ("3", "тугмаҳо дар саҳифа", "тугмаҳо")]
sc_ = ""
for k, (n, a, pre) in enumerate(steps):
    ti = WT(11, pre); sfx("pop", ti, 0.6)
    sc_ += f'<div class="rrow pop" style="--a:{ti:.2f}s;position:absolute;left:36px;right:36px;top:{440 + k * 62}px;padding:8px 16px"><span class="e" style="font:900 22px var(--mono);color:var(--purple);width:30px">{n}</span><b style="font-size:16px">{a}</b></div>'
t_more = WT(11, 'илова')
sc_ += f'<div class="pill pop" style="--a:{t_more:.2f}s;top:640px;font-size:15px;border-color:var(--purple);color:var(--purple)">…ва боз чизҳои нав</div>'
sfx("pop", t_more, 0.6)
scene(T[10] - 0.1, T[13] - 0.1, f'''{calc}
<div class="slam" style="--a:{WT(10, 'калкулятор'):.2f}s;top:80px;font-size:30px;color:var(--white);z-index:2"><span class="acc">КАЛКУЛЯТОР</span></div>{sc_}''')
sfx("hit", WT(10, 'калкулятор'), 0.9); sfx("pop", T[10] + 0.1, 0.6); sfx("chime", WT(10, 'калкулятор') + 0.2, 0.6)

# ===== F: ХУЛОСА (T13..T14) =====
scene(T[13] - 0.1, T[14] - 0.1, f'''{KICK("ХУЛОСА")}
<div class="h1 pop" style="--a:{T[13] + 0.05:.2f}s;top:190px;font-size:40px">КАЛКУЛЯТОР</div>
<div class="h1 acc pop" style="--a:{WT(13, 'функсия'):.2f}s;top:260px;font-size:34px">= функсия + шарт</div>
<div class="h1 acc pop" style="--a:{WT(13, 'хато'):.2f}s;top:320px;font-size:34px">+ хато + саҳифа</div>''')
sfx("hit", T[13] + 0.05, 0.7); sfx("pop", WT(13, 'функсия'), 0.6); sfx("pop", WT(13, 'хато'), 0.6); sfx("chime", WT(13, 'хато') + 0.3, 0.6)

# ===== G: САВОЛ (T14..T16) =====
nums = "".join(f'<div class="pop" style="--a:{T[14] + 0.6 + k * 0.08:.2f}s;width:78px;height:62px;border-radius:14px;background:var(--panel);border:1.5px solid var(--line);font:900 24px var(--mono);color:var(--purple);text-align:center;line-height:62px">{k + 1}</div>' for k in range(13))
scene(T[14] - 0.1, T[16] - 0.1, f'''{KICK("САВОЛ")}
<div class="h1 pop" style="--a:{T[14] + 0.1:.2f}s;top:150px;font-size:32px;padding:0 30px">Кадом дарс аз ҳама душвор буд?</div>
<div style="position:absolute;left:36px;right:36px;top:290px;display:flex;flex-wrap:wrap;gap:12px;justify-content:center">{nums}</div>
<div class="pill acc2 pop" style="--a:{T[15]:.2f}s;top:560px;font-size:18px">рақамашро дар шарҳ нависед 👇</div>''')
sfx("hit", T[14] + 0.1, 0.6); sfx("pop", T[15], 0.8)
for k in range(13): sfx("tick2", T[14] + 0.6 + k * 0.08, 0.25)

# ===== H: YOUTUBE (T16..T17) =====
t_vid = WT(16, "видеоҳои"); t_link = WT(16, "силка")
scene(T[16] - 0.1, T[17] - 0.1, f'''{KICK("ВИДЕОҲОИ ПУРРА")}
<div class="card pop" style="--a:{t_vid:.2f}s;left:40px;right:40px;top:150px;padding:0;overflow:hidden">
 <div style="height:150px;background:linear-gradient(135deg,#2a1f45,#1E1E1E);display:flex;align-items:center;justify-content:center"><div style="width:68px;height:48px;border-radius:12px;background:#F4443C;color:#fff;font-size:24px;line-height:48px;text-align:center">▶</div></div>
 <div style="padding:10px 18px"><div style="font:800 17px Inter;color:var(--white)">Барномасозӣ аз сифр · 13 дарс</div><div style="font:600 12px Inter;color:var(--muted);margin-top:3px">видеоҳои пурра · YouTube</div></div></div>
<div class="fl" style="--a:{t_link:.2f}s;left:250px;top:350px;font-size:42px;color:var(--purple)">↓</div>
<div class="card pop" style="--a:{t_link + 0.2:.2f}s;left:50px;right:50px;top:420px;display:flex;align-items:center;gap:14px">
 <div style="width:54px;height:54px;border-radius:50%;background:var(--accent)"></div>
 <div><div style="font:800 17px Inter;color:var(--white)">@shahriyor_yunusov</div><div style="font:700 13px Inter;color:var(--purple);margin-top:3px">🔗 пайванд дар Био</div></div></div>''')
sfx("pop", t_vid, 0.7); sfx("whoosh", t_link, 0.5); sfx("pop", t_link + 0.2, 0.7); sfx("chime", t_link + 0.3, 0.6)

# ===== I: ОБУНА (T17..END) =====
scene(T[17] - 0.1, END + 5, f'''{KICK("ҲАФТАИ ОЯНДА")}
<div class="fl" style="--a:{T[17] + 0.1:.2f}s;left:222px;top:170px;font-size:90px">🧮</div>
<div class="h1 pop" style="--a:{T[17] + 0.3:.2f}s;top:310px;font-size:46px"><span class="acc">КАЛКУЛЯТОР</span></div>
<div class="pill acc2 pop" style="--a:{WT(17, 'обуна'):.2f}s;top:450px;font-size:22px;padding:12px 30px">🔔 Обуна шавед</div>''')
sfx("hit", T[17] + 0.1, 0.7); sfx("pop", T[17] + 0.3, 0.7); sfx("pop", WT(17, 'обуна'), 0.8); sfx("ding", WT(17, 'обуна') + 0.1, 0.6)

html = f'''<!doctype html><html lang="tg"><head><meta charset="utf-8"><link rel="stylesheet" href="style.css"></head><body>
{"".join(H)}
{"".join(cap_html)}
</body></html>'''
open('reel.html', 'w', encoding='utf-8').write(html)
json.dump(dict(end=END, sfx=SFX), open('sfx.json', 'w'))
print('END', END, 'sfx', len(SFX), 'captions', len(cap_html))
