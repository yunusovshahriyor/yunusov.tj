# Собирает video.html (IDE web-режим: HTML/CSS/JS + пешнамоиш, слайды, таймлайн), sfx.json, .srt и главы для YouTube-урока 11.
import json, re, html
WJ = json.load(open('words.json')); W = WJ['words']; NARR_END = WJ['total']
toks = [re.sub(r'[^\w-]', '', w['w']).lower() for w in W]

def find(phrase, after=0):
    if isinstance(after, float):
        after = next((k for k, w in enumerate(W) if V(w['t0']) >= after - .01), len(W))
    seq = [re.sub(r'[^\w-]', '', x).lower() for x in phrase.split()]
    for i in range(after, len(W) - len(seq) + 1):
        if toks[i:i + len(seq)] == seq: return i
    raise SystemExit('not found: ' + phrase)

GAPS = []
def V(nt): return nt + sum(d for g, d in GAPS if g <= nt)
def N(nt): return round(V(nt), 3)          # время повествования (из транскрипта) -> время видео
def I(phrase, after=0): return find(phrase, after)
PAUSE = 5.0
GAP_Q = W[I('фикр кунед.', I('Ва санҷиши нав')) + 1]['t1'] + 0.05; GAPS.append((GAP_Q, PAUSE))
END = round(V(NARR_END) + 0.8, 2)

scenes, ide, marks, rings, ptr, chips, zooms, sfx, pv = [], [], [], [], [], [], [], [], []
def S(id, t0, t1): scenes.append(dict(id=id, t0=t0, t1=t1)); sfx.append(dict(name='whoosh', t=t0 - .15, gain=.35))
code = {'html': '', 'css': '', 'js': ''}
def setc(t, c, f): ide.append(dict(t=t, op='set', file=f, code=c)); code[f] = c
def typ(t, new, dur, f):
    ide.append(dict(t=t, op='type', file=f, dur=dur, **{'from': code[f], 'to': new}))
    n = len(new) - len(code[f])
    for j in range(max(1, min(abs(n), 60))): sfx.append(dict(name='key', t=round(t + dur * j / max(1, min(abs(n), 60)), 3), gain=.45))
    code[f] = new; return t + dur
def FS(t, f):   # переключить вкладку файла
    ide.append(dict(t=t, op='file', file=f)); ptr.append(dict(t=t, sel=f'#ftabs button:nth-child({["html", "css", "js"].index(f) + 1})')); sfx.append(dict(name='click', t=t, gain=.6))
def click(t, sel, op='click'):
    ptr.append(dict(t=t, sel=sel)); ide.append(dict(t=t, op=op, sel=sel)); sfx.append(dict(name='click', t=t, gain=.6))
def clear(t): ide.append(dict(t=t, op='clear'))
def PV(t, kind, sel, value=None):
    pv.append(dict(t=t, kind=kind, sel=sel, value=value))
    if kind == 'click': sfx.append(dict(name='click', t=t, gain=.6))
def mark(t0, t1, line, c0, c1, text='', color='y', pos='above'):
    marks.append(dict(t0=t0, t1=t1, line=line, c0=c0, c1=c1, text=text, color=color, pos=pos)); sfx.append(dict(name='pop', t=t0, gain=.35))
def MK(t0, t1, f, sub, text='', color='y', pos='above', nth=0):
    lines = code[f].split('\n'); k = 0
    for li, ln in enumerate(lines):
        pos0 = 0
        while True:
            c = ln.find(sub, pos0)
            if c < 0: break
            if k == nth: mark(t0, t1, li, c, c + len(sub), text, color, pos); return
            k += 1; pos0 = c + 1
    raise SystemExit('MK not found: ' + sub + ' in ' + f)
def ring(t0, t1, sel, text='', color='y', pad=6):
    rings.append(dict(t0=t0, t1=t1, sel=sel, text=text, color=color, pad=pad)); sfx.append(dict(name='pop', t=t0, gain=.35))
def chip(t0, t1, h, cls='', style=''):
    chips.append(dict(t0=t0, t1=t1, html=h, cls=cls, style=style)); sfx.append(dict(name='pop', t=t0, gain=.45))
def zoom(t0, t1, x, y, s): zooms.append(dict(t0=t0, t1=t1, x=x, y=y, s=s))

slides = []
def A(kind, t, o=None, ok='fade'):
    s = f'data-a="{kind};{t}"' + (f' data-o="{o}" data-ok="{ok}"' if o is not None else '')
    if kind in ('pop', 'stamp', 'drop'): sfx.append(dict(name={'pop': 'pop', 'stamp': 'thud', 'drop': 'thud'}[kind], t=t + (.35 if kind == 'drop' else 0), gain=.4))
    return s

# ---------- границы сцен (время повествования) ----------
T_HOUSE = N(24.7); T_IDE = N(104.2); T_BOX = N(388.8); T_BOXEND = N(407.6); T_DOM = N(432.4); T_IDE2 = N(466.5)
T_FILES = N(689.6); T_ERR = N(752.9); T_SUM = N(894.8); T_NEXT = N(916.6)

# ---------- 0. Хук ----------
slides.append(f'''<section class="scene" id="s-hook">
<div class="kicker" {A('down', .2)}><b>ДАРСИ 11</b>БАРНОМАСОЗӢ АЗ СИФР</div>
<div class="h1" style="left:60px;top:110px;font-size:100px" {A('stamp', .6)}>ҲАР САЙТ —</div>
<div class="h1 acc" style="left:60px;top:230px;font-size:100px" {A('stamp', 1.4)}>СЕ ЗАБОН</div>
<div style="left:68px;top:430px" {A('left', N(5.4))}><span class="pill"><span class="mono" style="color:var(--kw)">HTML</span> — сохтор</span></div>
<div style="left:68px;top:498px" {A('left', N(6.8))}><span class="pill"><span class="mono" style="color:var(--teal)">CSS</span> — ранг ва намуд</span></div>
<div style="left:68px;top:566px" {A('left', N(8.2))}><span class="pill"><span class="mono" style="color:var(--fn)">JavaScript</span> — ҳаракат</span></div>
<div class="node" style="left:880px;top:140px;width:330px;text-align:left" {A('pop', N(2.5))}><span class="mono" style="font-size:44px;color:var(--purple)">Салом!</span><small>сохтор (HTML)</small></div>
<div class="node" style="left:880px;top:290px;width:330px;border-color:var(--purple)" {A('pop', N(6.0))}><span style="font-size:34px;color:#fff;background:var(--accent);border-radius:12px;padding:6px 18px;color:#1E1E1E">Пахш кун</span><small>ранг (CSS)</small></div>
<div class="node" style="left:880px;top:440px;width:330px" {A('pop', N(8.6))}><span class="mono" style="font-size:44px">⚡ click</span><small>ҳаракат (JS)</small></div>
<div style="left:850px;top:640px" {A('pop', N(21.3))}><span class="pill accent">🎯 Дар охир: корти профил ва санҷиш</span></div>
</section>''')
S('s-hook', 0, T_HOUSE)

# ---------- 1. Хона ва браузер ----------
t_w = N(26.9); t_c = N(37.6); t_e = N(45.6); t_br = N(52.8); t_files = N(59.1); t_rd = N(68.3); t_three = N(72.4); t_work = N(85.2)
slides.append(f'''<section class="scene" id="s-house">
<div class="kicker" {A('down', T_HOUSE)}><b>01</b>ОБРАЗИ ХОНА</div>
<div class="node" style="left:70px;top:190px;width:360px" {A('up', t_w, t_br - .3)}><span class="big">🧱</span>Деворҳо<small><span class="mono">HTML</span> — сохтор</small></div>
<div class="node" style="left:460px;top:190px;width:360px" {A('up', t_c, t_br - .3)}><span class="big">🎨</span>Ранг<small><span class="mono">CSS</span> — намуд</small></div>
<div class="node yes" style="left:850px;top:190px;width:360px" {A('up', t_e, t_br - .3)}><span class="big">💡</span>Барқ<small><span class="mono">JavaScript</span> — ҳаракат</small></div>
<div class="h2" style="left:60px;top:90px;font-size:46px" {A('up', t_br, t_three - .3)}>Браузер ← сервер</div>
<div class="node" style="left:60px;top:200px;width:300px" {A('pop', t_br + .3, t_three - .3)}><span class="big">☁️</span>сервер</div>
<div class="node" style="left:900px;top:200px;width:300px" {A('pop', t_br + .6, t_three - .3)}><span class="big">🖥️</span>браузер</div>
<div class="codechip" style="left:440px;top:190px" {A('left', t_files, t_three - .3)}>index.html <span style="color:var(--muted)">— сохтор</span></div>
<div class="codechip" style="left:440px;top:262px" {A('left', t_files + 3.4, t_three - .3)}>style.css <span style="color:var(--muted)">— намуд</span></div>
<div class="codechip" style="left:440px;top:334px" {A('left', t_files + 6.8, t_three - .3)}>script.js <span style="color:var(--muted)">— рафтор</span></div>
<div style="left:300px;top:470px" {A('stamp', t_rd, t_three - .3)}><span class="pill accent" style="font-size:26px">браузер се файлро якҷоя мехонад</span></div>
<div class="h2" style="left:60px;top:90px;font-size:46px" {A('up', t_three, t_work - .3)}>Се забон — ҳамеша дар як ҷо</div>
<div style="left:60px;top:230px" {A('left', N(75.6), t_work - .3)}><span class="pill err">Бе <span class="mono">HTML</span> саҳифа нест</span></div>
<div style="left:60px;top:310px" {A('left', N(77.9), t_work - .3)}><span class="pill">Бе <span class="mono">CSS</span> — сафед ва оддӣ</span></div>
<div style="left:60px;top:390px" {A('left', N(81.3), t_work - .3)}><span class="pill">Бе <span class="mono">JavaScript</span> — ҳаракат нест</span></div>
<div class="h2" style="left:60px;top:90px;font-size:46px" {A('up', t_work)}>Дар хона ҳам ҳамин тавр</div>
<div class="node" style="left:70px;top:230px;width:360px" {A('up', N(86.9))}><span class="big">👷</span>сохтмончӣ<small>деворҳо</small></div>
<div class="node" style="left:460px;top:230px;width:360px" {A('up', N(88.9))}><span class="big">🧑‍🎨</span>рассом<small>ранг</small></div>
<div class="node" style="left:850px;top:230px;width:360px" {A('up', N(90.9))}><span class="big">🔌</span>барқчӣ<small>чароғ</small></div>
<div style="left:300px;top:470px" {A('pop', N(93.2))}><span class="pill accent" style="font-size:26px">се касб — як хона</span></div>
</section>''')
S('s-house', T_HOUSE, T_IDE)

# ---------- 2. IDE: HTML ----------
S('ide', T_IDE, T_BOX)
setc(T_IDE, '', 'html'); setc(T_IDE, '', 'css'); setc(T_IDE, '', 'js'); clear(T_IDE)
FS(T_IDE + .3, 'html')
chip(T_IDE + .1, T_IDE + 2.2, '<span>💻</span><div>Майдони озмоиш<small>02 · HTML · CSS · JS + натиҷа</small></div>', 'card')
chip(N(106.3), N(106.3) + 3.4, '🔗 yunusovshahriyor.github.io/yunusov.tj/ide', 'side yel', 'top:90px')
ring(N(109.9), N(114.5), '#ftabs', 'се равзана', 'y', 6)
ring(N(115.1), N(118.0), '#pvf', 'натиҷа — фавран', 'c', 4)
tH = N(126.9)
typ(tH, '<h1>', .8, 'html'); MK(tH + .2, N(130.5), 'html', '<h1>', '▶ кушодан', 'c')
typ(N(127.8), '<h1>Салом!', 1.2, 'html')
typ(N(131.8), '<h1>Салом!</h1>', 1.8, 'html'); MK(N(130.7), N(135.5), 'html', '</h1>', '■ пӯшидан', 'g')
ring(N(135.7), N(138.5), '#pvf', 'саҳифа фавран пайдо шуд!', 'g', 4)
MK(N(143.7), N(148.9), 'html', '<h1>Салом!</h1>', '📦 мисли қуттӣ: сарпӯш', 'y', 'below')
chip(N(149.4), N(163.0), '<div>h1 <span style="color:var(--muted)">калонтарин</span> · h2 · h3 · h4 · h5 · h6 <span style="color:var(--muted)">хурдтарин</span><small>h1 — як маротиба · h2 — барои қисмҳо</small></div>', 'card', 'top:420px')
H_P = '<h1>Салом!</h1>\n<p>Ман барномасоз мешавам.</p>'
typ(N(164.6), H_P, 2.6, 'html'); MK(N(165.0), N(168.4), 'html', '<p>', 'сархат', 'c', 'below')
H_B = H_P + '\n<button>Пахш кун</button>'
typ(N(168.7), H_B, 2.3, 'html'); MK(N(169.0), N(173.0), 'html', '<button>', 'тугма', 'c', 'below')
H_L = H_B + '\n<ul>\n  <li>HTML</li>\n  <li>CSS</li>\n  <li>JavaScript</li>\n</ul>'
typ(N(177.0), H_L, 7.0, 'html'); MK(N(177.6), N(182.0), 'html', '<ul>', 'рӯйхат', 'c', 'below'); MK(N(179.5), N(185.5), 'html', '<li>', 'хат', 'g', 'below')
H_A = H_L + '\n<a href="https://yunusovshahriyor.github.io/yunusov.tj/ide/">Мини-IDE</a>'
typ(N(187.0), H_A, 9.0, 'html'); MK(N(190.8), N(193.5), 'html', 'href', 'суроға', 'y')
H_I = H_A + '\n<img src="photo.jpg" alt="Сурат">'
typ(N(202.5), H_I, 7.5, 'html'); MK(N(203.6), N(208.5), 'html', 'src', 'суроғаи сурат', 'c', 'below'); MK(N(206.0), N(209.2), 'html', 'alt', 'матни ивазкунанда', 'g', 'below')
chip(N(209.3), N(213.5), 'img: <b style="color:var(--teal)">ҷуфт надорад</b> — пӯшидан лозим нест', 'side yel', 'top:90px')
chip(N(213.8), N(236.5), '<div><span class="mono">h</span> = heading · <span class="mono">p</span> = paragraph · <span class="mono">a</span> = anchor<small><span class="mono">ul</span> = unordered list · <span class="mono">li</span> = list item · <span class="mono">button</span></small></div>', 'card', 'top:430px')
def doc(body, card=False):
    inner = ('<div class="card">\n' + body + '\n</div>') if card else body
    return '<html>\n<head>\n  <title>Саҳифаи ман</title>\n</head>\n<body>\n' + inner + '\n</body>\n</html>'
HD0 = '<html>\n<head>\n  <title>Саҳифаи ман</title>\n</head>\n<body>\n' + H_I
typ(N(239.2), HD0, 6.0, 'html')
typ(N(246.0), doc(H_I), 2.0, 'html')
MK(N(241.5), N(246.5), 'html', '<head>', 'маълумоти саҳифа', 'c', 'below'); MK(N(246.8), N(251.8), 'html', '<body>', 'он чизе, ки мебинем', 'g', 'below')
chip(N(262.4), N(284.0), '<span>📄</span><div>index.html<small>Блокнот → «.html» → ду маротиба пахш → браузер</small></div>', 'card')

# ---------- 3. CSS ----------
FS(N(286.5), 'css'); chip(N(284.9), N(286.8), '<span>🎨</span><div>CSS: ранг ва намуд<small>03 · интихобкунанда · хусусият · қимат</small></div>', 'card')
tC = N(294.8)
typ(tC, 'h1 ', .4, 'css'); MK(N(294.6), N(298.0), 'css', 'h1', 'интихобкунанда', 'c')
typ(N(298.1), 'h1 {\n\n}', .8, 'css')
typ(N(300.0), 'h1 {\n  color\n}', 1.3, 'css'); MK(N(300.2), N(303.7), 'css', 'color', 'хусусият', 'y', 'below')
typ(N(303.8), 'h1 {\n  color:\n}', .4, 'css')
typ(N(305.5), 'h1 {\n  color: purple\n}', 1.0, 'css'); MK(N(305.6), N(307.7), 'css', 'purple', 'қимат', 'g', 'below')
typ(N(307.8), 'h1 {\n  color: purple;\n}', .3, 'css')
ring(N(308.9), N(311.5), '#pvf', 'сарлавҳа бунафш шуд!', 'g', 4)
C_P = 'h1 {\n  color: purple;\n}\n\np {\n  font-size: 20px;\n}'
typ(N(322.0), C_P, 3.5, 'css'); MK(N(322.4), N(326.0), 'css', 'font-size', 'андозаи ҳарф', 'c', 'below')
C_B = C_P + '\n\nbutton {\n  background: #BD93F9;\n  color: #1E1E1E;\n  border-radius: 8px;\n  padding: 10px 20px;\n}'
typ(N(326.4), C_B, 9.0, 'css')
MK(N(327.5), N(330.5), 'css', 'background', 'замина', 'y', 'below'); MK(N(331.0), N(333.0), 'css', 'border-radius', 'гирдкунӣ', 'c', 'below'); MK(N(333.6), N(336.5), 'css', 'padding', 'фосила дар дохил', 'g', 'below')
ring(N(336.0), N(338.0), '#pvf', 'тугма зебо шуд', 'g', 4)
CC1 = C_B.replace('purple', 'red')
typ(N(340.8), CC1, .7, 'css'); MK(N(341.6), N(343.5), 'css', 'red', 'ном', 'y')
CC2 = CC1.replace('color: red', 'color: #BD93F9', 1)
typ(N(343.8), CC2, 1.6, 'css'); MK(N(345.5), N(346.4), 'css', '#BD93F9', 'рамз', 'c')
CC3 = CC1.replace('color: red', 'color: rgb(189, 147, 249)', 1)
typ(N(346.5), CC3, 2.2, 'css'); MK(N(348.8), N(350.9), 'css', 'rgb(189, 147, 249)', 'се рақам', 'g')
typ(N(351.0), CC2, 1.2, 'css')
chip(N(354.0), N(358.4), '<div>20<span style="color:var(--muted)">px</span> · 16<span style="color:var(--muted)">px</span><small>андоза бо пиксел</small></div>', 'side yel', 'top:90px')
C_H = CC2 + '\n\nbutton:hover {\n  background: #FF79C6;\n}'
typ(N(359.0), C_H, 4.5, 'css'); MK(N(361.9), N(365.0), 'css', ':hover', 'мушро овардан', 'y', 'below')
PV(N(366.0), 'hover', 'button')
ring(N(366.4), N(371.5), '#pvf', 'муш болои тугма — ранг иваз шуд', 'g', 4)
PV(N(371.5), 'unhover', 'button')
# класс: HTML + CSS
FS(N(378.0), 'html')
HD1 = doc(H_I, True)
typ(N(380.0), HD1.replace('</div>', ''), 2.4, 'html'); MK(N(380.3), N(383.0), 'html', 'class="card"', 'класс', 'c', 'below')
typ(N(383.0), HD1, 1.0, 'html')
FS(N(383.4), 'css')
C_CL = C_H + '\n\n.card {\n}'
typ(N(384.6), C_CL, 1.2, 'css'); MK(N(384.7), N(388.5), 'css', '.card', 'нуқта = класс', 'c', 'below')
# --- слайд «қуттӣ» (модели коробки) ---
slides.append(f'''<section class="scene" id="s-box">
<div class="kicker" {A('down', T_BOX + .1)}><b>03</b>ҲАР ЭЛЕМЕНТ — ҚУТТӢ</div>
<div class="h2" style="left:600px;top:60px;font-size:40px" {A('up', T_BOX + .6)}>📦 ҳамон қуттии картонӣ аз дарси 1</div>
<div style="left:240px;top:140px;width:800px;height:500px;border:3px dashed var(--muted);border-radius:22px;background:rgba(139,148,158,.06)" {A('pop', N(404.4) - 1.5)}></div>
<div style="left:300px;top:200px;width:680px;height:380px;border:6px solid var(--purple);border-radius:18px;background:var(--panel)" {A('pop', N(402.0) - 1.5)}></div>
<div style="left:360px;top:260px;width:560px;height:260px;border:2px dashed #E2B070;border-radius:12px;background:rgba(226,176,112,.12)" {A('pop', N(397.8) - 1.5)}></div>
<div class="node" style="left:470px;top:340px;width:340px" {A('pop', N(396.1) - .5)}>матн<small>дохил (content)</small></div>
<div style="left:20px;top:150px" {A('pop', N(404.4) - .3)}><span class="pill">margin<br><span style="font-size:16px;font-weight:600;color:var(--muted)">масофа аз дигарон</span></span></div>
<div style="left:20px;top:290px" {A('pop', N(402.0) - .3)}><span class="pill" style="border-color:var(--purple)">border<br><span style="font-size:16px;font-weight:600;color:var(--muted)">худи девор</span></span></div>
<div style="left:20px;top:430px" {A('pop', N(397.8) - .3)}><span class="pill" style="border-color:#E2B070">padding<br><span style="font-size:16px;font-weight:600;color:var(--muted)">фосила дар дохил</span></span></div>
</section>''')
S('s-box', T_BOX, T_BOXEND)
S('ide', T_BOXEND, T_DOM)
C_CARD = C_H + '\n\n.card {\n  padding: 20px;\n  margin: 20px;\n  border: 2px solid #BD93F9;\n  border-radius: 16px;\n}'
typ(N(408.5), C_CARD, 7.0, 'css')
MK(N(409.0), N(411.0), 'css', 'padding: 20px', 'padding', 'y', 'below')
ring(N(416.0), N(421.5), '#pvf', 'корт пайдо шуд', 'g', 4)

# ---------- 4. JavaScript ----------
slides.append(f'''<section class="scene" id="s-dom">
<div class="kicker" {A('down', T_DOM + .1)}><b>04</b>DOM — ДАРАХТИ САҲИФА</div>
<div class="h2" style="left:60px;top:90px;font-size:44px" {A('up', T_DOM + .5, N(441.0))}>Браузер саҳифаро чӣ тавр мебинад?</div>
<div style="left:60px;top:190px" {A('left', N(438.2), N(441.0))}><span class="pill accent">HTML → дарахт</span></div>
<div class="node" style="left:520px;top:110px;width:240px" {A('pop', N(441.4))}><span class="mono">html</span><small>реша</small></div>
<div class="node" style="left:300px;top:260px;width:200px" {A('pop', N(443.5))}><span class="mono">head</span></div>
<div class="node" style="left:780px;top:260px;width:200px" {A('pop', N(444.6))}><span class="mono">body</span></div>
<svg style="left:0;top:0;width:1280px;height:720px" viewBox="0 0 1280 720" fill="none" stroke="#3C3C3C" stroke-width="3" stroke-linecap="round">
 <path d="M600 215 L420 262" {A('fade', N(443.5))}/><path d="M680 215 L880 262" {A('fade', N(444.6))}/>
 <path d="M850 345 L650 430" {A('fade', N(446.4))}/><path d="M880 345 L880 430" {A('fade', N(447.0))}/><path d="M910 345 L1110 430" {A('fade', N(447.8))}/></svg>
<div class="node" style="left:540px;top:430px;width:200px" {A('pop', N(446.4))}><span class="mono">h1</span></div>
<div class="node" style="left:780px;top:430px;width:200px" {A('pop', N(447.0))}><span class="mono">p</span></div>
<div class="node" style="left:1010px;top:430px;width:200px" {A('pop', N(447.8))}><span class="mono">button</span></div>
<div style="left:60px;top:150px" {A('pop', N(452.4))}><span class="pill accent" style="font-size:26px">DOM = дарахт</span></div>
<div style="left:60px;top:560px" {A('up', N(454.3))}><span class="pill ok">⚡ JavaScript элементро меёбад ва иваз мекунад</span></div>
<div style="left:60px;top:630px" {A('up', N(462.4))}><span class="pill"><span class="mono" style="color:var(--fn)">document</span> — ҳамаи саҳифа</span></div>
</section>''')
S('s-dom', T_DOM, T_IDE2)
S('ide', T_IDE2, T_FILES)
FS(N(467.9), 'js'); chip(N(466.5), N(468.4), '<span>⚡</span><div>JavaScript: ҳаракат<small>04 · function + DOM</small></div>', 'card')
typ(N(471.9), 'function greet() {\n}', 1.2, 'js')
J_G = 'function greet() {\n  document.querySelector("h1").textContent = "Салом, Нигина!";\n}'
typ(N(474.2), J_G, 10.0, 'js')
MK(N(474.9), N(478.5), 'js', 'document.querySelector("h1")', 'саҳифа, сарлавҳаро ёб', 'c', 'below'); MK(N(481.3), N(486.5), 'js', 'textContent', 'матнро иваз кун', 'g', 'below')
FS(N(486.8), 'html')
HD2 = HD1.replace('<button>Пахш кун</button>', '<button onclick="greet()">Пахш кун</button>')
typ(N(488.6), HD2, 2.6, 'html'); MK(N(488.7), N(494.5), 'html', 'onclick="greet()"', 'пахш кунанд → greet', 'y', 'below')
PV(N(495.2), 'click', 'button')
ring(N(495.3), N(499.0), '#pvf', 'сарлавҳа иваз шуд!', 'g', 4)
H_IN = '<input id="name" placeholder="Номи шумо">\n<button onclick="hello()">Салом</button>\n<p id="out"></p>'
HD3 = HD2.replace('<button onclick="greet()">Пахш кун</button>', '<button onclick="greet()">Пахш кун</button>\n' + H_IN)
typ(N(503.8), HD3, 7.5, 'html'); MK(N(504.0), N(507.4), 'html', '<input', 'майдони ном', 'c', 'below')
FS(N(511.4), 'js')
J_H = J_G + '\n\nfunction hello() {\n  let name = document.getElementById("name").value;\n  document.getElementById("out").textContent = "Салом, " + name + "!";\n}'
typ(N(511.5), J_G + '\n\nfunction hello() {\n}', 1.0, 'js')
typ(N(512.8), J_G + '\n\nfunction hello() {\n  let name = document.getElementById("name").value;\n}', 7.5, 'js')
MK(N(518.0), N(523.5), 'js', 'value', 'навиштаи корбар', 'y', 'below'); MK(N(521.5), N(524.0), 'js', 'let name', '📦 қуттӣ (дарси 1)', 'c')
typ(N(525.0), J_H, 3.8, 'js'); MK(N(529.0), N(532.2), 'js', '"Салом, " + name + "!"', 'матн + матн (дарси 1)', 'g', 'below')
PV(N(532.4), 'fill', '#name', 'Фарҳод')
PV(N(534.1), 'click', 'button[onclick="hello()"]')
ring(N(535.3), N(538.4), '#pvf', 'саҳифа ҷавоб медиҳад!', 'g', 4)
FS(N(538.3), 'html')
HD4 = HD3.replace('<p id="out"></p>', '<p id="out"></p>\n<button onclick="toggle()">Торик</button>')
typ(N(538.5), HD4, 1.6, 'html')
FS(N(540.2), 'css')
C_D = C_CARD + '\n\nbody.dark {\n  background: #1E1E1E;\n  color: #fff;\n}'
typ(N(540.4), C_D, 5.4, 'css'); MK(N(541.7), N(545.5), 'css', 'body.dark', 'класс «dark»', 'c', 'below')
FS(N(546.1), 'js')
J_T = J_H + '\n\nfunction toggle() {\n  document.body.classList.toggle("dark");\n}'
typ(N(547.4), J_T, 6.6, 'js'); MK(N(548.9), N(553.8), 'js', 'classList.toggle("dark")', 'ҳолатро иваз кун', 'g', 'below')
PV(N(554.4), 'click', 'button[onclick="toggle()"]'); ring(N(554.5), N(556.7), '#pvf', 'саҳифа торик', 'g', 4)
PV(N(556.9), 'click', 'button[onclick="toggle()"]'); ring(N(557.0), N(560.0), '#pvf', 'боз — равшан', 'c', 4)
FS(N(571.8), 'html')
H_N = '<h2 id="num">0</h2>\n<button onclick="add()">+1</button>'
HD5 = HD4.replace('<button onclick="toggle()">Торик</button>', '<button onclick="toggle()">Торик</button>\n' + H_N)
typ(N(572.0), HD5, 5.8, 'html')
FS(N(578.3), 'js')
J_C = 'let count = 0;\n\n' + J_T
typ(N(579.7), J_C, 2.6, 'js'); MK(N(580.2), N(583.8), 'js', 'let count = 0;', '📦 ҳамон қуттӣ', 'c')
J_A = J_C + '\n\nfunction add() {\n  count = count + 1;\n  document.getElementById("num").textContent = count;\n}'
typ(N(583.9), J_A, 12.0, 'js')
PV(N(598.3), 'click', 'button[onclick="add()"]'); PV(N(600.0), 'click', 'button[onclick="add()"]'); PV(N(600.8), 'click', 'button[onclick="add()"]')
ring(N(598.5), N(608.0), '#pvf', 'рақам ҳар бор калон мешавад', 'g', 4)
chip(N(608.2), N(617.0), '<div>тағйирёбанда <span style="color:var(--muted)">(дарси 1)</span> + функсия <span style="color:var(--muted)">(дарси 5)</span> + саҳифа</div>', 'card', 'top:560px')
J_L = J_A.replace('count = count + 1;', 'count = count + 1;\n  console.log(count);')
typ(N(622.4), J_L, 2.4, 'js')
PV(N(627.5), 'click', 'button[onclick="add()"]')
ring(N(628.0), N(634.5), '#out', 'console.log — дар сайт', 'c', 4)
chip(N(626.9), N(637.5), '<span class="big">F12</span><div>Консол<small>абзорҳои барномасоз</small></div>', 'card', 'top:250px')

# ---------- 5. Лоиҳа ----------
chip(N(638.1), N(641.5), '<span>🪪</span><div>Лоиҳа: корти профил<small>05 · ҳамааш якҷоя</small></div>', 'card')
FS(N(642.2), 'html'); MK(N(642.6), N(645.3), 'html', '<div class="card">', 'корт', 'c', 'below'); MK(N(645.6), N(654.5), 'html', '<ul>', 'малакаҳо', 'g', 'below'); MK(N(657.0), N(660.8), 'html', '<input', 'input + «Салом»', 'y', 'below'); MK(N(661.0), N(662.6), 'html', '<button onclick="toggle()">', '«Торик»', 'c', 'below')
FS(N(662.6), 'css')
C_P2 = C_D.replace('.card {\n  padding: 20px;', '.card {\n  background: #252526;\n  color: #fff;\n  padding: 20px;')
typ(N(663.8), C_P2, 4.5, 'css'); MK(N(664.0), N(668.5), 'css', 'background: #252526;', 'корт торик', 'y', 'below')
ring(N(668.5), N(672.5), '#pvf', 'корт торик шуд', 'g', 4)
FS(N(674.3), 'js'); MK(N(675.6), N(679.0), 'js', 'function hello()', 'ду функсия', 'c', 'below'); MK(N(676.5), N(679.5), 'js', 'function toggle()', '', 'g', 'below')
PV(N(682.0), 'fill', '#name', 'Нигина'); PV(N(683.2), 'click', 'button[onclick="hello()"]')
ring(N(679.8), N(688.5), '#pvf', 'корт кор мекунад!', 'g', 4)
# файлы
slides.append(f'''<section class="scene" id="s-files">
<div class="kicker" {A('down', T_FILES + .1)}><b>05</b>СЕ ФАЙЛ</div>
<div class="card3" style="left:60px;top:130px;width:370px;height:420px" {A('up', N(695.2))}><div class="t mono" style="font-size:24px">index.html</div><div class="u">сохтор</div>
 <div class="codechip" style="font-size:16px;line-height:1.5;white-space:pre-wrap"><span class="k">&lt;head&gt;</span>\n  <span class="k">&lt;link</span> rel=<span class="s">"stylesheet"</span>\n        href=<span class="s">"style.css"</span><span class="k">&gt;</span>\n<span class="k">&lt;/head&gt;</span>\n<span class="k">&lt;body&gt;</span> … \n  <span class="k">&lt;script</span> src=<span class="s">"script.js"</span><span class="k">&gt;&lt;/script&gt;</span>\n<span class="k">&lt;/body&gt;</span></div></div>
<div class="card3" style="left:455px;top:130px;width:370px;height:420px" {A('up', N(699.0))}><div class="t mono" style="font-size:24px">style.css</div><div class="u">намуд</div>
 <div class="codechip" style="font-size:16px;line-height:1.5;white-space:pre-wrap"><span class="f">h1</span> {{\n  <span class="k">color</span>: <span class="s">#BD93F9</span>;\n}}\n\n<span class="f">.card</span> {{\n  <span class="k">padding</span>: <span class="n">20px</span>;\n}}</div></div>
<div class="card3" style="left:850px;top:130px;width:370px;height:420px" {A('up', N(702.5))}><div class="t mono" style="font-size:24px">script.js</div><div class="u">рафтор</div>
 <div class="codechip" style="font-size:16px;line-height:1.5;white-space:pre-wrap"><span class="k">function</span> <span class="f">toggle</span>() {{\n  document.body\n    .classList.toggle(<span class="s">"dark"</span>);\n}}</div></div>
<div style="left:60px;top:590px" {A('stamp', N(728.0))}><span class="pill accent" style="font-size:26px">ҳамон се файл: сервер → браузер</span></div>
<div style="left:700px;top:590px" {A('pop', N(733.8))}><span class="pill">📨 дӯстатон ҳам онро мекушояд</span></div>
</section>''')
S('s-files', T_FILES, T_ERR)

# ---------- 6. Хатогиҳо ----------
S('ide', T_ERR, T_SUM)
chip(T_ERR + .1, T_ERR + 2.4, '<span>🐞</span><div>Се хатои маъмул<small>06 · ҳама хато мекунанд — ин муқаррарӣ аст</small></div>', 'card')
E_H = '<h1>Салом!</h1>\n<p>Ман барномасоз мешавам.</p>'
E_C = 'h1 {\n  color: #BD93F9;\n}'
setc(T_ERR + 1.2, E_H, 'html'); setc(T_ERR + 1.2, E_C, 'css'); setc(T_ERR + 1.2, '', 'js')
FS(T_ERR + 1.4, 'html')
chip(N(754.7), N(757.0), 'Хатои 1 / 3', 'side red', 'top:70px;left:1090px')
E1 = '<h1>Салом!\n<p>Ман барномасоз мешавам.</p>'
typ(N(755.6), E1, 1.4, 'html')
ring(N(758.5), N(764.0), '#pvf', 'матн ба сарлавҳа даромад', 'r', 4)
typ(N(764.2), E_H, 1.2, 'html'); MK(N(765.0), N(766.0), 'html', '</h1>', 'мепӯшем', 'g')
chip(N(766.0), N(768.5), 'Хатои 2 / 3', 'side red', 'top:70px;left:1090px')
FS(N(766.4), 'css')
E2 = 'h1 {\n  color #BD93F9;\n}'
typ(N(766.9), E2, 1.6, 'css'); MK(N(768.5), N(776.0), 'css', 'color #BD93F9', 'ду нуқта нест!', 'r', 'below')
ring(N(770.5), N(776.0), '#pvf', 'ранг кор намекунад', 'r', 4)
typ(N(776.2), E_C, 1.0, 'css')
chip(N(779.8), N(782.6), 'Хатои 3 / 3', 'side red', 'top:70px;left:1090px')
FS(N(780.0), 'js')
E3 = 'document.querySelector("h2").textContent = "x";'
typ(N(780.7), E3, 3.0, 'js'); MK(N(783.0), N(786.5), 'js', '"h2"', 'h2 дар саҳифа нест', 'r', 'below')
ring(N(786.0), N(793.5), '#out', 'null: элемент ёфт нашуд', 'r', 4)
chip(N(793.9), N(809.0), '<span class="big">F12</span><div>Console — хатои сурхро бихонед<small>абзорҳои барномасоз дар браузер</small></div>', 'card', 'top:260px')

# ---------- 7. Вазифаҳо ----------
t_tab = N(833.4); t_t1 = N(838.3); t_t2 = N(845.6); t_t3 = N(851.5); t_chk = N(856.9); t_q = N(863.9)
chip(N(830.9), N(833.2), '<span>🎯</span><div>Вазифаҳо барои шумо<small>07 · ҷадвали «11 · HTML, CSS, JS»</small></div>', 'card')
click(t_tab + .8, '#tabs .tab:nth-child(3)')
ST_H1 = '<!-- сарлавҳа ва сархат -->\n'
setc(t_tab + .85, ST_H1, 'html'); setc(t_tab + .85, '', 'css'); setc(t_tab + .85, '', 'js')
FS(t_tab + 1.0, 'html')
ring(N(836.9), t_t1 - .1, '#side', '📘 назария', 'c', 4)
ring(t_t1, t_t2 - .1, '#task', 'Вазифаи 1', 'y', 4)
typ(N(839.3), '<h1>Нигина</h1>\n<p>Ман барномасоз мешавам.</p>\n', 5.2, 'html')
click(t_t2 + .3, '#side button[data-i="1"]')
ST_H2 = '<h1>Нигина</h1>\n<p>Ман барномасоз мешавам.</p>\n<button>Пахш кун</button>\n'
setc(t_t2 + .32, ST_H2, 'html'); setc(t_t2 + .32, '/* h1 { ... } button { ... } */\n', 'css'); setc(t_t2 + .32, '', 'js')
FS(t_t2 + .5, 'css')
ring(t_t2 + .8, t_t3 - .1, '#task', 'Вазифаи 2', 'y', 4)
typ(N(846.8), 'h1 {\n  color: red;\n}\n\nbutton {\n  background: #BD93F9;\n}\n', 4.4, 'css')
click(t_t3 + .3, '#side button[data-i="2"]')
ST_H3 = '<h1>Нигина</h1>\n<button onclick="greet()">Пахш кун</button>\n'
setc(t_t3 + .32, ST_H3, 'html'); setc(t_t3 + .32, '', 'css'); setc(t_t3 + .32, 'function greet() {\n  // матни h1-ро иваз кунед\n}\n', 'js')
FS(t_t3 + .5, 'js')
ring(t_t3 + .8, t_chk - .1, '#task', 'Вазифаи 3', 'y', 4)
typ(N(852.6), 'function greet() {\n  document.querySelector("h1").textContent = "Салом, Нигина!";\n}\n', 3.8, 'js')
ring(t_chk - .3, t_chk + .9, '#check', '✓ Санҷиш', 'c', 6)
click(t_chk + .5, '#check', 'check'); sfx.append(dict(name='chime', t=t_chk + 1.4, gain=.6))
ring(t_chk + 1.6, t_q - .3, '#checks', '', 'g', 4)
# санҷиш (квиз)
g0 = V(GAP_Q) - PAUSE
q_what = N(874.8)
qbody = lambda sub: f'<div>Кадоме <b style="color:var(--kw)">HTML</b>, <b style="color:var(--teal)">CSS</b>, <b style="color:var(--fn)">JS</b>?<small>{sub}</small></div>'
chip(N(865.5), g0 - .3, '<span class="big">❓</span>' + qbody('сарлавҳа · ранги сабз · пахши тугма — видеоро пауза кунед ✍️'), 'card')
for k in range(5):
    chip(g0 + k + .02, g0 + k + .62, f'<span class="big">{5 - k}</span>' + qbody('фикр кунед · баъд ҷавобро мебинем ✅'), 'card')
    sfx.append(dict(name='tick', t=g0 + k, gain=.8))
a1 = N(883.7); a2 = N(886.8); a3 = N(889.0)
chip(a1, N(894.5), '<span style="font-size:44px">🏷️</span><div>сарлавҳа → <b style="color:var(--kw)">HTML</b></div>', 'card', 'top:190px')
chip(a2, N(894.5), '<span style="font-size:44px">🎨</span><div>ранги сабз → <b style="color:var(--teal)">CSS</b></div>', 'card', 'top:360px')
chip(a3, N(894.5), '<span style="font-size:44px">⚡</span><div>пахши тугма → <b style="color:var(--fn)">JavaScript</b></div>', 'card', 'top:530px')

# ---------- 8. Хулоса ----------
slides.append(f'''<section class="scene" id="s-sum">
<div class="kicker" {A('down', T_SUM + .2)}><b>08</b>ХУЛОСА</div>
<div class="h2" style="left:60px;top:90px;font-size:50px" {A('up', N(896.3))}><span class="mono" style="color:var(--kw)">HTML</span> · <span class="mono" style="color:var(--teal)">CSS</span> · <span class="mono" style="color:var(--fn)">JS</span></div>
<div class="card3" style="left:60px;top:220px;width:360px;height:260px" {A('up', N(896.6))}><div class="emo">🧱</div><div class="t">HTML = девор</div><div class="u">сохтори саҳифа</div></div>
<div class="card3" style="left:460px;top:220px;width:360px;height:260px" {A('up', N(900.3))}><div class="emo">🎨</div><div class="t">CSS = ранг</div><div class="u">намуд · ҳар элемент — қуттӣ</div></div>
<div class="card3" style="left:860px;top:220px;width:360px;height:260px" {A('up', N(905.5))}><div class="emo">⚡</div><div class="t">JS = барқ</div><div class="u">ҳаракат</div></div>
<div style="left:60px;top:520px" {A('up', N(908.8))}><span class="pill ok">се забон — як саҳифа 🏠</span></div>
<div style="left:60px;top:590px" {A('up', N(912.5))}><span class="pill accent">📘 Шпаргалкаи бепул (PDF) — дар тавсифи видео</span></div>
</section>''')
S('s-sum', T_SUM, T_NEXT)
x_sub = N(925.1)
slides.append(f'''<section class="scene" id="s-next">
<div class="kicker" {A('down', T_NEXT + .1)}><b>ДАРСИ 12</b>НАВБАТӢ</div>
<div class="h1" style="left:60px;top:130px;font-size:150px" {A('stamp', T_NEXT + .3)}>AI</div>
<div class="mono acc" style="left:66px;top:310px;font-size:50px;font-weight:800" {A('up', T_NEXT + .8)}>барои барномасоз</div>
<div class="sub" style="left:68px;top:390px" {A('up', N(920.3))}>бо ёрии AI код менависем ва онро месанҷем</div>
<div class="codechip" style="left:68px;top:470px;font-size:26px" {A('up', N(921.5))}><span class="c">// савол</span> → <span class="s">"Тугмаи «Торик» бисоз"</span> → код</div>
<div style="left:820px;top:170px" {A('pop', x_sub)}><span class="pill accent" style="font-size:34px;padding:20px 40px">🔔 Обуна шавед</span></div>
<div style="left:820px;top:270px" {A('pop', x_sub + .5)}><span class="pill" style="font-size:26px;padding:16px 30px">@shahriyor_yunusov</span></div>
</section>''')
S('s-next', T_NEXT, END + 1)

chapters = [dict(t=0, title='Хук'), dict(t=T_HOUSE, title='Образи хона ва браузер'), dict(t=T_IDE, title='HTML: сохтор'), dict(t=N(284.9), title='CSS: ранг, намуд ва «қуттӣ»'),
            dict(t=N(432.4), title='JavaScript: ҳаракат'), dict(t=N(638.1), title='Лоиҳа: корти профил'), dict(t=T_ERR, title='Хатогиҳои маъмул ва F12'), dict(t=N(830.9), title='Вазифаҳо ва санҷиш'), dict(t=T_SUM, title='Хулоса')]
ide.sort(key=lambda o: o['t']); ptr.sort(key=lambda o: o['t']); pv.sort(key=lambda o: o['t'])

MAP = [(r'ай-ди-и', 'IDE'), (r'мини-ай-ди-и', 'Мини-IDE'), (r'эйч-ти-эм-эл', 'HTML'), (r'си-эс-эс', 'CSS'), (r'джаваскрипт', 'JavaScript'), (r'эйч-ван', 'h1'), (r'эйч-ту', 'h2'),
       (r'эйч-три', 'h3'), (r'эйч-сикс', 'h6'), (r'кверӣ-селектор', 'querySelector'), (r'гет-элемент-бай-ай-ди', 'getElementById'), (r'текст-контент', 'textContent'), (r'класс-лист', 'classList'),
       (r'эф-дувоздаҳ', 'F12'), (r'эйч-реф', 'href'), (r'эс-эр-си', 'src'), (r'бордер-рейдиус', 'border-radius'), (r'фонт-сайз', 'font-size'), (r'бэкграунд', 'background'), (r'паддинг', 'padding'),
       (r'маржин', 'margin'), (r'бордер', 'border'), (r'хавер', 'hover'), (r'онклик', 'onclick'), (r'докюмент', 'document'), (r'консол', 'console'), (r'фанкшн', 'function'), (r'грит-ро', 'greet-ро'),
       (r'грит', 'greet'), (r'хэлло', 'hello'), (r'тоггл', 'toggle'), (r'каунт', 'count'), (r'эдд', 'add'), (r'нейм', 'name'), (r'вэлью', 'value'), (r'лет', 'let'), (r'калар', 'color'),
       (r'эй-ай', 'AI'), (r'ю-эл', 'ul'), (r'эл-ай', 'li'), (r'баттон', 'button'), (r'инпут', 'input'), (r'бодӣ', 'body'), (r'хед', 'head'), (r'дом', 'DOM'), (r'дарк', 'dark'), (r'див', 'div'),
       (r'класс', 'class'), (r'кард', 'card'), (r'линк', 'link'), (r'скрипт', 'script'), (r'стайлшит', 'stylesheet'), (r'рел', 'rel'), (r'ред', 'red'), (r'грин', 'green'), (r'алт', 'alt'),
       (r'имэйдж', 'img'), (r'тайтл', 'title'), (r'ар-джи-би', 'rgb'), (r'аут', 'out'), (r'нам', 'num'), (r'нал', 'null'), (r'Инстаграм', 'Instagram')]
def disp(s):
    for a, b in MAP: s = re.sub(r'(?<![\w])' + a + r'(?![\w])', b, s, flags=re.I)
    return s
caps = []; cur = []
def flush():
    if cur: caps.append(dict(t0=V(cur[0]['t0']), t1=V(cur[-1]['t1']), text=disp(' '.join(w['w'] for w in cur)))); cur.clear()
for w in W:
    cur.append(w)
    if w['w'][-1] in '.!?:' or len(cur) >= 9 or len(' '.join(x['w'] for x in cur)) > 62: flush()
flush()
for a, b in zip(caps, caps[1:]): a['t1'] = min(a['t1'] + .3, b['t0'])

TL = dict(end=END, scenes=scenes, ide=ide, marks=marks, rings=rings, ptr=ptr, chips=chips, zooms=zooms, caps=[], chapters=chapters, cd=[g0], pv=pv)

src = open('../../../../public/ide/index.html', encoding='utf8').read()
PTR = '<svg id="ptr" viewBox="0 0 24 24"><path d="M3 2l7.5 19 2.6-7.6L21 11z" fill="#fff" stroke="#111" stroke-width="1.4" stroke-linejoin="round"/></svg>'
inject_head = '<style>' + open('video.css', encoding='utf8').read() + '</style>'
inject_body = '<div id="ovl">' + PTR + '<div id="rip"></div></div>' + ''.join(slides)
src = src.replace('</head>', inject_head + '</head>', 1)
src = src.replace('<div class="app">', inject_body + '<div id="stagewrap"><div class="app">', 1)
src = src.replace('\n<script src="lessons/js.js"></script>\n<script src="lessons/web.js"></script>', '\n</div>\n<script src="file://' + __import__('os').path.abspath('../../../../public/ide/lessons/js.js') + '"></script>\n<script src="file://' + __import__('os').path.abspath('../../../../public/ide/lessons/web.js') + '"></script>', 1)
assert 'window.__ide = { lessons: LESSONS,' in src
src = src.replace('window.__ide = { lessons: LESSONS,', 'window.__ide = { cur: function () { return curFile; }, setFile: function (f) { saveFile(); curFile = f; ta.value = files[f]; ta.scrollTop = 0; paint(); drawFileTabs(); drawSyms(); }, setFileCode: function (f, c) { files[f] = c; if (f === curFile) { ta.value = c; paint(); } }, renderPreview: renderPreview, lessons: LESSONS,', 1)
src = src.replace('function confetti() {', 'function confetti() { return;')
i_end = src.rindex('</body>'); src = src[:i_end] + '<script>window.TL=' + json.dumps(TL, ensure_ascii=False) + ';</script><script>' + open('video.js', encoding='utf8').read() + '</script>' + src[i_end:]
open('video.html', 'w', encoding='utf8').write(src)

sfx = [s for s in sfx if 0 <= s['t'] < END]
json.dump(dict(end=END, sfx=sorted(sfx, key=lambda s: s['t'])), open('sfx.json', 'w'), indent=0)
json.dump(dict(gaps=GAPS, end=END), open('gaps.json', 'w'))
def ts(t): h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60; return f'{h:02}:{m:02}:{int(s):02},{int(round((s % 1) * 1000)) % 1000:03}'
with open('../youtube-lesson-11.srt', 'w', encoding='utf8') as f:
    for k, c in enumerate(caps, 1): f.write(f"{k}\n{ts(c['t0'])} --> {ts(c['t1'])}\n{c['text']}\n\n")
with open('chapters.txt', 'w', encoding='utf8') as f:
    for c in chapters: f.write(f"{int(c['t'] // 60)}:{int(c['t'] % 60):02} {c['title']}\n")
print('END', END, 'scenes', len(scenes), 'ide ops', len(ide), 'pv', len(pv), 'sfx', len(sfx))
print(open('chapters.txt').read())
