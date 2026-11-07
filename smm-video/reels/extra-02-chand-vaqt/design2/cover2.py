from make_glass import CSS
EXTRA = """
.tok{position:absolute;font:700 17px 'Cascadia Mono',Consolas;color:rgba(255,255,255,.2);filter:blur(1.2px)}
.orbit{position:absolute;display:flex;align-items:center;gap:10px;padding:12px 20px 12px 14px;border-radius:22px;background:linear-gradient(160deg,rgba(255,255,255,.16),rgba(255,255,255,.05));border:1px solid rgba(255,255,255,.22);backdrop-filter:blur(14px);box-shadow:0 22px 50px rgba(0,0,0,.5),inset 0 1px 0 rgba(255,255,255,.3);font:700 20px 'Segoe UI Semibold','Segoe UI'}
.orbit .i{width:40px;height:40px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:22px}
.big{position:absolute;left:0;right:0;text-align:center;font-family:'Segoe UI Black','Segoe UI Semibold','Segoe UI';letter-spacing:-2px;line-height:.95}
"""
A = '''
<div class="glow" style="width:560px;height:560px;left:-10px;top:250px;background:radial-gradient(circle,rgba(43,107,255,.8),rgba(20,50,150,.35) 55%,transparent 72%)"></div>
<div class="glow" style="width:300px;height:300px;right:-90px;top:120px;background:radial-gradient(circle,rgba(139,92,246,.8),transparent 70%)"></div>
<div class="glow" style="width:300px;height:300px;left:-100px;top:600px;background:radial-gradient(circle,rgba(53,224,181,.55),transparent 70%)"></div>
<div class="tok" style="left:30px;top:200px;transform:rotate(-8deg)">let</div><div class="tok" style="right:34px;top:250px;transform:rotate(7deg)">if ( )</div>
<div class="tok" style="left:44px;top:520px;transform:rotate(6deg)">for</div><div class="tok" style="right:40px;top:560px;transform:rotate(-6deg)">[ ]</div>
<div class="tok" style="left:120px;top:170px;font-size:13px">{ }</div><div class="tok" style="right:120px;top:740px;font-size:14px">=&gt;</div>
<div class="pillg" style="left:50%;transform:translateX(-50%);top:158px;font:700 12px 'Cascadia Mono',Consolas;letter-spacing:3px;color:#7DF0CF;border-color:rgba(53,224,181,.55);background:rgba(53,224,181,.08)">БАРНОМАСОЗӢ АЗ СИФР</div>
<div class="big" style="top:212px;font-size:38px;font-weight:600;letter-spacing:-.6px;font-family:'Segoe UI Semibold'">ДАР ЧАНД ВАҚТ</div>
<div class="big" style="top:256px;font-size:62px;background:linear-gradient(90deg,#7DF0CF,#5B8CFF 55%,#B49BFF);-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 6px 30px rgba(91,140,255,.55))">БАРНОМАСОЗ</div>
<div class="big" style="top:330px;font-size:38px;font-weight:600;letter-spacing:-.6px;font-family:'Segoe UI Semibold'">ШУДАН МУМКИН?</div>
<svg class="abs" style="left:0;top:380px" width="540" height="330" viewBox="0 0 540 330"><g stroke="rgba(255,255,255,.22)" stroke-width="2" stroke-dasharray="3 7" fill="none"><path d="M150 70 L225 130"/><path d="M390 70 L315 130"/><path d="M270 262 L270 215"/></g></svg>
<div class="abs" style="left:190px;top:440px;width:160px;height:160px;border-radius:46px;background:linear-gradient(160deg,rgba(255,255,255,.2),rgba(255,255,255,.05));border:1px solid rgba(255,255,255,.3);backdrop-filter:blur(14px);display:flex;align-items:center;justify-content:center;transform:perspective(700px) rotateX(10deg) rotateY(-12deg) rotate(-3deg);box-shadow:0 0 110px rgba(43,107,255,.9),0 40px 80px rgba(0,0,0,.55),inset 0 2px 0 rgba(255,255,255,.4)"><div class="num" style="font-size:124px;letter-spacing:0">?</div></div>
<div class="orbit" style="left:40px;top:395px;transform:rotate(-5deg)"><span class="i" style="background:linear-gradient(135deg,#FF4D6D,#FF8DA1)">⏱</span>1 ҳафта</div>
<div class="orbit" style="right:36px;top:395px;transform:rotate(5deg)"><span class="i" style="background:linear-gradient(135deg,#8B5CF6,#B49BFF)">📅</span>1 моҳ</div>
<div class="orbit" style="left:175px;top:640px;transform:rotate(-2deg)"><span class="i" style="background:linear-gradient(135deg,#35E0B5,#7DF0CF)">🗓</span>1 сол</div>
<div class="c" style="top:742px;font:600 17px 'Segoe UI Semibold';opacity:.8">Ин аз худи Шумо вобаста ҳаст <span style="color:#7DF0CF">→</span></div>
'''
B = '''
<div class="glow" style="width:520px;height:520px;left:10px;top:230px;background:radial-gradient(circle,rgba(110,240,205,.95),rgba(110,240,205,.25) 60%,transparent 72%)"></div>
<div class="glow" style="width:260px;height:260px;right:-70px;top:100px;background:radial-gradient(circle,rgba(160,130,255,.7),transparent 70%)"></div>
<div class="big" style="top:150px;font-size:330px;color:rgba(24,32,46,.05);letter-spacing:0">?</div>
<div class="pillg" style="left:50%;transform:translateX(-50%);top:158px;font:700 12px 'Cascadia Mono',Consolas;letter-spacing:3px;color:#0f8f72">БАРНОМАСОЗӢ АЗ СИФР</div>
<div class="big" style="top:212px;font-size:38px;font-weight:600;letter-spacing:-.6px;color:#18202E;font-family:'Segoe UI Semibold'">ДАР ЧАНД ВАҚТ</div>
<div class="big" style="top:256px;font-size:62px;color:#18202E">БАРНОМАСОЗ</div>
<div class="big" style="top:330px;font-size:38px;font-weight:600;letter-spacing:-.6px;font-family:'Segoe UI Semibold';background:linear-gradient(90deg,#2B6BFF,#8B5CF6);-webkit-background-clip:text;background-clip:text;color:transparent">ШУДАН МУМКИН?</div>
<div class="gl" style="left:70px;right:70px;top:420px;height:96px;display:flex;align-items:center;padding:0 26px;gap:16px;transform:rotate(-3deg)"><span style="width:52px;height:52px;border-radius:16px;background:linear-gradient(135deg,#FF4D6D,#FF8DA1);display:flex;align-items:center;justify-content:center;font-size:26px">⏱</span><span style="font:800 36px 'Segoe UI Black';color:#18202E;letter-spacing:-1px">1 ҳафта?</span></div>
<div class="gl" style="left:50px;right:90px;top:536px;height:96px;display:flex;align-items:center;padding:0 26px;gap:16px;transform:rotate(2.5deg)"><span style="width:52px;height:52px;border-radius:16px;background:linear-gradient(135deg,#8B5CF6,#B49BFF);display:flex;align-items:center;justify-content:center;font-size:26px">📅</span><span style="font:800 36px 'Segoe UI Black';color:#18202E;letter-spacing:-1px">1 моҳ?</span></div>
<div class="gl" style="left:90px;right:50px;top:652px;height:96px;display:flex;align-items:center;padding:0 26px;gap:16px;transform:rotate(-2deg);background:linear-gradient(90deg,#2B6BFF,#8B5CF6);border:0;box-shadow:0 26px 60px rgba(80,90,255,.4)"><span style="width:52px;height:52px;border-radius:16px;background:rgba(255,255,255,.22);display:flex;align-items:center;justify-content:center;font-size:26px">🗓</span><span style="font:800 36px 'Segoe UI Black';color:#fff;letter-spacing:-1px">1 сол?</span></div>
'''
for name, theme, body in (('A', 'dark', A), ('B', 'light', B)):
    html = f'<!doctype html><html lang="tg"><head><meta charset="utf-8"><style>{CSS}{EXTRA}</style></head><body class="{theme}">{body}</body></html>'
    open(f'cover{name}.html', 'w', encoding='utf-8').write(html)
