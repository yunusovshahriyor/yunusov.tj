from make_glass import CSS, DARKGLOW
body = DARKGLOW + '''
<div class="glass" style="left:-50px;top:290px;width:200px;height:120px;transform:rotate(-12deg);opacity:.3;filter:blur(2px)"></div>
<div class="glass" style="right:-60px;top:560px;width:220px;height:130px;transform:rotate(10deg);opacity:.3;filter:blur(2px)"></div>
<div class="pillg" style="left:50%;transform:translateX(-50%);top:168px;font:700 13px 'Cascadia Mono',Consolas;letter-spacing:3px;color:#7DF0CF;border-color:rgba(53,224,181,.5)">БАРНОМАСОЗӢ АЗ СИФР</div>
<div class="c" style="top:218px;font:600 46px/1.08 'Segoe UI Semibold','Segoe UI';letter-spacing:-.8px">Дар чанд вақт</div>
<div class="c" style="top:272px;font:700 58px/1.05 'Segoe UI Semibold','Segoe UI';letter-spacing:-1px;background:linear-gradient(90deg,#7DF0CF,#5B8CFF 60%,#A78BFA);-webkit-background-clip:text;background-clip:text;color:transparent">барномасоз</div>
<div class="c" style="top:340px;font:600 46px/1.08 'Segoe UI Semibold','Segoe UI';letter-spacing:-.8px">шудан мумкин?</div>
<div class="glass" style="left:195px;top:430px;width:150px;height:150px;border-radius:42px;display:flex;align-items:center;justify-content:center;box-shadow:0 0 90px rgba(43,107,255,.8),0 30px 70px rgba(0,0,0,.5),inset 0 1px 0 rgba(255,255,255,.35)"><div class="num" style="font-size:112px">?</div></div>
<div class="pillg" style="left:44px;top:610px">⏱ 1 ҳафта</div>
<div class="pillg" style="left:196px;top:650px">📅 1 моҳ</div>
<div class="pillg" style="left:340px;top:610px">🗓 1 сол</div>
<div class="c" style="top:716px;font:600 20px 'Segoe UI Semibold';opacity:.85">Ин аз худи Шумо вобаста ҳаст</div>'''
html = f'<!doctype html><html lang="tg"><head><meta charset="utf-8"><style>{CSS}</style></head><body class="dark">{body}</body></html>'
open('cover.html', 'w', encoding='utf-8').write(html)
