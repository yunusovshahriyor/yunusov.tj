# Одамак — қаҳрамони анимацияҳо. Чор ҳолат: нависандагӣ, ҳайрат, зери «Салом»-ҳо, хушҳол.
def limb(*pts, w=9, c="#F2F2F2"):
    d = "M" + " L".join(f"{x},{y}" for x, y in pts)
    return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'

def head(cx, cy, mood):
    face = ""
    if mood == "type":      # диққат, табассуми хурд
        face = (f'<circle cx="{cx-9}" cy="{cy-3}" r="3.2" fill="#1E1E1E"/><circle cx="{cx+9}" cy="{cy-3}" r="3.2" fill="#1E1E1E"/>'
                f'<path d="M{cx-9},{cy+9} Q{cx},{cy+16} {cx+9},{cy+9}" fill="none" stroke="#1E1E1E" stroke-width="3" stroke-linecap="round"/>')
    elif mood == "shock":   # чашмҳои калон, даҳони кушода
        face = (f'<circle cx="{cx-10}" cy="{cy-4}" r="7" fill="#fff"/><circle cx="{cx+10}" cy="{cy-4}" r="7" fill="#fff"/>'
                f'<circle cx="{cx-10}" cy="{cy-4}" r="2.6" fill="#1E1E1E"/><circle cx="{cx+10}" cy="{cy-4}" r="2.6" fill="#1E1E1E"/>'
                f'<ellipse cx="{cx}" cy="{cy+12}" rx="6" ry="8" fill="#1E1E1E"/>'
                f'<path d="M{cx-18},{cy-16} L{cx-5},{cy-12} M{cx+18},{cy-16} L{cx+5},{cy-12}" stroke="#1E1E1E" stroke-width="3" stroke-linecap="round"/>')
    elif mood == "happy":   # чашмони пӯшида, табассуми калон
        face = (f'<path d="M{cx-14},{cy-2} Q{cx-9},{cy-9} {cx-4},{cy-2} M{cx+4},{cy-2} Q{cx+9},{cy-9} {cx+14},{cy-2}" fill="none" stroke="#1E1E1E" stroke-width="3" stroke-linecap="round"/>'
                f'<path d="M{cx-12},{cy+6} Q{cx},{cy+22} {cx+12},{cy+6} Z" fill="#1E1E1E"/>')
    elif mood == "help":    # нигарон
        face = (f'<circle cx="{cx-9}" cy="{cy-3}" r="3.4" fill="#1E1E1E"/><circle cx="{cx+9}" cy="{cy-3}" r="3.4" fill="#1E1E1E"/>'
                f'<path d="M{cx-8},{cy+14} Q{cx},{cy+7} {cx+8},{cy+14}" fill="none" stroke="#1E1E1E" stroke-width="3" stroke-linecap="round"/>'
                f'<path d="M{cx-16},{cy-13} L{cx-5},{cy-10} M{cx+16},{cy-13} L{cx+5},{cy-10}" stroke="#1E1E1E" stroke-width="3" stroke-linecap="round"/>')
    # гӯшмонак (headphones) — нишони хосси Одамак
    hp = (f'<path d="M{cx-27},{cy+2} A27,27 0 0 1 {cx+27},{cy+2}" fill="none" stroke="#BD93F9" stroke-width="6" stroke-linecap="round"/>'
          f'<rect x="{cx-33}" y="{cy-4}" width="10" height="20" rx="5" fill="#FF79C6"/><rect x="{cx+23}" y="{cy-4}" width="10" height="20" rx="5" fill="#FF79C6"/>')
    return (f'<circle cx="{cx}" cy="{cy}" r="28" fill="url(#hg)" filter="url(#glow)"/>' + hp + face)

def laptop(x, y, scr="#BD93F9", w=70, h=52, lines=True, mark=""):
    s = (f'<g transform="translate({x},{y})">'
         f'<path d="M-6,{h} L{w+6},{h} L{w+14},{h+10} L-14,{h+10} Z" fill="#3a3a40" stroke="#555" stroke-width="2"/>'
         f'<rect x="0" y="0" width="{w}" height="{h}" rx="5" fill="#1E1E1E" stroke="{scr}" stroke-width="3" filter="url(#glow)"/>')
    if lines:
        cols = ["#569CD6", "#CE9178", "#B5CEA8", "#DCDCAA", "#9CDCFE"]
        for i in range(5):
            s += f'<rect x="8" y="{9+i*8}" width="{20+((i*13)%26)}" height="4" rx="2" fill="{cols[i]}"/>'
    s += mark + '</g>'
    return s

DEFS = '''<defs>
<linearGradient id="hg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#BD93F9"/><stop offset="1" stop-color="#FF79C6"/></linearGradient>
<filter id="glow" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="3.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>'''

def pose_type():
    return (limb((110,106),(106,168)) + limb((106,168),(152,192),(118,214)) + limb((106,168),(66,194),(108,214))
            + laptop(140,122,"#BD93F9",64,50) + limb((110,112),(134,152),(158,176)) + limb((110,112),(128,146),(150,170),w=8)
            + head(110,78,"type"))
def pose_shock():
    drops = '<path d="M60,40 q-5,9 0,12 q5,-3 0,-12z M205,52 q-5,9 0,12 q5,-3 0,-12z" fill="#4FC1FF"/>'
    return (limb((135,100),(135,166)) + limb((135,166),(112,214),(100,250)) + limb((135,166),(160,214),(176,250))
            + limb((135,104),(96,82),(80,46)) + limb((135,104),(174,82),(190,46))
            + head(135,70,"shock") + drops
            + laptop(188,196,"#F48771",60,44,True,'<text x="30" y="30" font-size="22" text-anchor="middle">🔥</text>'))
def pose_buried():
    pills = ""
    import random
    r = random.Random(4)
    for i in range(26):
        x = r.randint(10,205); y = r.randint(150,235); rot = r.randint(-25,25)
        c = "#BD93F9" if i % 2 else "#FF79C6"
        pills += (f'<g transform="translate({x},{y}) rotate({rot})"><rect width="58" height="22" rx="11" fill="{c}"/>'
                  f'<text x="29" y="15" font-size="12" font-weight="800" fill="#1E1E1E" text-anchor="middle" font-family="Inter,sans-serif">Салом</text></g>')
    return (head(135,118,"help") + limb((165,150),(190,112),(205,86)) + pills
            + '<text x="135" y="40" font-size="30" text-anchor="middle" fill="#FF79C6" font-family="monospace" font-weight="800">1 000 000×</text>')
def pose_happy():
    return (limb((135,100),(135,166)) + limb((135,166),(112,214),(100,250)) + limb((135,166),(160,214),(176,250))
            + limb((135,104),(100,70),(86,34)) + limb((135,104),(170,70),(184,34))
            + head(135,70,"happy")
            + '<text x="60" y="60" font-size="22">✨</text><text x="195" y="70" font-size="22">✨</text>'
            + laptop(190,198,"#4EC9B0",60,44,True,'<text x="30" y="30" font-size="22" font-weight="900" fill="#4EC9B0" text-anchor="middle">✓</text>'))

def svg(inner): return f'<svg viewBox="0 0 270 270" width="270" height="270">{DEFS}{inner}</svg>'
POSES = [("Нависандагӣ", pose_type), ("Ҳайрат!", pose_shock), ("Зери «Салом»-ҳо", pose_buried), ("Ҳал шуд!", pose_happy)]
if __name__ == "__main__":
    cells = "".join(f'<div class="cell">{svg(f())}<b>{n}</b></div>' for n, f in POSES)
    html = f'''<!doctype html><html lang="tg"><head><meta charset="utf-8"><link rel="stylesheet" href="style.css"><style>
body{{width:560px;height:740px}} .t{{position:absolute;left:0;right:0;top:34px;text-align:center}}
.t h1{{position:static;font-size:44px}} .t p{{font:800 11px var(--mono);letter-spacing:3px;color:var(--purple);margin-bottom:6px}}
.grid{{position:absolute;left:20px;right:20px;top:128px;display:grid;grid-template-columns:1fr 1fr;gap:14px}}
.cell{{background:var(--panel);border:1px solid var(--line);border-radius:18px;text-align:center;padding:8px 0 10px;box-shadow:0 10px 30px rgba(0,0,0,.4);
background-image:radial-gradient(rgba(255,255,255,.06) 1px,transparent 1px);background-size:14px 14px}}
.cell b{{display:block;font:800 14px Inter;color:#fff;margin-top:-6px}} svg{{display:block;margin:0 auto;width:100%;height:auto;max-width:240px}}
</style></head><body><div class="t"><p>ҚАҲРАМОНИ АНИМАЦИЯҲО</p><h1 class="h1" style="position:static"><span class="acc">Одамак</span></h1></div><div class="grid">{cells}</div></body></html>'''
    open("character.html", "w", encoding="utf-8").write(html)
