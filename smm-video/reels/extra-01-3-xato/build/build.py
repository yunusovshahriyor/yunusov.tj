# Ролик «3 хатои рӯзи аввал» — стили «VS Code Dark + бунафш». Тайминг: timelineA.json.
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
KW = {"хато", "хатои", "хатои", "роҳнамост", "console", "console.log", "console.log(\"салом\".", "syntaxerror", "age", "===", "душман"}
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

# ===== ХУК =====
p0, p1 = PRE
t_se = WT(0, "се", 0, p0)
cards = ""
for k in range(3):
    ta = WT(0, "хато", 0, p0) + 0.15 + k * 0.3
    cards += f'<div class="card pop" style="--a:{ta:.2f}s;left:{50 + k * 160}px;width:140px;top:300px;text-align:center;padding:18px 0;border-color:rgba(244,135,113,.5)"><div style="font:900 44px var(--mono);color:var(--err)">{k + 1}</div><div style="font:800 14px var(--mono);color:var(--muted);margin-top:4px">хато</div></div>'
    sfx("pop", ta, 0.7)
scene(0, T[0] - 0.1, f'''
<div class="kicker" style="top:110px;color:var(--err)">ДАР РӮЗИ АВВАЛ</div>
<div class="slam" style="--a:{t_se:.2f}s;top:150px;font-size:76px;color:var(--white)">3 <span style="color:var(--err)">ХАТО</span></div>
{cards}
<div class="pill err pop" style="--a:{WT(0, 'ташвиш', 0, p0):.2f}s;top:455px">😰 ҳамаро ба ташвиш меорад</div>
<div class="pill acc2 pop" style="--a:{p1['start']:.2f}s;top:520px;font-size:21px;padding:11px 26px">Шумо кадомашро кардед? 🤔</div>''', whoosh=False)
sfx("hit", t_se, 0.9); sfx("buzz", t_se + 0.1, 0.6); sfx("pop", p1['start'], 0.8)

# ===== ХАТОИ 1 (T0..T6) =====
t_if = WT(1, "иф"); t_ba = WT(2, "баробар"); t_q2 = WT(2, "муқоиса"); t_dur = WT(3, "дуруст")
a1 = 'let age = 15;'; a2 = 'if (age = 18) {'; a3 = '  console.log("Калон");'; a4 = '}'
ha1 = '<span class="k">let</span> <span class="p">age</span> = <span class="n">15</span>;'
ha2 = f'<span class="c">if</span> (<span class="p">age</span> <span class="hle" style="--a:{t_ba:.2f}s">=</span> <span class="n">18</span>) {{'
ha3 = '  <span class="f">console</span>.<span class="f">log</span>(<span class="s">"Калон"</span>);'
code1 = (f'<div class="ln">{TYP(T[0] + 0.1, 0.5, ha1, a1)}</div><div class="ln">{TYP(t_if, max(0.8, t_ba - t_if - 0.3), ha2, a2)}</div>'
         f'<div class="ln">{TYP(t_ba, 0.7, ha3, a3)}</div><div class="ln">{TYP(t_ba + 0.7, 0.1, "}", a4)}</div>')
t_out = t_dur - 0.5
fix = (f'<div class="pill ok pop" style="--a:{T[4]:.2f}s;top:560px;font:700 20px var(--mono)"><span class="p">age</span> <span style="color:var(--ok)">===</span> <span class="n">18</span> ✅</div>')
scene(T[0] - 0.1, T[6] - 0.1, f'''
<div class="xnum">ХАТОИ 1</div>
<div class="slam" style="--a:{T[0]:.2f}s;top:128px;font-size:50px;color:var(--err)">= ≠ ===</div>
<div class="ide" style="top:215px"><div class="bar"><i></i><i></i><i></i><span>shart.js</span></div><div class="code" style="font-size:15.5px">{code1}</div></div>
<div class="term abs" style="left:20px;right:20px;top:395px;border-radius:12px;border:1px solid var(--line);animation:fadein .2s {f(t_dur - 0.3)} both"><div class="ln"><span class="pr">$ </span>node shart.js</div><span class="out" style="--a:{t_dur:.2f}s">Калон  <span style="color:var(--err)">← age = 15, вале «Калон»?!</span></span></div>
<div class="pill err pop" style="--a:{t_ba + 0.3:.2f}s;top:520px">= қимат мегузорад, на муқоиса</div>
{fix}''')
sfx("hit", T[0], 0.8); sfx("buzz", t_ba, 0.6); sfx("pop", t_ba + 0.3, 0.6); sfx("ding", t_dur, 0.5); sfx("pop", T[4], 0.7); sfx("chime", T[4] + 0.1, 0.6)

# ===== ХАТОИ 2 (T6..T10) =====
t_k = WT(8, "калон"); t_x = WT(8, "хато"); t_ch1 = WT(9, "хурд"); t_ch2 = WT(9, "калон"); t_ne = WT(9, "ду")
b1 = 'Console.log("Салом");'
hb1 = f'<span class="f"><span class="hle" style="--a:{t_k:.2f}s">C</span>onsole</span>.<span class="f">log</span>(<span class="s">"Салом"</span>);'
scene(T[6] - 0.1, T[10] - 0.1, f'''
<div class="xnum">ХАТОИ 2</div>
<div class="slam" style="--a:{T[6]:.2f}s;top:128px;font-size:60px;color:var(--white)">A ≠ a</div>
<div class="ide" style="top:230px"><div class="bar"><i></i><i></i><i></i><span>salom.js</span></div><div class="code" style="font-size:16px"><div class="ln">{TYP(T[8] + 0.05, 1.2, hb1, b1)}</div></div></div>
<div class="term abs" style="left:20px;right:20px;top:330px;border-radius:12px;border:1px solid var(--line);animation:fadein .2s {f(t_x - 0.2)} both"><span class="out e" style="--a:{t_x:.2f}s">✖ ReferenceError: Console is not defined</span></div>
<div class="pill ok pop" style="--a:{t_ch1:.2f}s;left:-180px;right:0;margin:0 0 0 70px;top:440px;font:700 20px var(--mono)">console ✅</div>
<div class="abs pop" style="--a:{t_ne:.2f}s;left:0;right:0;text-align:center;top:442px;font:900 28px var(--mono);color:var(--purple)">≠</div>
<div class="pill err pop" style="--a:{t_ch2:.2f}s;left:0;right:-180px;margin:0 70px 0 0;top:440px;font:700 20px var(--mono)">Console ❌</div>''')
sfx("hit", T[6], 0.8); sfx("buzz", t_x, 0.6); sfx("pop", t_ch1, 0.7); sfx("pop", t_ne, 0.7); sfx("pop", t_ch2, 0.7)

# ===== ХАТОИ 3 (T10..T14) =====
t_cl = WT(11, "консол"); t_be = WT(11, "бе"); t_se2 = WT(12, "синтакс"); t_sat = WT(13, "сатри")
c1 = 'console.log("Салом"'
hc1 = '<span class="f">console</span>.<span class="f">log</span>(<span class="s">"Салом"</span>'
scene(T[10] - 0.1, T[14] - 0.1, f'''
<div class="xnum">ХАТОИ 3</div>
<div class="slam" style="--a:{T[10]:.2f}s;top:128px;font-size:64px;color:var(--white)">( &nbsp;<span style="color:var(--err)">)</span> ?</div>
<div class="ide" style="top:230px"><div class="bar"><i></i><i></i><i></i><span>salom.js</span></div><div class="code" style="font-size:16px"><div class="ln">{TYP(t_cl, max(0.8, t_be - t_cl - 0.2), hc1, c1)}<span class="miss" style="--a:{t_be:.2f}s">)</span></div></div></div>
<div class="term abs" style="left:20px;right:20px;top:330px;border-radius:12px;border:1px solid var(--line);animation:fadein .2s {f(t_se2 - 0.2)} both"><span class="out e" style="--a:{t_se2:.2f}s">✖ SyntaxError: missing ) after argument list</span>
<span class="out" style="--a:{t_sat:.2f}s;color:var(--muted)">  at <span class="hlt" style="--a:{t_sat:.2f}s;--b:{END + 5:.2f}s;color:var(--white)">salom.js:1</span> ← рақами сатр</span></div>
<div class="pill ok pop" style="--a:{WT(13, 'бихонед'):.2f}s;top:470px">📖 паёмро бихонед</div>
<div class="pill pop" style="--a:{t_sat:.2f}s;top:525px;border-color:var(--purple)">🔎 сатри хато: 1</div>''')
sfx("hit", T[10], 0.8); sfx("buzz", t_se2, 0.6); sfx("pop", t_be, 0.6); sfx("pop", WT(13, 'бихонед'), 0.7); sfx("ding", t_sat, 0.6)

# ===== ХУЛОСА (T14..T15) =====
scene(T[14] - 0.1, T[15] - 0.1, f'''
<div class="kicker" style="top:170px">ХУЛОСА</div>
<div class="h1 pop" style="--a:{T[14] + 0.05:.2f}s;top:215px;font-size:46px">Хато <span style="color:var(--err)">душман</span> нест</div>
<div class="h1 acc pop" style="--a:{WT(14, 'роҳнамост'):.2f}s;top:290px;font-size:56px">— роҳнамост 🧭</div>''')
sfx("hit", T[14] + 0.05, 0.7); sfx("pop", WT(14, 'роҳнамост'), 0.7); sfx("chime", WT(14, 'роҳнамост') + .2, 0.7)

# ===== САВОЛ (T15..T17) =====
t_1, t_2, t_3 = WT(16, "як"), WT(16, "ду"), WT(16, "серо")
qc = ""
for k, (tt, lab, sub) in enumerate([(t_1, "1", "="), (t_2, "2", "Aa"), (t_3, "3", ")")]):
    qc += f'<div class="card pop" style="--a:{tt:.2f}s;left:{40 + k * 165}px;width:145px;top:270px;text-align:center;padding:20px 0"><div style="font:900 52px var(--mono);color:var(--purple)">{lab}</div><div style="font:800 24px var(--mono);color:var(--err);margin-top:6px">{sub}</div></div>'
    sfx("pop", tt, 0.7)
scene(T[15] - 0.1, T[17] - 0.1, f'''
<div class="kicker" style="top:150px">ШУМО КАДОМАШРО КАРДЕД?</div>
<div class="h1 pop" style="--a:{T[15] + 0.05:.2f}s;top:185px;font-size:38px">1 · 2 · 3</div>
{qc}
<div class="pill ok pop" style="--a:{T[16] + 1.7:.2f}s;top:470px">💬 рақамро дар шарҳ нависед</div>''')
sfx("pop", T[15] + 0.05, 0.6); sfx("pop", T[16] + 1.7, 0.6)

# ===== ДАЪВАТ БА ШАРҲ (T17..T18) =====
t_vid = WT(17, "видео"); t_dir = WT(17, "директ")
kw_raw = "ХАТО"
scene(T[17] - 0.1, T[18] - 0.1, f'''
<div class="kicker" style="top:140px">ШАРҲ → DIRECT</div>
<div class="card pop" style="--a:{T[17] + 0.05:.2f}s;left:40px;right:40px;top:190px;display:flex;align-items:center;gap:14px">
 <div style="width:38px;height:38px;border-radius:50%;background:var(--accent)"></div>
 <div style="flex:1;background:#1E1E1E;border:1px solid var(--line);border-radius:999px;padding:11px 16px;font:700 17px var(--mono);color:var(--white)">{TYP(T[17] + 0.15, 0.8, kw_raw, kw_raw)}</div>
 <div style="font-weight:800;color:var(--purple)">➤</div></div>
<div class="card pop" style="--a:{t_vid:.2f}s;left:40px;right:40px;top:300px;padding:0;overflow:hidden">
 <div style="height:170px;background:linear-gradient(135deg,#3a1f2a,#1E1E1E);display:flex;align-items:center;justify-content:center"><div style="width:68px;height:48px;border-radius:12px;background:#F4443C;color:#fff;font-size:24px;line-height:48px;text-align:center">▶</div></div>
 <div style="padding:12px 18px"><div style="font:800 18px Inter;color:var(--white)">3 хатои рӯзи аввал</div><div style="font:600 13px Inter;color:var(--muted);margin-top:3px">видеои пурра · YouTube</div></div></div>
<div class="pill acc2 pop" style="--a:{t_dir:.2f}s;top:520px">✉ ба Direct мефиристам</div>''')
sfx("pop", T[17] + 0.05, 0.7); sfx("pop", t_vid, 0.7); sfx("chime", t_dir, 0.8); sfx("ding", t_dir + 0.1, 0.5)

# ===== ДАРСИ ОЯНДА (T18..END) =====
t_sub = SN[19]['start'] + 0.1
scene(T[18] - 0.1, END + 5, f'''
<div class="kicker" style="top:140px">ДАРСИ ОЯНДА</div>
<div class="h1 pop" style="--a:{T[18] + 0.05:.2f}s;top:180px;font-size:50px">Хатогӣ <span class="acc">ва дебаг</span> 🐞</div>
<div class="ide pop" style="--a:{WT(18, 'хатогӣ'):.2f}s;top:300px"><div class="bar"><i></i><i></i><i></i><span>debug.js</span></div>
<div class="code" style="font-size:15px"><div class="ln"><span class="k">let</span> <span class="p">age</span> = <span class="s">"25"</span> + <span class="n">1</span>;</div><div class="ln"><span class="f">console</span>.<span class="f">log</span>(<span class="p">age</span>); <span class="cm">// 251 ???</span></div></div></div>
<div class="pill acc2 pop" style="--a:{t_sub:.2f}s;top:470px;font-size:20px;padding:12px 30px">🔔 Обуна шавед</div>''')
sfx("hit", T[18] + 0.05, 0.7); sfx("pop", WT(18, 'хатогӣ'), 0.7); sfx("pop", t_sub, 0.8); sfx("ding", t_sub + 0.1, 0.6)

html = f'''<!doctype html><html lang="tg"><head><meta charset="utf-8"><link rel="stylesheet" href="style.css"></head><body>
{"".join(H)}
{"".join(cap_html)}
</body></html>'''
open('reel.html', 'w', encoding='utf-8').write(html)
json.dump(dict(end=END, sfx=SFX), open('sfx.json', 'w'))
print('END', END, 'sfx', len(SFX), 'captions', len(cap_html))
