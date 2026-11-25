# Ролик «Зеҳни сунъӣ барои барномасоз» — стили «VS Code Dark + бунафш». Тайминг: timelineA.json.
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
KW = {"зеҳни", "сунъӣ", "ёвар", "ҷонишин", "масъулият", "хато", "санҷед", "бифаҳмед", "дақиқ", "иҷро", "чаро", "ислоҳ", "матн"}
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

# ===== помощники кода =====
def code_ln(html, h=22): return f'<div class="ln" style="height:{h}px">{html}</div>'
FN = '<span class="k">function</span> <span class="f">add</span>(<span class="p">a</span>, <span class="p">b</span>) { <span class="c">return</span> <span class="p">a</span> + <span class="p">b</span>; }'
FN_RAW = 'function add(a, b) { return a + b; }'
def ide(top, a, fname, code_html, term_html="", h=None):
    return (f'<div class="ide pop" style="--a:{a:.2f}s;top:{top}px"><div class="bar"><i></i><i></i><i></i><span>{fname}</span></div>'
            f'<div class="code" style="font-size:13.5px;padding:10px 14px">{code_html}</div>{term_html}</div>')
def term(lines): return '<div class="term" style="font-size:14px;line-height:1.7;padding:8px 14px">' + "".join(lines) + '</div>'
def tline(a, cmd, out, ok=True, d=0.9):
    col = "var(--ok)" if ok else "var(--err)"
    return (f'<div class="ln" style="height:24px;opacity:0;animation:fadein .1s {f(a)} both"><span class="pr">&gt;</span> {cmd}</div>'
            f'<div class="ln" style="height:24px;opacity:0;animation:fadein .1s {f(a + d)} both;color:{col};font-weight:800">{out}</div>')

# ===== A: ХУК (0..PRE[2]) =====
p0, p1, p2 = PRE
KICK = lambda txt, top=104: f'<div class="kicker" style="top:{top}px">{txt}</div>'
scene(0, p2['start'] - 0.1, f'''{KICK("ДАРСИ 13 · ЗЕҲНИ СУНЪӢ")}
<div class="fl" style="--a:0.3s;left:110px;top:230px;font-size:100px">🤖</div>
<div class="fl" style="--a:0.6s;left:330px;top:230px;font-size:100px">🧑‍💻</div>
<div class="fl" style="--a:1.4s;left:238px;top:270px;font:900 80px var(--mono);color:var(--pink)">?</div>
<div class="pill err pop" style="--a:{p0['start'] + 2.0:.2f}s;top:420px;font-size:20px;padding:11px 26px">ҷои барномасозро мегирад?</div>
<div class="pill ok pop" style="--a:{p1['start'] + 0.3:.2f}s;top:500px;font-size:22px;padding:11px 26px">Не — агар дуруст истифода баред ✅</div>''', whoosh=False)
sfx("hit", 0.3, 0.7); sfx("pop", 0.6, 0.6); sfx("pop", 1.4, 0.7); sfx("pop", p0['start'] + 2.0, 0.6); sfx("ding", p1['start'] + 0.3, 0.7)
scene(p2['start'] - 0.1, T[0] - 0.1, f'''<div class="slam" style="--a:{p2['start']:.2f}s;top:210px;font-size:42px;color:var(--white)">ЗЕҲНИ СУНЪӢ<br><span class="acc">ЁВАР, НА ҶОНИШИН</span></div>
<div class="fl" style="--a:{p2['start'] + 0.4:.2f}s;left:222px;top:420px;font-size:90px">🤝</div>''', whoosh=True)
sfx("hit", p2['start'], 0.9); sfx("chime", p2['start'] + 0.4, 0.6)

# ===== B: ЁВАРИ ҶАВОН (T0..T3) =====
t_fast = WT(1, "зуд"); t_err = WT(1, "хато"); t_chk = WT(2, "месанҷед")
scene(T[0] - 0.1, T[3] - 0.1, f'''{KICK("ЁВАРИ ҶАВОН")}
<div class="fl" style="--a:{T[0] + 0.3:.2f}s;left:70px;top:190px;font-size:80px">🧑‍💼</div>
<div class="abs fade" style="--a:{T[0] + 0.3:.2f}s;left:78px;top:290px;font:800 13px var(--mono);color:var(--muted)">ёвар</div>
<div class="pill ok pop" style="--a:{t_fast:.2f}s;top:200px;left:230px;right:auto;margin:0;font-size:17px">⚡ хеле зуд</div>
<div class="pill err pop" style="--a:{t_err:.2f}s;top:255px;left:230px;right:auto;margin:0;font-size:17px">⚠ баъзан хато</div>
<div class="fl" style="--a:{T[2] + 0.2:.2f}s;left:330px;top:370px;font-size:80px">🧑‍💻</div>
<div class="abs fade" style="--a:{T[2] + 0.2:.2f}s;left:338px;top:470px;font:800 13px var(--mono);color:var(--muted)">шумо</div>
<div class="pill acc2 pop" style="--a:{t_chk:.2f}s;top:400px;left:36px;right:auto;margin:0;font-size:18px">🔍 месанҷед ✓</div>''')
sfx("pop", T[0] + 0.3, 0.6); sfx("pop", t_fast, 0.6); sfx("pop", t_err, 0.6); sfx("pop", T[2] + 0.2, 0.6); sfx("ding", t_chk, 0.6)

# ===== C: ЗС = ЁВАР (T3..T5) =====
t_resp = WT(4, "масъулият")
scene(T[3] - 0.1, T[5] - 0.1, f'''{KICK("ЗЕҲНИ СУНЪӢ ҲАМ ҲАМИН ТАВР")}
<div class="fl" style="--a:{T[3] + 0.2:.2f}s;left:215px;top:190px;font-size:96px">🤖</div>
<div class="card pop" style="--a:{WT(4, 'ёвари'):.2f}s;left:50px;right:50px;top:340px;text-align:center;font:800 21px Inter;color:var(--white)">⚡ ёвари зудкор</div>
<div class="card pop" style="--a:{t_resp:.2f}s;left:50px;right:50px;top:430px;text-align:center;font:800 21px Inter;color:var(--purple)">масъулият = <span class="acc">шумо</span></div>''')
sfx("pop", T[3] + 0.2, 0.7); sfx("pop", WT(4, 'ёвари'), 0.7); sfx("pop", t_resp, 0.8); sfx("chime", t_resp + 0.1, 0.5)

# ===== D: КОД (T5..T11) =====
t_ask = T[6]; t_code = T[7] + 0.2; t_ok = T[8]; t_run = T[9]
bubble = f'<div class="card pop" style="--a:{t_ask:.2f}s;left:30px;right:30px;top:140px;padding:12px 16px;font:700 15px Inter;color:var(--white)">🧑‍💻 Функсия бинавис, ки ду рақамро ҷамъ мекунад</div>'
scene(T[5] - 0.1, T[11] - 0.1, f'''{KICK("МИСОЛ")}
{bubble}
<div class="fl" style="--a:{t_code - 0.2:.2f}s;left:42px;top:226px;font-size:34px">🤖</div>
{ide(280, T[7], "add.js", code_ln(TYP(t_code, 1.6, FN, FN_RAW)), term([tline(t_run, 'add(25, 1)', '26 ✓', True, 0.7)]))}
<div class="pill ok pop" style="--a:{t_ok:.2f}s;top:520px;font-size:18px">ба назар дуруст аст ✅</div>''')
sfx("pop", t_ask, 0.6); sfx("pop", T[7], 0.6); sfx("ding", t_ok, 0.7)
sfx("click", t_run, 0.8); sfx("ding", t_run + 0.7, 0.7); sfx("pop", T[10], 0.5)

# ===== E: ХАТО (T11..T14) =====
t_str = WT(11, "матн"); t_bad = T[12]
scene(T[11] - 0.1, T[14] - 0.1, f'''{KICK("ЯК ҲОЛАТИ ДИГАР")}
{ide(150, T[11], "add.js", code_ln(FN), term([tline(t_bad - 0.7, 'add("25", 1)', '251 ✗', False, 0.7)]))}
<div class="pill err pop" style="--a:{t_str:.2f}s;top:380px;font-size:18px">"25" — матн</div>
<div class="fl" style="--a:{t_bad + 0.2:.2f}s;left:215px;top:450px;font-size:70px">😱</div>
<div class="pill pop" style="--a:{T[13]:.2f}s;top:560px;font-size:16px;border-color:var(--purple);color:var(--purple)">дарси 8 · матн + рақам = пайвастшавӣ</div>''')
sfx("pop", T[11], 0.6); sfx("pop", t_str, 0.6); sfx("click", t_bad - 0.7, 0.8); sfx("hit", t_bad + 0.05, 0.9); sfx("pop", t_bad + 0.2, 0.6); sfx("pop", T[13], 0.6)

# ===== F: ИСЛОҲ (T14..T16) =====
t_num = WT(15, "нампер")
scene(T[14] - 0.1, T[16] - 0.1, f'''{KICK("ХАТОИ ЗС НЕСТ")}
<div class="card pop" style="--a:{T[14] + 0.1:.2f}s;left:40px;right:40px;top:150px;text-align:center;padding:14px;font:700 17px Inter;color:var(--white)">дар хоҳиш ишора нашуд ⚠</div>
{ide(260, T[15] - 0.2, "add.js", code_ln(FN), term([tline(t_num, 'add(<span class="f">Number</span>(<span class="s">"25"</span>), 1)', '26 ✓', True, 0.7)]))}
<div class="pill ok pop" style="--a:{t_num + 0.8:.2f}s;top:500px;font-size:18px">шумо ёфтед ва ислоҳ кардед ✅</div>''')
sfx("pop", T[14] + 0.1, 0.6); sfx("pop", T[15] - 0.2, 0.6); sfx("click", t_num, 0.8); sfx("ding", t_num + 0.7, 0.7); sfx("chime", t_num + 0.9, 0.5)

# ===== G: СЕ ҚОИДА (T16..T22) =====
rules = [("1", "дақиқ пурс", "чӣ мехоҳӣ ва бо кадом маълумот", T[17]), ("2", "хон ва фаҳм", "чизи нофаҳмо — мондан не", T[18]), ("3", "иҷро кун ва санҷ", "рақам, матн, холӣ", T[19])]
rc = ""
for k, (n, a, b, ti) in enumerate(rules):
    rc += (f'<div class="rrow pop" style="--a:{ti:.2f}s;position:absolute;left:36px;right:36px;top:{150 + k * 105}px"><span class="e" style="font:900 28px var(--mono);color:var(--purple)">{n}</span><div><b>{a}</b><small>{b}</small></div></div>')
    sfx("pop", ti, 0.7)
t_why = WT(20, "чаро")
scene(T[16] - 0.1, T[22] - 0.1, f'''{KICK("СЕ ҚОИДА")}
{rc}
<div class="card pop" style="--a:{T[20]:.2f}s;left:40px;right:40px;top:470px;padding:10px 16px;font:700 15px Inter;color:var(--white)">🧑‍💻 Чаро ин хато шуд?</div>
<div class="card pop" style="--a:{T[21]:.2f}s;left:40px;right:40px;top:535px;padding:10px 16px;font:700 15px Inter;color:var(--purple)">🤖 Чунки "25" матн аст…</div>''')
sfx("whoosh", T[16], 0.4); sfx("pop", T[20], 0.6); sfx("pop", T[21], 0.6)

# ===== H: ХУЛОСА (T22..T23) =====
scene(T[22] - 0.1, T[23] - 0.1, f'''{KICK("ХУЛОСА")}
<div class="h1 pop" style="--a:{T[22] + 0.05:.2f}s;top:190px;font-size:44px">ЗЕҲНИ СУНЪӢ<br>менависад</div>
<div class="h1 acc pop" style="--a:{WT(22, 'шумо'):.2f}s;top:340px;font-size:44px">шумо мефаҳмед<br>ва месанҷед</div>
<div class="fl" style="--a:{WT(22, 'шумо'):.2f}s;left:222px;top:500px;font-size:70px">✅</div>''')
sfx("hit", T[22] + 0.05, 0.7); sfx("pop", WT(22, 'шумо'), 0.7); sfx("chime", WT(22, 'шумо') + 0.2, 0.6)

# ===== I: САНҶИШ (T23..T26) =====
scene(T[23] - 0.1, T[26] - 0.1, f'''{KICK("САНҶИШ")}
{ide(150, T[23] + 0.1, "add.js", code_ln(FN), term([f'<div class="ln" style="height:24px"><span class="pr">&gt;</span> add(<span class="s">"10"</span>, 5)</div>', f'<div class="ln" style="height:24px;color:var(--purple);font-weight:900">???</div>']))}
<div class="h1 acc pop" style="--a:{T[23] + 1.0:.2f}s;top:360px;font-size:80px">?</div>
<div class="pill pop" style="--a:{T[24]:.2f}s;top:470px;font-size:18px;border-color:var(--purple);color:var(--purple)">«10» — матн</div>
<div class="pill acc2 pop" style="--a:{T[25]:.2f}s;top:540px;font-size:18px">ҷавобро дар шарҳ нависед 👇</div>''')
sfx("hit", T[23] + 0.1, 0.6); sfx("pop", T[23] + 1.0, 0.8); sfx("pop", T[24], 0.6); sfx("pop", T[25], 0.7)

# ===== J: YOUTUBE (T26..T27) =====
t_vid = WT(26, "видеои"); t_link = WT(26, "силка")
scene(T[26] - 0.1, T[27] - 0.1, f'''{KICK("ВИДЕОИ ПУРРА")}
<div class="card pop" style="--a:{t_vid:.2f}s;left:40px;right:40px;top:150px;padding:0;overflow:hidden">
 <div style="height:150px;background:linear-gradient(135deg,#2a1f45,#1E1E1E);display:flex;align-items:center;justify-content:center"><div style="width:68px;height:48px;border-radius:12px;background:#F4443C;color:#fff;font-size:24px;line-height:48px;text-align:center">▶</div></div>
 <div style="padding:10px 18px"><div style="font:800 17px Inter;color:var(--white)">Зеҳни сунъӣ барои барномасоз</div><div style="font:600 12px Inter;color:var(--muted);margin-top:3px">видеои пурра · YouTube</div></div></div>
<div class="fl" style="--a:{t_link:.2f}s;left:250px;top:350px;font-size:42px;color:var(--purple)">↓</div>
<div class="card pop" style="--a:{t_link + 0.2:.2f}s;left:50px;right:50px;top:420px;display:flex;align-items:center;gap:14px">
 <div style="width:54px;height:54px;border-radius:50%;background:var(--accent)"></div>
 <div><div style="font:800 17px Inter;color:var(--white)">@shahriyor_yunusov</div><div style="font:700 13px Inter;color:var(--purple);margin-top:3px">🔗 пайванд дар Био</div></div></div>''')
sfx("pop", t_vid, 0.7); sfx("whoosh", t_link, 0.5); sfx("pop", t_link + 0.2, 0.7); sfx("chime", t_link + 0.3, 0.6)

# ===== K: ОБУНА (T27..END) =====
scene(T[27] - 0.1, END + 5, f'''{KICK("БАРНОМАСОЗӢ АЗ СИФР")}
<div class="h1 pop" style="--a:{T[27] + 0.05:.2f}s;top:190px;font-size:56px">13 <span class="acc">/ 13</span></div>
<div class="fl" style="--a:{T[27] + 0.4:.2f}s;left:222px;top:300px;font-size:80px">🎓</div>
<div class="pill acc2 pop" style="--a:{WT(27, 'обуна'):.2f}s;top:440px;font-size:22px;padding:12px 30px">🔔 Обуна шавед</div>''')
sfx("hit", T[27] + 0.05, 0.7); sfx("pop", T[27] + 0.4, 0.7); sfx("pop", WT(27, 'обуна'), 0.8); sfx("ding", WT(27, 'обуна') + 0.1, 0.6)

html = f'''<!doctype html><html lang="tg"><head><meta charset="utf-8"><link rel="stylesheet" href="style.css"></head><body>
{"".join(H)}
{"".join(cap_html)}
</body></html>'''
open('reel.html', 'w', encoding='utf-8').write(html)
json.dump(dict(end=END, sfx=SFX), open('sfx.json', 'w'))
print('END', END, 'sfx', len(SFX), 'captions', len(cap_html))
