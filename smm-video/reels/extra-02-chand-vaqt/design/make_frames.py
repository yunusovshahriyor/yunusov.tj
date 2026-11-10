# Тарҳи нави «мотиватсионӣ» барои Reels-и иловагӣ: 8 кадри асосӣ (540×960 @2x = 1080×1920).
NOISE = "url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/></filter><rect width='100%25' height='100%25' filter='url(%23n)'/></svg>\")"
CSS = """
:root{--ink:#0A0A12;--lime:#D7FF3A;--coral:#FF4D6D;--violet:#7C4DFF;--sky:#38D5FF;--white:#fff;--muted:#9A9AB5}
*{box-sizing:border-box;margin:0;padding:0}
body{width:540px;height:960px;overflow:hidden;position:relative;background:var(--ink);font-family:'Segoe UI',sans-serif;color:#fff}
body::after{content:"";position:absolute;inset:0;background-image:%s;opacity:.10;mix-blend-mode:overlay;pointer-events:none}
.orb{position:absolute;border-radius:50%%;filter:blur(70px)}
.abs{position:absolute}
.blk{font-family:'Segoe UI Black','Segoe UI',sans-serif;font-weight:900;letter-spacing:-1px;line-height:.98;text-transform:uppercase}
.c{position:absolute;left:0;right:0;text-align:center}
.stroke{color:transparent;-webkit-text-stroke:2px #fff}
.grad{background:linear-gradient(90deg,var(--lime),#FFE53A 60%%,#FFB23A);-webkit-background-clip:text;background-clip:text;color:transparent}
.sticker{position:absolute;left:50%%;transform:translateX(-50%%) rotate(var(--r,0deg));padding:10px 26px;border-radius:18px;font-family:'Segoe UI Black';font-size:var(--s,50px);white-space:nowrap;text-transform:uppercase;box-shadow:0 14px 0 rgba(0,0,0,.35),0 24px 50px rgba(0,0,0,.45)}
.pill{position:absolute;left:50%%;transform:translateX(-50%%);padding:8px 18px;border-radius:999px;font:800 13px 'Cascadia Mono',Consolas,monospace;letter-spacing:2px;white-space:nowrap}
.emo{font-family:'Segoe UI Emoji',sans-serif}
.safe{position:absolute;left:0;right:0;top:0;height:960px}
.handle{position:absolute;left:0;right:0;top:668px;text-align:center;font:700 12px 'Cascadia Mono',Consolas;letter-spacing:3px;color:rgba(255,255,255,.55)}
""" % NOISE

def page(body, bg=""):
    return f'<!doctype html><html lang="tg"><head><meta charset="utf-8"><style>{CSS}</style></head><body style="{bg}">{body}</body></html>'

F = {}

# 1 · ХУК
F[1] = page('''
<div class="orb" style="width:380px;height:380px;background:#7C4DFF;right:-120px;top:-60px;opacity:.75"></div>
<div class="orb" style="width:340px;height:340px;background:#FF4D6D;left:-130px;top:520px;opacity:.55"></div>
<div class="c blk" style="top:140px;font-size:240px;color:rgba(255,255,255,.05)">?</div>
<div class="pill" style="top:118px;background:rgba(215,255,58,.12);color:var(--lime);border:1.5px solid rgba(215,255,58,.5)">⚡ ВАҚТИ ТО БАРНОМАСОЗ ШУДАН</div>
<div class="c blk stroke" style="top:166px;font-size:38px">Дар чанд вақт</div>
<div class="c blk grad" style="top:208px;font-size:60px">барномасоз</div>
<div class="c blk" style="top:272px;font-size:46px">шудан мумкин?</div>
<div class="sticker" style="top:380px;--r:-4deg;--s:50px;background:#FF4D6D;color:#fff">1 ҳафта?</div>
<div class="sticker" style="top:470px;--r:3deg;--s:50px;background:#7C4DFF;color:#fff">1 моҳ?</div>
<div class="sticker" style="top:560px;--r:-2deg;--s:50px;background:#D7FF3A;color:#0A0A12">1 сол?</div>
<div class="handle">@SHAHRIYOR_YUNUSOV</div>''')

# 2 · ҶАВОБ
F[2] = page('''
<div class="abs" style="inset:0;background:linear-gradient(150deg,#FF4D6D 0%,#C23BDF 55%,#5B3DF5 100%)"></div>
<div class="orb" style="width:360px;height:360px;background:#FFB23A;left:-120px;top:-100px;opacity:.55"></div>
<div class="abs emo" style="right:24px;top:118px;font-size:92px;transform:rotate(14deg)">🫵</div>
<div class="c blk" style="top:190px;font-size:64px;text-align:left;padding-left:34px">Ин аз</div>
<div class="c blk" style="top:252px;font-size:112px;text-align:left;padding-left:30px">худи</div>
<div class="c blk" style="top:362px;font-size:112px;text-align:left;padding-left:30px;color:#0A0A12">Шумо</div>
<div class="abs blk" style="left:30px;top:482px;font-size:50px;background:#D7FF3A;color:#0A0A12;padding:6px 16px;border-radius:12px;transform:rotate(-2deg)">вобаста ҳаст!</div>
<div class="handle" style="color:rgba(255,255,255,.75)">@SHAHRIYOR_YUNUSOV</div>''')

# 3 · МИСОЛ: ЗАБОНИ НАВ
F[3] = page('''
<div class="abs" style="left:0;right:0;top:0;height:960px;background:#0A0A12"></div>
<div class="abs" style="left:0;right:0;top:0;height:500px;background:linear-gradient(160deg,#3a0f1f,#1a0a12);clip-path:polygon(0 0,100% 0,100% 82%,0 100%)"></div>
<div class="abs" style="left:0;right:0;top:300px;height:660px;background:linear-gradient(160deg,#0f3a22,#0A1A12);clip-path:polygon(0 25%,100% 8%,100% 100%,0 100%)"></div>
<div class="pill" style="top:118px;background:rgba(255,255,255,.08);color:#fff;border:1.5px solid rgba(255,255,255,.3)"><span class="emo">📖</span> ЗАБОНИ НАВ ОМӮХТАН</div>
<div class="abs blk" style="left:34px;top:165px;font-size:40px;color:#FF4D6D">1 рӯз:</div>
<div class="abs blk" style="left:34px;top:208px;font-size:68px">3 соат</div>
<div class="abs blk" style="left:34px;top:292px;font-size:30px;color:#FFB0BD">+ 7 рӯз нест</div>
<div class="abs" style="right:30px;top:250px;font-size:56px;transform:rotate(8deg)" ><span class="emo">🧠💨</span></div>
<div class="sticker" style="top:380px;--r:-3deg;--s:24px;background:#FF4D6D;color:#fff;font-size:24px">ҳама чиз аз ёд меравад ❌</div>
<div class="abs blk" style="right:34px;top:462px;font-size:40px;color:var(--lime);text-align:right">ҳар рӯз:</div>
<div class="abs blk grad" style="right:34px;top:508px;font-size:80px;text-align:right">20 дақиқа</div>
<div class="sticker" style="top:610px;--r:2deg;background:#D7FF3A;color:#0A0A12;font-size:23px">як моҳ баъд — ҷумла 💬✅</div>
<div class="handle" style="top:700px">@SHAHRIYOR_YUNUSOV</div>''')

# 4 · РОҲНАМО (ХАРИТАИ РОҲ)
F[4] = page('''
<div class="orb" style="width:330px;height:330px;background:#7C4DFF;left:-100px;top:200px;opacity:.5"></div>
<div class="orb" style="width:280px;height:280px;background:#38D5FF;right:-110px;top:520px;opacity:.35"></div>
<div class="pill" style="top:118px;background:rgba(215,255,58,.12);color:var(--lime);border:1.5px solid rgba(215,255,58,.5)">🗺 РОҲНАМО</div>
<svg class="abs" style="left:0;top:150px" width="540" height="560" viewBox="0 0 540 560"><defs><linearGradient id="g" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#FF4D6D"/><stop offset=".5" stop-color="#7C4DFF"/><stop offset="1" stop-color="#D7FF3A"/></linearGradient></defs>
<path d="M150 520 C 420 470, 420 400, 270 360 S 120 250, 340 210 S 430 120, 300 70" fill="none" stroke="url(#g)" stroke-width="10" stroke-linecap="round" stroke-dasharray="2 22"/></svg>
<div class="abs blk" style="left:24px;top:636px;font-size:15px;color:var(--muted)">ШУМО ИНҶО</div>
<div class="abs" style="left:160px;top:626px;width:36px;height:36px;border-radius:50%;background:#fff;box-shadow:0 0 0 8px rgba(255,255,255,.18)"></div>
<div class="abs" style="left:390px;top:550px"></div>
<div class="abs" style="left:70px;top:455px;width:64px;height:64px;border-radius:50%;background:#FF4D6D;display:flex;align-items:center;justify-content:center;font:900 30px 'Segoe UI Black';box-shadow:0 0 40px #FF4D6D99">1</div>
<div class="abs" style="left:150px;top:445px;background:rgba(10,10,18,.75);padding:8px 12px;border-radius:12px"><div class="blk" style="font-size:30px">АСОСҲО</div><div style="font:700 15px 'Segoe UI';color:#FFB0BD;margin-top:4px">1–3 моҳ · let · if · for</div></div>
<div class="abs" style="right:70px;top:318px;width:64px;height:64px;border-radius:50%;background:#7C4DFF;display:flex;align-items:center;justify-content:center;font:900 30px 'Segoe UI Black';box-shadow:0 0 40px #7C4DFF99">2</div>
<div class="abs" style="right:150px;top:306px;text-align:right;background:rgba(10,10,18,.75);padding:8px 12px;border-radius:12px"><div class="blk" style="font-size:28px">БАРНОМАИ ХУРД</div><div style="font:700 15px 'Segoe UI';color:#C9B8FF;margin-top:4px">+2–3 моҳ · рӯйхати харид</div></div>
<div class="abs" style="left:90px;top:200px;width:64px;height:64px;border-radius:50%;background:#D7FF3A;color:#0A0A12;display:flex;align-items:center;justify-content:center;font:900 30px 'Segoe UI Black';box-shadow:0 0 40px #D7FF3A99">3</div>
<div class="abs" style="left:170px;top:190px;background:rgba(10,10,18,.75);padding:8px 12px;border-radius:12px"><div class="blk" style="font-size:30px;color:var(--lime)">ҲАР РӮЗ</div><div style="font:700 15px 'Segoe UI';color:#E9FF9A;margin-top:4px">20 дақиқа · ҳатто бо чой ☕</div></div>
<div class="abs emo" style="right:60px;top:138px;font-size:64px">🚀</div>
<div class="handle" style="top:700px">@SHAHRIYOR_YUNUSOV</div>''')

# 5 · СЕРИЯИ 30 РӮЗА
cells = ""
for k in range(30):
    on = k < 24
    cells += f'<div style="width:34px;height:34px;border-radius:9px;background:{"linear-gradient(135deg,#D7FF3A,#FFB23A)" if on else "rgba(255,255,255,.08)"};{"box-shadow:0 0 18px rgba(215,255,58,.45)" if on else ""}"></div>'
F[5] = page(f'''
<div class="orb" style="width:420px;height:420px;background:#FF7A2D;left:60px;top:80px;opacity:.55"></div>
<div class="pill" style="top:118px;background:rgba(255,122,45,.15);color:#FFB27A;border:1.5px solid rgba(255,122,45,.6)">🔥 СЕРИЯИ ШУМО</div>
<div class="c emo" style="top:150px;font-size:110px">🔥</div>
<div class="c blk grad" style="top:282px;font-size:110px">30 РӮЗ</div>
<div class="c blk" style="top:392px;font-size:30px">ҲАР РӮЗ 20 ДАҚИҚА</div>
<div class="abs" style="left:34px;right:34px;top:458px;display:grid;grid-template-columns:repeat(10,1fr);gap:6px;justify-items:center">{cells}</div>
<div class="sticker" style="top:610px;--r:-2deg;background:#fff;color:#0A0A12;font-size:22px">аз ҳама бештар — мунтазам</div>
<div class="handle" style="top:700px">@SHAHRIYOR_YUNUSOV</div>''')

# 6 · ХУЛОСА: 20
F[6] = page('''
<div class="orb" style="width:400px;height:400px;background:#7C4DFF;left:70px;top:150px;opacity:.6"></div>
<div class="pill" style="top:118px;background:rgba(255,255,255,.08);color:#fff;border:1.5px solid rgba(255,255,255,.3)">ХУЛОСА</div>
<svg class="abs" style="left:70px;top:170px" width="400" height="400" viewBox="0 0 400 400"><defs><linearGradient id="r" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#D7FF3A"/><stop offset="1" stop-color="#FF4D6D"/></linearGradient></defs>
<circle cx="200" cy="200" r="170" fill="none" stroke="rgba(255,255,255,.1)" stroke-width="22"/>
<circle cx="200" cy="200" r="170" fill="none" stroke="url(#r)" stroke-width="22" stroke-linecap="round" stroke-dasharray="1068" stroke-dashoffset="300" transform="rotate(-90 200 200)"/></svg>
<div class="c blk" style="top:262px;font-size:150px">20</div>
<div class="c blk grad" style="top:410px;font-size:36px">дақиқа</div>
<div class="c blk" style="top:454px;font-size:26px;color:rgba(255,255,255,.7)">ҳар рӯз</div>
<div class="sticker" style="top:604px;--r:-3deg;background:#D7FF3A;color:#0A0A12;font-size:22px;left:30%">каме</div>
<div class="sticker" style="top:604px;--r:2deg;background:#FF4D6D;color:#fff;font-size:22px;left:58%">бефосила</div>
<div class="sticker" style="top:646px;--r:-1deg;background:#7C4DFF;color:#fff;font-size:22px">мунтазам</div>''')

# 7 · САВОЛ (ОПРОС)
F[7] = page('''
<div class="abs" style="inset:0;background:linear-gradient(170deg,#2a1070 0%,#0A0A12 70%)"></div>
<div class="orb" style="width:340px;height:340px;background:#FF4D6D;right:-100px;top:120px;opacity:.45"></div>
<div class="pill" style="top:118px;background:rgba(215,255,58,.12);color:var(--lime);border:1.5px solid rgba(215,255,58,.5)">🎯 САВОЛ БА ШУМО</div>
<div class="abs" style="left:34px;right:34px;top:170px;background:#fff;border-radius:28px;padding:26px 22px 22px;box-shadow:0 22px 60px rgba(0,0,0,.55);transform:rotate(-1.5deg)">
 <div class="blk" style="color:#0A0A12;font-size:36px;text-align:center;line-height:1.05">Чанд дақиқа дар рӯз?</div>
 <div style="display:flex;gap:10px;margin-top:20px">
  <div style="flex:1;text-align:center;padding:16px 0;border-radius:16px;background:#F0EEFF"><div class="blk" style="color:#0A0A12;font-size:44px">10</div><div style="font:700 13px 'Segoe UI';color:#555">дақиқа</div></div>
  <div style="flex:1;text-align:center;padding:16px 0;border-radius:16px;background:linear-gradient(135deg,#D7FF3A,#FFE53A);box-shadow:0 8px 0 rgba(0,0,0,.15)"><div class="blk" style="color:#0A0A12;font-size:44px">20</div><div style="font:700 13px 'Segoe UI';color:#333">дақиқа</div></div>
  <div style="flex:1;text-align:center;padding:16px 0;border-radius:16px;background:#F0EEFF"><div class="blk" style="color:#0A0A12;font-size:44px">30</div><div style="font:700 13px 'Segoe UI';color:#555">дақиқа</div></div></div></div>
<div class="sticker" style="top:470px;--r:2deg;background:#FF4D6D;color:#fff;font-size:24px">💬 ҷавобро дар шарҳ нависед</div>
<div class="handle" style="top:700px">@SHAHRIYOR_YUNUSOV</div>''')

# 8 · ДАЪВАТ (ВАҚТ → DIRECT)
F[8] = page('''
<div class="abs" style="inset:0;background:linear-gradient(160deg,#0A0A12 0%,#1a0f3a 100%)"></div>
<div class="orb" style="width:360px;height:360px;background:#D7FF3A;left:-140px;top:420px;opacity:.28"></div>
<div class="pill" style="top:118px;background:rgba(255,255,255,.08);color:#fff;border:1.5px solid rgba(255,255,255,.3)">ШАРҲ ➜ DIRECT</div>
<div class="abs" style="left:40px;right:40px;top:170px;background:#fff;border-radius:34px 34px 34px 8px;padding:22px 24px;box-shadow:0 20px 50px rgba(0,0,0,.5)">
 <div style="display:flex;align-items:center;gap:14px"><div style="width:40px;height:40px;border-radius:50%;background:linear-gradient(135deg,#7C4DFF,#FF4D6D)"></div><div class="blk" style="color:#0A0A12;font-size:46px;letter-spacing:2px">ВАҚТ</div><div style="margin-left:auto;font:900 24px 'Segoe UI';color:#7C4DFF">➤</div></div></div>
<div class="abs" style="left:50%;top:292px;transform:translateX(-50%);font-size:54px;color:var(--lime)">↓</div>
<div class="abs" style="left:70px;right:70px;top:360px;background:linear-gradient(135deg,#7C4DFF,#FF4D6D);border-radius:26px;padding:24px;text-align:center;transform:rotate(-2deg);box-shadow:0 20px 50px rgba(0,0,0,.5)">
 <div class="emo" style="font-size:68px">📘</div><div class="blk" style="font-size:30px;margin-top:6px">Шпаргалкаи бепул</div><div style="font:700 14px 'Segoe UI';margin-top:6px;opacity:.9">дарсҳои 1–5 · PDF · ба Direct</div></div>
<div class="sticker" style="top:600px;--r:0deg;background:#D7FF3A;color:#0A0A12;font-size:24px">🔔 Обуна шавед</div>
<div class="handle" style="top:700px">@SHAHRIYOR_YUNUSOV</div>''')

if __name__ == '__main__':
    for k, h in F.items():
        open(f'f{k}.html', 'w', encoding='utf-8').write(h)
    print('ok', len(F))
