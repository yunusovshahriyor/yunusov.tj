# Генерирует reel.html с таймингами, привязанными к длительности реплик.
D=[4.50,7.41,3.62,3.56,5.17,4.17]
T=[0.2]
for d in D[:-1]: T.append(round(T[-1]+d,2))
END=round(T[-1]+D[-1]+0.4,2)
T1,T2,T3,T4,T5,T6=T
subs=["Тағйирёбанда чист? Аз он ки шумо фикр мекунед, хеле осонтар аст.",
"Тасаввур кунед: як қуттӣ доред. Болои он ном менависед: age, яъне синну сол.",
"Дар дохили қуттӣ рақами 25-ро мегузоред.",
"Баъд рақамро иваз мекунед: акнун 26.",
"Ана ҳамин тағйирёбанда аст: қуттӣ бо ном, ки қимат нигоҳ медорад.",
"Шумо дар қуттии худ чӣ мегузоред? Дар шарҳ нависед!"]
sub_html="\n".join(f'<div class="abs sub" style="--s:{T[i]}s;--len:{D[i]}s">{subs[i]}</div>' for i in range(6))
html=f"""<!doctype html><html lang="tg"><head><meta charset="utf-8"><style>
:root{{--acc:#155EEF;--dark:#101114;--muted:#5C616B}}
*{{box-sizing:border-box;margin:0}}
body{{width:540px;height:960px;overflow:hidden;font-family:Inter,"DejaVu Sans",sans-serif;background:linear-gradient(160deg,#EAF1FF,#F6F6F8);position:relative}}
.abs{{position:absolute}}
.blob{{position:absolute;border-radius:50%;background:var(--acc);opacity:.07}}
.title{{left:0;right:0;top:110px;text-align:center;animation:rise .6s ease-out .1s both}}
.title b{{display:block;font-size:50px;font-weight:800;color:var(--dark);letter-spacing:-1px}}
.title span{{font-size:22px;color:var(--acc);font-weight:700;letter-spacing:3px}}
@keyframes rise{{from{{transform:translateY(24px);opacity:0}}to{{transform:none;opacity:1}}}}
@keyframes pop{{from{{transform:scale(0) rotate(-12deg)}}to{{transform:scale(1) rotate(0)}}}}
@keyframes fadein{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes fadeout{{to{{opacity:0;transform:scale(.8)}}}}
@keyframes float{{0%,100%{{translate:0 0}}50%{{translate:0 -10px}}}}
.fl{{padding:12px 22px;border-radius:16px;background:#101114;color:#8fe3a8;font:700 26px "DejaVu Sans Mono",monospace;box-shadow:0 12px 30px rgba(16,17,20,.2);
 animation:pop .5s cubic-bezier(.3,1.6,.5,1) var(--d) both,float 2.6s ease-in-out calc(var(--d) + .5s) infinite,fadeout .4s ease-in {T2-0.3}s both}}
.q{{left:0;right:0;top:290px;text-align:center;font-size:150px;font-weight:800;color:var(--acc);animation:pop .5s cubic-bezier(.3,1.6,.5,1) .3s both,fadeout .4s ease-in {T2-0.3}s both}}
/* box */
.stage{{left:140px;top:205px;width:260px;height:260px;animation:pop .6s cubic-bezier(.3,1.6,.5,1) {T2}s both,glow 1.4s ease-in-out {T5}s infinite,outro .4s ease-in {T6-0.2}s both}}
@keyframes glow{{0%,100%{{filter:none}}50%{{filter:drop-shadow(0 0 22px rgba(21,94,239,.55))}}}}
@keyframes outro{{to{{opacity:0;transform:scale(.8)}}}}
.back{{left:0;top:70px;width:260px;height:190px;border-radius:14px;background:#C8975A}}
.front{{left:0;top:130px;width:260px;height:130px;border-radius:6px 6px 18px 18px;background:linear-gradient(#E2B070,#C8975A);z-index:3;display:flex;align-items:center;justify-content:center}}
.tag{{background:#fff;border-radius:10px;padding:8px 22px;font:800 34px "DejaVu Sans Mono",monospace;color:var(--dark);box-shadow:0 4px 10px rgba(0,0,0,.18)}}
.flapL{{left:-6px;top:50px;width:136px;height:30px;background:#B5844A;border-radius:6px;transform:rotate(-8deg);z-index:1}}
.flapR{{left:130px;top:50px;width:136px;height:30px;background:#B5844A;border-radius:6px;transform:rotate(8deg);z-index:1}}
.num{{left:75px;width:110px;height:84px;border-radius:20px;background:linear-gradient(135deg,#3B7BFF,#0F46B8);color:#fff;font-size:52px;font-weight:800;display:flex;align-items:center;justify-content:center;z-index:2;opacity:0}}
.n25{{animation:drop .7s cubic-bezier(.4,1.4,.6,1) {T3}s forwards,up .45s ease-in {T4}s forwards}}
.n26{{animation:drop .7s cubic-bezier(.4,1.4,.6,1) {T4+0.5}s forwards}}
@keyframes drop{{from{{top:-170px;opacity:1}}to{{top:62px;opacity:1}}}}
@keyframes up{{from{{top:62px;opacity:1}}to{{top:-120px;opacity:0}}}}
/* code */
.code{{left:50px;right:50px;top:480px;height:118px;border-radius:18px;background:var(--dark);padding:20px 26px;box-shadow:0 14px 36px rgba(16,17,20,.28);animation:rise .5s ease-out {T3-0.1}s both,outro .4s ease-in {T6-0.2}s both}}
.cl{{font:600 29px "DejaVu Sans Mono",monospace;color:#e7e9ee;white-space:pre;animation:type .7s steps(14,end) var(--d) both;width:max-content}}
@keyframes type{{from{{clip-path:inset(0 100% 0 0)}}to{{clip-path:inset(0 0 0 0)}}}}
.kw{{color:#7aa7ff}}.nm{{color:#ffd479}}.v{{color:#8fe3a8}}
.l1{{animation:type .7s steps(14,end) {T3+0.3}s both,dim .3s linear {T4+0.5}s both}}
@keyframes dim{{to{{opacity:.4}}}}
/* labels */
.lab{{background:#fff;border:2px solid var(--acc);border-radius:12px;padding:6px 14px;font-size:21px;font-weight:700;color:var(--acc);animation:pop .5s cubic-bezier(.3,1.6,.5,1) var(--d) both,outro .4s ease-in {T6-0.2}s both}}
/* end card */
.end{{left:40px;right:40px;top:280px;text-align:center;animation:rise .6s ease-out {T6+0.1}s both}}
.end b{{display:block;font-size:46px;line-height:1.2;color:var(--dark);font-weight:800}}
.end span{{display:inline-block;margin-top:26px;background:var(--acc);color:#fff;border-radius:40px;padding:14px 30px;font-size:26px;font-weight:700}}
/* subs */
.sub{{left:34px;right:34px;bottom:200px;text-align:center;font-size:28px;line-height:1.25;font-weight:800;color:#fff;background:rgba(16,17,20,.85);padding:12px 18px;border-radius:16px;opacity:0;animation:subs var(--len) linear var(--s) both;z-index:9}}
@keyframes subs{{0%{{opacity:0;transform:translateY(8px)}}6%{{opacity:1;transform:none}}94%{{opacity:1}}100%{{opacity:0}}}}
.prog{{left:0;bottom:0;height:5px;width:100%;background:var(--acc);transform-origin:left;animation:progr {END}s linear 0s both;z-index:10}}
@keyframes progr{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
</style></head><body>
<div class="blob" style="left:330px;top:-100px;width:360px;height:360px"></div>
<div class="blob" style="left:-120px;top:700px;width:300px;height:300px"></div>
<div class="abs title"><b>Тағйирёбанда</b><span>VARIABLE</span></div>
<div class="abs fl" style="--d:{T1+0.1}s;left:50px;top:270px">age</div>
<div class="abs fl" style="--d:{T1+0.5}s;left:300px;top:230px">name</div>
<div class="abs fl" style="--d:{T1+0.9}s;left:70px;top:390px">price</div>
<div class="abs fl" style="--d:{T1+1.3}s;left:310px;top:390px">city</div>
<div class="abs q">?</div>
<div class="abs stage">
 <div class="abs flapL"></div><div class="abs flapR"></div>
 <div class="abs back"></div>
 <div class="abs num n25">25</div><div class="abs num n26">26</div>
 <div class="abs front"><div class="tag">age</div></div>
</div>
<div class="abs code"><div class="cl l1"><span class="kw">let</span> <span class="nm">age</span> = <span class="v">25</span>;</div><div class="cl" style="--d:{T4+0.5}s;margin-top:6px"><span class="nm">age</span> = <span class="v">26</span>;</div></div>
<div class="abs lab" style="--d:{T5}s;left:20px;top:250px">ном: age</div>
<div class="abs lab" style="--d:{T5+0.6}s;left:370px;top:250px">қимат: 26</div>
<div class="abs end"><b>Шумо дар қуттии худ чӣ мегузоред?</b><span>Дар шарҳ нависед</span></div>
{sub_html}
<div class="abs prog"></div>
</body></html>"""
open('reel.html','w').write(html)
open('timing.json','w').write(str({'T':T,'END':END}))
print(T,END)
