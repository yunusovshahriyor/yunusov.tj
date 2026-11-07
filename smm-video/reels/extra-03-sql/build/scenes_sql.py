
LIGHT = []
HANDLE = '<div class="handle"><span class="ig"></span>@SHAHRIYOR_YUNUSOV</div>'
DGLOW = '<div class="glow fade" style="--a:0s;width:520px;height:520px;left:10px;top:150px;background:radial-gradient(circle,rgba(43,107,255,.75),rgba(20,50,150,.35) 55%,transparent 72%)"></div>'
LGLOW = '<div class="glow fade" style="--a:0s;width:480px;height:480px;left:30px;top:220px;background:radial-gradient(circle,rgba(110,240,205,.85),rgba(110,240,205,.22) 60%,transparent 72%)"></div>'

def sc3(a, b, body, light=False, whoosh=True):
    if light: LIGHT.append((a, b))
    bg = '<div class="bgl"></div>' if light else '<div class="bgd"></div>'
    H.append(f'<div class="sc{" l" if light else ""}" style="{S(a, b)}">{bg}{body}{HANDLE}</div>')
    if whoosh: sfx("whoosh", a - 0.05, 0.35)

H.append('''<style>
.tb{position:absolute;left:36px;right:36px;border-radius:22px;overflow:hidden;background:linear-gradient(160deg,rgba(255,255,255,.13),rgba(255,255,255,.04));border:1px solid rgba(255,255,255,.17);box-shadow:0 26px 60px rgba(0,0,0,.5),inset 0 1px 0 rgba(255,255,255,.25)}
.l .tb{background:rgba(255,255,255,.86);border:1px solid #fff;box-shadow:0 22px 50px rgba(60,90,130,.2)}
.tb .th,.tb .tr{display:grid;gap:8px;padding:11px 18px;align-items:center}
.tb .th{font:700 12px 'Cascadia Mono',Consolas,monospace;letter-spacing:2px;color:#8B949E;background:rgba(255,255,255,.06)}
.l .tb .th{background:rgba(24,32,46,.05)}
.tb .tr{border-top:1px solid rgba(255,255,255,.08);font:700 20px 'Segoe UI'}
.l .tb .tr{border-top:1px solid rgba(24,32,46,.08)}
.tr.hlon{animation:rhl .35s ease-out var(--h) forwards}
@keyframes rhl{to{background:rgba(91,140,255,.32)}}
.l .tr.hlon{animation:rhl2 .35s ease-out var(--h) forwards}
@keyframes rhl2{to{background:#CFE0FF}}
.tr.dimon{animation:rdim .35s ease-out var(--h) forwards}
@keyframes rdim{to{opacity:.25}}
.idc{color:#FFE53A;font-family:'Cascadia Mono',Consolas,monospace}
.l .idc{color:#B8860B}
.glass.ph{border-radius:36px}
.hide{position:absolute;inset:0;pointer-events:none;animation:hide .3s ease-in var(--g) forwards}
@keyframes hide{to{opacity:0}}
.contact{display:flex;align-items:center;gap:12px;padding:10px 14px;border-top:1px solid rgba(255,255,255,.08);font:700 16px 'Segoe UI'}
.av{width:34px;height:34px;border-radius:50%;background:linear-gradient(135deg,#2B6BFF,#8B5CF6);display:flex;align-items:center;justify-content:center;font:800 14px 'Segoe UI'}
.contact small{display:block;font:500 11px 'Cascadia Mono',Consolas,monospace;color:#8B949E}
.cap.lt{--hi:#1F6BFF}
</style>''')

def tbl(top, rows, a, cols=("ном", "шаҳр"), widths=None, ids=False, hl=(), dim=(), hlat=0, stagger=0.25, cls="glin", left=36, right=36, pad=None):
    n = len(cols) + (1 if ids else 0)
    tpl = widths or ("46px " if ids else "") + " ".join(["1fr"] * len(cols))
    head = ("<span>id</span>" if ids else "") + "".join(f"<span>{c}</span>" for c in cols)
    body = ""
    for k, r in enumerate(rows):
        cells = (f'<span class="idc">{k + 1}</span>' if ids else "") + "".join(f"<span>{x}</span>" for x in r)
        extra = ""
        if k in hl: extra += f' hlon" style="--h:{hlat:.2f}s;grid-template-columns:{tpl}'
        elif k in dim: extra += f' dimon" style="--h:{hlat:.2f}s;grid-template-columns:{tpl}'
        if extra: body += f'<div class="tr{extra}">{cells}</div>'
        else: body += f'<div class="tr" style="grid-template-columns:{tpl}">{cells}</div>'
    return (f'<div class="tb {cls}" style="--a:{a:.2f}s;top:{top}px;left:{left}px;right:{right}px"><div class="th" style="grid-template-columns:{tpl}">{head}</div>{body}</div>')

CUST = [("Алӣ", "Душанбе"), ("Мариям", "Хуҷанд"), ("Фарҳод", "Душанбе")]
FN = lambda s: f'<span style="color:#FFE08A">{s}</span>'

# ===== 1 · ХУК (0..T0) =====
p0, p1 = PRE
w_tel = WT(0, "телефони", 0, p0); w_sad = WT(0, "садҳо", 0, p0); w_har = WT(0, "ҳар", 0, p0); w_son = WT(0, "сония", 0, p0); w_ch = WT(1, "чӣ", 0, p1)
contacts = [("А", "Алӣ", "+992 90 ••• 12 34"), ("М", "Мариям", "+992 93 ••• 56 78"), ("Ф", "Фарҳод", "+992 91 ••• 90 12"), ("Н", "Нилуфар", "+992 98 ••• 34 56"), ("Р", "Рустам", "+992 92 ••• 78 90")]
crow = ""
for k, (l, n, p) in enumerate(contacts):
    cl = ' hlon" style="--h:' + f"{w_son:.2f}s" if k == 0 else (' dimon" style="--h:' + f"{w_son:.2f}s" if k > 0 else "")
    crow += f'<div class="contact{cl}"><div class="av">{l}</div><div>{n}<small>{p}</small></div></div>'
sc3(0, T[0] - 0.1, f'''
{DGLOW}
<div class="glass glin" style="--a:{w_tel:.2f}s;left:150px;top:140px;width:240px;height:450px;border-radius:36px;overflow:hidden">
 <div class="abs" style="left:0;right:0;top:0;height:6px"></div>
 <div style="margin:18px 14px 8px;padding:9px 14px;border-radius:99px;background:rgba(255,255,255,.1);font:600 15px 'Segoe UI';display:flex;gap:8px"><span>🔍</span><span style="min-height:20px"><span class="reveal" style="--a:{w_har:.2f}s;--d:0.5s">Алӣ</span></span></div>
 <div class="fade" style="--a:{w_sad:.2f}s">{crow}</div></div>
<div class="pillg pop" style="--a:{w_son:.2f}s;left:36%;top:620px">⏱ 1 сония</div>
<div class="pillg pop" style="--a:{w_ch:.2f}s;left:62%;top:620px;background:linear-gradient(90deg,#2B6BFF,#8B5CF6);border:0">Чӣ тавр? 🤔</div>''', whoosh=False)
sfx("pop", w_tel, 0.5); sfx("tick2", w_har, 0.4); sfx("ding", w_son, 0.6); sfx("pop", w_ch, 0.7)

# ===== 2 · БАЗАИ МАЪЛУМОТ + «ТАРСОНАНДА → ОДДӢ» (T0..T2) =====
w_ts = WT(1, "тарсонанда"); w_df = WT(1, "дафтари")
sc3(T[0] - 0.1, T[2] - 0.1, f'''
{DGLOW}
<div class="c emo pop bob" style="--a:{T[0]:.2f}s;top:150px;font-size:80px">🗄</div>
<div class="c rise" style="--a:{T[0] + 0.1:.2f}s;top:270px;font:700 44px/1.1 'Segoe UI Semibold';letter-spacing:-.6px">Базаи</div>
<div class="c num blurin" style="--a:{T[0] + 0.25:.2f}s;top:322px;font-size:72px;letter-spacing:-3px">маълумот</div>
<div class="glass pop" style="--a:{w_ts:.2f}s;left:70px;right:70px;top:470px;height:120px;border-color:rgba(255,200,80,.5);text-align:center;padding-top:20px"><div class="emo" style="font-size:36px">⚠️</div><div style="font:700 20px 'Segoe UI Semibold';margin-top:4px">калимаи тарсонанда</div></div>
<div class="glass pop" style="--a:{w_df:.2f}s;left:70px;right:70px;top:470px;height:120px;border-color:rgba(53,224,181,.5);text-align:center;padding-top:20px;background:linear-gradient(160deg,rgba(53,224,181,.2),rgba(53,224,181,.05))"><div class="emo" style="font-size:36px">📒</div><div style="font:700 20px 'Segoe UI Semibold';margin-top:4px">дафтари хубсохташуда</div></div>''')
sfx("hit", T[0], 0.6); sfx("pop", T[0] + 0.1, 0.5); sfx("buzz", w_ts, 0.4); sfx("chime", w_df, 0.6)

# ===== 3 · ДАФТАРЧА → ҶАДВАЛ (T2..T6) =====
w_sat = WT(5, "сатр", 0); w_sut = WT(5, "сутун")
sc3(T[2] - 0.1, T[6] - 0.1, f'''
{DGLOW}
<div class="title rise" style="--a:{T[2]:.2f}s;top:135px">Дафтарчаи мағоза 📒</div>
{tbl(215, CUST, T[3], cols=("ном", "шаҳр"), hl=(), stagger=0.3)}
<div class="pillg pop" style="--a:{T[3] + 0.2:.2f}s;left:20px;top:410px">сатр = як харидор</div>
<div class="glass slamin" style="--a:{T[4]:.2f}s;left:150px;right:150px;top:470px;height:70px;border-radius:99px;display:flex;align-items:center;justify-content:center;background:linear-gradient(90deg,rgba(43,107,255,.5),rgba(139,92,246,.5));font:800 28px 'Segoe UI Semibold'">ҶАДВАЛ</div>
<div class="pillg pop" style="--a:{w_sat:.2f}s;left:50px;top:580px;border-color:rgba(255,141,161,.6);color:#FF8DA1">→ сатр = як нафар</div>
<div class="pillg pop" style="--a:{w_sut:.2f}s;left:270px;top:580px;border-color:rgba(125,240,207,.6);color:#7DF0CF">↓ сутун = як хосият</div>''')
sfx("pop", T[2] + 0.1, 0.5); sfx("pop", T[3], 0.6); sfx("hit", T[4], 0.6); sfx("pop", w_sat, 0.5); sfx("pop", w_sut, 0.5)

# ===== 4 · 5 → 5 000 (T6..T9) =====
w_hz = WT(7, "ҳазор"); w_im = WT(8, "имконнопазир")
bars = "".join(f'<i style="display:block;height:6px;border-radius:3px;background:rgba(255,255,255,{.35 if k % 5 else .6});margin:5px 0;width:{55 + (k * 37) % 40}%"></i>' for k in range(30))
sc3(T[6] - 0.1, T[9] - 0.1, f'''
{DGLOW}
<div class="title rise" style="--a:{T[6]:.2f}s;top:135px">Ҳоло дар дафтар</div>
<div class="hide" style="--g:{w_hz:.2f}s"><div class="c num blurin" style="--a:{T[6] + 0.2:.2f}s;top:200px;font-size:150px">5</div>
<div class="c rise" style="--a:{T[6] + 0.4:.2f}s;top:360px;font:600 24px 'Segoe UI Semibold';opacity:.8">харидор — ҳама чиз равшан ✓</div></div>
<div class="c num blurin" style="--a:{w_hz:.2f}s;top:215px;font-size:110px">5 000</div>
<div class="glass glin" style="--a:{w_hz + 0.3:.2f}s;left:50px;right:50px;top:380px;height:190px;overflow:hidden;padding:14px 18px"><div class="bob">{bars}</div></div>
<div class="pillg pop" style="--a:{w_im:.2f}s;left:130px;top:600px;border-color:rgba(255,77,109,.6);color:#FF8DA1">✋ дастӣ — имконнопазир</div>''')
sfx("thud", T[6] + 0.2, 0.6); sfx("whoosh", w_hz - 0.1, 0.5); sfx("thud", w_hz, 0.8); sfx("buzz", w_im, 0.5)

# ===== 5 · SQL — ЗАБОНИ ПУРСИШ (T9..T11) =====
w_sql = WT(9, "эс");
sc3(T[9] - 0.1, T[11] - 0.1, f'''
{DGLOW}
<div class="title rise" style="--a:{T[9]:.2f}s;top:135px">Барои ин — забони махсус</div>
<div class="glass pop" style="--a:{w_sql:.2f}s;left:150px;top:230px;width:240px;height:130px;display:flex;align-items:center;justify-content:center;box-shadow:0 0 80px rgba(43,107,255,.7),0 30px 70px rgba(0,0,0,.5)"><div class="num" style="font-size:78px;letter-spacing:-1px">SQL</div></div>
<div class="glass glin" style="--a:{T[10]:.2f}s;left:36px;right:36px;top:410px;padding:20px 22px;text-align:center"><div style="font:600 13px 'Cascadia Mono',Consolas;letter-spacing:2px;color:#7DF0CF;margin-bottom:8px">МИСЛИ ҶУМЛАИ ОДДӢ</div>
 <div style="font:700 26px/1.3 'Segoe UI Semibold'">гир <b style="color:#5B8CFF">ном</b> аз <b style="color:#5B8CFF">харидорон</b>,<br>ки <b style="color:#5B8CFF">шаҳр</b> — Душанбе</div></div>''')
sfx("pop", w_sql, 0.7); sfx("chime", w_sql + 0.2, 0.5); sfx("pop", T[10] + 0.1, 0.5)

# ===== 6 · ЗАПРОС + НАТИҶА (T11..T13) =====
qh = FN("SELECT") + " name " + FN("FROM") + " customers " + FN("WHERE") + " city = " + '<span style="color:#FF9A6B">\'Душанбе\'</span>'
qr = "SELECT name FROM customers WHERE city = 'Душанбе'"
chips = [("SELECT", "гир", "селект"), ("name", "ном", "неим"), ("FROM", "аз", "фром"), ("customers", "харидорон", "кастомерс"), ("WHERE", "ки", "вер"), ("city", "шаҳр", "сити")]
cx = ""
for k, (en, tj, voice) in enumerate(chips):
    t_ = WT(11, voice)
    cx += f'<div class="pillg pop" style="--a:{t_:.2f}s;left:{36 + (k % 3) * 160}px;top:{250 + (k // 3) * 52}px;font-size:13px;padding:8px 12px"><span style="font-family:Cascadia Mono,Consolas;color:#FFE08A">{en}</span> = {tj}</div>'
    sfx("tick2", t_, 0.3)
w_aly = WT(12, "алӣ"); w_sn = WT(12, "сония")
sc3(T[11] - 0.1, T[13] - 0.1, f'''
{DGLOW}
<div class="title rise" style="--a:{T[11]:.2f}s;top:135px">Запрос</div>
<div class="glass glin" style="--a:{T[11]:.2f}s;left:20px;right:20px;top:195px;height:60px;display:flex;align-items:center;padding:0 16px;font:600 13.5px 'Cascadia Mono',Consolas;border-radius:16px">{TYP(T[11] + 0.1, 2.6, qh, qr)}</div>
{cx}
{tbl(375, CUST, w_aly - 0.5, cols=("ном", "шаҳр"), hl=(0, 2), dim=(1,), hlat=w_aly, stagger=0.2, cls="glin")}
<div class="pillg pop" style="--a:{w_sn:.2f}s;left:150px;top:560px">⏱ дар як сония</div>''')
sfx("pop", T[11], 0.4); sfx("ding", w_aly, 0.6); sfx("ding", w_aly + 0.4, 0.6); sfx("pop", w_sn, 0.5)

# ===== 7 · ДУ «АЛӢ» → РАҚАМИ ЯКТО (T13..T17) =====
w_rq = WT(15, "рақами"); w_sh = WT(15, "шиноснома"); w_kd = WT(16, "калиди")
ROWS4 = [("Алӣ", "Душанбе"), ("Мариям", "Хуҷанд"), ("Фарҳод", "Душанбе"), ("Алӣ", "Кӯлоб")]
sc3(T[13] - 0.1, T[17] - 0.1, f'''
{LGLOW}
<div class="title rise" style="--a:{T[13]:.2f}s;top:135px">Ду «Алӣ» 🤔</div>
{tbl(205, ROWS4, T[13] + 0.1, cols=("ном", "шаҳр"), hl=(0, 3), hlat=T[13] + 0.6, stagger=0.2, cls="glin")}
<div class="pillg pop" style="--a:{T[14]:.2f}s;left:110px;top:455px;font-size:17px">Чӣ тавр фарқ кунем?</div>
<div class="gl pop" style="--a:{w_rq:.2f}s;left:70px;right:70px;top:515px;height:90px;display:flex;align-items:center;gap:16px;padding:0 24px"><span class="emo" style="font-size:40px">🪪</span><span style="font:700 22px 'Segoe UI Semibold'">рақами якто — мисли шиноснома</span></div>
<div class="pillg pop" style="--a:{w_kd:.2f}s;left:120px;top:625px;background:linear-gradient(90deg,#FFB23A,#FF7A2D);border:0;color:#18202E">🔑 калиди асосӣ</div>''', light=True)
sfx("pop", T[13] + 0.1, 0.5); sfx("pop", T[14], 0.5); sfx("pop", w_rq, 0.6); sfx("chime", w_kd, 0.7)

# ===== 8 · ҶАДВАЛИ ДУЮМ (T17..T21) =====
w_ch = WT(18, "чек"); w_iv = WT(19, "иваз"); w_pv = WT(20, "пайваст")
PUR = [("1", "нон"), ("3", "шир"), ("4", "себ")]
sc3(T[17] - 0.1, T[21] - 0.1, f'''
{DGLOW}
<div class="title rise" style="--a:{T[17]:.2f}s;top:135px">Ҷадвалҳо бо рақам</div>
<div class="c rise" style="--a:{T[17] + 0.1:.2f}s;top:182px;font:600 13px 'Cascadia Mono',Consolas;letter-spacing:2px;color:#8B949E">харидорон</div>
{tbl(205, ROWS4, T[17] - 0.1, cols=("ном", "шаҳр"), ids=True, left=36, right=36, cls="fade")}
<div class="c rise" style="--a:{T[17] + 0.3:.2f}s;top:430px;font:600 13px 'Cascadia Mono',Consolas;letter-spacing:2px;color:#8B949E">харидҳо</div>
{tbl(452, PUR, T[17] + 0.4, cols=("рақами харидор", "мол"), widths="1.2fr 1fr", cls="glin")}
<div class="pillg pop" style="--a:{w_ch:.2f}s;left:60px;top:648px;font-size:14px">🧾 мисли чек: танҳо рақам</div>
<div class="pillg pop" style="--a:{w_iv:.2f}s;left:300px;top:648px;font-size:14px;border-color:rgba(125,240,207,.6);color:#7DF0CF">✏ ном — як ҷо</div>''')
sfx("pop", T[17], 0.5); sfx("pop", T[17] + 0.4, 0.5); sfx("pop", w_ch, 0.5); sfx("ding", w_iv, 0.5); sfx("chime", w_pv, 0.6)

# ===== 9 · ҲАМА СОҲА (T21..T23) =====
w_mu = WT(21, "муаллим"); w_tb = WT(21, "табиб"); w_dh = WT(21, "деҳқон"); w_hm = WT(22, "ҷадвал")
cards = [("📚", "Муаллим", "журнали синф", w_mu), ("🩺", "Табиб", "рӯйхати беморон", w_tb), ("🌾", "Деҳқон", "ҳисоби ҳосил", w_dh)]
cc = "".join(f'<div class="gl glin" style="--a:{t_:.2f}s;left:46px;right:46px;top:{200 + k * 112}px;height:92px;display:flex;align-items:center;gap:18px;padding:0 24px"><span class="emo" style="font-size:42px">{e}</span><div><div style="font:700 24px \'Segoe UI Semibold\'">{n}</div><div style="font:600 16px \'Segoe UI\';color:#5a6579">{d}</div></div><span style="margin-left:auto;font:800 12px \'Cascadia Mono\',Consolas;color:#1F6BFF;letter-spacing:2px">ҶАДВАЛ</span></div>' for k, (e, n, d, t_) in enumerate(cards))
sc3(T[21] - 0.1, T[23] - 0.1, f'''
{LGLOW}
<div class="title rise" style="--a:{T[21]:.2f}s;top:135px">Дар ҳама соҳа</div>
{cc}
<div class="pillg pop" style="--a:{w_hm:.2f}s;left:130px;top:555px;background:linear-gradient(90deg,#2B6BFF,#8B5CF6);border:0;color:#fff">ҳамаи инҳо — ҷадвал ✓</div>''', light=True)
for t_ in (w_mu, w_tb, w_dh): sfx("pop", t_, 0.6)
sfx("chime", w_hm, 0.6)

# ===== 10 · МОТИВАТСИЯ (T23..T25) =====
w_mt = WT(23, "барномасоз"); w_ls = WT(23, "лозим"); w_rz = WT(24, "рӯз")
dots = "".join(f'<i class="pop" style="--a:{w_rz + 0.2 + k * 0.05:.2f}s;display:block;width:22px;height:22px;border-radius:7px;background:linear-gradient(135deg,#7DF0CF,#5B8CFF)"></i>' for k in range(21))
sc3(T[23] - 0.1, T[25] - 0.1, f'''
<div class="glow fade" style="--a:{T[23]:.2f}s;width:520px;height:520px;left:10px;top:80px;background:radial-gradient(circle,rgba(139,92,246,.75),rgba(43,107,255,.3) 55%,transparent 72%)"></div>
<div class="glow fade" style="--a:{T[23]:.2f}s;width:340px;height:340px;left:-80px;top:540px;background:radial-gradient(circle,rgba(53,224,181,.5),transparent 70%)"></div>
<div class="c rise" style="--a:{T[23] + 0.05:.2f}s;top:170px;font:600 36px/1.1 'Segoe UI Semibold';letter-spacing:-.5px">барномасоз будан</div>
<div class="c blurin" style="--a:{w_ls:.2f}s;top:225px;font:300 64px/1 'Segoe UI Light';letter-spacing:-2px">лозим нест</div>
<div class="glass glin" style="--a:{w_rz:.2f}s;left:50px;right:50px;top:380px;height:170px;text-align:center;padding-top:22px"><div style="font:600 22px 'Segoe UI Semibold'">ҳар рӯз каме ⏱</div><div style="display:grid;grid-template-columns:repeat(7,1fr);gap:8px;justify-items:center;margin:16px 22px 0">{dots}</div></div>''')
sfx("hit", T[23] + 0.05, 0.6); sfx("pop", w_ls, 0.6)
for k in range(0, 21, 3): sfx("tick", w_rz + 0.2 + k * 0.05, 0.4)
sfx("chime", w_rz + 1.2, 0.5)

# ===== 11 · ХУЛОСА (T25..T27) =====
w_rk = WT(25, "рақамҳои"); w_sq = WT(26, "эс-кю-эл") if False else T[26]
sc3(T[25] - 0.1, T[27] - 0.1, f'''
{DGLOW}
<div class="title rise" style="--a:{T[25]:.2f}s;top:135px">Хулоса</div>
<div class="glass pop" style="--a:{T[25] + 0.1:.2f}s;left:70px;right:70px;top:220px;height:100px;display:flex;align-items:center;justify-content:center;font:700 30px 'Segoe UI Semibold'">ҷадвалҳо</div>
<div class="c pop" style="--a:{w_rk - 0.2:.2f}s;top:340px;font-size:44px;color:#5B8CFF">+</div>
<div class="glass pop" style="--a:{w_rk:.2f}s;left:70px;right:70px;top:410px;height:100px;display:flex;align-items:center;justify-content:center;font:700 26px 'Segoe UI Semibold'">🔑 рақамҳои пайвасткунанда</div>
<div class="pillg pop" style="--a:{T[26]:.2f}s;left:110px;top:560px;background:linear-gradient(90deg,#2B6BFF,#8B5CF6);border:0;font-size:18px;padding:12px 24px">SQL — забон барои пурсидан</div>''')
sfx("pop", T[25] + 0.1, 0.5); sfx("pop", w_rk, 0.6); sfx("chime", T[26], 0.7)

# ===== 12 · САНҶИШ (T27..END) =====
w_hj = WT(28, "хуҷанд"); q_h = WT(28, "бипурсем")
qh2 = FN("SELECT") + " name " + FN("FROM") + " customers " + FN("WHERE") + " city = " + '<span style="color:#FF9A6B">\'Хуҷанд\'</span>'
qr2 = "SELECT name FROM customers WHERE city = 'Хуҷанд'"
sc3(T[27] - 0.1, END + 5, f'''
{LGLOW}
<div class="title rise" style="--a:{T[27]:.2f}s;top:135px">Санҷиш 🎯</div>
{tbl(195, CUST, T[27] + 0.3, cols=("ном", "шаҳр"), cls="glin")}
<div class="gl glin" style="--a:{q_h:.2f}s;left:20px;right:20px;top:395px;height:56px;display:flex;align-items:center;padding:0 14px;font:700 13px 'Cascadia Mono',Consolas;border-radius:16px;color:#18202E">{TYP(q_h + 0.05, 2.0, qh2.replace("#FFE08A", "#B8860B"), qr2)}</div>
<div class="c blurin" style="--a:{w_hj + 0.3:.2f}s;top:470px;font:700 100px 'Segoe UI';color:#1F6BFF">?</div>
<div class="pillg pop" style="--a:{T[29]:.2f}s;left:130px;top:620px;background:linear-gradient(90deg,#2B6BFF,#8B5CF6);border:0;color:#fff">💬 ҷавобро дар шарҳ нависед</div>''', light=True)
sfx("pop", T[27] + 0.3, 0.5); sfx("pop", w_hj + 0.3, 0.7); sfx("tick2", w_hj + 0.3, 0.4); sfx("pop", T[29], 0.6)

def _lt(h):
    a = float(re.search(r'--a:([\d.]+)s', h).group(1))
    return any(x <= a < y for x, y in LIGHT)
cap_html = [h.replace('<div class="cap"', '<div class="cap lt"', 1) if _lt(h) else h for h in cap_html]
H = [re.sub(r'</div>\s+<div class="ln"', '</div><div class="ln"', h) for h in H]
html = f'''<!doctype html><html lang="tg"><head><meta charset="utf-8"><link rel="stylesheet" href="style3.css"></head><body>
{"".join(H)}
{"".join(cap_html)}
</body></html>'''
open('reel.html', 'w', encoding='utf-8').write(html)
json.dump(dict(end=END, sfx=SFX), open('sfx.json', 'w'))
print('END', END, 'sfx', len(SFX), 'captions', len(cap_html), 'light', LIGHT)
