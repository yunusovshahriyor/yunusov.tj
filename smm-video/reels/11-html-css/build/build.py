# Ролик «Лоиҳа қ.2: функсияҳо» (дарси 10) — стили «VS Code Dark + бунафш». Тайминг: timelineA.json.
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
KW = {"html", "css", "скелет", "либос", "барчасп", "тугма", "javascript", "намуд", "намуди"}
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


# ================= САҲНАҲОИ ДАРСИ 11: HTML ВА CSS =================
TG = lambda s: f'<span style="color:#808080">&lt;</span><span class="k">{s}</span><span style="color:#808080">&gt;</span>'
TGC = lambda s: f'<span style="color:#808080">&lt;/</span><span class="k">{s}</span><span style="color:#808080">&gt;</span>'

def brw(top, a, body, url="todo.html", cls="pop", left=40, right=40, extra=""):
    return (f'<div class="brw {cls}" style="--a:{a:.2f}s;top:{top}px;left:{left}px;right:{right}px;{extra}">'
            f'<div class="ub"><i></i><i></i><i></i><span>🔒 {url}</span></div><div class="pg">{body}</div></div>')

def todo_rows(rows):
    out = ""
    for t, done in rows:
        ck = '<span class="ckb on">✓</span>' if done else '<span class="ckb"></span>'
        tx = f'<s style="color:#9aa0a6">{t}</s>' if done else t
        out += f'<div class="rw">{ck}{tx}</div>'
    return out

def nice_todo(rows, cnt):
    return (f'<div class="ntd"><div class="tp"><b>Вазифаҳо</b><span>{cnt}</span></div>{todo_rows(rows)}'
            f'<div class="addb">＋ Илова</div></div>')

CSS11 = '''<style>
.brw{position:absolute;border-radius:14px;overflow:hidden;background:#fff;border:1px solid #5a5a62;box-shadow:0 16px 44px rgba(0,0,0,.6)}
.brw .ub{height:32px;background:#E8EAED;display:flex;align-items:center;gap:6px;padding:0 10px}
.brw .ub i{width:9px;height:9px;border-radius:50%;background:#F48771}.brw .ub i:nth-child(2){background:#E2B93B}.brw .ub i:nth-child(3){background:#4EC9B0}
.brw .ub span{flex:1;margin-left:8px;background:#fff;border-radius:99px;font:600 11px 'Segoe UI';color:#555;padding:3px 12px}
.brw .pg{padding:16px 20px;color:#000;position:relative}
.rh1{font:700 34px 'Times New Roman',serif;color:#000;margin-bottom:12px}
.rbtn{display:inline-block;font:400 19px Arial,sans-serif;padding:4px 12px;background:#efefef;border:2px outset #767676;color:#000}
.rp{font:400 17px 'Times New Roman',serif;color:#000;margin-top:10px}
.ntd{border-radius:20px;overflow:hidden;background:#fff;border:1.5px solid #e3d8fb;box-shadow:0 10px 26px rgba(120,80,200,.22)}
.ntd .tp{padding:10px 16px;background:linear-gradient(90deg,#BD93F9,#FF79C6);color:#1E1E1E;display:flex;justify-content:space-between;align-items:center}
.ntd .tp b{font:900 19px 'Segoe UI Black','Segoe UI'}.ntd .tp span{font:800 12px 'Segoe UI'}
.ntd .rw{display:flex;align-items:center;gap:10px;padding:9px 16px;border-bottom:1px solid #eee;font:700 17px 'Segoe UI';color:#222}
.ntd .addb{margin:10px 16px 12px;padding:8px;border-radius:12px;background:#4EC9B0;color:#fff;font:800 16px 'Segoe UI';text-align:center}
.ckb{width:22px;height:22px;border-radius:7px;border:2.5px solid #BD93F9;display:flex;align-items:center;justify-content:center;font-size:14px}
.ckb.on{background:#4EC9B0;border-color:#4EC9B0;color:#fff;font-weight:900}
.wf{position:absolute;border:2.5px dashed #8B949E;border-radius:8px;display:flex;align-items:center;justify-content:center;font:800 15px var(--mono);color:#555;background:rgba(189,147,249,.10)}
.lang{position:absolute;width:215px;height:230px;border-radius:24px;background:var(--panel);border:1.5px solid var(--line);text-align:center;box-shadow:0 16px 40px rgba(0,0,0,.5)}
.lang .nm{font:900 46px 'Segoe UI Black','Segoe UI';margin-top:26px}.lang .ic{font-size:60px;margin-top:6px}.lang .ds{font:800 19px 'Segoe UI';color:var(--white);margin-top:6px}
.sumc{position:absolute;left:34px;right:34px;height:104px;border-radius:20px;background:var(--panel);border:1.5px solid var(--line);display:flex;align-items:center;gap:16px;padding:0 20px;box-shadow:0 12px 30px rgba(0,0,0,.45)}
.sumc .ic{font-size:42px}.sumc .nm{font:900 30px 'Segoe UI Black','Segoe UI';width:118px}.sumc .ds{font:800 20px 'Segoe UI';color:var(--white)}
.demo{position:absolute;width:150px;height:150px;border-radius:20px;background:var(--panel);border:1px solid var(--line);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;box-shadow:0 12px 30px rgba(0,0,0,.45)}
.demo small{font:800 14px 'Segoe UI';color:var(--muted)}
.bob{animation:popin .45s cubic-bezier(.3,1.6,.5,1) var(--a) both,bob 1s ease-in-out var(--a) infinite}
@keyframes bob{50%{translate:0 8px}}
</style>'''
H.append(CSS11)

RAW_PAGE = '<div class="rh1">Вазифаҳо</div><span class="rbtn">Илова</span>'

# ===== ХУК (0..T0) =====
p0 = PRE[0]
t_kn = WT(0, "консол", 0, p0); t_ch = WT(0, "чӣ", 0, p0); t_zb = WT(0, "зебо", 0, p0); t_br = WT(0, "браузер", 0, p0)
scene(0, T[0] - 0.1, f'''
<div class="kicker" style="top:100px">ДАРСИ 11 · HTML ВА CSS</div>
<div class="term abs pop" style="--a:0.2s;left:60px;right:60px;top:135px;border-radius:14px;border:1px solid var(--line);padding:12px 18px;font-size:17px"><div style="color:var(--muted);font:700 11px var(--mono);margin-bottom:6px">КОНСОЛ</div><div style="color:var(--ok)">☑ нон харидан</div><div>☐ дарс хондан</div></div>
<div class="pill pop" style="--a:{t_kn:.2f}s;top:262px;font-size:16px;border-color:var(--err);color:var(--err)">ҳоло — танҳо матн 😐</div>
<div class="h1 pop bob" style="--a:{t_zb:.2f}s;top:310px;font-size:40px;color:var(--purple)">↓</div>
{brw(368, t_br, nice_todo([("нон харидан", True), ("дарс хондан", False)], "1 / 2"), left=70, right=70)}
<div class="pill acc2 pop" style="--a:{t_ch:.2f}s;top:316px;left:auto;right:30px;font-size:20px;padding:9px 22px;rotate:6deg">Чӣ тавр? 🤔</div>''', whoosh=False)
sfx("hit", 0.0, 0.8); sfx("pop", 0.2, 0.6); sfx("pop", t_kn, 0.6); sfx("pop", t_ch, 0.8); sfx("pop", t_zb, 0.6); sfx("chime", t_br, 0.7)

# ===== НАМУДИ БАРНОМА (T0..T1) =====
scene(T[0] - 0.1, T[1] - 0.1, f'''
<div class="slam acc" style="--a:{T[0]:.2f}s;top:210px;font-size:66px">НАМУДИ</div>
<div class="slam" style="--a:{T[0] + 0.15:.2f}s;top:292px;font-size:50px;color:#fff">барнома</div>
<div class="emo pop" style="--a:{T[0] + 0.4:.2f}s;position:absolute;left:0;right:0;top:400px;text-align:center;font-size:84px">🎨</div>''')
sfx("hit", T[0], 0.9); sfx("chime", T[0] + 0.4, 0.5)

# ===== ХОНА (T1..T4) =====
w_dv = WT(2, "девор"); w_hj = WT(2, "ҳуҷраҳо"); w_sk = WT(2, "скелет")
w_rg = WT(3, "ранг"); w_pr = WT(3, "парда"); w_mb = WT(3, "мебел"); w_nm = WT(3, "намуд")
dash = 'fill="none" stroke="#9aa3ad" stroke-width="4" stroke-dasharray="10 7" stroke-linejoin="round"'
scene(T[1] - 0.1, T[4] - 0.1, f'''
<div class="kicker" style="top:105px">ХОНА МЕСОЗЕМ 🏠</div>
<svg class="abs" style="left:95px;top:150px" width="350" height="330" viewBox="0 0 350 330">
 <defs><linearGradient id="rf" x1="0" x2="1"><stop offset="0" stop-color="#BD93F9"/><stop offset="1" stop-color="#FF79C6"/></linearGradient></defs>
 <g class="fade" style="--a:{w_dv:.2f}s"><polygon points="175,12 335,125 15,125" {dash}/><rect x="40" y="125" width="270" height="190" {dash}/></g>
 <g class="fade" style="--a:{w_hj:.2f}s"><line x1="175" y1="125" x2="175" y2="315" {dash}/><line x1="40" y1="215" x2="310" y2="215" {dash}/></g>
 <g class="fade" style="--a:{w_rg:.2f}s"><polygon points="175,12 335,125 15,125" fill="url(#rf)"/><rect x="40" y="125" width="270" height="190" fill="#F3E9D2"/>
  <rect x="68" y="150" width="78" height="52" rx="6" fill="#8fd3ff" stroke="#fff" stroke-width="4"/><rect x="204" y="150" width="78" height="52" rx="6" fill="#8fd3ff" stroke="#fff" stroke-width="4"/>
  <rect x="146" y="238" width="58" height="77" rx="6" fill="#8a5a3c"/><circle cx="194" cy="278" r="4" fill="#FFD166"/></g>
 <g class="fade" style="--a:{w_pr:.2f}s"><path d="M68 150 h30 q-4 30 -30 46z M146 150 h-30 q4 30 30 46z M204 150 h30 q-4 30 -30 46z M282 150 h-30 q4 30 30 46z" fill="#FF79C6"/></g>
</svg>
<div class="emo pop" style="--a:{w_mb:.2f}s;position:absolute;left:142px;top:392px;font-size:40px">🛋</div>
<div class="emo pop" style="--a:{w_mb + 0.15:.2f}s;position:absolute;left:350px;top:392px;font-size:40px">🪴</div>
<div class="pill pop gone" style="--a:{w_sk:.2f}s;--g:{w_rg - 0.05:.2f}s;top:510px;font-size:24px;padding:11px 28px;border-color:#9aa3ad;color:#cfd6dd">🧱 скелет</div>
<div class="pill acc2 pop" style="--a:{w_nm:.2f}s;top:510px;font-size:24px;padding:11px 28px">🎨 намуд</div>
<div class="pill pop" style="--a:{w_nm + 0.3:.2f}s;top:580px;font-size:17px">аввал скелет → баъд намуд</div>''')
sfx("pop", w_dv, 0.7); sfx("tick2", w_hj, 0.5); sfx("pop", w_sk, 0.8); sfx("chime", w_rg, 0.6); sfx("pop", w_pr, 0.5); sfx("pop", w_mb, 0.6); sfx("ding", w_nm, 0.6)

# ===== ДУ ЗАБОН (T4..T6) =====
w_h = WT(5, "эйч"); w_c = WT(5, "си")
scene(T[4] - 0.1, T[6] - 0.1, f'''
<div class="kicker" style="top:120px">ДАР САЙТ ҲАМ ҲАМИН ТАВР</div>
<div class="h1 pop" style="--a:{T[5]:.2f}s;top:165px;font-size:44px">ду <span class="acc">забон</span></div>
<div class="lang pop" style="--a:{w_h:.2f}s;left:40px;top:270px;border-color:rgba(189,147,249,.6)"><div class="nm" style="color:var(--purple)">HTML</div><div class="ic emo">🧱</div><div class="ds">скелет</div></div>
<div class="lang pop" style="--a:{w_c:.2f}s;left:285px;top:270px;border-color:rgba(255,121,198,.6)"><div class="nm" style="color:var(--pink)">CSS</div><div class="ic emo">🎨</div><div class="ds">намуд</div></div>
<div class="pill pop" style="--a:{w_c + 0.5:.2f}s;top:540px;font-size:18px">ду забон — ду кор</div>''')
sfx("pop", T[5], 0.6); sfx("pop", w_h, 0.9); sfx("pop", w_c, 0.9); sfx("ding", w_c + 0.5, 0.4)

# ===== HTML — СКЕЛЕТ: ЧӢ ҲАСТ (T6..T8) =====
w_sr = WT(7, "сарлавҳа"); w_tg = WT(7, "тугма"); w_mt = WT(7, "матн")
wire = (f'<div style="height:250px"></div>'
        f'<div class="wf pop" style="--a:{w_sr:.2f}s;left:20px;right:20px;top:18px;height:62px;font-size:19px">сарлавҳа</div>'
        f'<div class="wf pop" style="--a:{w_tg:.2f}s;left:20px;width:150px;top:98px;height:50px">тугма</div>'
        f'<div class="wf pop" style="--a:{w_mt:.2f}s;left:20px;right:20px;top:166px;height:76px">матн</div>')
scene(T[6] - 0.1, T[8] - 0.1, f'''
<div class="kicker" style="top:100px">HTML — СКЕЛЕТ 🧱</div>
<div class="h1 pop" style="--a:{T[6] + 0.05:.2f}s;top:135px;font-size:36px"><span class="acc">HTML</span>: дар саҳифа чӣ ҳаст?</div>
{brw(215, T[7], wire, url="саҳифа", left=60, right=60)}
<div class="pill pop" style="--a:{w_mt + 0.4:.2f}s;top:560px;font-size:17px;border-color:var(--purple);color:var(--purple)">HTML мегӯяд: ЧӢ ҳаст</div>''')
sfx("hit", T[6] + 0.05, 0.6); sfx("pop", T[7], 0.5)
for t_ in (w_sr, w_tg, w_mt): sfx("pop", t_, 0.8)

# ===== HTML КОД (T8..T11) =====
h1c = TG("h1") + "Вазифаҳо" + TGC("h1"); btc = TG("button") + "Илова" + TGC("button")
w_ku = WT(10, "кушода"); w_pu = WT(10, "пӯшида"); w_bc = WT(10, "барчасп")
h1c_hl = (f'<span class="hlt" style="--a:{w_ku:.2f}s;--b:{END + 5:.2f}s">{TG("h1")}</span>Вазифаҳо'
          f'<span class="hlt" style="--a:{w_pu:.2f}s;--b:{END + 5:.2f}s">{TGC("h1")}</span>')
scene(T[8] - 0.1, T[11] - 0.1, f'''
<div class="kicker" style="top:100px">HTML · БАРЧАСПҲО</div>
<div class="ide" style="top:132px"><div class="bar"><i></i><i></i><i></i><span>index.html</span></div><div class="code" style="font-size:19px;padding-top:12px">
<div class="ln" style="height:34px">{TYP(T[8] + 0.3, 1.2, h1c_hl, '<h1>Вазифаҳо</h1> ')}</div>
<div class="ln" style="height:34px">{TYP(T[9] + 0.05, 0.9, btc, '<button>Илова</button> ')}</div></div></div>
<div class="pill pop" style="--a:{w_ku:.2f}s;left:40px;right:auto;top:298px;font-size:16px;border-color:var(--ok);color:var(--ok)">&lt;h1&gt; — кушода</div>
<div class="pill pop" style="--a:{w_pu:.2f}s;left:auto;right:40px;top:298px;font-size:16px;border-color:var(--pink);color:var(--pink)">&lt;/h1&gt; — пӯшида</div>
<div class="brw pop" style="--a:{T[8] + 0.2:.2f}s;top:350px;left:60px;right:60px"><div class="ub"><i></i><i></i><i></i><span>🔒 index.html</span></div><div class="pg" style="height:130px">
 <div class="rh1 fade" style="--a:{T[8] + 1.6:.2f}s">Вазифаҳо</div><span class="rbtn fade" style="--a:{T[9] + 1.0:.2f}s">Илова</span></div></div>
<div class="pill pop" style="--a:{T[8] + 1.7:.2f}s;top:548px;font-size:16px;border-color:var(--kw);color:var(--kw)">h1 — сарлавҳаи калон</div>
<div class="pill pop" style="--a:{T[9] + 1.05:.2f}s;top:596px;font-size:16px;border-color:var(--kw);color:var(--kw)">button — тугма</div>
<div class="pill acc2 pop" style="--a:{w_bc:.2f}s;top:648px;font-size:17px">ҳар чиз — байни ду барчасп</div>''')
sfx("pop", T[8] + 0.2, 0.5); sfx("ding", T[8] + 1.6, 0.5); sfx("ding", T[9] + 1.0, 0.5); sfx("pop", w_bc, 0.6); sfx("pop", w_ku, 0.8); sfx("pop", w_pu, 0.8)

# ===== ОДДӢ ВА ХИРА → CSS (T11..T13) =====
w_od = WT(11, "оддӣ")
scene(T[11] - 0.1, T[13] - 0.1, f'''
<div class="kicker" style="top:110px">САҲИФА ҲАСТ, АММО…</div>
{brw(150, T[11], '<div style="height:118px">' + RAW_PAGE + '</div>', url="index.html", left=60, right=60)}
<div class="pill err pop" style="--a:{w_od:.2f}s;top:345px;font-size:20px">оддӣ ва хира 😐</div>
<div class="slam acc" style="--a:{T[12] + 0.3:.2f}s;top:430px;font-size:90px">CSS</div>
<div class="pill ok pop" style="--a:{T[12] + 0.7:.2f}s;top:560px;font-size:19px">ёрӣ медиҳад 🎨</div>''')
sfx("pop", T[11], 0.5); sfx("buzz", w_od, 0.35); sfx("hit", T[12] + 0.3, 0.9); sfx("chime", T[12] + 0.7, 0.6)

# ===== CSS — ЛИБОС (T13..T15) =====
w_r = WT(14, "ранг"); w_a = WT(14, "андоза"); w_g = WT(14, "гӯшаҳои")
scene(T[13] - 0.1, T[15] - 0.1, f'''
<div class="kicker" style="top:100px">CSS — ЛИБОС 👕</div>
<div class="h1 pop" style="--a:{T[13] + 0.05:.2f}s;top:135px;font-size:36px"><span class="acc">CSS</span>: чӣ гуна менамояд?</div>
<div class="emo pop" style="--a:{T[13] + 0.3:.2f}s;position:absolute;left:0;right:0;top:215px;text-align:center;font-size:70px">👕</div>
<div class="demo pop" style="--a:{w_r:.2f}s;left:24px;top:350px"><div style="display:flex;gap:6px"><i style="width:30px;height:30px;border-radius:50%;background:#4EC9B0"></i><i style="width:30px;height:30px;border-radius:50%;background:#BD93F9"></i><i style="width:30px;height:30px;border-radius:50%;background:#FF79C6"></i></div><small>ранг</small></div>
<div class="demo pop" style="--a:{w_a:.2f}s;left:195px;top:350px"><div style="color:#fff;font-weight:900"><span style="font-size:20px">А</span> <span style="font-size:36px">А</span> <span style="font-size:56px;line-height:1">А</span></div><small>андоза</small></div>
<div class="demo pop" style="--a:{w_g:.2f}s;left:366px;top:350px"><div style="display:flex;gap:10px;align-items:center"><i style="width:44px;height:44px;background:#8B949E"></i><span style="color:var(--purple);font-weight:900">→</span><i style="width:44px;height:44px;border-radius:14px;background:var(--accent)"></i></div><small>гӯшаҳои мудаввар</small></div>
<div class="pill pop" style="--a:{w_g + 0.6:.2f}s;top:560px;font-size:17px;border-color:var(--pink);color:var(--pink)">CSS мегӯяд: ЧӢ ГУНА менамояд</div>''')
sfx("hit", T[13] + 0.05, 0.6)
for t_ in (w_r, w_a, w_g): sfx("pop", t_, 0.8)

# ===== CSS КОД (T15..T18) =====
w_no = WT(15, "номи"); w_qv = WT(15, "қавси"); w_qo = WT(15, "қоида")
w_bt = WT(16, "баттн"); w_bg = WT(16, "бэкграунд"); w_sb = WT(16, "сабз"); w_bd = WT(16, "бордер"); w_dv2 = WT(16, "дувоздаҳ")
c2 = "  " + P("background") + ": " + S_("green") + ";"
c3 = "  " + P("border-radius") + ": " + N("12px") + ";"
BT = 'display:inline-block;font:400 30px Arial,sans-serif;padding:8px 22px;color:#000;border:2px outset #767676'
scene(T[15] - 0.1, T[18] - 0.1, f'''
<div class="kicker" style="top:100px">CSS · ҚОИДА</div>
<div class="ide" style="top:132px"><div class="bar"><i></i><i></i><i></i><span>style.css</span></div><div class="code" style="font-size:19px;padding-top:12px">
<div class="ln" style="height:34px">{TYP(w_no, 0.6, '<span class="hlt" style="--a:' + f'{w_bt:.2f}s;--b:{w_bg:.2f}s' + '"><span class="f">button</span></span>', 'button')}{TYP(w_qv, 0.25, " {", " {")}</div>
<div class="ln" style="height:34px">{TYP(w_bg, w_sb - w_bg + 0.35, c2, '  background: green; ')}</div>
<div class="ln" style="height:34px">{TYP(w_bd, w_dv2 - w_bd + 0.45, c3, '  border-radius: 12px; ')}</div>
<div class="ln" style="height:34px"><span class="fade" style="--a:{w_qv + 0.3:.2f}s">}}</span></div></div></div>
<div class="pill pop gone" style="--a:{w_no:.2f}s;--g:{w_bg - 0.1:.2f}s;left:16px;right:auto;top:366px;font-size:13px;padding:6px 12px;border-color:var(--fn);color:var(--fn)">номи чиз</div>
<div class="pill pop gone" style="--a:{w_qv:.2f}s;--g:{w_bg - 0.1:.2f}s;top:366px;left:128px;right:auto;font-size:13px;padding:6px 12px;border-color:var(--purple);color:var(--purple)">{{ }} қавси системавӣ</div>
<div class="pill pop gone" style="--a:{w_qo:.2f}s;--g:{w_bg - 0.1:.2f}s;left:auto;right:16px;top:366px;font-size:13px;padding:6px 12px;border-color:var(--pink);color:var(--pink)">дар дохил — қоида</div>
<div class="brw pop" style="--a:{T[15] + 0.2:.2f}s;top:412px;left:70px;right:70px"><div class="ub"><i></i><i></i><i></i><span>🔒 index.html</span></div><div class="pg" style="height:130px;display:flex;align-items:center;justify-content:center">
 <span class="abs" style="{BT};background:#efefef">Илова</span>
 <span class="abs fade" style="--a:{w_sb:.2f}s;{BT};background:green">Илова</span>
 <span class="abs fade" style="--a:{w_dv2 + 0.3:.2f}s;{BT};background:green;border-radius:12px;box-shadow:0 0 0 6px #fff">Илова</span></div></div>
<div class="pill pop" style="--a:{w_sb + 0.1:.2f}s;left:40px;right:auto;top:606px;font-size:16px;border-color:var(--ok);color:var(--ok)">сабз ✓</div>
<div class="pill pop" style="--a:{w_dv2 + 0.4:.2f}s;left:auto;right:40px;top:606px;font-size:16px;border-color:var(--ok);color:var(--ok)">гӯшаҳо мудаввар ✓</div>
<div class="pill acc2 pop" style="--a:{T[17] + 0.2:.2f}s;top:654px;font-size:18px">дарҳол иваз шуд ⚡</div>''')
sfx("pop", T[15] + 0.2, 0.5); sfx("pop", w_no, 0.5); sfx("pop", w_qv, 0.5); sfx("pop", w_qo, 0.5)
sfx("ding", w_sb, 0.8); sfx("ding", w_dv2 + 0.3, 0.8); sfx("chime", T[17] + 0.2, 0.7)

# ===== ХУЛОСА (T18..T21) =====
scene(T[18] - 0.1, T[21] - 0.1, f'''
<div class="kicker" style="top:120px">ХУЛОСА</div>
<div class="sumc pop" style="--a:{WT(18, 'эйч'):.2f}s;top:165px;border-color:rgba(189,147,249,.6)"><div class="ic emo">🧱</div><div class="nm" style="color:var(--purple)">HTML</div><div class="ds">чӣ ҳаст</div></div>
<div class="sumc pop" style="--a:{T[19]:.2f}s;top:290px;border-color:rgba(255,121,198,.6)"><div class="ic emo">🎨</div><div class="nm" style="color:var(--pink)">CSS</div><div class="ds">чӣ гуна менамояд</div></div>
<div class="sumc pop" style="--a:{WT(20, 'ҷаваскрипт'):.2f}s;top:415px;border-color:rgba(220,220,170,.6)"><div class="ic emo">⚙️</div><div class="nm" style="color:var(--fn)">JS</div><div class="ds">чӣ кор мекунад</div></div>
<div class="pill ok pop" style="--a:{WT(20, 'кор') + 0.3:.2f}s;top:560px;font-size:18px">се забон — як сайт</div>''')
sfx("pop", WT(18, 'эйч'), 0.9); sfx("pop", T[19], 0.9); sfx("pop", WT(20, 'ҷаваскрипт'), 0.9); sfx("ding", WT(20, 'кор') + 0.3, 0.5)

# ===== САНҶИШ (T21..T24) =====
w_q1 = WT(21, "эйч")
qc = F("h1") + " { " + P("color") + ": " + S_("red") + "; }"
scene(T[21] - 0.1, T[24] - 0.1, f'''
<div class="kicker" style="top:110px">САНҶИШ</div>
<div class="h1 pop" style="--a:{T[21] + 0.05:.2f}s;top:138px;font-size:34px">ранги кадом чиз<br><span style="color:#FF5C5C">сурх</span> мешавад?</div>
<div class="ide" style="top:238px;left:40px;right:40px"><div class="bar"><i></i><i></i><i></i><span>style.css</span></div><div class="code" style="font-size:21px;padding-top:12px">
<div class="ln" style="height:36px">{TYP(w_q1, 1.3, qc, 'h1 { color: red; } ')}</div></div></div>
{brw(386, T[21] + 0.3, '<div style="height:100px">' + RAW_PAGE + '</div>', url="index.html", left=70, right=70)}
<div class="h1 acc pop" style="--a:{T[22]:.2f}s;top:550px;font-size:60px">?</div>
<div class="pill ok pop" style="--a:{T[23]:.2f}s;top:654px">💬 ҷавобро дар шарҳ нависед</div>''')
sfx("pop", T[21] + 0.05, 0.6); sfx("pop", T[21] + 0.3, 0.5); sfx("pop", T[22], 0.8); sfx("tick2", T[22], 0.5); sfx("pop", T[23], 0.6)

# ===== ПАЙВАНД ДАР ОПИСАНИЯ (T24..T25) =====
w_vd = WT(24, "видеои"); w_sl = WT(24, "силка"); w_op = WT(24, "описанияи")
scene(T[24] - 0.1, T[25] - 0.1, f'''
<div class="kicker" style="top:105px">ВИДЕОИ ПУРРА ДАР YOUTUBE</div>
<div class="card pop" style="--a:{w_vd:.2f}s;left:50px;right:50px;top:135px;padding:0;overflow:hidden">
 <div style="height:120px;background:linear-gradient(135deg,#2a1f45,#1E1E1E);display:flex;align-items:center;justify-content:center"><div style="width:58px;height:42px;border-radius:11px;background:#F4443C;color:#fff;font-size:20px;line-height:42px;text-align:center">▶</div></div>
 <div style="padding:9px 16px"><div style="font:800 16px 'Segoe UI';color:var(--white)">Дарси 11: HTML ва CSS</div><div style="font:600 12px 'Segoe UI';color:var(--muted);margin-top:2px">YouTube · видеои пурраи дарс</div></div></div>
<div class="h1 pop bob" style="--a:{w_sl - 0.2:.2f}s;top:290px;font-size:40px;color:var(--purple)">↓</div>
<div class="abs pop" style="--a:{w_sl:.2f}s;left:70px;top:345px;width:400px;height:335px;border-radius:18px;overflow:hidden;border:1px solid var(--line);box-shadow:0 20px 50px rgba(0,0,0,.6)"><img src="profile.png" style="width:400px;height:335px;display:block"/>
 <div class="hlt" style="--a:{w_op:.2f}s;--b:{END + 5:.2f}s;position:absolute;left:8px;top:260px;width:290px;height:30px;border-radius:10px;border:2.5px solid var(--pink)"></div></div>''')
sfx("pop", w_vd, 0.7); sfx("pop", w_sl, 0.7); sfx("chime", w_op + 0.1, 0.7)

# ===== ДАРСИ ОЯНДА (T25..T26) =====
t_s = WT(25, "сайт"); t_k = WT(25, "кор")
scene(T[25] - 0.1, T[26] - 0.1, f'''
<div class="kicker" style="top:120px">ДАРСИ ОЯНДА</div>
<div class="h1 pop" style="--a:{T[25] + 0.05:.2f}s;top:158px;font-size:36px">12 · <span class="acc">Сайт чӣ тавр</span><br>кор мекунад?</div>
<div class="demo pop" style="--a:{t_s:.2f}s;left:24px;top:300px"><div class="emo" style="font-size:54px">💻</div><small>браузер</small></div>
<div class="demo pop" style="--a:{t_s + 0.25:.2f}s;left:195px;top:300px"><div class="emo" style="font-size:54px">🌐</div><small>интернет</small></div>
<div class="demo pop" style="--a:{t_k:.2f}s;left:366px;top:300px"><div class="emo" style="font-size:54px">🗄</div><small>сервер</small></div>
<div class="pill acc2 pop" style="--a:{t_k + 0.3:.2f}s;top:500px;font-size:19px;padding:10px 24px">аз суроға то саҳифа</div>''')
sfx("hit", T[25] + 0.05, 0.7); sfx("pop", t_s, 0.7); sfx("pop", t_s + 0.25, 0.7); sfx("pop", t_k, 0.7)

# ===== ОБУНА (T26..END) =====
t_sub = SN[26]['start'] + 0.2
scene(T[26] - 0.1, END + 5, f'''
<div class="kicker" style="top:150px">БАРНОМАСОЗӢ АЗ СИФР</div>
<div class="h1 pop" style="--a:{T[26] + 0.05:.2f}s;top:200px;font-size:50px"><span class="acc">HTML</span> ва <span class="acc">CSS</span></div>
<div class="pill acc2 pop" style="--a:{t_sub:.2f}s;top:330px;font-size:22px;padding:13px 32px">🔔 Обуна шавед</div>''')
sfx("hit", T[26] + 0.05, 0.7); sfx("pop", t_sub, 0.8); sfx("ding", t_sub + 0.1, 0.6)

H = [re.sub(r'</div>\s+<div class="ln"', '</div><div class="ln"', h) for h in H]
html = f'''<!doctype html><html lang="tg"><head><meta charset="utf-8"><link rel="stylesheet" href="style.css"></head><body>
{"".join(H)}
{"".join(cap_html)}
</body></html>'''
open('reel.html', 'w', encoding='utf-8').write(html)
json.dump(dict(end=END, sfx=SFX), open('sfx.json', 'w'))
print('END', END, 'sfx', len(SFX), 'captions', len(cap_html))
