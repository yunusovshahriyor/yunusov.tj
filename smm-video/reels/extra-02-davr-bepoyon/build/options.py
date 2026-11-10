# Ду вариант: (1) истода бо ноутбук дар даст, (2) дар курсӣ нишаста
import json
rig = open('rig.js', encoding='utf-8').read()
html = f'''<!doctype html><html lang="tg"><head><meta charset="utf-8"><link rel="stylesheet" href="style.css"><style>
body{{width:560px;height:660px}} .t{{position:absolute;left:0;right:0;top:30px;text-align:center}}
.t p{{font:800 11px var(--mono);letter-spacing:3px;color:var(--purple);margin-bottom:6px}}
.card{{position:absolute;width:260px;height:470px;top:128px;border-radius:18px;background:var(--panel);border:1px solid var(--line);overflow:hidden;
box-shadow:0 10px 30px rgba(0,0,0,.4);background-image:radial-gradient(rgba(255,255,255,.06) 1px,transparent 1px);background-size:14px 14px}}
.card svg{{position:absolute;left:0;top:110px}}
.card b{{position:absolute;left:0;right:0;bottom:12px;text-align:center;font:800 14px Inter;color:#fff}}
.card .code{{position:absolute;left:0;right:0;top:46px;text-align:center;font:600 15px/1.5 var(--mono);color:var(--text);padding:0;white-space:pre}}
</style></head><body>
<svg id="stage" width="0" height="0"><defs>{{DEFS}}</defs><g id="rig"></g></svg>
<div class="t"><p>ҚАҲРАМОН · НАВИШТАНИ КОД</p><h1 class="h1" style="position:static;font-size:38px">Кадомаш <span class="acc">беҳтар</span> аст?</h1></div>
<div class="card" style="left:14px"><svg id="a" viewBox="0 450 270 270" width="260" height="360"></svg><div class="code"><span style="color:#C586C0">while</span> (<span style="color:#569CD6">true</span>) {{\n  <span style="color:#DCDCAA">console</span>.log(<span style="color:#CE9178">"Салом"</span>);\n}}</div><b>1 · истода, ноутбук дар даст</b></div>
<div class="card" style="left:286px"><svg id="b" viewBox="0 450 270 270" width="260" height="360"></svg><div class="code"><span style="color:#C586C0">while</span> (<span style="color:#569CD6">true</span>) {{\n  <span style="color:#DCDCAA">console</span>.log(<span style="color:#CE9178">"Салом"</span>);\n}}</div><b>2 · дар курсӣ нишаста</b></div>
<script>{rig}</script>
<script>
const STAND = window.__STAND, GY = window.__GY;
const base = {{ x:120, y:STAND, torso:6, tilt:7, look:5, hL:5, kL:-5, hR:-8, kR:-8, aL:[0,0], aR:[0,0], bL:1, bR:-1, lx:0, ly:0, lrot:0, heat:0 }};
// 1 — истода: ноутбук дар даст (паҳлӯ)
const A = Object.assign({{}}, base, {{ x:78, side:1, torso:3, tilt:5, look:9, hL:8, kL:-6, hR:-6, kR:-8 }});
A.lx = A.x + 64; A.ly = A.y - 26; A.aL = [A.x + 34, A.ly + 4]; A.aR = [A.lx - 6, A.ly - 10]; A.bL = 1; A.bR = 1;
document.getElementById('a').innerHTML = `<defs>` + document.querySelector('#stage defs').innerHTML + `</defs>` + window.__drawPose(A, 'type', 0.5, null);
// 2 — дар курсӣ (паҳлӯ)
const seatTop = GY - 46;
const B = Object.assign({{}}, base, {{ x:92, y:seatTop - 14, side:1, torso:10, tilt:8, look:9, hL:90, kL:-90, hR:88, kR:-90 }});
B.lx = B.x + 36; B.ly = B.y - 6; B.aL = [B.lx - 22, B.ly - 10]; B.aR = [B.lx - 4, B.ly - 10]; B.bL = 1; B.bR = 1;
document.getElementById('b').innerHTML = `<defs>` + document.querySelector('#stage defs').innerHTML + `</defs>` + window.__drawPose(B, 'type', 0.5, {{ cx: B.x - 4, top: seatTop }});
</script></body></html>'''
import character as C
html = html.replace('{DEFS}', C.DEFS.replace('<defs>', '').replace('</defs>', ''))
open('options.html', 'w', encoding='utf-8').write(html)
