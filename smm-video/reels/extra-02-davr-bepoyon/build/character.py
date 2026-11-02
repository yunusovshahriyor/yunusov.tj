# Одамак v2 — қаҳрамони воқеъбинтар: сари инсонӣ бо мӯй ва гӯши табиӣ, гардан, ҷомаи бунафш, ҷинс, кроссовка.
import random
SKIN, SKIN2 = "#F2C7A0", "#DDA97C"
HAIR = "#2A2233"; HOOD, HOOD2 = "#8A63E0", "#6A47C4"; JEANS, JEANS2 = "#34416A", "#27325A"

def stroke(pts, w, c, cap="round"):
    d = "M" + " L".join(f"{x},{y}" for x, y in pts)
    return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="{cap}" stroke-linejoin="round"/>'
def arm(s, e, h, front=True):
    c = HOOD if front else HOOD2
    return stroke([s, e, h], 14, c) + f'<circle cx="{h[0]}" cy="{h[1]}" r="7.2" fill="{SKIN}"/>'
def leg(h, k, f, front=True, flip=1):
    c = JEANS if front else JEANS2
    fx, fy = f
    shoe = f'<ellipse cx="{fx+flip*6}" cy="{fy+3}" rx="12" ry="6" fill="#F5F5F7" stroke="#C9C9D2" stroke-width="1.5"/><rect x="{fx+flip*6-12}" y="{fy+6}" width="24" height="2.5" rx="1" fill="#BD93F9"/>'
    return stroke([h, k, f], 15, c) + shoe
def torso(sh_l, sh_r, hip_l, hip_r):
    (a, b), (c, d), (e, f), (g, h) = sh_l, sh_r, hip_r, hip_l
    path = f'M{a},{b+4} Q{a-2},{b-3} {a+8},{b-4} L{c-8},{d-4} Q{c+2},{d-3} {c},{d+4} L{e},{f} Q{(e+g)/2},{f+8} {g},{h} Z'
    return (f'<path d="{path}" fill="url(#hood)"/>'
            f'<path d="M{(a+c)/2-12},{b-4} Q{(a+c)/2},{b+10} {(a+c)/2+12},{d-4}" fill="none" stroke="{HOOD2}" stroke-width="5" stroke-linecap="round"/>')
def neck(x, y): return f'<rect x="{x-6}" y="{y}" width="12" height="16" rx="5" fill="{SKIN2}"/>'

def face(cx, cy, mood):
    def eye(dx, wide=False, closed=False, happy=False):
        x = cx + dx
        if happy: return f'<path d="M{x-6},{cy-1} Q{x},{cy-9} {x+6},{cy-1}" fill="none" stroke="#2A2233" stroke-width="2.6" stroke-linecap="round"/>'
        r = 6.5 if wide else 5
        return f'<ellipse cx="{x}" cy="{cy-3}" rx="{r}" ry="{r+1}" fill="#fff"/><circle cx="{x+(0.6 if dx<0 else -0.6)}" cy="{cy-3}" r="{3 if not wide else 2.4}" fill="#2A2233"/>'
    nose = f'<path d="M{cx},{cy+1} Q{cx+3},{cy+7} {cx},{cy+8}" fill="none" stroke="{SKIN2}" stroke-width="2" stroke-linecap="round"/>'
    if mood == "type":
        return (eye(-9)+eye(9)+nose+f'<path d="M{cx-14},{cy-13} Q{cx-9},{cy-16} {cx-4},{cy-13} M{cx+4},{cy-13} Q{cx+9},{cy-16} {cx+14},{cy-13}" fill="none" stroke="{HAIR}" stroke-width="2.6" stroke-linecap="round"/>'
                f'<path d="M{cx-8},{cy+13} Q{cx},{cy+19} {cx+8},{cy+13}" fill="none" stroke="#7a3b3b" stroke-width="2.6" stroke-linecap="round"/>')
    if mood == "shock":
        return (eye(-9,True)+eye(9,True)+nose+f'<path d="M{cx-16},{cy-18} L{cx-3},{cy-13} M{cx+16},{cy-18} L{cx+3},{cy-13}" stroke="{HAIR}" stroke-width="2.8" stroke-linecap="round"/>'
                f'<ellipse cx="{cx}" cy="{cy+15}" rx="6" ry="8" fill="#5a1f2b"/><ellipse cx="{cx}" cy="{cy+18}" rx="3.5" ry="3" fill="#E36F7B"/>')
    if mood == "happy":
        return (eye(-9,happy=True)+eye(9,happy=True)+nose+f'<path d="M{cx-12},{cy+9} Q{cx},{cy+25} {cx+12},{cy+9} Z" fill="#5a1f2b"/><path d="M{cx-9},{cy+10} Q{cx},{cy+14} {cx+9},{cy+10}" fill="#fff"/>'
                f'<ellipse cx="{cx-15}" cy="{cy+8}" rx="4" ry="2.6" fill="#F59BA4" opacity=".6"/><ellipse cx="{cx+15}" cy="{cy+8}" rx="4" ry="2.6" fill="#F59BA4" opacity=".6"/>')
    return (eye(-9)+eye(9)+nose+f'<path d="M{cx-15},{cy-12} L{cx-4},{cy-15} M{cx+15},{cy-12} L{cx+4},{cy-15}" stroke="{HAIR}" stroke-width="2.8" stroke-linecap="round"/>'
            f'<path d="M{cx-8},{cy+16} Q{cx},{cy+10} {cx+8},{cy+16}" fill="none" stroke="#7a3b3b" stroke-width="2.6" stroke-linecap="round"/>')
def head(cx, cy, mood):
    ears = "".join(f'<ellipse cx="{cx+s*25}" cy="{cy+3}" rx="5.5" ry="8" fill="{SKIN2}"/><ellipse cx="{cx+s*25}" cy="{cy+3}" rx="2.6" ry="4.5" fill="#C98F66"/>' for s in (-1, 1))
    hair = (f'<path d="M{cx-26},{cy-2} Q{cx-30},{cy-38} {cx},{cy-34} Q{cx+30},{cy-38} {cx+26},{cy-2} Q{cx+22},{cy-18} {cx+6},{cy-21} Q{cx-10},{cy-14} {cx-26},{cy-2} Z" fill="{HAIR}"/>'
            f'<path d="M{cx-4},{cy-32} Q{cx+14},{cy-44} {cx+20},{cy-30}" fill="none" stroke="{HAIR}" stroke-width="7" stroke-linecap="round"/>')
    return (neck(cx, cy+22) + ears + f'<ellipse cx="{cx}" cy="{cy}" rx="25" ry="28" fill="url(#skin)"/>' + hair + face(cx, cy, mood))

def laptop(x, y, scr="#BD93F9", w=70, h=52, mark=""):
    s = (f'<g transform="translate({x},{y})"><path d="M-6,{h} L{w+6},{h} L{w+14},{h+10} L-14,{h+10} Z" fill="#3a3a40" stroke="#555" stroke-width="2"/>'
         f'<rect x="0" y="0" width="{w}" height="{h}" rx="5" fill="#1E1E1E" stroke="{scr}" stroke-width="3" filter="url(#glow)"/>')
    cols = ["#569CD6", "#CE9178", "#B5CEA8", "#DCDCAA", "#9CDCFE"]
    for i in range(5): s += f'<rect x="8" y="{9+i*8}" width="{20+((i*13)%26)}" height="4" rx="2" fill="{cols[i]}"/>'
    return s + mark + '</g>'

DEFS = f'''<defs>
<linearGradient id="skin" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F8D5B2"/><stop offset="1" stop-color="{SKIN2}"/></linearGradient>
<linearGradient id="hood" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{HOOD}"/><stop offset="1" stop-color="{HOOD2}"/></linearGradient>
<filter id="glow" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="3.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>'''

def pose_type():
    return (leg((104,170),(150,192),(116,214),False) + leg((104,170),(64,194),(104,216),True,-1)
            + arm((112,114),(138,150),(160,178),False) + torso((90,112),(126,112),(88,172),(120,172)) + head(108,76,"type")
            + laptop(142,124,"#BD93F9",64,50) + arm((92,116),(124,152),(148,178)))
def pose_shock():
    drops = '<path d="M58,40 q-5,9 0,12 q5,-3 0,-12z M208,52 q-5,9 0,12 q5,-3 0,-12z" fill="#4FC1FF"/>'
    return (leg((126,170),(108,214),(96,250),False,-1) + leg((146,170),(164,214),(178,250)) + arm((152,112),(178,84),(190,48),False)
            + torso((112,112),(158,112),(116,172),(154,172)) + head(135,68,"shock") + arm((118,112),(92,84),(80,48)) + drops
            + laptop(188,196,"#F48771",60,44,'<text x="30" y="30" font-size="22" text-anchor="middle">🔥</text>'))
def pose_buried():
    r = random.Random(4); pills = ""
    for i in range(26):
        x = r.randint(10, 205); y = r.randint(150, 235); rot = r.randint(-25, 25); c = "#BD93F9" if i % 2 else "#FF79C6"
        pills += (f'<g transform="translate({x},{y}) rotate({rot})"><rect width="58" height="22" rx="11" fill="{c}"/>'
                  f'<text x="29" y="15" font-size="12" font-weight="800" fill="#1E1E1E" text-anchor="middle" font-family="Inter,sans-serif">Салом</text></g>')
    return (arm((168,168),(190,126),(206,88),False) + head(135,120,"help") + pills
            + '<text x="135" y="40" font-size="30" text-anchor="middle" fill="#FF79C6" font-family="monospace" font-weight="800">1 000 000×</text>')
def pose_happy():
    return (leg((126,170),(108,214),(96,250),False,-1) + leg((146,170),(164,214),(178,250)) + arm((152,112),(184,78),(194,40),False)
            + torso((112,112),(158,112),(116,172),(154,172)) + head(135,68,"happy") + arm((118,112),(86,78),(76,40))
            + '<text x="52" y="64" font-size="22">✨</text><text x="205" y="74" font-size="22">✨</text>'
            + laptop(190,198,"#4EC9B0",60,44,'<text x="30" y="30" font-size="22" font-weight="900" fill="#4EC9B0" text-anchor="middle">✓</text>'))

def svg(inner): return f'<svg viewBox="0 0 270 270" width="270" height="270">{DEFS}{inner}</svg>'
POSES = [("Нависандагӣ", pose_type), ("Ҳайрат!", pose_shock), ("Зери «Салом»-ҳо", pose_buried), ("Ҳал шуд!", pose_happy)]
if __name__ == "__main__":
    cells = "".join(f'<div class="cell">{svg(f())}<b>{n}</b></div>' for n, f in POSES)
    html = f'''<!doctype html><html lang="tg"><head><meta charset="utf-8"><link rel="stylesheet" href="style.css"><style>
body{{width:560px;height:740px}} .t{{position:absolute;left:0;right:0;top:34px;text-align:center}}
.t p{{font:800 11px var(--mono);letter-spacing:3px;color:var(--purple);margin-bottom:6px}}
.grid{{position:absolute;left:20px;right:20px;top:128px;display:grid;grid-template-columns:1fr 1fr;gap:14px}}
.cell{{background:var(--panel);border:1px solid var(--line);border-radius:18px;text-align:center;padding:8px 0 10px;box-shadow:0 10px 30px rgba(0,0,0,.4);
background-image:radial-gradient(rgba(255,255,255,.06) 1px,transparent 1px);background-size:14px 14px}}
.cell b{{display:block;font:800 14px Inter;color:#fff;margin-top:-6px}} svg{{display:block;margin:0 auto;width:100%;height:auto;max-width:240px}}
</style></head><body><div class="t"><p>ҚАҲРАМОНИ АНИМАЦИЯҲО</p><h1 class="h1" style="position:static;font-size:44px"><span class="acc">Одамак</span></h1></div><div class="grid">{cells}</div></body></html>'''
    open("character.html", "w", encoding="utf-8").write(html)
