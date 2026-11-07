# Ролик «Хатогӣ ва дебаг» (дарси 8) — стили «VS Code Dark + бунафш». Тайминг: timelineA.json.
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
KW = {"дебаг", "дебаг!", "баг", "бубин", "санҷ", "ислоҳ", "age", "string", "матн"}
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

# ===== ХУК: 25 + 1 = 251?! (0..T0) =====
p0 = PRE[0]
t_251 = WT(0, "дусаду", 0, p0); t_q = WT(0, "чӣ", 0, p0)
scene(0, T[0] - 0.1, f'''
<div class="kicker" style="top:100px">ДАРСИ 8 · ХАТОГӢ ВА ДЕБАГ</div>
<div class="h1 pop" style="--a:0.15s;top:190px;font-size:104px">25 + 1</div>
<div class="h1 pop" style="--a:{t_251:.2f}s;top:330px;font-size:104px;{ERR}">= 251</div>
<div class="pill err pop" style="--a:{t_251 + 0.3:.2f}s;top:500px;font-size:20px">🐞 хато!</div>
<div class="pill acc2 pop" style="--a:{t_q:.2f}s;top:570px;font-size:22px;padding:11px 26px">Чӣ тавр? 🤔</div>''', whoosh=False)
sfx("hit", 0.0, 0.8); sfx("pop", 0.15, 0.7); sfx("buzz", t_251 + 0.1, 0.8); sfx("pop", t_251 + 0.3, 0.6); sfx("pop", t_q, 0.8)

# ===== ДЕБАГ: баг + ёфтан/ислоҳ (T0..T3) =====
t_bag = WT(1, "баг"); t_yo = WT(2, "ёфтан"); t_is = WT(2, "ислоҳ"); t_dg = WT(2, "дебаг")
scene(T[0] - 0.1, T[3] - 0.1, f'''
<div class="slam acc" style="--a:{T[0]:.2f}s;top:100px;font-size:66px">ДЕБАГ!</div>
<div class="card pop" style="--a:{t_bag:.2f}s;left:50px;right:50px;top:230px;display:flex;align-items:center;gap:18px"><span class="emo" style="font-size:54px">🐞</span><div><div style="font:900 30px 'Segoe UI';color:var(--white)">БАГ</div><div style="font:600 15px 'Segoe UI';color:var(--muted);margin-top:3px">хатои барнома</div></div></div>
<div class="pill pop" style="--a:{t_yo:.2f}s;top:380px;font-size:19px;border-color:var(--cyan);color:var(--cyan)">🔍 ёфтан</div>
<div class="pill pop" style="--a:{t_is:.2f}s;top:435px;font-size:19px;border-color:var(--ok);color:var(--ok)">🔧 ислоҳ кардан</div>
<div class="pill acc2 pop" style="--a:{t_dg:.2f}s;top:500px;font-size:20px;padding:11px 26px">ёфтан + ислоҳ = дебаг</div>''')
sfx("hit", T[0], 0.9); sfx("pop", t_bag, 0.8); sfx("pop", t_yo, 0.6); sfx("pop", t_is, 0.6); sfx("chime", t_dg + 0.1, 0.6)

# ===== МИСОЛ: МЕХАНИК (T3..T6) =====
t_mb = WT(5, "мебинад"); t_ms = WT(5, "месанҷад")
scene(T[3] - 0.1, T[6] - 0.1, f'''
<div class="kicker" style="top:130px">МИСОЛ</div>
<div class="card pop" style="--a:{T[3] + 0.05:.2f}s;left:50px;right:50px;top:175px;display:flex;align-items:center;gap:18px"><span class="emo" style="font-size:52px">🚗</span><div style="font:800 20px 'Segoe UI';color:var(--white)">мошин ҳаракат намекунад</div></div>
<div class="pill err pop" style="--a:{T[3] + 0.4:.2f}s;top:300px">⚠️ чароғи хато</div>
<div class="card pop" style="--a:{T[4] + 0.05:.2f}s;left:50px;right:50px;top:365px;display:flex;align-items:center;gap:18px"><span class="emo" style="font-size:52px">🧑‍🔧</span><div style="font:800 20px 'Segoe UI';color:var(--white)">механик</div></div>
<div class="pill pop" style="--a:{t_mb:.2f}s;top:495px;font-size:20px;border-color:var(--cyan);color:var(--cyan)">👀 1 · мебинад</div>
<div class="pill pop" style="--a:{t_ms:.2f}s;top:555px;font-size:20px;border-color:var(--purple);color:var(--purple)">🔍 2 · месанҷад</div>''')
sfx("pop", T[3] + 0.05, 0.7); sfx("buzz", T[3] + 0.4, 0.6); sfx("pop", T[4] + 0.05, 0.7); sfx("pop", t_mb, 0.7); sfx("pop", t_ms, 0.7)

# ===== КОД: let age = "25" + 1 → 251 (T6..T10) =====
t_251b = WT(8, "дусаду"); t_26 = WT(9, "бисту")
l1 = '<span class="k">let</span> <span class="p">age</span> = <span class="s">"25"</span> + <span class="n">1</span>;'
r1 = 'let age = "25" + 1;'
l2 = FN("console") + "." + FN("log") + '(<span class="p">age</span>);'
r2 = 'console.log(age);'
scene(T[6] - 0.1, T[10] - 0.1, f'''
<div class="kicker" style="top:100px">ДАР КОД ҲАМ ҲАМИН ТАВР</div>
<div class="ide" style="top:135px"><div class="bar"><i></i><i></i><i></i><span>bug.js</span></div><div class="code" style="font-size:16px">
<div class="ln">{TYP(T[7] + 0.05, max(0.8, T[8] - T[7] - 0.6), l1, r1)}</div>
<div class="ln">{TYP(T[8] + 0.05, max(0.5, t_251b - T[8] - 0.2), l2, r2)}</div></div></div>
<div class="term abs fade" style="left:20px;right:20px;top:250px;border-radius:12px;border:1px solid var(--line);--a:{T[8] + 0.3:.2f}s"><div class="ln"><span class="pr">&gt; </span><span class="out" style="--a:{t_251b:.2f}s;display:inline;{ERR}">251</span></div></div>
<div class="pill err pop" style="--a:{t_251b + 0.2:.2f}s;top:345px">гирифтем: 251 😱</div>
<div class="pill ok pop" style="--a:{t_26:.2f}s;top:405px">интизор будем: 26</div>''')
sfx("pop", T[6] + 0.1, 0.5); sfx("buzz", t_251b + 0.05, 0.7); sfx("pop", t_251b + 0.2, 0.6); sfx("pop", t_26, 0.7)

# ===== ҚАДАМИ 1: БУБИН (T10..T12) =====
t_gi = WT(11, "гирифтем"); t_me = WT(11, "мехостем")
scene(T[10] - 0.1, T[12] - 0.1, f'''
<div class="slam acc" style="--a:{T[10]:.2f}s;top:100px;font-size:52px">1 · БУБИН 👀</div>
<div class="card pop" style="--a:{t_gi:.2f}s;left:40px;right:40px;top:230px;text-align:center"><div style="font:800 12px var(--mono);letter-spacing:2px;color:var(--muted)">ГИРИФТЕМ</div><div style="font:900 54px var(--mono);color:var(--err);margin-top:6px">251</div></div>
<div class="card pop" style="--a:{t_me:.2f}s;left:40px;right:40px;top:385px;text-align:center;border-color:var(--ok)"><div style="font:800 12px var(--mono);letter-spacing:2px;color:var(--muted)">МЕХОСТЕМ</div><div style="font:900 54px var(--mono);color:var(--ok);margin-top:6px">26</div></div>''')
sfx("hit", T[10], 0.8); sfx("pop", t_gi, 0.8); sfx("pop", t_me, 0.8); sfx("chime", t_me + 0.2, 0.5)

# ===== ҚАДАМИ 2: САНҶ (T12..T15) =====
t_st = WT(13, "стринг"); t_mt = WT(14, "матн")
l3 = FN("console") + "." + FN("log") + '(<span class="k">typeof</span> <span class="p">age</span>)'
r3 = 'console.log(typeof age)'
scene(T[12] - 0.1, T[15] - 0.1, f'''
<div class="slam acc" style="--a:{T[12]:.2f}s;top:100px;font-size:52px">2 · САНҶ 🔍</div>
<div class="ide" style="top:190px"><div class="bar"><i></i><i></i><i></i><span>bug.js</span></div><div class="code" style="font-size:16px"><div class="ln">{TYP(T[13] + 0.05, max(0.8, t_st - T[13] - 0.9), l3, r3)}</div></div></div>
<div class="term abs fade" style="left:20px;right:20px;top:272px;border-radius:12px;border:1px solid var(--line);--a:{T[13] + 0.3:.2f}s"><div class="ln"><span class="pr">&gt; </span><span class="out" style="--a:{t_st:.2f}s;display:inline;color:var(--str)">string</span></div></div>
<div class="box pop" style="--a:{T[14]:.2f}s;left:210px;top:370px"><div class="tag">age</div><div class="num" style="font-size:34px;color:#7a2d00">"25"</div></div>
<div class="pill err pop" style="--a:{t_mt:.2f}s;top:505px;font-size:18px">«25» — матн, на рақам</div>''')
sfx("hit", T[12], 0.8); sfx("ding", t_st + 0.05, 0.7); sfx("pop", T[14], 0.8); sfx("buzz", t_mt, 0.5)

# ===== ҚАДАМИ 3: ИСЛОҲ (T15..T17) =====
t_sh = WT(16, "шаш")
l4 = FN("Number") + '(<span class="s">"25"</span>) + <span class="n">1</span>'
r4 = 'Number("25") + 1'
scene(T[15] - 0.1, T[17] - 0.1, f'''
<div class="slam acc" style="--a:{T[15]:.2f}s;top:100px;font-size:52px">3 · ИСЛОҲ 🔧</div>
<div class="ide" style="top:190px"><div class="bar"><i></i><i></i><i></i><span>bug.js</span></div><div class="code" style="font-size:16px"><div class="ln">{TYP(T[16] + 0.05, max(0.8, t_sh - T[16] - 1.0), l4, r4)}</div></div></div>
<div class="term abs fade" style="left:20px;right:20px;top:272px;border-radius:12px;border:1px solid var(--line);--a:{T[16] + 0.3:.2f}s"><div class="ln"><span class="pr">&gt; </span><span class="out" style="--a:{t_sh:.2f}s;display:inline">26</span></div></div>
<div class="box pop" style="--a:{T[15] + 0.1:.2f}s;left:210px;top:370px"><div class="tag">age</div>
<div class="num" style="position:relative;height:40px;width:100px;text-align:center"><span class="abs" style="left:0;right:0;font-size:34px;color:#7a2d00;animation:gone .2s ease-in {f(t_sh)} forwards">"25"</span><span class="abs pop" style="left:0;right:0;--a:{t_sh + 0.05:.2f}s;color:#7a2d00">26</span></div></div>
<div class="pill ok pop" style="--a:{t_sh + 0.2:.2f}s;top:505px;font-size:18px">ҳоло рақам ✅</div>''')
sfx("hit", T[15], 0.8); sfx("ding", t_sh + 0.05, 0.8); sfx("chime", t_sh + 0.1, 0.7); sfx("pop", t_sh + 0.2, 0.6)

# ===== ХУЛОСА (T17..T18) =====
scene(T[17] - 0.1, T[18] - 0.1, f'''
<div class="kicker" style="top:130px">ХУЛОСА</div>
<div class="h1 pop" style="--a:{T[17] + 0.05:.2f}s;top:170px;font-size:60px"><span class="acc">ДЕБАГ</span></div>
<div class="card pop" style="--a:{WT(17, 'бубин'):.2f}s;left:70px;right:70px;top:290px;text-align:center;font:800 24px 'Segoe UI';color:var(--white)">👀 бубин</div>
<div class="card pop" style="--a:{WT(17, 'санҷ'):.2f}s;left:70px;right:70px;top:370px;text-align:center;font:800 24px 'Segoe UI';color:var(--white)">🔍 санҷ</div>
<div class="card pop" style="--a:{WT(17, 'ислоҳ'):.2f}s;left:70px;right:70px;top:450px;text-align:center;font:800 24px 'Segoe UI';color:var(--white)">🔧 ислоҳ кун</div>''')
sfx("hit", T[17] + 0.05, 0.7)
for w_ in ("бубин", "санҷ", "ислоҳ"): sfx("pop", WT(17, w_), 0.7)
sfx("chime", WT(17, 'ислоҳ') + 0.4, 0.6)

# ===== САНҶИШ (T18..T21) =====
t_c = WT(18, "чӣ")
q1 = 'console.log("10" + 5);'
hq1 = FN("console") + "." + FN("log") + '(<span class="s">"10"</span> + <span class="n">5</span>);'
scene(T[18] - 0.1, T[21] - 0.1, f'''
<div class="kicker" style="top:140px">САНҶИШ</div>
<div class="h1 pop" style="--a:{T[18] + 0.05:.2f}s;top:175px;font-size:40px">чӣ чоп мешавад?</div>
<div class="ide" style="top:250px;left:12px;right:12px"><div class="bar"><i></i><i></i><i></i><span>test.js</span></div>
<div class="code" style="font-size:16px"><div class="ln">{TYP(T[18] + 0.1, 2.2, hq1, q1)}</div></div></div>
<div class="h1 acc pop" style="--a:{t_c:.2f}s;top:380px;font-size:110px">?</div>
<div class="pill pop" style="--a:{T[19]:.2f}s;top:560px;font-size:17px;border-color:var(--str);color:var(--str)">«10» дар қавс — матн</div>
<div class="pill ok pop" style="--a:{T[20]:.2f}s;top:615px">💬 ҷавобро дар шарҳ нависед</div>''')
sfx("hit", T[18] + 0.05, 0.7); sfx("pop", t_c, 0.8); sfx("tick2", t_c, 0.5); sfx("pop", T[19], 0.6); sfx("pop", T[20], 0.6)

# ===== ДАЪВАТ БА ШАРҲ (T21..T22) =====
t_vid = WT(21, "видео"); t_dir = WT(21, "директ")
kw_raw = "ДЕБАГ"
scene(T[21] - 0.1, T[22] - 0.1, f'''
<div class="kicker" style="top:140px">ШАРҲ → DIRECT</div>
<div class="card pop" style="--a:{T[21] + 0.05:.2f}s;left:40px;right:40px;top:190px;display:flex;align-items:center;gap:14px">
 <div style="width:38px;height:38px;border-radius:50%;background:var(--accent)"></div>
 <div style="flex:1;background:#1E1E1E;border:1px solid var(--line);border-radius:999px;padding:11px 16px;font:700 17px var(--mono);color:var(--white)">{TYP(T[21] + 0.15, 1.0, kw_raw, kw_raw)}</div>
 <div style="font-weight:800;color:var(--purple)">➤</div></div>
<div class="card pop" style="--a:{t_vid:.2f}s;left:40px;right:40px;top:300px;padding:0;overflow:hidden">
 <div style="height:170px;background:linear-gradient(135deg,#2a1f45,#1E1E1E);display:flex;align-items:center;justify-content:center"><div style="width:68px;height:48px;border-radius:12px;background:#F4443C;color:#fff;font-size:24px;line-height:48px;text-align:center">▶</div></div>
 <div style="padding:12px 18px"><div style="font:800 18px 'Segoe UI';color:var(--white)">Дарси 8: Хатогӣ ва дебаг</div><div style="font:600 13px 'Segoe UI';color:var(--muted);margin-top:3px">видеои пурраи дарс · YouTube</div></div></div>
<div class="pill acc2 pop" style="--a:{t_dir:.2f}s;top:520px">✉ ба Direct мефиристам</div>''')
sfx("pop", T[21] + 0.05, 0.7); sfx("pop", t_vid, 0.7); sfx("chime", t_dir, 0.8); sfx("ding", t_dir + 0.1, 0.5)

# ===== ДАРСИ ОЯНДА (T22..END) =====
t_sub = SN[23]['start'] + 0.1
scene(T[22] - 0.1, END + 5, f'''
<div class="kicker" style="top:140px">ДАРСИ ОЯНДА</div>
<div class="h1 pop" style="--a:{T[22] + 0.05:.2f}s;top:180px;font-size:52px">9 · <span class="acc">Лоиҳа</span></div>
<div class="card pop" style="--a:{WT(22, 'вазифаҳо'):.2f}s;left:60px;right:60px;top:290px;font:700 19px/2 'Segoe UI';color:var(--white)"><div>☑ <s style="color:var(--muted)">хариди нон</s></div><div>☐ дарси барномасозӣ</div><div>☐ занг ба дӯст</div></div>
<div class="pill acc2 pop" style="--a:{t_sub:.2f}s;top:520px;font-size:20px;padding:12px 30px">🔔 Обуна шавед</div>''')
sfx("hit", T[22] + 0.05, 0.7); sfx("pop", WT(22, 'вазифаҳо'), 0.7); sfx("pop", t_sub, 0.8); sfx("ding", t_sub + 0.1, 0.6)

html = f'''<!doctype html><html lang="tg"><head><meta charset="utf-8"><link rel="stylesheet" href="style.css"></head><body>
{"".join(H)}
{"".join(cap_html)}
</body></html>'''
open('reel.html', 'w', encoding='utf-8').write(html)
json.dump(dict(end=END, sfx=SFX), open('sfx.json', 'w'))
print('END', END, 'sfx', len(SFX), 'captions', len(cap_html))
