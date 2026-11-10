
HANDLE = '<div class="handle" style="top:690px">@SHAHRIYOR_YUNUSOV</div>'
LIMEPILL = "background:rgba(215,255,58,.12);color:var(--lime);border:1.5px solid rgba(215,255,58,.5)"
WHITEPILL = "background:rgba(255,255,255,.08);color:#fff;border:1.5px solid rgba(255,255,255,.3)"
def bgn(extra=""): return f'<div class="abs" style="inset:0;{extra}"></div>'

# ===== 1 · ХУК (0..T0) =====
p0 = PRE[0]
t_h = WT(0, "ҳафта", 0, p0); t_m = WT(0, "моҳ", 0, p0); t_s = WT(0, "сол", 0, p0)
scene(0, T[0] - 0.1, f'''
<div class="orb bob" style="width:380px;height:380px;background:#7C4DFF;right:-120px;top:-60px;opacity:.75"></div>
<div class="orb bob" style="width:340px;height:340px;background:#FF4D6D;left:-130px;top:520px;opacity:.55"></div>
<div class="c blk rise" style="--a:0.05s;top:140px;font-size:240px;color:rgba(255,255,255,.05)">?</div>
<div class="pill pop" style="--a:0.1s;top:118px;{LIMEPILL}">⚡ ВАҚТИ ТО БАРНОМАСОЗ ШУДАН</div>
<div class="c blk stroke rise" style="--a:0.2s;top:166px;font-size:38px">Дар чанд вақт</div>
<div class="c blk grad rise" style="--a:0.35s;top:208px;font-size:60px">барномасоз</div>
<div class="c blk rise" style="--a:0.5s;top:272px;font-size:46px">шудан мумкин?</div>
<div class="sticker" style="--a:{t_h:.2f}s;top:380px;--r:-4deg;background:#FF4D6D;color:#fff">1 ҳафта?</div>
<div class="sticker" style="--a:{t_m:.2f}s;top:470px;--r:3deg;background:#7C4DFF;color:#fff">1 моҳ?</div>
<div class="sticker" style="--a:{t_s:.2f}s;top:560px;--r:-2deg;background:#D7FF3A;color:#0A0A12">1 сол?</div>
{HANDLE}''', whoosh=False)
sfx("hit", 0.0, 0.8)
for t_ in (0.2, 0.35, 0.5): sfx("tick", t_, 0.5)
for t_ in (t_h, t_m, t_s): sfx("thud", t_, 0.9); sfx("pop", t_ + 0.1, 0.6)

# ===== 2 · ҶАВОБ (T0..T1) =====
w_az = WT(0, "аз"); w_kh = WT(0, "худи"); w_sh = WT(0, "шумо"); w_vo = WT(0, "вобаста")
scene(T[0] - 0.1, T[1] - 0.1, f'''
{bgn("background:linear-gradient(150deg,#FF4D6D 0%,#C23BDF 55%,#5B3DF5 100%)")}
<div class="orb bob" style="width:360px;height:360px;background:#FFB23A;left:-120px;top:-100px;opacity:.55"></div>
<div class="abs emo pop wig" style="--a:{T[0] + 0.3:.2f}s;right:24px;top:118px;font-size:92px">🫵</div>
<div class="abs blk slidel" style="--a:{T[0]:.2f}s;left:34px;top:190px;font-size:64px">Ин аз</div>
<div class="abs blk slidel" style="--a:{w_kh:.2f}s;left:30px;top:252px;font-size:112px">худи</div>
<div class="abs blk slamin" style="--a:{w_sh:.2f}s;left:30px;top:362px;font-size:112px;color:#0A0A12">Шумо</div>
<div class="abs blk pop" style="--a:{w_vo:.2f}s;left:30px;top:482px;font-size:50px;background:#D7FF3A;color:#0A0A12;padding:6px 16px;border-radius:12px;rotate:-2deg">вобаста ҳаст!</div>
{HANDLE}''')
sfx("hit", T[0], 0.9); sfx("whoosh", w_kh - 0.05, 0.5); sfx("hit", w_sh, 0.9); sfx("pop", w_vo, 0.8); sfx("chime", w_vo + 0.2, 0.6)

# ===== 3 · ЗАБОНИ НАВ (T1..T4) =====
t_se = WT(2, "се"); t_hf = WT(2, "ҳафта"); t_lu = WT(2, "луғат"); t_yod = WT(2, "ёд"); t_hr = WT(3, "ҳар"); t_b = WT(3, "бист"); t_j = WT(3, "ҷумла")
scene(T[1] - 0.1, T[4] - 0.1, f'''
{bgn("background:#0A0A12")}
<div class="abs" style="left:0;right:0;top:0;height:500px;background:linear-gradient(160deg,#3a0f1f,#1a0a12);clip-path:polygon(0 0,100% 0,100% 82%,0 100%)"></div>
<div class="abs fade" style="--a:{t_hr - 0.2:.2f}s;left:0;right:0;top:300px;height:660px;background:linear-gradient(160deg,#0f3a22,#0A1A12);clip-path:polygon(0 25%,100% 8%,100% 100%,0 100%)"></div>
<div class="pill pop" style="--a:{T[1] + 0.05:.2f}s;top:118px;{WHITEPILL}"><span class="emo">📖</span> ЗАБОНИ НАВ ОМӮХТАН</div>
<div class="abs blk slidel" style="--a:{T[2]:.2f}s;left:34px;top:165px;font-size:40px;color:#FF4D6D">1 рӯз:</div>
<div class="abs blk slamin" style="--a:{t_se:.2f}s;left:34px;top:208px;font-size:68px">3 соат</div>
<div class="abs blk rise" style="--a:{t_hf:.2f}s;left:34px;top:292px;font-size:30px;color:#FFB0BD">+ 7 рӯз нест</div>
<div class="abs emo pop bob" style="--a:{t_lu:.2f}s;right:30px;top:250px;font-size:56px;rotate:8deg">🧠💨</div>
<div class="sticker" style="--a:{t_yod:.2f}s;top:380px;--r:-3deg;--s:24px;background:#FF4D6D;color:#fff">ҳама чиз аз ёд меравад ❌</div>
<div class="abs blk slider" style="--a:{t_hr:.2f}s;right:34px;top:462px;font-size:40px;color:var(--lime);text-align:right">ҳар рӯз:</div>
<div class="abs blk grad slamin" style="--a:{t_b:.2f}s;right:34px;top:508px;font-size:80px;text-align:right">20 дақиқа</div>
<div class="sticker" style="--a:{t_j:.2f}s;top:610px;--r:2deg;--s:23px;background:#D7FF3A;color:#0A0A12">як моҳ баъд — ҷумла 💬✅</div>
{HANDLE}''')
sfx("pop", T[1] + 0.05, 0.6); sfx("thud", t_se, 0.8); sfx("pop", t_hf, 0.6); sfx("pop", t_lu, 0.6); sfx("buzz", t_yod, 0.6)
sfx("whoosh", t_hr - 0.1, 0.5); sfx("thud", t_b, 0.9); sfx("chime", t_j, 0.8); sfx("ding", t_j + 0.1, 0.5)

# ===== 4 · ДАР БАРНОМАСОЗӢ ҲАМ (T4..T6) =====
t_k = WT(5, "компютер")
scene(T[4] - 0.1, T[6] - 0.1, f'''
{bgn("background:linear-gradient(170deg,#0d1b3a 0%,#0A0A12 70%)")}
<div class="orb bob" style="width:340px;height:340px;background:#38D5FF;right:-110px;top:140px;opacity:.4"></div>
<div class="pill pop" style="--a:{T[4]:.2f}s;top:118px;{LIMEPILL}">💻 ДАР БАРНОМАСОЗӢ ҲАМ</div>
<div class="c blk stroke slamin" style="--a:{T[4] + 0.05:.2f}s;top:190px;font-size:46px">ҳамин тавр</div>
<div class="abs" style="left:30px;right:30px;top:300px;background:#12121f;border:2px solid #38D5FF;border-radius:20px;padding:22px 18px;box-shadow:0 0 40px rgba(56,213,255,.35)" >
 <div style="font:700 13px var(--mono);color:#38D5FF;letter-spacing:2px;margin-bottom:10px">salom.js</div>
 <div style="font:700 19px var(--mono);color:#fff;white-space:pre">{TYP(T[4] + 0.2, 1.4, '<span style="color:#FFE53A">console</span>.<span style="color:#FFE53A">log</span>(<span style="color:#FF9A6B">"Салом, ҷаҳон!"</span>);', 'console.log("Салом, ҷаҳон!");')}</div>
 <div class="fade" style="--a:{T[5]:.2f}s;font:700 19px var(--mono);color:#D7FF3A;margin-top:12px">&gt; Салом, ҷаҳон!</div></div>
<div class="sticker" style="--a:{t_k:.2f}s;top:520px;--r:-2deg;--s:30px;background:#D7FF3A;color:#0A0A12">забони компютер</div>
{HANDLE}''')
sfx("pop", T[4], 0.6); sfx("ding", T[5], 0.6); sfx("thud", t_k, 0.9)

# ===== 5 · РОҲНАМО (T6..T14) =====
t_a = WT(7, "як"); t_w = WT(11, "рӯйхати")
scene(T[6] - 0.1, T[14] - 0.1, f'''
{bgn()}
<div class="orb bob" style="width:330px;height:330px;background:#7C4DFF;left:-100px;top:200px;opacity:.5"></div>
<div class="orb bob" style="width:280px;height:280px;background:#38D5FF;right:-110px;top:520px;opacity:.35"></div>
<div class="pill pop" style="--a:{T[6]:.2f}s;top:118px;{LIMEPILL}">🗺 РОҲНАМО</div>
<svg class="abs" style="left:0;top:150px" width="540" height="560" viewBox="0 0 540 560"><defs>
<linearGradient id="g" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#FF4D6D"/><stop offset=".5" stop-color="#7C4DFF"/><stop offset="1" stop-color="#D7FF3A"/></linearGradient>
<mask id="m"><path d="M186 520 C 420 470, 420 400, 270 360 S 120 250, 340 210 S 430 120, 300 70" fill="none" stroke="#fff" stroke-width="16" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" class="draw" style="--a:{T[6]:.2f}s;--d:{T[14] - T[6] - 1.2:.2f}s"/></mask></defs>
<g mask="url(#m)"><path d="M186 520 C 420 470, 420 400, 270 360 S 120 250, 340 210 S 430 120, 300 70" fill="none" stroke="url(#g)" stroke-width="10" stroke-linecap="round" stroke-dasharray="2 22"/></g></svg>
<div class="abs blk fade" style="--a:{T[6]:.2f}s;left:24px;top:636px;font-size:15px;color:var(--muted)">ШУМО ИНҶО</div>
<div class="abs pop" style="--a:{T[6]:.2f}s;left:160px;top:626px;width:36px;height:36px;border-radius:50%;background:#fff;box-shadow:0 0 0 8px rgba(255,255,255,.18)"></div>
<div class="abs pop" style="--a:{T[6] + 0.1:.2f}s;left:70px;top:455px;width:64px;height:64px;border-radius:50%;background:#FF4D6D;display:flex;align-items:center;justify-content:center;font:900 30px 'Segoe UI Black';box-shadow:0 0 40px #FF4D6D99">1</div>
<div class="abs slidel" style="--a:{t_a:.2f}s;left:150px;top:445px;background:rgba(10,10,18,.75);padding:8px 12px;border-radius:12px"><div class="blk" style="font-size:30px">АСОСҲО</div><div style="font:700 15px 'Segoe UI';color:#FFB0BD;margin-top:4px">1–3 моҳ · let · if · for</div></div>
<div class="abs pop" style="--a:{T[9]:.2f}s;right:70px;top:318px;width:64px;height:64px;border-radius:50%;background:#7C4DFF;display:flex;align-items:center;justify-content:center;font:900 30px 'Segoe UI Black';box-shadow:0 0 40px #7C4DFF99">2</div>
<div class="abs slider" style="--a:{T[9] + 0.1:.2f}s;right:150px;top:306px;text-align:right;background:rgba(10,10,18,.75);padding:8px 12px;border-radius:12px"><div class="blk" style="font-size:28px">БАРНОМАИ ХУРД</div><div style="font:700 15px 'Segoe UI';color:#C9B8FF;margin-top:4px">+2–3 моҳ · рӯйхати харид</div></div>
<div class="sticker" style="--a:{t_w:.2f}s;left:26%;top:392px;--r:-5deg;--s:19px;background:#fff;color:#0A0A12;padding:8px 16px">☑ нон ☐ шир ☐ себ</div>
<div class="abs pop" style="--a:{T[12]:.2f}s;left:90px;top:200px;width:64px;height:64px;border-radius:50%;background:#D7FF3A;color:#0A0A12;display:flex;align-items:center;justify-content:center;font:900 30px 'Segoe UI Black';box-shadow:0 0 40px #D7FF3A99">3</div>
<div class="abs slidel" style="--a:{T[12] + 0.1:.2f}s;left:170px;top:190px;background:rgba(10,10,18,.75);padding:8px 12px;border-radius:12px"><div class="blk" style="font-size:30px;color:var(--lime)">ҲАР РӮЗ</div><div style="font:700 15px 'Segoe UI';color:#E9FF9A;margin-top:4px">20 дақиқа · ҳатто бо чой ☕</div></div>
<div class="abs emo pop bob" style="--a:{T[13]:.2f}s;left:24px;top:124px;font-size:56px">☕</div>
<div class="abs emo pop bob" style="--a:{T[12] + 0.3:.2f}s;right:60px;top:138px;font-size:64px">🚀</div>
{HANDLE}''')
sfx("pop", T[6] + 0.1, 0.8); sfx("whoosh", T[6], 0.5); sfx("pop", t_a, 0.6); sfx("riser", T[8] + 0.5, 0.25)
sfx("pop", T[9], 0.8); sfx("pop", T[9] + 0.1, 0.6); sfx("pop", t_w, 0.7)
sfx("pop", T[12], 0.8); sfx("chime", T[12] + 0.2, 0.7); sfx("pop", T[13], 0.7)

# ===== 6 · СЕРИЯИ 30 РӮЗА (T14..каме) =====
t_ka = WT(14, "каме")
cells = ""
for k in range(30):
    if k < 24:
        cells += f'<div class="cell" style="--a:{T[14] + 0.5 + k * 0.05:.2f}s;width:34px;height:34px"></div>'
        if k % 3 == 0: sfx("tick", T[14] + 0.5 + k * 0.05, 0.5)
    else:
        cells += '<div style="width:34px;height:34px;border-radius:9px;background:rgba(255,255,255,.08)"></div>'
scene(T[14] - 0.1, t_ka - 0.15, f'''
{bgn()}
<div class="orb bob" style="width:420px;height:420px;background:#FF7A2D;left:60px;top:80px;opacity:.55"></div>
<div class="pill pop" style="--a:{T[14]:.2f}s;top:118px;background:rgba(255,122,45,.15);color:#FFB27A;border:1.5px solid rgba(255,122,45,.6)">🔥 СЕРИЯИ ШУМО</div>
<div class="c emo pop bob" style="--a:{T[14] + 0.1:.2f}s;top:150px;font-size:110px">🔥</div>
<div class="c blk grad slamin" style="--a:{T[14] + 0.3:.2f}s;top:282px;font-size:110px">30 РӮЗ</div>
<div class="c blk rise" style="--a:{T[14] + 0.5:.2f}s;top:392px;font-size:30px">ҲАР РӮЗ 20 ДАҚИҚА</div>
<div class="abs" style="left:34px;right:34px;top:458px;display:grid;grid-template-columns:repeat(10,1fr);gap:6px;justify-items:center">{cells}</div>
{HANDLE}''')
sfx("hit", T[14] + 0.3, 0.8); sfx("chime", T[14] + 1.8, 0.5)

# ===== 7 · ХУЛОСА: 20 + каме/бефосила/мунтазам (каме..T15) =====
t_be = WT(14, "бефосила"); t_mu = WT(14, "мунтазам")
scene(t_ka - 0.2, T[15] - 0.1, f'''
{bgn()}
<div class="orb bob" style="width:400px;height:400px;background:#7C4DFF;left:70px;top:150px;opacity:.6"></div>
<div class="pill pop" style="--a:{t_ka - 0.1:.2f}s;top:118px;{WHITEPILL}">ХУЛОСА</div>
<svg class="abs" style="left:70px;top:170px" width="400" height="400" viewBox="0 0 400 400"><defs><linearGradient id="r" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#D7FF3A"/><stop offset="1" stop-color="#FF4D6D"/></linearGradient></defs>
<circle cx="200" cy="200" r="170" fill="none" stroke="rgba(255,255,255,.1)" stroke-width="22"/>
<circle cx="200" cy="200" r="170" fill="none" stroke="url(#r)" stroke-width="22" stroke-linecap="round" stroke-dasharray="1068" stroke-dashoffset="1068" class="ringfill" style="--a:{t_ka - 0.1:.2f}s;--d:1.6s;stroke-dashoffset:1068" transform="rotate(-90 200 200)"/></svg>
<div class="c blk slamin" style="--a:{t_ka - 0.05:.2f}s;top:262px;font-size:150px">20</div>
<div class="c blk grad rise" style="--a:{t_ka + 0.1:.2f}s;top:410px;font-size:36px">дақиқа</div>
<div class="c blk rise" style="--a:{t_ka + 0.2:.2f}s;top:454px;font-size:26px;color:rgba(255,255,255,.7)">ҳар рӯз</div>
<div class="sticker" style="--a:{t_ka:.2f}s;top:604px;--r:-3deg;--s:22px;background:#D7FF3A;color:#0A0A12;left:28%">каме</div>
<div class="sticker" style="--a:{t_be:.2f}s;top:604px;--r:2deg;--s:22px;background:#FF4D6D;color:#fff;left:62%">бефосила</div>
<div class="sticker" style="--a:{t_mu:.2f}s;top:650px;--r:-1deg;--s:22px;background:#7C4DFF;color:#fff">мунтазам</div>''')
sfx("hit", t_ka, 0.8); sfx("thud", t_ka, 0.8); sfx("thud", t_be, 0.8); sfx("thud", t_mu, 0.8); sfx("chime", t_mu + 0.3, 0.7)

# ===== 8 · САВОЛ (T15..T17) =====
o10 = WT(15, "даҳ"); o20 = WT(15, "бист"); o30 = WT(15, "сӣ")
scene(T[15] - 0.1, T[17] - 0.1, f'''
{bgn("background:linear-gradient(170deg,#2a1070 0%,#0A0A12 70%)")}
<div class="orb bob" style="width:340px;height:340px;background:#FF4D6D;right:-100px;top:120px;opacity:.45"></div>
<div class="pill pop" style="--a:{T[15]:.2f}s;top:118px;{LIMEPILL}">🎯 САВОЛ БА ШУМО</div>
<div class="abs pop" style="--a:{T[15] + 0.1:.2f}s;left:34px;right:34px;top:170px;background:#fff;border-radius:28px;padding:26px 22px 22px;box-shadow:0 22px 60px rgba(0,0,0,.55);rotate:-1.5deg">
 <div class="blk" style="color:#0A0A12;font-size:36px;text-align:center;line-height:1.05">Чанд дақиқа дар рӯз?</div>
 <div style="display:flex;gap:10px;margin-top:20px">
  <div class="flip" style="--a:{o10:.2f}s;flex:1;text-align:center;padding:16px 0;border-radius:16px;background:#F0EEFF"><div class="blk" style="color:#0A0A12;font-size:44px">10</div><div style="font:700 13px 'Segoe UI';color:#555">дақиқа</div></div>
  <div class="flip hl" style="--a:{o20:.2f}s;flex:1;text-align:center;padding:16px 0;border-radius:16px;background:#F0EEFF"><div class="blk" style="color:#0A0A12;font-size:44px">20</div><div style="font:700 13px 'Segoe UI';color:#333">дақиқа</div></div>
  <div class="flip" style="--a:{o30:.2f}s;flex:1;text-align:center;padding:16px 0;border-radius:16px;background:#F0EEFF"><div class="blk" style="color:#0A0A12;font-size:44px">30</div><div style="font:700 13px 'Segoe UI';color:#555">дақиқа</div></div></div></div>
<div class="sticker" style="--a:{T[16]:.2f}s;top:470px;--r:2deg;--s:24px;background:#FF4D6D;color:#fff">💬 ҷавобро дар шарҳ нависед</div>
{HANDLE}''')
sfx("pop", T[15] + 0.1, 0.7)
for t_ in (o10, o20, o30): sfx("tick2", t_, 0.5)
sfx("thud", T[16], 0.8)

# ===== 9 · ДАЪВАТ (T17..T18) =====
t_vid = WT(18 - 1, "шпаргалкаи"); t_dir = WT(17, "директ")
scene(T[17] - 0.1, T[18] - 0.1, f'''
{bgn("background:linear-gradient(160deg,#0A0A12 0%,#1a0f3a 100%)")}
<div class="orb bob" style="width:360px;height:360px;background:#D7FF3A;left:-140px;top:420px;opacity:.28"></div>
<div class="pill pop" style="--a:{T[17]:.2f}s;top:118px;{WHITEPILL}">ШАРҲ ➜ DIRECT</div>
<div class="abs pop" style="--a:{T[17] + 0.05:.2f}s;left:40px;right:40px;top:170px;background:#fff;border-radius:34px 34px 34px 8px;padding:22px 24px;box-shadow:0 20px 50px rgba(0,0,0,.5)">
 <div style="display:flex;align-items:center;gap:14px"><div style="width:40px;height:40px;border-radius:50%;background:linear-gradient(135deg,#7C4DFF,#FF4D6D)"></div><div class="blk" style="color:#0A0A12;font-size:46px;letter-spacing:2px;min-width:140px">{TYP(T[17] + 0.2, 0.9, "ВАҚТ", "ВАҚТ")}</div><div style="margin-left:auto;font:900 24px 'Segoe UI';color:#7C4DFF">➤</div></div></div>
<div class="abs rise bob" style="--a:{t_vid - 0.3:.2f}s;left:50%;top:292px;translate:-50% 0;font-size:54px;color:var(--lime)">↓</div>
<div class="abs slamin" style="--a:{t_vid:.2f}s;left:70px;right:70px;top:360px;background:linear-gradient(135deg,#7C4DFF,#FF4D6D);border-radius:26px;padding:24px;text-align:center;rotate:-2deg;box-shadow:0 20px 50px rgba(0,0,0,.5)">
 <div class="emo" style="font-size:68px">📘</div><div class="blk" style="font-size:30px;margin-top:6px">Шпаргалкаи бепул</div><div style="font:700 14px 'Segoe UI';margin-top:6px;opacity:.9">дарсҳои 1–5 · PDF · ба Direct</div></div>
<div class="sticker" style="--a:{t_dir:.2f}s;top:600px;--r:0deg;--s:24px;background:#D7FF3A;color:#0A0A12">✉ ба Direct мефиристам</div>
{HANDLE}''')
sfx("pop", T[17] + 0.05, 0.7); sfx("hit", t_vid, 0.8); sfx("chime", t_dir, 0.8); sfx("ding", t_dir + 0.1, 0.5)

# ===== 10 · ОБУНА (T18..END) =====
scene(T[18] - 0.1, END + 5, f'''
{bgn("background:linear-gradient(150deg,#5B3DF5 0%,#C23BDF 55%,#FF4D6D 100%)")}
<div class="orb bob" style="width:340px;height:340px;background:#D7FF3A;right:-120px;top:-80px;opacity:.4"></div>
<div class="c blk slamin" style="--a:{T[18] + 0.05:.2f}s;top:200px;font-size:76px;line-height:1">Ҳар рӯз</div>
<div class="c blk slamin" style="--a:{T[18] + 0.25:.2f}s;top:280px;font-size:76px;color:#0A0A12">каме пеш</div>
<div class="sticker" style="--a:{T[18] + 0.8:.2f}s;top:420px;--r:-2deg;--s:30px;background:#D7FF3A;color:#0A0A12">🔔 Обуна шавед</div>
<div class="pill pop" style="--a:{T[18] + 1.1:.2f}s;top:520px;background:rgba(10,10,18,.55);color:#fff;font-size:16px">@shahriyor_yunusov</div>''')
sfx("hit", T[18] + 0.05, 0.8); sfx("hit", T[18] + 0.25, 0.8); sfx("thud", T[18] + 0.8, 0.9); sfx("ding", T[18] + 0.9, 0.7); sfx("pop", T[18] + 1.1, 0.6)

html = f'''<!doctype html><html lang="tg"><head><meta charset="utf-8"><link rel="stylesheet" href="style2.css"></head><body>
{"".join(H)}
{"".join(cap_html)}
</body></html>'''
open('reel.html', 'w', encoding='utf-8').write(html)
json.dump(dict(end=END, sfx=SFX), open('sfx.json', 'w'))
print('END', END, 'sfx', len(SFX), 'captions', len(cap_html))
