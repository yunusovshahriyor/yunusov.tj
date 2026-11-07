# Карусел «Хатои рӯз: = ё ===» — 5 слайд, 1080×1350 (540×675 @2x).
K = lambda s: f'<span class="k">{s}</span>'; P = lambda s: f'<span class="p">{s}</span>'
S_ = lambda s: f'<span class="s">{s}</span>'; N = lambda s: f'<span class="n">{s}</span>'; F = lambda s: f'<span class="f">{s}</span>'; C = lambda s: f'<span class="cm">{s}</span>'
def ide(name, lines):
    body = "".join(f'<div class="ln">{l}</div>' for l in lines)
    return f'<div class="ide rel"><div class="bar"><i></i><i></i><i></i><span>{name}</span></div><div class="code">{body}</div></div>'
def slide(n, inner, swipe=True):
    dots = "".join(f'<i class="{"on" if i == n else ""}"></i>' for i in range(1, 6))
    sw = '<div class="sw">СВАЙП ➜</div>' if swipe else ''
    return f'<!doctype html><html lang="tg"><head><meta charset="utf-8"><link rel="stylesheet" href="base.css"></head><body><div class="w">{inner}</div>{sw}<div class="foot"><span>ХАТОИ РӮЗ · = ё ===</span><span class="dots">{dots}</span></div></body></html>'
if_age = lambda op: [K("let") + " " + P("age") + " = " + N("12") + ";", K("if") + " (" + P("age") + f" {op} " + N("18") + ") {", "  " + F("console") + "." + F("log") + "(" + S_('"Дароед"') + ");", "}"]
sl = {}
sl[1] = ('<div class="chip">ХАТОИ РӮЗ</div><div class="t" style="font-size:44px">Ин шарт ҳамеша «дуруст» мегӯяд <span class="emo">😱</span></div>'
         + ide("age.js", if_age("=")) + '<div class="p">Синну сол <b>12</b>, аммо «Дароед» чоп мешавад. <b>Чаро?</b></div>')
sl[2] = ('<div class="chip">1 · ЧӢ ШУД</div><div class="t">Як баробар қимат мегузорад</div>'
         '<div class="p"><b>age = 18</b> — ин «ба age қимати 18 бидеҳ» аст. Муқоиса нест.</div>'
         '<div style="display:flex;align-items:center;justify-content:center;gap:26px;margin:6px 0"><div class="box" style="position:relative;display:flex"><div class="tag">age</div><div class="num">12</div></div>'
         '<div style="font:900 44px var(--mono);color:var(--purple)">➜</div><div class="box" style="position:relative;display:flex"><div class="tag">age</div><div class="num">18</div></div></div>'
         '<div class="p">Барнома 18-ро «дуруст» мешуморад — шарт <b>ҳамеша мегузарад</b>.</div>')
sl[3] = ('<div class="chip">2 · ДУРУСТ</div><div class="t">Барои муқоиса — <span class="acc">се баробар</span></div>'
         + ide("age.js", if_age("===")) + '<div class="pill ok rel" style="max-width:none">12 ≠ 18 → чизе чоп намешавад ✅</div>')
sl[4] = ('<div class="chip">3 · ЁД ГИРЕД</div><div class="t">Ду нишона — ду кор</div>'
         '<div class="tbl"><div><b>=</b><span>қимат мегузорад</span></div><div><b>===</b><span>муқоиса мекунад</span></div></div>'
         '<div class="p"><b>Маслиҳат:</b> ҳамеша <b>===</b> нависед. <b>"5" == 5</b> дуруст аст, аммо <b>"5" === 5</b> не.</div>')
sl[5] = ('<div class="chip">САНҶИШ</div><div class="t">Чӣ чоп мешавад?</div>'
         + ide("test.js", [K("let") + " " + P("x") + " = " + N("5") + ";", F("console") + "." + F("log") + "(" + P("x") + " === " + S_('"5"') + ");"])
         + '<div class="pill ok rel" style="max-width:none">💬 Ҷавобро дар шарҳ нависед</div>'
         '<div class="p">🔖 <b>Захира кунед</b> · калимаи <b>«ХАТО»</b> — видеои «3 хатои рӯзи аввал» ба Direct.</div>')
for i, h in sl.items():
    open(f'slide-{i}.html', 'w', encoding='utf-8').write(slide(i, h, swipe=i < 5))
print('ok')
