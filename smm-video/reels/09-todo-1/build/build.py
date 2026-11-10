# Ролик «Лоиҳа қ.1: рӯйхати вазифаҳо» (дарси 9) — стили «VS Code Dark + бунафш». Тайминг: timelineA.json.
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
KW = {"вазифа", "рӯйхат", "объект", "tasks", "push", "to-do", "done", "text", "тру", "лоиҳа", "лоиҳа!"}
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

K = lambda s: f'<span class="k">{s}</span>'; P = lambda s: f'<span class="p">{s}</span>'
S_ = lambda s: f'<span class="s">{s}</span>'; N = lambda s: f'<span class="n">{s}</span>'; F = lambda s: f'<span class="f">{s}</span>'
CT = lambda s: f'<span class="c">{s}</span>'; CM = lambda s: f'<span class="cm">{s}</span>'
ERR = "color:var(--err)"

def task(top, text, a, left=40, right=40, done=False, idx=None, extra="", cls="pop"):
    mark = "☑" if done else "☐"
    ix = f'<span style="font:800 13px var(--mono);color:var(--muted);margin-right:12px">[{idx}]</span>' if idx is not None else ""
    st = "text-decoration:line-through;color:var(--muted)" if done else "color:var(--white)"
    return (f'<div class="card {cls}" style="--a:{a:.2f}s;left:{left}px;right:{right}px;top:{top}px;padding:12px 18px;display:flex;align-items:center;{extra}">'
            f'{ix}<span style="font:700 22px \'Segoe UI\';margin-right:12px;color:var(--purple)">{mark}</span><span style="font:700 20px \'Segoe UI\';{st}">{text}</span></div>')

# ===== ХУК (0..T0) =====
p0 = PRE[0]
t_df = WT(0, "дафтари", 0, p0); t_ko = WT(0, "код", 0, p0); t_ch = WT(0, "чӣ", 0, p0)
scene(0, T[0] - 0.1, f'''
<div class="kicker" style="top:100px">ДАРСИ 9 · ЛОИҲА</div>
<div class="card pop" style="--a:{t_df:.2f}s;left:40px;right:40px;top:150px;padding:16px 20px"><div style="font:800 12px var(--mono);letter-spacing:2px;color:var(--purple);margin-bottom:6px">ДАФТАРЧА 📓</div>
 <div style="font:700 20px/1.8 'Segoe UI';color:var(--white)">☐ нон харидан<br>☐ дарс хондан<br>☐ занг задан</div></div>
<div class="h1 pop" style="--a:{t_ko:.2f}s;top:350px;font-size:44px">↓</div>
<div class="ide pop" style="--a:{t_ko + 0.1:.2f}s;top:415px"><div class="bar"><i></i><i></i><i></i><span>todo.js</span></div><div class="code" style="font-size:14px;line-height:1.5;padding-top:8px"><div class="ln" style="height:22px">{K("let")} {P("tasks")} = [</div><div class="ln" style="height:22px">  {{ {P("text")}: {S_('"нон харидан"')}, {P("done")}: {K("false")} }},</div><div class="ln" style="height:22px">  …</div><div class="ln" style="height:22px">];</div></div></div>
<div class="pill acc2 pop" style="--a:{t_ch:.2f}s;top:580px;font-size:22px;padding:11px 26px">Чӣ тавр? 🤔</div>''', whoosh=False)
sfx("hit", 0.0, 0.8); sfx("pop", t_df, 0.7); sfx("pop", t_ko, 0.7); sfx("chime", t_ko + 0.2, 0.5); sfx("pop", t_ch, 0.8)

# ===== ЛОИҲА! (T0..T1) =====
scene(T[0] - 0.1, T[1] - 0.1, f'''
<div class="slam acc" style="--a:{T[0]:.2f}s;top:230px;font-size:76px">ЛОИҲА!</div>
<div class="pill ok pop" style="--a:{T[0] + 0.3:.2f}s;top:340px;font-size:20px">қисми 1 · to-do</div>
<div class="emo pop" style="--a:{T[0] + 0.4:.2f}s;position:absolute;left:0;right:0;top:420px;text-align:center;font-size:84px">📝</div>''')
sfx("hit", T[0], 0.9); sfx("chime", T[0] + 0.3, 0.6)

# ===== ДАФТАРЧА (T1..T4) =====
t_n1 = WT(2, "нон"); t_n2 = WT(2, "дарс"); t_mk = WT(3, "иҷро")
scene(T[1] - 0.1, T[4] - 0.1, f'''
<div class="kicker" style="top:130px">ДАФТАРЧА 📓</div>
{task(190, "нон харидан", t_n1)}
{task(268, "дарс хондан", t_n2)}
{task(346, "занг задан", t_n2 + 0.8)}
<div class="pill pop" style="--a:{T[3]:.2f}s;top:450px;font-size:18px;border-color:var(--purple);color:var(--purple)">як сатр + нишона</div>
<div class="pill ok pop" style="--a:{t_mk:.2f}s;top:510px;font-size:19px">☑ иҷро шуд · ☐ не</div>''')
sfx("pop", t_n1, 0.7); sfx("pop", t_n2, 0.7); sfx("pop", t_n2 + 0.8, 0.7); sfx("pop", T[3], 0.6); sfx("ding", t_mk, 0.6)

# ===== ОБЪЕКТ (T4..T6) =====
t_mt = WT(5, "матн"); t_hl = WT(5, "ҳолат")
scene(T[4] - 0.1, T[6] - 0.1, f'''
<div class="kicker" style="top:110px">ДАР БАРНОМАСОЗӢ ҲАМ ҲАМИН ТАВР</div>
<div class="h1 pop" style="--a:{T[5]:.2f}s;top:170px;font-size:44px">вазифа = <span class="acc">объект</span></div>
<div class="card pop" style="--a:{T[5] + 0.2:.2f}s;left:50px;right:50px;top:270px;font:700 20px/1.9 var(--mono);color:var(--white)"><span style="color:var(--purple)">{{</span><br>
&nbsp;&nbsp;<span class="p hlt" style="--a:{t_mt:.2f}s;--b:{T[6]:.2f}s">text</span>: <span class="s">"нон харидан"</span>,<br>
&nbsp;&nbsp;<span class="p hlt" style="--a:{t_hl:.2f}s;--b:{T[6]:.2f}s">done</span>: <span class="k">false</span><br><span style="color:var(--purple)">}}</span></div>
<div class="pill pop" style="--a:{t_mt:.2f}s;top:505px;border-color:var(--par);color:var(--par)">text = матн</div>
<div class="pill pop" style="--a:{t_hl:.2f}s;top:560px;border-color:var(--str);color:var(--str)">done = ҳолат (иҷро шуд?)</div>''')
sfx("hit", T[5], 0.7); sfx("pop", t_mt, 0.7); sfx("pop", t_hl, 0.7)

# ===== РӮЙХАТ (T6..T7) =====
t_ob = WT(6, "объектҳо"); t_ry = WT(6, "рӯйхат")
scene(T[6] - 0.1, T[7] - 0.1, f'''
<div class="kicker" style="top:110px">ОБЪЕКТҲО ДАР РӮЙХАТ</div>
<div class="h1 pop" style="--a:{T[6]:.2f}s;top:160px;font-size:36px">[ <span class="acc">объект, объект</span> ]</div>
{task(260, "нон харидан", t_ob, idx=0)}
{task(338, "дарс хондан", t_ob + 0.25, idx=1)}
<div class="pill pop" style="--a:{t_ry:.2f}s;top:440px;font-size:18px;border-color:var(--kw);color:var(--kw)">рӯйхат — дарси 4 · шумора аз 0</div>''')
sfx("pop", T[6] + 0.1, 0.6); sfx("pop", t_ob, 0.7); sfx("pop", t_ob + 0.25, 0.7); sfx("chime", t_ry, 0.5)

# ===== КОД: let tasks = [...] (T7..T9) =====
l1 = K("let") + " " + P("tasks") + " = ["
l2 = "  { " + P("text") + ": " + S_('"нон харидан"') + ", " + P("done") + ": " + K("false") + " },"
l3 = "  { " + P("text") + ": " + S_('"дарс хондан"') + ", " + P("done") + ": " + K("false") + " }"
l4 = "];"
r1, r2, r3, r4 = 'let tasks = [', '  { text: "нон харидан", done: false },', '  { text: "дарс хондан", done: false }', '];'
d7 = T[8] - T[7]
scene(T[7] - 0.1, T[9] - 0.1, f'''
<div class="kicker" style="top:100px">ДАФТАРЧА ДАР КОД</div>
<div class="ide" style="top:135px"><div class="bar"><i></i><i></i><i></i><span>todo.js</span></div><div class="code" style="font-size:14.5px;padding-top:10px">
<div class="ln">{TYP(T[7] + 0.1, 0.7, l1, r1)}</div>
<div class="ln">{TYP(T[7] + 1.6, 2.2, l2, r2)}</div>
<div class="ln">{TYP(T[7] + 4.2, 2.2, l3, r3)}</div>
<div class="ln">{TYP(T[7] + 6.7, 0.3, l4, r4)}</div></div></div>
{task(330, "нон харидан", T[7] + 3.9, idx=0)}
{task(408, "дарс хондан", T[7] + 6.5, idx=1)}
<div class="pill acc2 pop" style="--a:{T[8] + 0.1:.2f}s;top:510px;font-size:20px;padding:11px 26px">📓 ин дафтарча аст</div>''')
sfx("pop", T[7] + 3.9, 0.6); sfx("pop", T[7] + 6.5, 0.6); sfx("chime", T[8] + 0.1, 0.7)

# ===== PUSH (T9..T11) =====
pl = P("tasks") + "." + F("push") + "(" + "{ " + P("text") + ": " + S_('"занг задан"') + ", " + P("done") + ": " + K("false") + " });"
pr = 'tasks.push({ text: "занг задан", done: false });'
t_zg = WT(9, "занг")
scene(T[9] - 0.1, T[11] - 0.1, f'''
<div class="kicker" style="top:100px">ВАЗИФАИ НАВ</div>
<div class="ide" style="top:135px"><div class="bar"><i></i><i></i><i></i><span>todo.js</span></div><div class="code" style="font-size:13.5px;padding-top:10px"><div class="ln">{TYP(T[9] + 0.2, max(1.5, t_zg - T[9] - 0.2), pl, pr)}</div></div></div>
{task(260, "нон харидан", T[9], idx=0)}
{task(330, "дарс хондан", T[9] + 0.1, idx=1)}
{task(400, "занг задан", t_zg + 1.0, idx=2, extra="border-color:var(--purple)")}
<div class="pill pop" style="--a:{T[10]:.2f}s;top:500px;font-size:18px;border-color:var(--kw);color:var(--kw)">push — аз дарси 4: ба охир илова мекунад</div>''')
sfx("pop", T[9], 0.5); sfx("hit", t_zg + 1.0, 0.7); sfx("pop", t_zg + 1.0, 0.6); sfx("chime", T[10], 0.5)

# ===== ДАВР (T11..T14) =====
f1 = CT("for") + " (" + K("let") + " " + P("i") + " = " + N("0") + "; " + P("i") + " &lt; " + P("tasks") + ".length; " + P("i") + "++) {"
f2 = "  " + F("console") + "." + F("log") + "(" + P("i") + " + " + N("1") + " + " + S_('". "') + " + " + P("tasks") + "[" + P("i") + "]." + P("text") + ");"
fr1 = 'for (let i = 0; i < tasks.length; i++) {'
fr2 = '  console.log(i + 1 + ". " + tasks[i].text);'
t_y = WT(13, "яке"); t_d = WT(13, "ду"); t_s = WT(13, "се")
scene(T[11] - 0.1, T[14] - 0.1, f'''
<div class="kicker" style="top:100px">ЧОП БО ДАВР · ДАРСИ 3</div>
<div class="ide" style="top:135px"><div class="bar"><i></i><i></i><i></i><span>todo.js</span></div><div class="code" style="font-size:13.5px;padding-top:10px">
<div class="ln">{TYP(T[11] + 2.4, 3.6, f1, fr1)}</div>
<div class="ln">{TYP(T[12] + 0.1, max(2.0, T[13] - T[12] - 0.6), f2, fr2)}</div>
<div class="ln">}}</div></div></div>
<div class="term abs fade" style="left:20px;right:20px;top:290px;border-radius:12px;border:1px solid var(--line);--a:{t_y - 0.2:.2f}s;padding:12px 16px">
<div class="ln fade" style="--a:{t_y:.2f}s"><span class="pr">&gt; </span>1. нон харидан</div>
<div class="ln fade" style="--a:{t_d:.2f}s"><span class="pr">&gt; </span>2. дарс хондан</div>
<div class="ln fade" style="--a:{t_s:.2f}s"><span class="pr">&gt; </span>3. занг задан</div></div>''')
sfx("pop", T[11] + 2.4, 0.4); sfx("ding", t_y, 0.6); sfx("ding", t_d, 0.6); sfx("ding", t_s, 0.6)

# ===== ИҶРО ШУД (T14..T15) =====
t_tr = WT(14, "тру")
dl = P("tasks") + "[" + N("0") + "]." + P("done") + " = " + K("true") + ";"
dr = 'tasks[0].done = true;'
scene(T[14] - 0.1, T[15] - 0.1, f'''
<div class="kicker" style="top:100px">ИҶРО ШУД ✅</div>
<div class="ide" style="top:135px"><div class="bar"><i></i><i></i><i></i><span>todo.js</span></div><div class="code" style="font-size:16px;padding-top:10px"><div class="ln">{TYP(T[14] + 0.2, max(1.0, t_tr - T[14] - 0.3), dl, dr)}</div></div></div>
{task(250, "нон харидан", T[14], idx=0)}
{task(250, "нон харидан", t_tr + 0.1, idx=0, done=True, extra="border-color:var(--ok)")}
{task(328, "дарс хондан", T[14] + 0.1, idx=1)}
{task(406, "занг задан", T[14] + 0.2, idx=2)}
<div class="pill ok pop" style="--a:{t_tr + 0.3:.2f}s;top:510px;font-size:19px">нон харида шуд ✅</div>''')
sfx("pop", T[14], 0.5); sfx("ding", t_tr + 0.1, 0.8); sfx("chime", t_tr + 0.2, 0.6)

# ===== ХУЛОСА (T15..T16) =====
scene(T[15] - 0.1, T[16] - 0.1, f'''
<div class="kicker" style="top:170px">ХУЛОСА</div>
<div class="h1 pop" style="--a:{T[15] + 0.05:.2f}s;top:215px;font-size:56px">TO-DO</div>
<div class="h1 acc pop" style="--a:{WT(15, 'рӯйхати'):.2f}s;top:290px;font-size:38px">= рӯйхати объектҳо</div>
<div class="card pop" style="--a:{WT(15, 'вазифа'):.2f}s;left:50px;right:50px;top:400px;text-align:center;font:700 20px 'Segoe UI';color:var(--white)">ҳар вазифа — <span style="color:var(--par)">text</span> + <span style="color:var(--par)">done</span></div>''')
sfx("hit", T[15] + 0.05, 0.7); sfx("pop", WT(15, 'рӯйхати'), 0.7); sfx("pop", WT(15, 'вазифа'), 0.6); sfx("chime", WT(15, 'вазифа') + 0.3, 0.6)

# ===== САНҶИШ (T16..T20) =====
t_c = WT(17, "чӣ")
q1 = 'console.log(tasks[1].text);'
hq1 = F("console") + "." + F("log") + "(" + P("tasks") + "[" + N("1") + "]." + P("text") + ");"
scene(T[16] - 0.1, T[20] - 0.1, f'''
<div class="kicker" style="top:140px">САНҶИШ</div>
<div class="h1 pop" style="--a:{T[16] + 0.05:.2f}s;top:175px;font-size:40px">чӣ чоп мешавад?</div>
<div class="ide" style="top:240px;left:12px;right:12px"><div class="bar"><i></i><i></i><i></i><span>test.js</span></div>
<div class="code" style="font-size:16px"><div class="ln">{TYP(T[17] + 0.05, 2.0, hq1, q1)}</div></div></div>
{task(305, "нон харидан", T[16] + 0.4, idx=0, extra="padding:7px 16px")}
{task(353, "дарс хондан", T[16] + 0.5, idx=1, extra="padding:7px 16px")}
{task(401, "занг задан", T[16] + 0.6, idx=2, extra="padding:7px 16px")}
<div class="h1 acc pop" style="--a:{t_c:.2f}s;top:455px;font-size:100px">?</div>
<div class="pill pop" style="--a:{T[18]:.2f}s;top:590px;font-size:17px;border-color:var(--kw);color:var(--kw)">шумора аз 0 оғоз мешавад</div>
<div class="pill ok pop" style="--a:{T[19]:.2f}s;top:640px">💬 ҷавобро дар шарҳ нависед</div>''')
sfx("hit", T[16] + 0.05, 0.7); sfx("pop", t_c, 0.8); sfx("tick2", t_c, 0.5); sfx("pop", T[18], 0.6); sfx("pop", T[19], 0.6)

# ===== ДАЪВАТ БА ШАРҲ (T20..T21) =====
t_vid = WT(20, "видеои"); t_dir = WT(20, "директ")
kw_raw = "ВАЗИФА"
scene(T[20] - 0.1, T[21] - 0.1, f'''
<div class="kicker" style="top:140px">ШАРҲ → DIRECT</div>
<div class="card pop" style="--a:{T[20] + 0.05:.2f}s;left:40px;right:40px;top:190px;display:flex;align-items:center;gap:14px">
 <div style="width:38px;height:38px;border-radius:50%;background:var(--accent)"></div>
 <div style="flex:1;background:#1E1E1E;border:1px solid var(--line);border-radius:999px;padding:11px 16px;font:700 17px var(--mono);color:var(--white)">{TYP(T[20] + 0.15, 1.2, kw_raw, kw_raw)}</div>
 <div style="font-weight:800;color:var(--purple)">➤</div></div>
<div class="card pop" style="--a:{t_vid:.2f}s;left:40px;right:40px;top:300px;padding:0;overflow:hidden">
 <div style="height:170px;background:linear-gradient(135deg,#2a1f45,#1E1E1E);display:flex;align-items:center;justify-content:center"><div style="width:68px;height:48px;border-radius:12px;background:#F4443C;color:#fff;font-size:24px;line-height:48px;text-align:center">▶</div></div>
 <div style="padding:12px 18px"><div style="font:800 18px 'Segoe UI';color:var(--white)">Дарси 9: Лоиҳа — рӯйхати вазифаҳо</div><div style="font:600 13px 'Segoe UI';color:var(--muted);margin-top:3px">видеои пурраи дарс · YouTube</div></div></div>
<div class="pill acc2 pop" style="--a:{t_dir:.2f}s;top:520px">✉ ба Direct мефиристам</div>''')
sfx("pop", T[20] + 0.05, 0.7); sfx("pop", t_vid, 0.7); sfx("chime", t_dir, 0.8); sfx("ding", t_dir + 0.1, 0.5)

# ===== ДАРСИ ОЯНДА (T21..T22) =====
t_fn = WT(21, "функсия")
cl = K("function") + " " + F("addTask") + "(" + P("text") + ") {"
cr = 'function addTask(text) {'
scene(T[21] - 0.1, T[22] - 0.1, f'''
<div class="kicker" style="top:140px">ДАРСИ ОЯНДА</div>
<div class="h1 pop" style="--a:{T[21] + 0.05:.2f}s;top:180px;font-size:54px">10 · <span class="acc">Лоиҳа, қ.2</span></div>
<div class="ide pop" style="--a:{t_fn:.2f}s;top:290px"><div class="bar"><i></i><i></i><i></i><span>todo.js</span></div>
<div class="code" style="font-size:15px"><div class="ln">{TYP(t_fn + 0.1, 1.4, cl, cr)}</div><div class="ln">  {CM("// ...")}</div><div class="ln">}}</div></div></div>''')
sfx("hit", T[21] + 0.05, 0.7); sfx("pop", t_fn, 0.7)

# ===== ОБУНА (T22..END) =====
t_sub = SN[22]['start'] + 0.2
scene(T[22] - 0.1, END + 5, f'''
<div class="kicker" style="top:150px">БАРНОМАСОЗӢ АЗ СИФР</div>
<div class="h1 pop" style="--a:{T[22] + 0.05:.2f}s;top:200px;font-size:50px"><span class="acc">Лоиҳаи</span> шумо</div>
<div class="pill acc2 pop" style="--a:{t_sub:.2f}s;top:330px;font-size:22px;padding:13px 32px">🔔 Обуна шавед</div>''')
sfx("hit", T[22] + 0.05, 0.7); sfx("pop", t_sub, 0.8); sfx("ding", t_sub + 0.1, 0.6)

H = [re.sub(r'</div>\s+<div class="ln"', '</div><div class="ln"', h) for h in H]
html = f'''<!doctype html><html lang="tg"><head><meta charset="utf-8"><link rel="stylesheet" href="style.css"></head><body>
{"".join(H)}
{"".join(cap_html)}
</body></html>'''
open('reel.html', 'w', encoding='utf-8').write(html)
json.dump(dict(end=END, sfx=SFX), open('sfx.json', 'w'))
print('END', END, 'sfx', len(SFX), 'captions', len(cap_html))
