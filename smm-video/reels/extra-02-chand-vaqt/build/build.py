# Ролик «Дар чанд вақт барномасоз шудан мумкин аст?» — стили «VS Code Dark + бунафш». Тайминг: timelineA.json.
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
KW = {"вақт", "дақиқа", "рӯз", "забон", "20", "каме,", "бефосила", "мунтазам", "ҳар"}
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

ERR = "color:var(--err)"
FN = lambda s: f'<span class="f">{s}</span>'

# ===== ХУК: савол + се вариант (0..T0) =====
p0 = PRE[0]
t_h = WT(0, "ҳафта", 0, p0); t_m = WT(0, "моҳ", 0, p0); t_s = WT(0, "сол", 0, p0)
scene(0, T[0] - 0.1, f'''
<div class="kicker" style="top:100px">САВОЛ</div>
<div class="h1 pop" style="--a:0.15s;top:140px;font-size:44px">Дар чанд вақт<br><span class="acc">барномасоз шудан?</span></div>
<div class="card pop" style="--a:{t_h:.2f}s;left:70px;right:70px;top:340px;text-align:center;font:900 40px 'Segoe UI';color:var(--white)">1 ҳафта?</div>
<div class="card pop" style="--a:{t_m:.2f}s;left:70px;right:70px;top:440px;text-align:center;font:900 40px 'Segoe UI';color:var(--white)">1 моҳ?</div>
<div class="card pop" style="--a:{t_s:.2f}s;left:70px;right:70px;top:540px;text-align:center;font:900 40px 'Segoe UI';color:var(--white)">1 сол?</div>''', whoosh=False)
sfx("hit", 0.0, 0.8); sfx("pop", 0.15, 0.7)
for t_ in (t_h, t_m, t_s): sfx("pop", t_, 0.8)

# ===== ҶАВОБ (T0..T1) =====
scene(T[0] - 0.1, T[1] - 0.1, f'''
<div class="slam acc" style="--a:{T[0]:.2f}s;top:230px;font-size:50px;line-height:1.15;padding:0 24px">Ин аз худи<br>Шумо вобаста ҳаст!</div>
<div class="emo pop" style="--a:{T[0] + 0.3:.2f}s;position:absolute;left:0;right:0;top:470px;text-align:center;font-size:84px">🫵</div>''')
sfx("hit", T[0], 0.9); sfx("chime", T[0] + 0.3, 0.6)

# ===== МИСОЛ: ЗАБОНИ НАВ (T1..T4) =====
t_lu = WT(2, "луғат"); t_yod = WT(2, "ёд"); t_b = WT(3, "бист"); t_j = WT(3, "ҷумла")
scene(T[1] - 0.1, T[4] - 0.1, f'''
<div class="kicker" style="top:110px">МИСОЛ</div>
<div class="card pop" style="--a:{T[1] + 0.05:.2f}s;left:60px;right:60px;top:150px;display:flex;align-items:center;gap:16px"><span class="emo" style="font-size:44px">📖</span><div style="font:800 22px 'Segoe UI';color:var(--white)">забони нав омӯхтан</div></div>
<div class="card pop" style="--a:{t_lu:.2f}s;left:40px;right:40px;top:260px;text-align:center;border-color:var(--err)"><div style="font:800 12px var(--mono);letter-spacing:2px;color:var(--muted)">1 РӮЗ</div><div style="font:900 30px 'Segoe UI';color:var(--white);margin-top:4px">3 соат · баъд 7 рӯз нест</div></div>
<div class="pill err pop" style="--a:{t_yod:.2f}s;top:385px;font-size:19px">ҳама чиз аз ёд меравад ❌</div>
<div class="card pop" style="--a:{t_b:.2f}s;left:40px;right:40px;top:460px;text-align:center;border-color:var(--ok)"><div style="font:800 12px var(--mono);letter-spacing:2px;color:var(--muted)">ҲАР РӮЗ</div><div style="font:900 30px 'Segoe UI';color:var(--white);margin-top:4px">20 дақиқа</div></div>
<div class="pill ok pop" style="--a:{t_j:.2f}s;top:585px;font-size:19px">як моҳ баъд — ҷумла ✅</div>''')
sfx("pop", T[1] + 0.05, 0.7); sfx("pop", t_lu, 0.7); sfx("buzz", t_yod, 0.6); sfx("pop", t_b, 0.7); sfx("chime", t_j, 0.7)

# ===== ДАР БАРНОМАСОЗӢ ҲАМ (T4..T6) =====
t_z = WT(5, "забони", 0); t_k = WT(5, "компютер")
cl = FN("console") + "." + FN("log") + '(<span class="s">"Салом, ҷаҳон!"</span>);'
cr = 'console.log("Салом, ҷаҳон!");'
scene(T[4] - 0.1, T[6] - 0.1, f'''
<div class="kicker" style="top:110px">ДАР БАРНОМАСОЗӢ ҲАМ ҲАМИН ТАВР</div>
<div class="ide" style="top:160px"><div class="bar"><i></i><i></i><i></i><span>salom.js</span></div><div class="code" style="font-size:16px"><div class="ln">{TYP(T[4] + 0.15, 1.6, cl, cr)}</div></div></div>
<div class="term abs fade" style="left:20px;right:20px;top:245px;border-radius:12px;border:1px solid var(--line);--a:{T[5] - 0.2:.2f}s"><div class="ln"><span class="pr">&gt; </span><span class="out" style="--a:{T[5]:.2f}s;display:inline">Салом, ҷаҳон!</span></div></div>
<div class="pill acc2 pop" style="--a:{t_k:.2f}s;top:360px;font-size:21px;padding:11px 26px">💻 забони компютер</div>''')
sfx("pop", T[4] + 0.1, 0.5); sfx("ding", T[5], 0.6); sfx("pop", t_k, 0.8)

# ===== ҚАДАМИ 1: АСОСҲО (T6..T9) =====
chips = [("let", "тағйирёбанда", WT(7, "тағйирёбанда")), ("if", "шарт", WT(7, "шарт")), ("for", "давр", WT(7, "давр")), ("[ ]", "рӯйхат", WT(7, "рӯйхат")), ("function", "функсия", WT(7, "функсия"))]
chs = ""
for k, (c, n_, ti) in enumerate(chips):
    chs += f'<div class="card pop" style="--a:{ti:.2f}s;left:50px;right:50px;top:{225 + k * 66}px;padding:10px 18px;display:flex;justify-content:space-between;align-items:center"><span style="font:800 20px var(--mono);color:var(--kw)">{c}</span><span style="font:700 19px \'Segoe UI\';color:var(--white)">{n_}</span></div>'
    sfx("pop", ti, 0.7)
scene(T[6] - 0.1, T[9] - 0.1, f'''
<div class="slam acc" style="--a:{T[6]:.2f}s;top:100px;font-size:48px">1 · АСОСҲО 🔤</div>
<div class="pill ok pop" style="--a:{WT(7, 'як'):.2f}s;top:175px;font-size:18px">аз 1 то 3 моҳ</div>
{chs}
<div class="pill acc2 pop" style="--a:{T[8] + 0.1:.2f}s;top:585px;font-size:19px;padding:10px 24px">«алифбо»-и барномасозӣ</div>''')
sfx("hit", T[6], 0.8); sfx("pop", WT(7, 'як'), 0.6); sfx("chime", T[8] + 0.1, 0.6)

# ===== ҚАДАМИ 2: БАРНОМАИ ХУРД (T9..T12) =====
t_r = WT(11, "рӯйхати"); t_hr = WT(11, "харид")
scene(T[9] - 0.1, T[12] - 0.1, f'''
<div class="slam acc" style="--a:{T[9]:.2f}s;top:100px;font-size:34px">2 · БАРНОМАИ ХУРД 🛠</div>
<div class="pill ok pop" style="--a:{T[10]:.2f}s;top:190px;font-size:18px">боз 2–3 моҳ</div>
<div class="card pop" style="--a:{t_r:.2f}s;left:60px;right:60px;top:270px;font:700 22px/2.1 'Segoe UI';color:var(--white)"><div style="font:800 12px var(--mono);letter-spacing:2px;color:var(--purple)">РӮЙХАТИ ХАРИД</div>
<div class="fade" style="--a:{t_r + 0.2:.2f}s">☑ <s style="color:var(--muted)">нон</s></div><div class="fade" style="--a:{t_r + 0.5:.2f}s">☐ шир</div><div class="fade" style="--a:{t_hr:.2f}s">☐ себ</div></div>
<div class="pill acc2 pop" style="--a:{t_hr + 0.3:.2f}s;top:510px;font-size:19px">барномаи худатон ✨</div>''')
sfx("hit", T[9], 0.8); sfx("pop", T[10], 0.6); sfx("pop", t_r, 0.7); sfx("tick", t_r + 0.2, 0.5); sfx("tick", t_r + 0.5, 0.5); sfx("chime", t_hr + 0.3, 0.6)

# ===== ҚАДАМИ 3: ҲАР РӮЗ (T12..T14) =====
t_20 = WT(12, "бист"); t_pr = WT(12, "барномаи")
dots = ""
for k in range(28):
    dots += f'<i class="pop" style="--a:{T[12] + 0.2 + k * 0.07:.2f}s;width:26px;height:26px;border-radius:50%;background:var(--accent);display:block"></i>'
    if k % 3 == 0: sfx("tick", T[12] + 0.2 + k * 0.07, 0.4)
scene(T[12] - 0.1, T[14] - 0.1, f'''
<div class="slam acc" style="--a:{T[12]:.2f}s;top:100px;font-size:48px">3 · ҲАР РӮЗ ⏱</div>
<div class="pill acc2 pop" style="--a:{t_20:.2f}s;top:190px;font-size:22px;padding:11px 28px">20 дақиқа</div>
<div class="card" style="left:50px;right:50px;top:270px;padding:18px;animation:popin .45s cubic-bezier(.3,1.6,.5,1) {f(T[12] + 0.1)} both"><div style="display:grid;grid-template-columns:repeat(7,1fr);gap:10px;justify-items:center">{dots}</div></div>
<div class="pill pop" style="--a:{t_pr:.2f}s;top:500px;font-size:19px;border-color:var(--purple);color:var(--purple)">кор дар болои барномаи шахсӣ</div>
<div class="emo pop" style="--a:{T[13]:.2f}s;position:absolute;left:0;right:0;top:575px;text-align:center;font-size:64px">☕</div>''')
sfx("hit", T[12], 0.8); sfx("pop", t_20, 0.7); sfx("pop", t_pr, 0.6); sfx("chime", T[13], 0.7)

# ===== ХУЛОСА (T14..T15) =====
scene(T[14] - 0.1, T[15] - 0.1, f'''
<div class="kicker" style="top:130px">ХУЛОСА</div>
<div class="h1 pop" style="--a:{T[14] + 0.05:.2f}s;top:170px;font-size:50px">ҲАР РӮЗ<br><span class="acc">20 ДАҚИҚА</span></div>
<div class="card pop" style="--a:{WT(14, 'каме'):.2f}s;left:80px;right:80px;top:380px;text-align:center;font:800 24px 'Segoe UI';color:var(--white)">каме</div>
<div class="card pop" style="--a:{WT(14, 'бефосила'):.2f}s;left:80px;right:80px;top:455px;text-align:center;font:800 24px 'Segoe UI';color:var(--white)">бефосила</div>
<div class="card pop" style="--a:{WT(14, 'мунтазам'):.2f}s;left:80px;right:80px;top:530px;text-align:center;font:800 24px 'Segoe UI';color:var(--white)">мунтазам</div>''')
sfx("hit", T[14] + 0.05, 0.7)
for w_ in ("каме", "бефосила", "мунтазам"): sfx("pop", WT(14, w_), 0.7)
sfx("chime", WT(14, 'мунтазам') + 0.3, 0.6)

# ===== САВОЛ (T15..T17) =====
opts = [("10", WT(15, "даҳ")), ("20", WT(15, "бист")), ("30", WT(15, "сӣ"))]
oc = ""
for k, (n_, ti) in enumerate(opts):
    oc += f'<div class="card pop" style="--a:{ti:.2f}s;left:{30 + k * 160}px;width:140px;top:300px;text-align:center"><div style="font:900 44px var(--mono);color:var(--white)">{n_}</div><div style="font:700 14px \'Segoe UI\';color:var(--muted)">дақиқа</div></div>'
    sfx("pop", ti, 0.7)
scene(T[15] - 0.1, T[17] - 0.1, f'''
<div class="kicker" style="top:140px">САВОЛ</div>
<div class="h1 pop" style="--a:{T[15] + 0.05:.2f}s;top:175px;font-size:40px">Чанд дақиқа<br>дар рӯз?</div>
{oc}
<div class="pill ok pop" style="--a:{T[16]:.2f}s;top:470px">💬 ҷавобро дар шарҳ нависед</div>''')
sfx("hit", T[15] + 0.05, 0.7); sfx("pop", T[16], 0.6)

# ===== ДАЪВАТ БА ШАРҲ (T17..T18) =====
t_vid = WT(17, "шпаргалкаи"); t_dir = WT(17, "директ")
kw_raw = "ВАҚТ"
scene(T[17] - 0.1, T[18] - 0.1, f'''
<div class="kicker" style="top:140px">ШАРҲ → DIRECT</div>
<div class="card pop" style="--a:{T[17] + 0.05:.2f}s;left:40px;right:40px;top:190px;display:flex;align-items:center;gap:14px">
 <div style="width:38px;height:38px;border-radius:50%;background:var(--accent)"></div>
 <div style="flex:1;background:#1E1E1E;border:1px solid var(--line);border-radius:999px;padding:11px 16px;font:700 17px var(--mono);color:var(--white)">{TYP(T[17] + 0.15, 1.0, kw_raw, kw_raw)}</div>
 <div style="font-weight:800;color:var(--purple)">➤</div></div>
<div class="card pop" style="--a:{t_vid:.2f}s;left:40px;right:40px;top:300px;padding:0;overflow:hidden">
 <div style="height:150px;background:linear-gradient(135deg,#2a1f45,#1E1E1E);display:flex;align-items:center;justify-content:center;font-size:64px" class="emo">📘</div>
 <div style="padding:12px 18px"><div style="font:800 18px 'Segoe UI';color:var(--white)">Шпаргалки бепул</div><div style="font:600 13px 'Segoe UI';color:var(--muted);margin-top:3px">дарсҳои 1–5 · PDF</div></div></div>
<div class="pill acc2 pop" style="--a:{t_dir:.2f}s;top:520px">✉ ба Direct мефиристам</div>''')
sfx("pop", T[17] + 0.05, 0.7); sfx("pop", t_vid, 0.7); sfx("chime", t_dir, 0.8); sfx("ding", t_dir + 0.1, 0.5)

# ===== ОБУНА (T18..END) =====
scene(T[18] - 0.1, END + 5, f'''
<div class="kicker" style="top:150px">БАРНОМАСОЗӢ АЗ СИФР</div>
<div class="h1 pop" style="--a:{T[18] + 0.05:.2f}s;top:200px;font-size:50px"><span class="acc">Ҳар рӯз</span><br>каме пеш</div>
<div class="pill acc2 pop" style="--a:{T[18] + 0.8:.2f}s;top:410px;font-size:22px;padding:13px 32px">🔔 Обуна шавед</div>
<div class="pill pop" style="--a:{T[18] + 1.1:.2f}s;top:480px;font-size:17px;font-family:var(--mono)">@shahriyor_yunusov</div>''')
sfx("hit", T[18] + 0.05, 0.7); sfx("pop", T[18] + 0.8, 0.8); sfx("ding", T[18] + 0.9, 0.6); sfx("pop", T[18] + 1.1, 0.6)

html = f'''<!doctype html><html lang="tg"><head><meta charset="utf-8"><link rel="stylesheet" href="style.css"></head><body>
{"".join(H)}
{"".join(cap_html)}
</body></html>'''
open('reel.html', 'w', encoding='utf-8').write(html)
json.dump(dict(end=END, sfx=SFX), open('sfx.json', 'w'))
print('END', END, 'sfx', len(SFX), 'captions', len(cap_html))
