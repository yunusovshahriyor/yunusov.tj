# Ролик «Сайт чӣ тавр кор мекунад?» — стили «VS Code Dark + бунафш». Тайминг: timelineA.json.
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
KW = {"браузер", "сервер", "клиент", "дархост", "ҷавоб", "интернет", "санҷиш", "скелет", "либос", "рафтор", "сайт", "network", "html", "css", "javascript"}
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
p0, p1, p2 = PRE
KICK = lambda txt, top=104: f'<div class="kicker" style="top:{top}px">{txt}</div>'
page_html = '<h1 class="t">Вазифаҳо</h1><span class="gbtn">Илова</span>'
scene(0, p2['start'] - 0.1, f'''{KICK("ДАРСИ 12 · САЙТ")}
<div class="brw pop" style="--a:0.3s;top:150px"><div class="tb"><i></i><i></i><i></i><div class="url">🔒 саҳифаи ман</div></div><div class="pg">{page_html}</div></div>
<div class="fl" style="--a:1.2s;left:250px;top:352px;font-size:46px;color:var(--purple)">↓</div>
<div class="fl" style="--a:1.5s;left:230px;top:420px;font-size:90px">📱</div>
<div class="fl" style="--a:{p1['start'] + 0.2:.2f}s;left:330px;top:410px;font:900 70px var(--mono);color:var(--pink)">?</div>
<div class="pill acc2 pop" style="--a:{p1['start'] + 0.9:.2f}s;top:560px;font-size:22px;padding:11px 26px">Чӣ тавр? 🤔</div>''', whoosh=False)
sfx("hit", 0.3, 0.7); sfx("pop", 1.5, 0.6); sfx("pop", p1['start'] + 0.2, 0.7); sfx("pop", p1['start'] + 0.9, 0.7)
scene(p2['start'] - 0.1, T[0] - 0.1, f'''<div class="slam" style="--a:{p2['start']:.2f}s;top:230px;font-size:46px;color:var(--white)">САЙТ ЧӢ ТАВР<br><span class="acc">КОР МЕКУНАД?</span></div>
<div class="fl" style="--a:{p2['start'] + 0.3:.2f}s;left:222px;top:420px;font-size:90px">🌐</div>''', whoosh=True)
sfx("hit", p2['start'], 0.9); sfx("chime", p2['start'] + 0.3, 0.6)

# ===== B: РЕСТОРАН (T0..T3) =====
tg = T[1] + 0.2; tb = T[1] + 1.8
scene(T[0] - 0.1, T[3] - 0.1, f'''{KICK("МИСОЛИ ҲАЁТӣ")}
<div class="abs" style="left:30px;right:30px;top:560px;height:2px;background:var(--line)"></div>
<div class="abs" style="left:318px;top:250px;width:4px;height:310px;background:repeating-linear-gradient(var(--line) 0 10px,transparent 10px 18px)"></div>
<div class="abs fade" style="--a:{T[0] + 0.3:.2f}s;left:30px;top:300px;font-size:70px">🙋</div>
<div class="abs fade" style="--a:{T[0] + 0.3:.2f}s;left:36px;top:500px;font:800 13px var(--mono);color:var(--muted)">меҳмон</div>
<div class="abs fade" style="--a:{T[0] + 0.3:.2f}s;left:70px;top:440px;font-size:46px">🍽️</div>
<div class="abs fade" style="--a:{T[1] + 0.1:.2f}s;left:410px;top:290px;font-size:70px">🧑‍🍳</div>
<div class="abs fade" style="--a:{T[1] + 0.1:.2f}s;left:410px;top:500px;font:800 13px var(--mono);color:var(--muted)">ошхона</div>
<div class="waiter" style="left:110px;top:360px;opacity:0;animation:fadein .1s {f(tg)} both,wgo 1.2s ease-in-out {f(tg)} forwards,gone .2s {f(tg + 1.15)} forwards">🛎️🧾</div>
<div class="waiter" style="left:110px;top:360px;opacity:0;animation:fadein .1s {f(tb)} both,wback 1.2s ease-in-out {f(tb)} forwards,gone .2s {f(tb + 1.15)} forwards">🛎️🍲</div>
<div class="pill ok pop" style="--a:{T[1] + 0.2:.2f}s;top:610px;font-size:16px">официант мебарад ва меорад</div>''')
sfx("pop", T[0] + 0.3, 0.6); sfx("pop", T[1] + 0.1, 0.6); sfx("whoosh", tg, 0.5); sfx("whoosh", tb, 0.5); sfx("ding", tb + 1.1, 0.5)

# ===== C: МУВОФИҚАТ (T3..T6) =====
rows = [("🙋", "меҳмон", "= браузер (клиент)", WT(3, "браузер")), ("🧑‍🍳", "ошхона", "= сервер", WT(4, "сервер")), ("🛎️", "официант", "= интернет", WT(5, "официант"))]
rc = ""
for k, (e, n, m, ti) in enumerate(rows):
    rc += f'<div class="rrow pop" style="--a:{ti:.2f}s;position:absolute;left:36px;right:36px;top:{180 + k * 110}px"><span class="e emo">{e}</span><div><b>{n}</b><small>{m}</small></div></div>'
    sfx("pop", ti, 0.7)
scene(T[3] - 0.1, T[6] - 0.1, f'{KICK("РЕСТОРАН ↔ ИНТЕРНЕТ")}{rc}')
sfx("chime", T[5] + 0.6, 0.5)

# ===== D: ҚАДАМИ 1 — ДАРХОСТ (T6..T8) =====
t_url = WT(6, "юнусов"); t_req = T[7]
def server(top, a, lab="СЕРВЕР"):
    return (f'<div class="srv pop" style="--a:{a:.2f}s;top:{top}px"><span class="ld" style="left:200px"></span><span class="ld" style="left:214px;animation-delay:.3s"></span><div class="lab">{lab}</div></div>')
scene(T[6] - 0.1, T[8] - 0.1, f'''{KICK("ҚАДАМИ 1 · ДАРХОСТ")}
<div class="brw pop" style="--a:{T[6]:.2f}s;top:140px"><div class="tb"><i></i><i></i><i></i><div class="url">🔒 {TYP(t_url, 1.2, "yunusov.tj", "yunusov.tj")}</div></div><div class="pg" style="min-height:70px"></div></div>
{server(470, T[6] + 0.3)}
<div class="pk" style="--a:{t_req:.2f}s;--dy:200px;--d:1.4s;left:176px;top:330px;background:var(--accent);color:#1E1E1E">GET yunusov.tj ↓</div>
<div class="pill err pop" style="--a:{t_req + 0.1:.2f}s;top:600px;font-size:16px">дархост (request)</div>''')
sfx("pop", T[6], 0.6); sfx("whoosh", t_req, 0.6); sfx("pop", t_req + 0.1, 0.6)

# ===== E: ҚАДАМИ 2 — СЕРВЕР ТАЙЁР МЕКУНАД (T8..T9) =====
scene(T[8] - 0.1, T[9] - 0.1, f'''{KICK("ҚАДАМИ 2 · СЕРВЕР")}
{server(330, T[8])}
<div class="fl" style="--a:{T[8] + 0.2:.2f}s;left:225px;top:200px;font-size:60px;animation:popin .4s var(--a) both,spin 1.6s linear {f(T[8] + 0.6)} infinite">⚙️</div>
<div class="fcd pop" style="--a:{T[8] + 1.2:.2f}s;left:30px;top:470px;width:140px"><span class="ic">📄</span><b>index.html</b></div>
<div class="fcd pop" style="--a:{T[8] + 1.7:.2f}s;left:200px;top:470px;width:140px"><span class="ic">📄</span><b>style.css</b></div>
<div class="fcd pop" style="--a:{T[8] + 2.2:.2f}s;left:370px;top:470px;width:140px"><span class="ic">📄</span><b>script.js</b></div>
<div class="pill pop" style="--a:{T[8] + 0.5:.2f}s;top:590px;font-size:15px;border-color:var(--purple)">тайёр мекунад…</div>''')
sfx("pop", T[8], 0.6); sfx("riser", T[8] + 0.2, 0.3)
for d in (1.2, 1.7, 2.2): sfx("pop", T[8] + d, 0.6)

# ===== F: ҚАДАМИ 3 — ҶАВОБ + СЕ ФАЙЛ (T9..T13) =====
t_h, t_c, t_j = WT(11, "скелет"), WT(11, "либос"), WT(11, "рафтор")
t_f1, t_f2, t_f3 = WT(12, "индекс"), WT(12, "стайл"), WT(12, "скрипт")
scene(T[9] - 0.1, T[13] - 0.1, f'''{KICK("ҚАДАМИ 3 · ҶАВОБ")}
<div class="brw pop" style="--a:{T[9]:.2f}s;top:130px"><div class="tb"><i></i><i></i><i></i><div class="url">🔒 yunusov.tj</div></div><div class="pg" style="min-height:60px"></div></div>
{server(520, T[9])}
<div class="pk" style="--a:{T[9] + 0.2:.2f}s;--dy:-170px;--d:1.3s;left:196px;top:500px;background:var(--ok);color:#1E1E1E">200 OK ↑</div>
<div class="pill ok pop" style="--a:{T[9] + 0.3:.2f}s;top:600px;font-size:16px;left:auto;right:36px;margin:0">ҷавоб (response)</div>
<div class="pill pop" style="--a:{T[10]:.2f}s;top:330px;font-size:14px;border-color:var(--purple);color:var(--purple)">дарси 11</div>
<div class="fcd pop" style="--a:{t_h:.2f}s;left:30px;top:380px"><span class="ic emo">🏠</span><b>index.html</b><small>скелет · HTML</small></div>
<div class="fcd pop" style="--a:{t_c:.2f}s;left:195px;top:380px"><span class="ic emo">🎨</span><b>style.css</b><small>либос · CSS</small></div>
<div class="fcd pop" style="--a:{t_j:.2f}s;left:360px;top:380px;width:150px"><span class="ic emo">⚡</span><b>script.js</b><small>рафтор · JS</small></div>''')
sfx("pop", T[9], 0.6); sfx("whoosh", T[9] + 0.2, 0.5); sfx("ding", T[9] + 1.4, 0.7); sfx("pop", T[10], 0.5)
for t_ in (t_h, t_c, t_j): sfx("pop", t_, 0.7); sfx("chime", t_ + 0.05, 0.4)

# ===== G: БРАУЗЕР ҶАМЪ МЕКУНАД (T13..T16) =====
t_s, t_sc = WT(14, "стайл"), WT(14, "скрипт"); t_ask = WT(15, "мепурсад"); t_live = WT(15, "зинда")
html_code = ('<div class="ln"><span class="k">&lt;link</span> <span class="p">rel</span>=<span class="s">"stylesheet"</span> <span class="p">href</span>=<span class="s">"style.css"</span><span class="k">&gt;</span></div>'
             '<div class="ln"><span class="k">&lt;script</span> <span class="p">src</span>=<span class="s">"script.js"</span><span class="k">&gt;&lt;/script&gt;</span></div>')
scene(T[13] - 0.1, T[16] - 0.1, f'''{KICK("БРАУЗЕР ҶАМЪ МЕКУНАД")}
<div class="brw pop" style="--a:{T[13]:.2f}s;top:130px"><div class="tb"><i></i><i></i><i></i><div class="url">🔒 yunusov.tj</div></div>
 <div class="pg" style="min-height:130px">
  <div style="animation:gone .2s {f(t_live)} forwards"><div class="skel">сарлавҳа</div><div class="skel" style="width:90px">тугма</div></div>
  <div style="position:absolute;left:16px;top:38px;opacity:0;animation:fadein .4s {f(t_live)} both"><h1 class="t" style="color:#BD93F9">Вазифаҳо</h1><span class="gbtn">Илова</span></div>
 </div></div>
<div class="ide pop" style="--a:{T[14]:.2f}s;top:330px;left:20px;right:20px"><div class="bar"><i></i><i></i><i></i><span>index.html</span></div><div class="code" style="font-size:11.5px;padding:8px 12px">{html_code.replace('class="ln"', 'class="ln" style="height:20px"')}</div></div>
<div class="pk" style="--a:{t_s:.2f}s;--dy:-90px;--d:1.1s;left:60px;top:560px;background:var(--panel2);border:1.5px solid var(--purple);color:var(--purple)">GET style.css</div>
<div class="pk" style="--a:{t_sc:.2f}s;--dy:-90px;--d:1.1s;left:300px;top:560px;background:var(--panel2);border:1.5px solid var(--pink);color:var(--pink)">GET script.js</div>
{server(590, T[14] + 0.3)}
<div class="pill ok pop" style="--a:{t_live:.2f}s;top:520px;font-size:15px">саҳифаи зинда ✅</div>''')
sfx("pop", T[13], 0.6); sfx("pop", T[14], 0.6); sfx("whoosh", t_s, 0.5); sfx("whoosh", t_sc, 0.5); sfx("ding", t_live, 0.7); sfx("chime", t_live + 0.1, 0.7)

# ===== H: F12 → NETWORK (T16..T17) =====
t_f12 = WT(16, "эф"); t_net = WT(16, "нетворк")
scene(T[16] - 0.1, T[17] - 0.1, f'''{KICK("ХУДАТОН БУБИНЕД")}
<div class="pill acc2 pop" style="--a:{t_f12:.2f}s;top:150px;font:900 24px var(--mono);padding:10px 28px">F12</div>
<div class="dev pop" style="--a:{t_f12 + 0.4:.2f}s;top:240px"><div class="tabs"><span>Elements</span><span>Console</span><span class="on">Network</span><span>Sources</span></div>
 <div class="row h"><span>Name</span><span>Status</span><span>Type</span></div>
 <div class="row fade" style="--a:{t_net:.2f}s"><span>index.html</span><span>200</span><span>document</span></div>
 <div class="row fade" style="--a:{t_net + 0.4:.2f}s"><span>style.css</span><span>200</span><span>stylesheet</span></div>
 <div class="row fade" style="--a:{t_net + 0.8:.2f}s"><span>script.js</span><span>200</span><span>script</span></div></div>
<div class="pill pop" style="--a:{WT(16, 'дархост'):.2f}s;top:450px;border-color:var(--purple);font-size:15px">ҳар дархост ва ҳар ҷавоб — дар рӯйхат</div>''')
sfx("pop", t_f12, 0.7); sfx("click", t_f12, 0.8); sfx("pop", t_f12 + 0.4, 0.6)
for d in (0, 0.4, 0.8): sfx("tick2", t_net + d, 0.4)

# ===== I: ХУЛОСА (T17..T18) =====
scene(T[17] - 0.1, T[18] - 0.1, f'''{KICK("ХУЛОСА")}
<div class="h1 pop" style="--a:{T[17] + 0.05:.2f}s;top:200px;font-size:52px">САЙТ</div>
<div class="h1 acc pop" style="--a:{WT(17, 'дархост'):.2f}s;top:270px;font-size:40px">= дархост + ҷавоб</div>
<div class="card pop" style="--a:{WT(17, 'дархост') + 0.3:.2f}s;left:50px;right:50px;top:380px;text-align:center;font:700 20px Inter;color:var(--white)">🌐 браузер мепурсад ↓<br>🖥️ сервер ҷавоб медиҳад ↑</div>''')
sfx("hit", T[17] + 0.05, 0.7); sfx("pop", WT(17, 'дархост'), 0.7); sfx("chime", WT(17, 'дархост') + 0.3, 0.6)

# ===== J: САНҶИШ (T18..T22) =====
scene(T[18] - 0.1, T[22] - 0.1, f'''{KICK("САНҶИШ")}
<div class="brw pop" style="--a:{T[18] + 0.1:.2f}s;top:140px"><div class="tb"><i></i><i></i><i></i><div class="url">🔒 yunusov.tj</div></div><div class="pg" style="min-height:70px"><span class="gbtn" style="background:#F4443C;animation:press .5s ease-out {f(T[18] + 1.8)} both">❤ Лайк</span></div></div>
<div class="fl" style="--a:{T[18] + 1.9:.2f}s;left:250px;top:330px;font-size:40px;color:var(--purple)">↓</div>
<div class="srv pop" style="--a:{T[18] + 0.3:.2f}s;top:390px;left:150px"><span class="ld" style="left:200px"></span><div class="lab">СЕРВЕР</div></div>
<div class="h1 acc pop" style="--a:{T[19]:.2f}s;top:500px;font-size:80px">?</div>
<div class="card pop" style="--a:{T[19] + 0.3:.2f}s;left:36px;width:215px;top:610px;text-align:center;padding:12px 0;z-index:3"><div style="font:900 22px Inter;color:var(--purple)">дархост</div></div>
<div class="card pop" style="--a:{T[19] + 0.6:.2f}s;left:289px;width:215px;top:610px;text-align:center;padding:12px 0;z-index:3"><div style="font:900 22px Inter;color:var(--purple)">ҷавоб</div></div>''')
sfx("hit", T[18] + 0.1, 0.6); sfx("pop", T[19], 0.8); sfx("pop", T[19] + 0.3, 0.6); sfx("pop", T[19] + 0.6, 0.6); sfx("click", T[18] + 1.8, 0.8); sfx("tick2", T[19], 0.4)

# ===== K: ДАЪВАТ БА YOUTUBE (T22..T23) =====
t_vid = WT(22, "видеои"); t_link = WT(22, "силка")
scene(T[22] - 0.1, T[23] - 0.1, f'''{KICK("ВИДЕОИ ПУРРА")}
<div class="card pop" style="--a:{t_vid:.2f}s;left:40px;right:40px;top:150px;padding:0;overflow:hidden">
 <div style="height:150px;background:linear-gradient(135deg,#2a1f45,#1E1E1E);display:flex;align-items:center;justify-content:center"><div style="width:68px;height:48px;border-radius:12px;background:#F4443C;color:#fff;font-size:24px;line-height:48px;text-align:center">▶</div></div>
 <div style="padding:10px 18px"><div style="font:800 17px Inter;color:var(--white)">Сайт чӣ тавр кор мекунад</div><div style="font:600 12px Inter;color:var(--muted);margin-top:3px">видеои пурра · YouTube</div></div></div>
<div class="fl" style="--a:{t_link:.2f}s;left:250px;top:350px;font-size:42px;color:var(--purple)">↓</div>
<div class="card pop" style="--a:{t_link + 0.2:.2f}s;left:50px;right:50px;top:420px;display:flex;align-items:center;gap:14px">
 <div style="width:54px;height:54px;border-radius:50%;background:var(--accent)"></div>
 <div><div style="font:800 17px Inter;color:var(--white)">@shahriyor_yunusov</div><div style="font:700 13px Inter;color:var(--purple);margin-top:3px">🔗 пайванд дар Био</div></div></div>''')
sfx("pop", t_vid, 0.7); sfx("whoosh", t_link, 0.5); sfx("pop", t_link + 0.2, 0.7); sfx("chime", t_link + 0.3, 0.6)

# ===== L: ДАРСИ ОЯНДА (T23..END) =====
t_sub = SN[24]['start'] + 0.1
scene(T[23] - 0.1, END + 5, f'''{KICK("ДАРСИ ОЯНДА")}
<div class="h1 pop" style="--a:{T[23] + 0.05:.2f}s;top:170px;font-size:56px">13 · <span class="acc">AI</span></div>
<div class="fl" style="--a:{T[23] + 0.4:.2f}s;left:216px;top:270px;font-size:80px">🤖</div>
<div class="card pop" style="--a:{WT(23, 'ёвар'):.2f}s;left:50px;right:50px;top:400px;text-align:center;font:800 21px Inter;color:var(--white)">ёвар, на ҷонишин</div>
<div class="pill acc2 pop" style="--a:{t_sub:.2f}s;top:500px;font-size:20px;padding:12px 30px">🔔 Обуна шавед</div>''')
sfx("hit", T[23] + 0.05, 0.7); sfx("pop", T[23] + 0.4, 0.7); sfx("pop", WT(23, 'ёвар'), 0.7); sfx("pop", t_sub, 0.8); sfx("ding", t_sub + 0.1, 0.6)

html = f'''<!doctype html><html lang="tg"><head><meta charset="utf-8"><link rel="stylesheet" href="style.css"></head><body>
{"".join(H)}
{"".join(cap_html)}
</body></html>'''
open('reel.html', 'w', encoding='utf-8').write(html)
json.dump(dict(end=END, sfx=SFX), open('sfx.json', 'w'))
print('END', END, 'sfx', len(SFX), 'captions', len(cap_html))
