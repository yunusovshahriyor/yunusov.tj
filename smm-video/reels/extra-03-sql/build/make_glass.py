# Тарҳи «шишагӣ» (glass UI) барои Reels-и иловагӣ — 10 кадр (540×960 @2x = 1080×1920).
CSS = """
:root{--blue:#2B6BFF;--blue2:#5B8CFF;--mint:#35E0B5;--violet:#8B5CF6;--amber:#FFB23A;--ink:#04060D;--lt:#EDF1F7}
*{box-sizing:border-box;margin:0;padding:0}
body{width:540px;height:960px;overflow:hidden;position:relative;font-family:'Segoe UI',sans-serif;color:#fff}
body.dark{background:#04060D}
body.light{background:#EDF1F7;color:#18202E}
.abs{position:absolute}.c{position:absolute;left:0;right:0;text-align:center}
.glow{position:absolute;border-radius:50%;filter:blur(40px)}
.glass{position:absolute;background:linear-gradient(160deg,rgba(255,255,255,.13),rgba(255,255,255,.04));border:1px solid rgba(255,255,255,.17);border-radius:28px;backdrop-filter:blur(14px);box-shadow:0 30px 70px rgba(0,0,0,.5),inset 0 1px 0 rgba(255,255,255,.28)}
.gl{position:absolute;background:rgba(255,255,255,.78);border:1px solid #fff;border-radius:26px;box-shadow:0 26px 60px rgba(60,90,130,.18),0 2px 0 rgba(255,255,255,.9) inset}
.title{position:absolute;left:0;right:0;text-align:center;font:600 30px/1.15 'Segoe UI Semibold','Segoe UI';letter-spacing:-.3px}
.sub{position:absolute;left:0;right:0;text-align:center;font:500 16px 'Segoe UI';opacity:.65}
.chip{position:absolute;width:46px;height:46px;border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:22px;background:linear-gradient(160deg,rgba(255,255,255,.16),rgba(255,255,255,.05));border:1px solid rgba(255,255,255,.2)}
.light .chip{background:#fff;border:1px solid #fff;box-shadow:0 10px 24px rgba(60,90,130,.16)}
.pillg{position:absolute;padding:9px 18px;border-radius:999px;font:600 15px 'Segoe UI Semibold','Segoe UI';white-space:nowrap;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2)}
.light .pillg{background:#fff;border:1px solid #fff;box-shadow:0 10px 24px rgba(60,90,130,.14);color:#18202E}
.num{font-family:'Segoe UI Light','Segoe UI';font-weight:300;letter-spacing:-4px;line-height:1}
.emo{font-family:'Segoe UI Emoji',sans-serif}
.handle{position:absolute;right:26px;top:102px;display:flex;align-items:center;gap:6px;font:700 10px 'Cascadia Mono',Consolas;letter-spacing:1px;opacity:.55}
.ig{width:16px;height:16px;border-radius:5px;border:2px solid currentColor;position:relative}.ig::after{content:"";position:absolute;inset:3px;border-radius:50%;border:1.5px solid currentColor}
.bar{height:10px;border-radius:99px;background:rgba(255,255,255,.12);overflow:hidden}.light .bar{background:rgba(24,32,46,.08)}
.bar>i{display:block;height:100%;border-radius:99px}
.cap{position:absolute;left:18px;right:18px;top:716px;text-align:center;font:700 29px/1.2 'Segoe UI';text-shadow:0 2px 14px rgba(0,0,0,.45)}
.light .cap{color:#18202E;text-shadow:0 1px 10px rgba(255,255,255,.7)}
.cap b{font-weight:700;color:var(--blue2)}
.light .cap b{color:#1F6BFF}
"""
def page(theme, body, cap=None):
    capdiv = f'<div class="cap">{cap}</div>' if cap else ''
    return f'<!doctype html><html lang="tg"><head><meta charset="utf-8"><style>{CSS}</style></head><body class="{theme}">{body}<div class="handle"><span class="ig"></span>@SHAHRIYOR_YUNUSOV</div>{capdiv}</body></html>'
DARKGLOW = '<div class="glow" style="width:520px;height:520px;left:10px;top:150px;background:radial-gradient(circle,rgba(43,107,255,.75),rgba(20,50,150,.35) 55%,transparent 72%)"></div>'
G = {}

# 1 · ХУК (торик)
G[1] = page('dark', DARKGLOW + '''
<div class="glass" style="left:-40px;top:300px;width:200px;height:120px;transform:rotate(-12deg);opacity:.35;filter:blur(2px)"></div>
<div class="glass" style="right:-50px;top:420px;width:210px;height:130px;transform:rotate(10deg);opacity:.35;filter:blur(2px)"></div>
<div class="title" style="top:150px">Дар чанд вақт<br>барномасоз шудан мумкин?</div>
<div class="glass" style="left:185px;top:290px;width:170px;height:170px;border-radius:46px;display:flex;align-items:center;justify-content:center;box-shadow:0 0 90px rgba(43,107,255,.8),0 30px 70px rgba(0,0,0,.5),inset 0 1px 0 rgba(255,255,255,.35)"><div class="num" style="font-size:130px">?</div></div>
<div class="pillg" style="left:60px;top:520px">⏱ 1 ҳафта</div>
<div class="pillg" style="left:205px;top:560px">📅 1 моҳ</div>
<div class="pillg" style="left:350px;top:520px">🗓 1 сол</div>''', 'Як ҳафта? <b>Як моҳ?</b> Як сол?')

# 2 · ҶАВОБ (сабук, нанъно)
G[2] = page('light', '''
<div class="glow" style="width:480px;height:480px;left:30px;top:200px;background:radial-gradient(circle,rgba(110,240,205,.9),rgba(110,240,205,.25) 60%,transparent 72%)"></div>
<div class="title" style="top:160px;font-size:40px">Ин аз худи Шумо<br>вобаста ҳаст</div>
<div class="gl" style="left:190px;top:330px;width:160px;height:160px;border-radius:80px;display:flex;align-items:center;justify-content:center;box-shadow:0 0 70px rgba(53,224,181,.7),0 26px 60px rgba(60,90,130,.2)"><span class="emo" style="font-size:74px">🫵</span></div>
<div class="pillg" style="left:60px;top:540px">🎯 ҳадаф</div>
<div class="pillg" style="left:190px;top:580px">⏱ вақт</div>
<div class="pillg" style="left:320px;top:540px">💪 одат</div>''', 'Ин аз худи Шумо <b>вобаста ҳаст!</b>')

# 3 · ЗАБОНИ НАВ (торик; хотира vs малака)
G[3] = page('dark', DARKGLOW + '''
<div class="title" style="top:140px">Забони нав омӯхтан</div>
<div class="glass" style="left:36px;right:36px;top:215px;height:200px;transform:perspective(900px) rotateX(8deg);border-color:rgba(255,77,109,.45)">
 <div class="abs" style="left:22px;top:18px;font:600 15px 'Segoe UI';color:#FF8DA1">1 РӮЗ · 3 СОАТ, БАЪД 7 РӮЗ НЕСТ</div>
 <div class="abs num" style="left:22px;top:46px;font-size:64px">3 соат</div>
 <div class="abs" style="left:22px;right:22px;top:128px"><div class="bar"><i style="width:14%;background:linear-gradient(90deg,#FF4D6D,#FF8DA1)"></i></div><div style="font:600 13px 'Segoe UI';opacity:.7;margin-top:8px">хотира → ҳама чиз аз ёд меравад ❌</div></div></div>
<div class="glass" style="left:36px;right:36px;top:445px;height:200px;transform:perspective(900px) rotateX(-6deg);border-color:rgba(53,224,181,.5)">
 <div class="abs" style="left:22px;top:18px;font:600 15px 'Segoe UI';color:#7DF0CF">ҲАР РӮЗ · 20 ДАҚИҚА</div>
 <div class="abs num" style="left:22px;top:46px;font-size:64px">20 дақиқа</div>
 <div class="abs" style="left:22px;right:22px;top:128px"><div class="bar"><i style="width:88%;background:linear-gradient(90deg,#35E0B5,#7DF0CF)"></i></div><div style="font:600 13px 'Segoe UI';opacity:.7;margin-top:8px">як моҳ баъд — ҷумла 💬✅</div></div></div>''', 'Ҳар рӯз <b>бист дақиқа</b> —')

# 4 · ДАР БАРНОМАСОЗӢ ҲАМ (торик; терминал)
G[4] = page('dark', DARKGLOW + '''
<div class="title" style="top:140px">Дар барномасозӣ ҳам<br>ҳамин тавр</div>
<div class="glass" style="left:30px;right:30px;top:260px;height:230px;transform:perspective(900px) rotateX(7deg) rotateY(-8deg)">
 <div class="abs" style="left:18px;top:14px;display:flex;gap:6px"><i style="width:10px;height:10px;border-radius:50%;background:#FF5F57"></i><i style="width:10px;height:10px;border-radius:50%;background:#FEBC2E"></i><i style="width:10px;height:10px;border-radius:50%;background:#28C840"></i></div>
 <div class="abs" style="left:22px;top:52px;font:600 19px 'Cascadia Mono',Consolas;white-space:pre"><span style="color:#FFE08A">console</span>.<span style="color:#FFE08A">log</span>(<span style="color:#FF9A6B">"Салом, ҷаҳон!"</span>);</div>
 <div class="abs" style="left:22px;top:110px;font:600 19px 'Cascadia Mono',Consolas;color:#7DF0CF">&gt; Салом, ҷаҳон!</div>
 <div class="abs" style="left:22px;right:22px;top:170px"><div class="bar"><i style="width:100%;background:linear-gradient(90deg,#2B6BFF,#5B8CFF)"></i></div></div></div>
<div class="chip" style="left:60px;top:560px">💻</div><div class="chip" style="left:122px;top:560px">🌐</div><div class="chip" style="left:184px;top:560px">🧠</div>
<div class="pillg" style="left:260px;top:566px;background:linear-gradient(90deg,var(--blue),var(--violet));border:0">забони компютер</div>''', 'Ин ҳам забон аст — <b>забони компютер.</b>')

# 5 · РОҲНАМО (сабук)
G[5] = page('light', '''
<div class="glow" style="width:420px;height:420px;left:60px;top:260px;background:radial-gradient(circle,rgba(110,240,205,.75),transparent 70%)"></div>
<div class="title" style="top:140px">Се қадам</div>
<div class="abs" style="left:62px;top:230px;width:4px;height:400px;border-radius:4px;background:linear-gradient(#35E0B5,#8B5CF6)"></div>
<div class="abs" style="left:52px;top:236px;width:24px;height:24px;border-radius:50%;background:#35E0B5;box-shadow:0 0 0 8px rgba(53,224,181,.25)"></div>
<div class="gl" style="left:92px;right:30px;top:215px;height:130px;padding:16px 18px"><div style="font:600 13px 'Segoe UI';color:#7a8599">1–3 МОҲ</div><div style="font:700 26px 'Segoe UI Semibold','Segoe UI';margin-top:2px">Асосҳо</div><div style="display:flex;gap:6px;margin-top:10px;font:700 12px 'Cascadia Mono',Consolas"><span style="background:#E8EEFF;color:#2B6BFF;padding:5px 8px;border-radius:8px">let</span><span style="background:#E8EEFF;color:#2B6BFF;padding:5px 8px;border-radius:8px">if</span><span style="background:#E8EEFF;color:#2B6BFF;padding:5px 8px;border-radius:8px">for</span><span style="background:#E8EEFF;color:#2B6BFF;padding:5px 8px;border-radius:8px">[ ]</span><span style="background:#E8EEFF;color:#2B6BFF;padding:5px 8px;border-radius:8px">function</span></div></div>
<div class="abs" style="left:52px;top:396px;width:24px;height:24px;border-radius:50%;background:#8B5CF6;box-shadow:0 0 0 8px rgba(139,92,246,.22)"></div>
<div class="gl" style="left:92px;right:30px;top:372px;height:120px;padding:16px 18px"><div style="font:600 13px 'Segoe UI';color:#7a8599">+2–3 МОҲ</div><div style="font:700 26px 'Segoe UI Semibold','Segoe UI';margin-top:2px">Барномаи хурд</div><div style="font:600 15px 'Segoe UI';margin-top:8px;color:#4a5468">☑ нон &nbsp; ☐ шир &nbsp; ☐ себ</div></div>
<div class="abs" style="left:52px;top:556px;width:24px;height:24px;border-radius:50%;background:#FFB23A;box-shadow:0 0 0 8px rgba(255,178,58,.25)"></div>
<div class="gl" style="left:92px;right:30px;top:520px;height:100px;padding:16px 18px"><div style="font:600 13px 'Segoe UI';color:#7a8599">ҲАР РӮЗ</div><div style="font:700 26px 'Segoe UI Semibold','Segoe UI';margin-top:2px">20 дақиқа ☕</div></div>''', 'Қадами <b>як:</b> асосҳо.')

# 6 · СЕРИЯ (торик, ғарбӣ-норанҷӣ)
cells = "".join(f'<div style="width:34px;height:34px;border-radius:10px;{"background:linear-gradient(135deg,#FFD86B,#FF9A3A);box-shadow:0 0 16px rgba(255,170,60,.55)" if k<24 else "background:rgba(255,255,255,.08)"}"></div>' for k in range(30))
G[6] = page('dark', '''
<div class="glow" style="width:520px;height:520px;left:10px;top:120px;background:radial-gradient(circle,rgba(255,150,40,.7),rgba(120,50,10,.3) 55%,transparent 72%)"></div>
<div class="title" style="top:140px">Серияи шумо</div>
<div class="c emo" style="top:200px;font-size:76px">🔥</div>
<div class="c num" style="top:300px;font-size:130px">30</div>
<div class="c" style="top:432px;font:600 20px 'Segoe UI Semibold';opacity:.8">рӯз пай дар пай</div>
<div class="glass" style="left:30px;right:30px;top:490px;height:120px;padding:16px"><div style="display:grid;grid-template-columns:repeat(10,1fr);gap:6px;justify-items:center">''' + cells + '''</div></div>''', 'Барномасоз шудан = <b>ҳар рӯз 20 дақиқа</b>')

# 7 · ХУЛОСА (торик; ҳалқа)
G[7] = page('dark', DARKGLOW + '''
<div class="title" style="top:140px">Хулоса</div>
<svg class="abs" style="left:70px;top:210px" width="400" height="400" viewBox="0 0 400 400"><defs><linearGradient id="r" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#35E0B5"/><stop offset="1" stop-color="#5B8CFF"/></linearGradient></defs>
<circle cx="200" cy="200" r="165" fill="none" stroke="rgba(255,255,255,.1)" stroke-width="18"/>
<circle cx="200" cy="200" r="165" fill="none" stroke="url(#r)" stroke-width="18" stroke-linecap="round" stroke-dasharray="1037" stroke-dashoffset="290" transform="rotate(-90 200 200)"/></svg>
<div class="c num" style="top:300px;font-size:150px">20</div>
<div class="c" style="top:455px;font:600 24px 'Segoe UI Semibold'">дақиқа · ҳар рӯз</div>
<div class="pillg" style="left:70px;top:640px">✓ каме</div>
<div class="pillg" style="left:190px;top:640px">✓ бефосила</div>
<div class="pillg" style="left:340px;top:640px">✓ мунтазам</div>''', 'Каме, вале <b>бефосила</b> ва мунтазам.')

# 8 · САВОЛ (сабук, бунафш)
G[8] = page('light', '''
<div class="glow" style="width:460px;height:460px;left:40px;top:200px;background:radial-gradient(circle,rgba(160,130,255,.7),transparent 70%)"></div>
<div class="title" style="top:140px">Савол ба шумо</div>
<div class="gl" style="left:34px;right:34px;top:230px;height:330px;padding:24px 22px">
 <div style="font:700 28px/1.15 'Segoe UI Semibold','Segoe UI';text-align:center">Чанд дақиқа вақт<br>ҷудо карда метавонед?</div>
 <div style="margin-top:24px;display:flex;flex-direction:column;gap:12px">
  <div style="padding:16px 18px;border-radius:16px;background:#F1F4FA;font:600 20px 'Segoe UI Semibold';display:flex;justify-content:space-between"><span>10 дақиқа</span><span style="opacity:.4">○</span></div>
  <div style="padding:16px 18px;border-radius:16px;background:linear-gradient(90deg,#2B6BFF,#8B5CF6);color:#fff;font:600 20px 'Segoe UI Semibold';display:flex;justify-content:space-between;box-shadow:0 12px 26px rgba(80,90,255,.35)"><span>20 дақиқа</span><span>●</span></div>
  <div style="padding:16px 18px;border-radius:16px;background:#F1F4FA;font:600 20px 'Segoe UI Semibold';display:flex;justify-content:space-between"><span>30 дақиқа</span><span style="opacity:.4">○</span></div></div></div>
<div class="pillg" style="left:150px;top:600px">💬 ҷавобро дар шарҳ нависед</div>''', 'Даҳ, бист ё <b>сӣ?</b>')

# 9 · ДАЪВАТ (торик; шарҳ → Direct)
G[9] = page('dark', DARKGLOW + '''
<div class="title" style="top:140px">Шарҳ → Direct</div>
<div class="glass" style="left:40px;right:40px;top:230px;height:90px;border-radius:999px;display:flex;align-items:center;padding:0 24px;gap:14px"><div style="width:42px;height:42px;border-radius:50%;background:linear-gradient(135deg,#2B6BFF,#8B5CF6)"></div><div style="font:700 30px 'Segoe UI Semibold';letter-spacing:3px">ВАҚТ</div><div style="margin-left:auto;font:700 22px 'Segoe UI';color:#5B8CFF">➤</div></div>
<div class="c" style="top:340px;font-size:34px;color:#5B8CFF">↓</div>
<div class="glass" style="left:80px;right:80px;top:400px;height:190px;transform:perspective(900px) rotateX(8deg) rotate(-2deg);text-align:center;padding-top:26px"><div class="emo" style="font-size:62px">📘</div><div style="font:700 24px 'Segoe UI Semibold';margin-top:6px">Шпаргалкаи бепул</div><div style="font:500 14px 'Segoe UI';opacity:.65;margin-top:4px">дарсҳои 1–5 · PDF · ба Direct</div></div>
<div class="pillg" style="left:180px;top:620px;background:linear-gradient(90deg,var(--blue),var(--violet));border:0">✉ ба Direct мефиристам</div>''', 'Калимаи <b>«ВАҚТ»</b>-ро дар шарҳ нависед')

# 10 · ОХИР (торик, аврора)
G[10] = page('dark', '''
<div class="glow" style="width:520px;height:520px;left:10px;top:60px;background:radial-gradient(circle,rgba(139,92,246,.75),rgba(43,107,255,.3) 55%,transparent 72%)"></div>
<div class="glow" style="width:360px;height:360px;left:-80px;top:520px;background:radial-gradient(circle,rgba(53,224,181,.5),transparent 70%)"></div>
<div class="c" style="top:200px;font:600 44px/1.1 'Segoe UI Semibold';letter-spacing:-.6px">Ҳар рӯз</div>
<div class="c num" style="top:262px;font-size:76px;letter-spacing:-3px">каме пеш</div>
<div class="glass" style="left:100px;right:100px;top:420px;height:120px;border-radius:999px;display:flex;align-items:center;justify-content:center;gap:12px"><span class="emo" style="font-size:28px">🔔</span><span style="font:700 24px 'Segoe UI Semibold'">Обуна шавед</span></div>
<div class="c" style="top:566px;font:700 14px 'Cascadia Mono',Consolas;letter-spacing:2px;opacity:.7">@SHAHRIYOR_YUNUSOV</div>''', 'Обуна шавед, то аз ҷаҳони <b>барномасозӣ</b> бехабар намонед!')

if __name__ == '__main__':
    for k, h in G.items():
        open(f'g{k}.html', 'w', encoding='utf-8').write(h)
    print('ok', len(G))
