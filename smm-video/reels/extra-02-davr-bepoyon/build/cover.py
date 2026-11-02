import character as C
shock = C.svg(C.pose_shock())
html = f'''<!doctype html><html lang="tg"><head><meta charset="utf-8"><link rel="stylesheet" href="build/style.css"><style>
.cc{{position:absolute;left:0;right:0;text-align:center}}
.big svg{{position:absolute;left:70px;top:440px;width:400px;height:400px;overflow:visible}}
.p{{position:absolute;width:58px;height:22px;border-radius:11px;font:800 12px/22px Inter;text-align:center;color:#1E1E1E}}
</style></head><body>
<div class="pill" style="top:150px;background:transparent;border:2px solid var(--pink);color:var(--pink);font:800 15px var(--mono);letter-spacing:4px;padding:8px 22px">ДАВР · ҲАҶВ</div>
<div class="h1" style="top:205px;font-size:76px;color:#fff">Давр ист<br><span class="acc">намекунад!</span></div>
<div class="ide" style="top:420px;left:40px;right:40px"><div class="code" style="font-size:17.5px;padding:10px 16px"><span class="c">while</span> (<span class="k">true</span>) {{ <span class="f">console</span>.<span class="f">log</span>(<span class="s">"Салом"</span>); }}</div></div>
<div class="big">{shock}</div>
<div class="p" style="left:40px;top:760px;background:#BD93F9;rotate:-12deg">Салом</div><div class="p" style="left:110px;top:790px;background:#FF79C6;rotate:8deg">Салом</div>
<div class="p" style="left:380px;top:770px;background:#BD93F9;rotate:14deg">Салом</div><div class="p" style="left:430px;top:735px;background:#FF79C6;rotate:-6deg">Салом</div>
</body></html>'''
open('../cover.html', 'w', encoding='utf-8').write(html)
