import sys; sys.path.insert(0, '.')
from make_glass import CSS, DARKGLOW
body = DARKGLOW + '''
<div class="glass" style="left:-50px;top:300px;width:200px;height:120px;transform:rotate(-12deg);opacity:.3;filter:blur(2px)"></div>
<div class="glass" style="right:-60px;top:600px;width:220px;height:130px;transform:rotate(10deg);opacity:.3;filter:blur(2px)"></div>
<div class="pillg" style="left:50%;transform:translateX(-50%);top:158px;font:700 12px 'Cascadia Mono',Consolas;letter-spacing:3px;color:#7DF0CF;border-color:rgba(53,224,181,.55);background:rgba(53,224,181,.08)">БАРОИ ҲАМА · ОДДӢ</div>
<div class="c" style="top:205px;font:700 44px/1.08 'Segoe UI Semibold','Segoe UI';letter-spacing:-.8px">Базаи маълумот</div>
<div class="c" style="top:258px;font:800 64px/1.05 'Segoe UI Black','Segoe UI';letter-spacing:-1.5px;background:linear-gradient(90deg,#7DF0CF,#5B8CFF 60%,#B49BFF);-webkit-background-clip:text;background-clip:text;color:transparent">чист?</div>
<div class="glass" style="left:70px;right:70px;top:380px;height:215px;overflow:hidden;transform:perspective(900px) rotateX(8deg) rotateY(-6deg)">
 <div style="display:grid;grid-template-columns:1fr 1fr;padding:12px 20px;font:700 12px 'Cascadia Mono',Consolas;letter-spacing:2px;color:#8B949E;background:rgba(255,255,255,.06)"><span>НОМ</span><span>ШАҲР</span></div>
 <div style="display:grid;grid-template-columns:1fr 1fr;padding:14px 20px;font:700 24px 'Segoe UI';border-top:1px solid rgba(255,255,255,.08);background:rgba(91,140,255,.3)"><span>Алӣ</span><span>Душанбе</span></div>
 <div style="display:grid;grid-template-columns:1fr 1fr;padding:14px 20px;font:700 24px 'Segoe UI';border-top:1px solid rgba(255,255,255,.08);opacity:.35"><span>Мариям</span><span>Хуҷанд</span></div>
 <div style="display:grid;grid-template-columns:1fr 1fr;padding:14px 20px;font:700 24px 'Segoe UI';border-top:1px solid rgba(255,255,255,.08);background:rgba(91,140,255,.3)"><span>Фарҳод</span><span>Душанбе</span></div></div>
<div class="pillg" style="left:50%;transform:translateX(-50%);top:630px;font:700 18px 'Cascadia Mono',Consolas;background:linear-gradient(90deg,#2B6BFF,#8B5CF6);border:0;padding:12px 24px">SELECT name WHERE city = 'Душанбе'</div>
<div class="c" style="top:700px;font:600 18px 'Segoe UI Semibold';opacity:.85">барои ҳама касб — на танҳо барномасозон</div>'''
open('cover.html', 'w', encoding='utf-8').write(f'<!doctype html><html lang="tg"><head><meta charset="utf-8"><style>{CSS}</style></head><body class="dark">{body}</body></html>')
