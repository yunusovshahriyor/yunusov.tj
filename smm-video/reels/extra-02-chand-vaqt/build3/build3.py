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
KW = {"вақт", "дақиқа", "рӯз", "забон", "20", "каме,", "бефосила", "мунтазам"}
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

LIGHT = []
HANDLE = '<div class="handle"><span class="ig"></span>@SHAHRIYOR_YUNUSOV</div>'
DGLOW = '<div class="glow fade" style="--a:0s;width:520px;height:520px;left:10px;top:150px;background:radial-gradient(circle,rgba(43,107,255,.75),rgba(20,50,150,.35) 55%,transparent 72%)"></div>'
FN = lambda s: f'<span style="color:#FFE08A">{s}</span>'

def sc3(a, b, body, light=False, whoosh=True):
    if light: LIGHT.append((a, b))
    bg = '<div class="bgl"></div>' if light else '<div class="bgd"></div>'
    H.append(f'<div class="sc{" l" if light else ""}" style="{S(a, b)}">{bg}{body}{HANDLE}</div>')
    if whoosh: sfx("whoosh", a - 0.05, 0.35)

# ===== 1 · ХУК (0..T0) — торик =====
p0 = PRE[0]
t_h = WT(0, "ҳафта", 0, p0); t_m = WT(0, "моҳ", 0, p0); t_s = WT(0, "сол", 0, p0)
sc3(0, T[0] - 0.1, f'''
{DGLOW}
<div class="glass bob" style="left:-40px;top:300px;width:200px;height:120px;rotate:-12deg;opacity:.35;filter:blur(2px)"></div>
<div class="glass bob" style="right:-50px;top:420px;width:210px;height:130px;rotate:10deg;opacity:.35;filter:blur(2px)"></div>
<div class="title rise" style="--a:0.2s;top:150px">Дар чанд вақт<br>барномасоз шудан мумкин?</div>
<div class="glass pop" style="--a:0.5s;left:185px;top:290px;width:170px;height:170px;border-radius:46px;display:flex;align-items:center;justify-content:center;box-shadow:0 0 90px rgba(43,107,255,.8),0 30px 70px rgba(0,0,0,.5),inset 0 1px 0 rgba(255,255,255,.35)"><div class="num bob" style="font-size:130px">?</div></div>
<div class="pillg rise" style="--a:{t_h:.2f}s;left:60px;top:520px">⏱ 1 ҳафта</div>
<div class="pillg rise" style="--a:{t_m:.2f}s;left:205px;top:560px">📅 1 моҳ</div>
<div class="pillg rise" style="--a:{t_s:.2f}s;left:350px;top:520px">🗓 1 сол</div>''', whoosh=False)
sfx("pop", 0.5, 0.6)
for t_ in (t_h, t_m, t_s): sfx("tick2", t_, 0.35); sfx("pop", t_ + 0.05, 0.5)

# ===== 2 · ҶАВОБ (T0..T1) — сабук =====
w_kh = WT(0, "худи"); w_vo = WT(0, "вобаста")
sc3(T[0] - 0.1, T[1] - 0.1, f'''
<div class="glow fade" style="--a:{T[0]:.2f}s;width:480px;height:480px;left:30px;top:200px;background:radial-gradient(circle,rgba(110,240,205,.9),rgba(110,240,205,.25) 60%,transparent 72%)"></div>
<div class="title rise" style="--a:{T[0]:.2f}s;top:160px;font-size:40px">Ин аз худи Шумо</div>
<div class="title rise" style="--a:{w_vo:.2f}s;top:210px;font-size:40px">вобаста ҳаст</div>
<div class="abs pop" style="--a:{T[0] + 0.2:.2f}s;left:190px;top:330px;width:160px;height:160px;border-radius:80px;background:rgba(255,255,255,.82);border:1px solid #fff;display:flex;align-items:center;justify-content:center;box-shadow:0 0 70px rgba(53,224,181,.7),0 26px 60px rgba(60,90,130,.2)"><span class="emo wig" style="--a:{T[0] + 0.5:.2f}s;font-size:74px;display:block">🫵</span></div>
<div class="pillg pop" style="--a:{w_vo + 0.2:.2f}s;left:60px;top:540px">🎯 ҳадаф</div>
<div class="pillg pop" style="--a:{w_vo + 0.35:.2f}s;left:190px;top:580px">⏱ вақт</div>
<div class="pillg pop" style="--a:{w_vo + 0.5:.2f}s;left:320px;top:540px">💪 одат</div>''')
sfx("pop", T[0] + 0.2, 0.7); sfx("chime", w_vo, 0.5)
for k in range(3): sfx("tick", w_vo + 0.2 + k * 0.15, 0.4)

# ===== 3 · ЗАБОНИ НАВ (T1..T4) — торик =====
t_se = WT(2, "се"); t_hf = WT(2, "ҳафта"); t_yod = WT(2, "ёд"); t_hr = WT(3, "ҳар"); t_b = WT(3, "бист"); t_j = WT(3, "ҷумла")
sc3(T[1] - 0.1, T[4] - 0.1, f'''
{DGLOW}
<div class="title rise" style="--a:{T[1]:.2f}s;top:140px">Забони нав омӯхтан</div>
<div class="glass glin" style="--a:{T[2]:.2f}s;left:36px;right:36px;top:215px;height:200px;border-color:rgba(255,77,109,.45)">
 <div class="abs" style="left:22px;top:18px;font:600 15px 'Segoe UI';color:#FF8DA1">1 РӮЗ · 3 СОАТ, БАЪД 7 РӮЗ НЕСТ</div>
 <div class="abs num blurin" style="--a:{t_se:.2f}s;left:22px;top:46px;font-size:64px">3 соат</div>
 <div class="abs" style="left:22px;right:22px;top:128px"><div class="bar"><i class="shrinkx" style="--a:{t_hf:.2f}s;--d:{max(0.6, t_yod - t_hf + 0.8):.2f}s;width:14%;background:linear-gradient(90deg,#FF4D6D,#FF8DA1)"></i></div><div class="fade" style="--a:{t_yod:.2f}s;font:600 13px 'Segoe UI';opacity:.7;margin-top:8px">хотира → ҳама чиз аз ёд меравад ❌</div></div></div>
<div class="glass glin" style="--a:{t_hr:.2f}s;left:36px;right:36px;top:445px;height:200px;border-color:rgba(53,224,181,.5)">
 <div class="abs" style="left:22px;top:18px;font:600 15px 'Segoe UI';color:#7DF0CF">ҲАР РӮЗ · 20 ДАҚИҚА</div>
 <div class="abs num blurin" style="--a:{t_b:.2f}s;left:22px;top:46px;font-size:64px">20 дақиқа</div>
 <div class="abs" style="left:22px;right:22px;top:128px"><div class="bar"><i class="fillx" style="--a:{t_b:.2f}s;--d:2.2s;width:88%;background:linear-gradient(90deg,#35E0B5,#7DF0CF)"></i></div><div class="fade" style="--a:{t_j:.2f}s;font:600 13px 'Segoe UI';opacity:.7;margin-top:8px">як моҳ баъд — ҷумла 💬✅</div></div></div>''')
sfx("pop", T[2] + 0.1, 0.5); sfx("thud", t_se, 0.7); sfx("buzz", t_yod, 0.45); sfx("pop", t_hr + 0.1, 0.5); sfx("thud", t_b, 0.7); sfx("chime", t_j, 0.6); sfx("ding", t_j + 0.1, 0.4)

# ===== 4 · ДАР БАРНОМАСОЗӢ ҲАМ (T4..T6) — торик =====
t_k = WT(5, "компютер")
cl = FN("console") + "." + FN("log") + '(<span style="color:#FF9A6B">"Салом, ҷаҳон!"</span>);'
cr = 'console.log("Салом, ҷаҳон!");'
sc3(T[4] - 0.1, T[6] - 0.1, f'''
{DGLOW}
<div class="title rise" style="--a:{T[4]:.2f}s;top:140px">Дар барномасозӣ ҳам<br>ҳамин тавр</div>
<div class="glass glin" style="--a:{T[4] + 0.1:.2f}s;left:30px;right:30px;top:260px;height:230px;rotate:-1deg">
 <div class="abs" style="left:18px;top:14px;display:flex;gap:6px"><i style="width:10px;height:10px;border-radius:50%;background:#FF5F57"></i><i style="width:10px;height:10px;border-radius:50%;background:#FEBC2E"></i><i style="width:10px;height:10px;border-radius:50%;background:#28C840"></i></div>
 <div class="abs" style="left:22px;top:52px;font:600 19px var(--mono)">{TYP(T[4] + 0.3, 1.4, cl, cr)}</div>
 <div class="abs fade" style="--a:{T[5]:.2f}s;left:22px;top:110px;font:600 19px var(--mono);color:#7DF0CF">&gt; Салом, ҷаҳон!</div>
 <div class="abs" style="left:22px;right:22px;top:170px"><div class="bar"><i class="fillx" style="--a:{T[5]:.2f}s;--d:1.6s;width:100%;background:linear-gradient(90deg,#2B6BFF,#5B8CFF)"></i></div></div></div>
<div class="chip pop" style="--a:{T[5] + 0.2:.2f}s;left:60px;top:560px">💻</div><div class="chip pop" style="--a:{T[5] + 0.3:.2f}s;left:122px;top:560px">🌐</div><div class="chip pop" style="--a:{T[5] + 0.4:.2f}s;left:184px;top:560px">🧠</div>
<div class="pillg rise" style="--a:{t_k:.2f}s;left:260px;top:566px;background:linear-gradient(90deg,#2B6BFF,#8B5CF6);border:0">забони компютер</div>''')
sfx("pop", T[4] + 0.1, 0.5); sfx("ding", T[5], 0.5); sfx("pop", T[5] + 0.2, 0.4); sfx("thud", t_k, 0.7)

# ===== 5 · СЕ ҚАДАМ (T6..T14) — сабук =====
w_let = WT(7, "тағйирёбанда"); w_if = WT(7, "шарт"); w_for = WT(7, "давр"); w_arr = WT(7, "рӯйхат"); w_fn = WT(7, "функсия"); t_w = WT(11, "рӯйхати"); t_hr2 = WT(11, "харид")
CH = "background:#E8EEFF;color:#2B6BFF;padding:5px 8px;border-radius:8px"
sc3(T[6] - 0.1, T[14] - 0.1, f'''
<div class="glow fade" style="--a:{T[6]:.2f}s;width:420px;height:420px;left:60px;top:260px;background:radial-gradient(circle,rgba(110,240,205,.75),transparent 70%)"></div>
<div class="title rise" style="--a:{T[6]:.2f}s;top:140px">Се қадам</div>
<div class="abs growy" style="--a:{T[6] + 0.2:.2f}s;--d:{T[14] - T[6] - 0.8:.2f}s;left:62px;top:230px;width:4px;height:400px;border-radius:4px;background:linear-gradient(#35E0B5,#8B5CF6)"></div>
<div class="abs pop" style="--a:{T[6] + 0.2:.2f}s;left:52px;top:236px;width:24px;height:24px;border-radius:50%;background:#35E0B5;box-shadow:0 0 0 8px rgba(53,224,181,.25)"></div>
<div class="gl glin" style="--a:{T[6] + 0.3:.2f}s;left:92px;right:30px;top:215px;height:130px;padding:16px 18px"><div style="font:600 13px 'Segoe UI';color:#7a8599">1–3 МОҲ</div><div style="font:700 26px 'Segoe UI Semibold','Segoe UI';margin-top:2px">Асосҳо</div>
<div style="display:flex;gap:6px;margin-top:10px;font:700 12px var(--mono)"><span class="pop" style="--a:{w_let:.2f}s;{CH}">let</span><span class="pop" style="--a:{w_if:.2f}s;{CH}">if</span><span class="pop" style="--a:{w_for:.2f}s;{CH}">for</span><span class="pop" style="--a:{w_arr:.2f}s;{CH}">[ ]</span><span class="pop" style="--a:{w_fn:.2f}s;{CH}">function</span></div></div>
<div class="abs pop" style="--a:{T[9]:.2f}s;left:52px;top:396px;width:24px;height:24px;border-radius:50%;background:#8B5CF6;box-shadow:0 0 0 8px rgba(139,92,246,.22)"></div>
<div class="gl glin" style="--a:{T[9] + 0.05:.2f}s;left:92px;right:30px;top:372px;height:120px;padding:16px 18px"><div style="font:600 13px 'Segoe UI';color:#7a8599">+2–3 МОҲ</div><div style="font:700 26px 'Segoe UI Semibold','Segoe UI';margin-top:2px">Барномаи хурд</div>
<div style="font:600 15px 'Segoe UI';margin-top:8px;color:#4a5468"><span class="fade" style="--a:{t_w:.2f}s">☑ нон</span> &nbsp; <span class="fade" style="--a:{t_w + 0.3:.2f}s">☐ шир</span> &nbsp; <span class="fade" style="--a:{t_hr2:.2f}s">☐ себ</span></div></div>
<div class="abs pop" style="--a:{T[12]:.2f}s;left:52px;top:556px;width:24px;height:24px;border-radius:50%;background:#FFB23A;box-shadow:0 0 0 8px rgba(255,178,58,.25)"></div>
<div class="gl glin" style="--a:{T[12] + 0.05:.2f}s;left:92px;right:30px;top:520px;height:100px;padding:16px 18px"><div style="font:600 13px 'Segoe UI';color:#7a8599">ҲАР РӮЗ</div><div style="font:700 26px 'Segoe UI Semibold','Segoe UI';margin-top:2px">20 дақиқа <span class="emo pop bob" style="--a:{T[13]:.2f}s;display:inline-block">☕</span></div></div>''', light=True)
sfx("pop", T[6] + 0.2, 0.5)
for w_ in (w_let, w_if, w_for, w_arr, w_fn): sfx("tick2", w_, 0.35)
sfx("pop", T[9], 0.6); sfx("ding", t_w, 0.4); sfx("pop", T[12], 0.6); sfx("chime", T[12] + 0.2, 0.5); sfx("pop", T[13], 0.5)

# ===== 6 · СЕРИЯ (T14..каме) — норанҷӣ =====
t_ka = WT(14, "каме")
cells = ""
for k in range(30):
    if k < 24:
        cells += f'<div class="cell" style="--a:{T[14] + 0.5 + k * 0.05:.2f}s;width:34px;height:34px"></div>'
        if k % 3 == 0: sfx("tick", T[14] + 0.5 + k * 0.05, 0.4)
    else:
        cells += '<div style="width:34px;height:34px;border-radius:10px;background:rgba(255,255,255,.08)"></div>'
sc3(T[14] - 0.1, t_ka - 0.15, f'''
<div class="glow fade" style="--a:{T[14]:.2f}s;width:520px;height:520px;left:10px;top:120px;background:radial-gradient(circle,rgba(255,150,40,.7),rgba(120,50,10,.3) 55%,transparent 72%)"></div>
<div class="title rise" style="--a:{T[14]:.2f}s;top:140px">Серияи шумо</div>
<div class="c emo pop bob" style="--a:{T[14] + 0.1:.2f}s;top:200px;font-size:76px">🔥</div>
<div class="c num blurin" style="--a:{T[14] + 0.3:.2f}s;top:300px;font-size:130px">30</div>
<div class="c rise" style="--a:{T[14] + 0.5:.2f}s;top:432px;font:600 20px 'Segoe UI Semibold';opacity:.8">рӯз пай дар пай</div>
<div class="glass glin" style="--a:{T[14] + 0.4:.2f}s;left:30px;right:30px;top:490px;height:120px;padding:16px"><div style="display:grid;grid-template-columns:repeat(10,1fr);gap:6px;justify-items:center">{cells}</div></div>''')
sfx("pop", T[14] + 0.1, 0.5); sfx("thud", T[14] + 0.3, 0.7); sfx("chime", T[14] + 1.9, 0.4)

# ===== 7 · ХУЛОСА (каме..T15) — торик =====
t_be = WT(14, "бефосила"); t_mu = WT(14, "мунтазам")
sc3(t_ka - 0.2, T[15] - 0.1, f'''
{DGLOW}
<div class="title rise" style="--a:{t_ka - 0.1:.2f}s;top:140px">Хулоса</div>
<svg class="abs" style="left:70px;top:210px" width="400" height="400" viewBox="0 0 400 400"><defs><linearGradient id="r" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#35E0B5"/><stop offset="1" stop-color="#5B8CFF"/></linearGradient></defs>
<circle cx="200" cy="200" r="165" fill="none" stroke="rgba(255,255,255,.1)" stroke-width="18"/>
<circle cx="200" cy="200" r="165" fill="none" stroke="url(#r)" stroke-width="18" stroke-linecap="round" stroke-dasharray="1037" stroke-dashoffset="1037" class="ring" style="--a:{t_ka - 0.1:.2f}s;--d:1.6s" transform="rotate(-90 200 200)"/></svg>
<div class="c num blurin" style="--a:{t_ka:.2f}s;top:300px;font-size:150px">20</div>
<div class="c rise" style="--a:{t_ka + 0.2:.2f}s;top:455px;font:600 24px 'Segoe UI Semibold'">дақиқа · ҳар рӯз</div>
<div class="pillg pop" style="--a:{t_ka:.2f}s;left:70px;top:640px">✓ каме</div>
<div class="pillg pop" style="--a:{t_be:.2f}s;left:190px;top:640px">✓ бефосила</div>
<div class="pillg pop" style="--a:{t_mu:.2f}s;left:340px;top:640px">✓ мунтазам</div>''')
sfx("thud", t_ka, 0.7); sfx("pop", t_ka, 0.5); sfx("pop", t_be, 0.5); sfx("pop", t_mu, 0.5); sfx("chime", t_mu + 0.3, 0.6)

# ===== 8 · САВОЛ (T15..T17) — сабук =====
o10 = WT(15, "даҳ"); o20 = WT(15, "бист"); o30 = WT(15, "сӣ")
OPT = "padding:16px 18px;border-radius:16px;background:#F1F4FA;font:600 20px 'Segoe UI Semibold';display:flex;justify-content:space-between"
sc3(T[15] - 0.1, T[17] - 0.1, f'''
<div class="glow fade" style="--a:{T[15]:.2f}s;width:460px;height:460px;left:40px;top:200px;background:radial-gradient(circle,rgba(160,130,255,.7),transparent 70%)"></div>
<div class="title rise" style="--a:{T[15]:.2f}s;top:140px">Савол ба шумо</div>
<div class="gl glin" style="--a:{T[15] + 0.1:.2f}s;left:34px;right:34px;top:230px;height:330px;padding:24px 22px">
 <div style="font:700 28px/1.15 'Segoe UI Semibold','Segoe UI';text-align:center">Чанд дақиқа вақт<br>ҷудо карда метавонед?</div>
 <div style="margin-top:24px;display:flex;flex-direction:column;gap:12px">
  <div class="rise" style="--a:{o10:.2f}s;{OPT}"><span>10 дақиқа</span><span style="opacity:.4">○</span></div>
  <div class="rsel" style="--a:{o20:.2f}s;{OPT}"><span>20 дақиқа</span><span>●</span></div>
  <div class="rise" style="--a:{o30:.2f}s;{OPT}"><span>30 дақиқа</span><span style="opacity:.4">○</span></div></div></div>
<div class="pillg rise" style="--a:{T[16]:.2f}s;left:150px;top:600px">💬 ҷавобро дар шарҳ нависед</div>''', light=True)
sfx("pop", T[15] + 0.1, 0.5)
for t_ in (o10, o20, o30): sfx("tick2", t_, 0.4)
sfx("ding", o20 + 0.2, 0.4); sfx("pop", T[16], 0.5)

# ===== 9 · ДАЪВАТ (T17..T18) — торик =====
t_vid = WT(17, "шпаргалкаи"); t_dir = WT(17, "директ")
sc3(T[17] - 0.1, T[18] - 0.1, f'''
{DGLOW}
<div class="title rise" style="--a:{T[17]:.2f}s;top:140px">Шарҳ → Direct</div>
<div class="glass glin" style="--a:{T[17] + 0.05:.2f}s;left:40px;right:40px;top:230px;height:90px;border-radius:999px;display:flex;align-items:center;padding:0 24px;gap:14px"><div style="width:42px;height:42px;border-radius:50%;background:linear-gradient(135deg,#2B6BFF,#8B5CF6)"></div><div style="font:700 30px 'Segoe UI Semibold';letter-spacing:3px;min-width:110px"><span class="reveal" style="--a:{T[17] + 0.2:.2f}s;--d:0.9s">ВАҚТ</span></div><div style="margin-left:auto;font:700 22px 'Segoe UI';color:#5B8CFF">➤</div></div>
<div class="c rise bob" style="--a:{t_vid - 0.3:.2f}s;top:340px;font-size:34px;color:#5B8CFF">↓</div>
<div class="glass glin" style="--a:{t_vid:.2f}s;left:80px;right:80px;top:400px;height:190px;rotate:-2deg;text-align:center;padding-top:26px"><div class="emo" style="font-size:62px">📘</div><div style="font:700 24px 'Segoe UI Semibold';margin-top:6px">Шпаргалкаи бепул</div><div style="font:500 14px 'Segoe UI';opacity:.65;margin-top:4px">дарсҳои 1–5 · PDF · ба Direct</div></div>
<div class="pillg rise" style="--a:{t_dir:.2f}s;left:180px;top:620px;background:linear-gradient(90deg,#2B6BFF,#8B5CF6);border:0">✉ ба Direct мефиристам</div>''')
sfx("pop", T[17] + 0.05, 0.5); sfx("pop", t_vid, 0.6); sfx("chime", t_dir, 0.6); sfx("ding", t_dir + 0.1, 0.4)

# ===== 10 · ОХИР (T18..END) — торик =====
sc3(T[18] - 0.1, END + 5, f'''
<div class="glow fade" style="--a:{T[18]:.2f}s;width:520px;height:520px;left:10px;top:60px;background:radial-gradient(circle,rgba(139,92,246,.75),rgba(43,107,255,.3) 55%,transparent 72%)"></div>
<div class="glow fade" style="--a:{T[18]:.2f}s;width:360px;height:360px;left:-80px;top:520px;background:radial-gradient(circle,rgba(53,224,181,.5),transparent 70%)"></div>
<div class="c rise" style="--a:{T[18] + 0.05:.2f}s;top:200px;font:600 44px/1.1 'Segoe UI Semibold';letter-spacing:-.6px">Ҳар рӯз</div>
<div class="c num blurin" style="--a:{T[18] + 0.25:.2f}s;top:262px;font-size:76px;letter-spacing:-3px">каме пеш</div>
<div class="glass glin" style="--a:{T[18] + 0.8:.2f}s;left:100px;right:100px;top:420px;height:120px;border-radius:999px;display:flex;align-items:center;justify-content:center;gap:12px"><span class="emo" style="font-size:28px">🔔</span><span style="font:700 24px 'Segoe UI Semibold'">Обуна шавед</span></div>
<div class="c fade" style="--a:{T[18] + 1.1:.2f}s;top:566px;font:700 14px var(--mono);letter-spacing:2px;opacity:.7">@SHAHRIYOR_YUNUSOV</div>''')
sfx("pop", T[18] + 0.05, 0.5); sfx("thud", T[18] + 0.25, 0.7); sfx("pop", T[18] + 0.8, 0.6); sfx("ding", T[18] + 0.9, 0.5)

# ----- субтитр: саҳнаҳои сабук → матни тира -----
def _lt(h):
    a = float(re.search(r'--a:([\d.]+)s', h).group(1))
    return any(x <= a < y for x, y in LIGHT)
cap_html = [h.replace('<div class="cap"', '<div class="cap lt"', 1) if _lt(h) else h for h in cap_html]

html = f'''<!doctype html><html lang="tg"><head><meta charset="utf-8"><link rel="stylesheet" href="style3.css"></head><body>
{"".join(H)}
{"".join(cap_html)}
</body></html>'''
open('reel.html', 'w', encoding='utf-8').write(html)
json.dump(dict(end=END, sfx=SFX), open('sfx.json', 'w'))
print('END', END, 'sfx', len(SFX), 'captions', len(cap_html), 'light', LIGHT)
