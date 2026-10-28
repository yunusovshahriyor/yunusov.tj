# Генерирует reel.html; все тайминги берутся из timeline.json (начало/конец каждого предложения записи).
import json
TL=json.load(open('timeline.json'))
t=[o['start'] for o in TL]; e=[o['end'] for o in TL]; d=[e[i]-t[i] for i in range(len(t))]
END=round(e[-1]+0.5,2)
f=lambda x:f"{x:.2f}s"
def at(i,frac): return t[i]+d[i]*frac

# Субтитры: длинные предложения делятся на две части пропорционально длине
subs=[]
for o in TL:
    txt=o['text']
    if len(txt)>72 and ',' in txt:
        k=txt.index(',',len(txt)//3)+1
        a,b=txt[:k].strip(),txt[k:].strip()
        m=o['start']+(o['end']-o['start'])*len(a)/len(txt)
        subs+= [(a,o['start'],m),(b,m,o['end'])]
    else: subs.append((txt,o['start'],o['end']))
sub_html="\n".join(f'<div class="abs sub" style="--s:{f(s)};--len:{f(max(en-s,0.4)+0.12)}">{x}</div>' for x,s,en in subs)

HIDE=t[14]-0.25; SHOW=t[17]-0.2; OUT=t[20]-0.25
html=f"""<!doctype html><html lang="tg"><head><meta charset="utf-8"><style>
:root{{--acc:#155EEF;--dark:#101114;--muted:#5C616B}}
*{{box-sizing:border-box;margin:0}}
body{{width:540px;height:960px;overflow:hidden;font-family:Inter,"DejaVu Sans",sans-serif;background:linear-gradient(160deg,#EAF1FF,#F6F6F8);position:relative}}
.abs{{position:absolute}}
.blob{{position:absolute;border-radius:50%;background:var(--acc);opacity:.07}}
.title{{left:0;right:0;top:110px;text-align:center;animation:rise .6s ease-out .05s both}}
.title b{{display:block;font-size:50px;font-weight:800;color:var(--dark);letter-spacing:-1px}}
.title span{{font-size:22px;color:var(--acc);font-weight:700;letter-spacing:3px}}
@keyframes rise{{from{{transform:translateY(24px);opacity:0}}to{{transform:none;opacity:1}}}}
@keyframes pop{{from{{transform:scale(0) rotate(-12deg)}}to{{transform:scale(1) rotate(0)}}}}
@keyframes hide{{from{{opacity:1}}to{{opacity:0}}}}
@keyframes show{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes out{{from{{opacity:1;transform:none}}to{{opacity:0;transform:scale(.85)}}}}
@keyframes float{{0%,100%{{translate:0 0}}50%{{translate:0 -10px}}}}
@keyframes pulse{{0%,100%{{scale:1}}50%{{scale:1.15}}}}
.fl{{padding:12px 22px;border-radius:16px;background:#101114;color:#8fe3a8;font:700 26px "DejaVu Sans Mono",monospace;box-shadow:0 12px 30px rgba(16,17,20,.2);
 animation:pop .5s cubic-bezier(.3,1.6,.5,1) var(--d) both,float 2.6s ease-in-out calc(var(--d) + .5s) infinite,out .4s ease-in {f(t[3]-0.35)} forwards}}
.q{{left:0;right:0;top:290px;text-align:center;font-size:150px;font-weight:800;color:var(--acc);animation:pop .5s cubic-bezier(.3,1.6,.5,1) {f(t[1])} both,pulse 1.2s ease-in-out {f(t[1]+0.5)} infinite,out .4s ease-in {f(t[3]-0.35)} forwards}}
/* box */
.stage{{left:140px;top:205px;width:260px;height:260px;animation:pop .6s cubic-bezier(.3,1.6,.5,1) {f(t[3])} both,glow 1.4s ease-in-out {f(t[13])} 3,hide .35s ease-in {f(HIDE)} forwards,show .35s ease-out {f(SHOW)} forwards,out .4s ease-in {f(OUT)} forwards}}
@keyframes glow{{0%,100%{{filter:none}}50%{{filter:drop-shadow(0 0 22px rgba(21,94,239,.6))}}}}
.back{{left:0;top:70px;width:260px;height:190px;border-radius:14px;background:#C8975A}}
.front{{left:0;top:130px;width:260px;height:130px;border-radius:6px 6px 18px 18px;background:linear-gradient(#E2B070,#C8975A);z-index:3;display:flex;align-items:center;justify-content:center}}
.tag{{background:#fff;border-radius:10px;padding:8px 22px;font:800 34px "DejaVu Sans Mono",monospace;color:var(--dark);box-shadow:0 4px 10px rgba(0,0,0,.18);animation:pop .5s cubic-bezier(.3,1.6,.5,1) {f(at(5,0.55))} both}}
.flapL{{left:-6px;top:50px;width:136px;height:30px;background:#B5844A;border-radius:6px;transform:rotate(-8deg)}}
.flapR{{left:130px;top:50px;width:136px;height:30px;background:#B5844A;border-radius:6px;transform:rotate(8deg)}}
.num{{left:75px;top:62px;width:110px;height:84px;border-radius:20px;background:linear-gradient(135deg,#3B7BFF,#0F46B8);color:#fff;font-size:52px;font-weight:800;display:flex;align-items:center;justify-content:center;z-index:2;opacity:0}}
@keyframes drop{{from{{top:-60px;opacity:0}}30%{{opacity:1}}to{{top:62px;opacity:1}}}}
@keyframes up{{from{{top:62px;opacity:1}}to{{top:-40px;opacity:0}}}}
.n25{{animation:drop .7s cubic-bezier(.4,1.4,.6,1) {f(e[6]-1.1)} forwards,up .45s ease-in {f(at(10,0.22))} forwards}}
.n26{{animation:drop .7s cubic-bezier(.4,1.4,.6,1) {f(at(10,0.72))} forwards,up .45s ease-in {f(t[19]+0.3)} forwards}}
.n27{{animation:drop .7s cubic-bezier(.4,1.4,.6,1) {f(t[19]+0.8)} forwards}}
/* code */
.code{{left:50px;right:50px;top:480px;height:118px;border-radius:18px;background:var(--dark);padding:20px 26px;box-shadow:0 14px 36px rgba(16,17,20,.28);opacity:0;animation:show .4s ease-out {f(t[7])} forwards,hide .35s ease-in {f(HIDE)} forwards,show .35s ease-out {f(SHOW)} forwards,out .4s ease-in {f(OUT)} forwards}}
.cl{{font:600 29px "DejaVu Sans Mono",monospace;color:#e7e9ee;white-space:pre;width:max-content;clip-path:inset(0 100% 0 0)}}
@keyframes type{{from{{clip-path:inset(0 100% 0 0)}}to{{clip-path:inset(0 0 0 0)}}}}
@keyframes dim{{to{{opacity:.4}}}}
.kw{{color:#7aa7ff}}.nm{{color:#ffd479}}.v{{color:#8fe3a8}}
.l1{{animation:type .8s steps(14,end) {f(e[7]-2.0)} forwards,dim .3s linear {f(at(10,0.72))} forwards}}
.l2{{margin-top:6px;animation:type .7s steps(10,end) {f(at(10,0.72))} forwards}}
/* labels */
.lab{{background:#fff;border:2px solid var(--acc);border-radius:12px;padding:6px 16px;font-size:24px;font-weight:800;color:var(--acc);opacity:0}}
.labN{{left:28px;top:250px;animation:pop .5s cubic-bezier(.3,1.6,.5,1) {f(at(11,0.55))} forwards,show .01s {f(at(11,0.55))} forwards,hide .35s ease-in {f(HIDE)} forwards,show .35s ease-out {f(SHOW)} forwards,pulse .6s ease-in-out {f(t[17]+0.2)} 2,out .4s ease-in {f(OUT)} forwards}}
.labQ{{left:388px;top:250px;animation:pop .5s cubic-bezier(.3,1.6,.5,1) {f(t[12])} forwards,show .01s {f(t[12])} forwards,hide .35s ease-in {f(HIDE)} forwards,show .35s ease-out {f(SHOW)} forwards,pulse .6s ease-in-out {f(t[18]+0.2)} 2,out .4s ease-in {f(OUT)} forwards}}
/* examples */
.ex{{left:40px;right:40px;top:225px;opacity:0;animation:show .35s ease-out {f(t[14])} forwards,hide .35s ease-in {f(SHOW)} forwards}}
.exh{{text-align:center;font-size:30px;font-weight:800;color:var(--dark);margin-bottom:18px}}
.card{{position:relative;height:104px;border-radius:22px;background:#fff;box-shadow:0 12px 30px rgba(16,17,20,.12);margin-bottom:16px;display:flex;align-items:center;padding:0 22px;gap:18px;animation:pop .5s cubic-bezier(.3,1.6,.5,1) var(--d) both}}
.ic{{width:64px;height:64px;border-radius:18px;display:flex;align-items:center;justify-content:center;flex:none}}
.ct{{font-size:24px;font-weight:700;color:var(--dark)}}
.val{{position:absolute;right:24px;top:30px;font-size:34px;font-weight:800;color:var(--acc)}}
.old{{animation:up2 .4s ease-in var(--c) forwards}}
.new{{opacity:0;animation:in2 .4s ease-out calc(var(--c) + .3s) forwards}}
@keyframes up2{{to{{transform:translateY(-26px);opacity:0}}}}
@keyframes in2{{from{{transform:translateY(26px);opacity:0}}to{{transform:none;opacity:1}}}}
/* end */
.end{{left:36px;right:36px;top:250px;text-align:center;opacity:0;animation:show .5s ease-out {f(t[20])} forwards}}
.end b{{display:block;font-size:40px;line-height:1.2;color:var(--dark);font-weight:800}}
.chip{{display:inline-block;margin-top:22px;border-radius:40px;padding:14px 28px;font-size:25px;font-weight:700;animation:pop .5s cubic-bezier(.3,1.6,.5,1) var(--d) both}}
.c1{{background:var(--acc);color:#fff}}.c2{{background:#fff;color:var(--dark);border:2px solid #E4E5E9}}
.c3{{background:var(--dark);color:#fff;animation:pop .5s cubic-bezier(.3,1.6,.5,1) var(--d) both,pulse 1s ease-in-out calc(var(--d) + .5s) infinite}}
/* subs */
.sub{{left:34px;right:34px;bottom:200px;text-align:center;font-size:28px;line-height:1.25;font-weight:800;color:#fff;background:rgba(16,17,20,.85);padding:12px 18px;border-radius:16px;opacity:0;animation:subs var(--len) linear var(--s) both;z-index:9}}
@keyframes subs{{0%{{opacity:0;transform:translateY(6px)}}5%{{opacity:1;transform:none}}96%{{opacity:1}}100%{{opacity:0}}}}
.prog{{left:0;bottom:0;height:5px;width:100%;background:var(--acc);transform-origin:left;animation:progr {f(END)} linear 0s both;z-index:10}}
@keyframes progr{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
</style></head><body>
<div class="blob" style="left:330px;top:-100px;width:360px;height:360px"></div>
<div class="blob" style="left:-120px;top:700px;width:300px;height:300px"></div>
<div class="abs title"><b>Тағйирёбанда</b><span>VARIABLE</span></div>
<div class="abs fl" style="--d:{f(t[1]+0.2)};left:50px;top:270px">age</div>
<div class="abs fl" style="--d:{f(t[1]+0.7)};left:300px;top:230px">name</div>
<div class="abs fl" style="--d:{f(t[1]+1.2)};left:70px;top:390px">price</div>
<div class="abs fl" style="--d:{f(t[1]+1.7)};left:310px;top:390px">city</div>
<div class="abs q">?</div>
<div class="abs stage">
 <div class="abs flapL"></div><div class="abs flapR"></div>
 <div class="abs back"></div>
 <div class="abs num n25">25</div><div class="abs num n26">26</div><div class="abs num n27">27</div>
 <div class="abs front"><div class="tag">age</div></div>
</div>
<div class="abs code"><div class="cl l1"><span class="kw">let</span> <span class="nm">age</span> = <span class="v">25</span>;</div><div class="cl l2"><span class="nm">age</span> = <span class="v">26</span>;</div></div>
<div class="abs lab labN">ном</div>
<div class="abs lab labQ">қимат</div>
<div class="abs ex"><div class="exh">Дар ҳаёт</div>
 <div class="card" style="--d:{f(t[15])}"><div class="ic" style="background:#FF9500"><svg width="38" height="38" viewBox="0 0 24 24" fill="#fff"><path d="M12 2l3 6.5 7 .8-5.2 4.8 1.4 7L12 17.6 5.8 21.1l1.4-7L2 9.3l7-.8z"/></svg></div><div class="ct">Холи бозӣ</div><div class="val old" style="--c:{f(t[16])}">120</div><div class="val new" style="--c:{f(t[16])}">150</div></div>
 <div class="card" style="--d:{f(at(15,0.3))}"><div class="ic" style="background:#155EEF"><svg width="38" height="38" viewBox="0 0 24 24" fill="#fff"><path d="M3 5h18a1 1 0 0 1 1 1v3H2V6a1 1 0 0 1 1-1zm-1 6h20v7a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1v-7zm3 4v2h5v-2H5z"/></svg></div><div class="ct">Бақияи ҳисоб</div><div class="val old" style="--c:{f(t[16]+0.25)}">500 с.</div><div class="val new" style="--c:{f(t[16]+0.25)}">350 с.</div></div>
 <div class="card" style="--d:{f(at(15,0.62))}"><div class="ic" style="background:#E1306C"><svg width="38" height="38" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-7 8-7s8 2.6 8 7"/></svg></div><div class="ct">Пайравон</div><div class="val old" style="--c:{f(t[16]+0.5)}">1 443</div><div class="val new" style="--c:{f(t[16]+0.5)}">1 500</div></div>
</div>
<div class="abs end"><b>Номи қуттии шумо чӣ мебуд?<br>Дар дохилаш чӣ мегузоштед?</b>
 <div class="chip c1" style="--d:{f(t[21])}">Дар шарҳ нависед</div><br>
 <div class="chip c2" style="--d:{f(t[22])}">Дарси оянда: шарт (if/else)</div><br>
 <div class="chip c3" style="--d:{f(t[23])}">Обуна шавед</div>
</div>
{sub_html}
<div class="abs prog"></div>
</body></html>"""
open('reel.html','w').write(html)
print(END)
