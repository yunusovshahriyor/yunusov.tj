# Собирает video.html (IDE + слайды + таймлайн), sfx.json, .srt (для YouTube; в видео субтитров НЕТ) и главы для YouTube-урока 13 «Зеҳни сунъӣ барои барномасоз»
import json, re, html, os
WJ = json.load(open('words.json')); W = WJ['words']; NARR_END = WJ['total']
toks = [re.sub(r'[^\w-]', '', w['w']).lower() for w in W]

def find(phrase, after=0):
    seq = [re.sub(r'[^\w-]', '', x).lower() for x in phrase.split()]
    for i in range(after, len(W) - len(seq) + 1):
        if toks[i:i + len(seq)] == seq: return i
    raise SystemExit('not found: ' + phrase)

GAPS = []
def V(nt): return nt + sum(d for g, d in GAPS if g <= nt)
def N(nt): return round(V(nt), 3)
def I(phrase, after=0): return find(phrase, after)
PAUSE = 5.0
GAP_Q = W[I('фикр кунед.', I('Ва санҷиши нав')) + 1]['t1'] + 0.05; GAPS.append((GAP_Q, PAUSE))
END = round(V(NARR_END) + 0.8, 2)

scenes, ide, marks, rings, ptr, chips, zooms, sfx = [], [], [], [], [], [], [], []
def S(id, t0, t1): scenes.append(dict(id=id, t0=t0, t1=t1)); sfx.append(dict(name='whoosh', t=t0 - .15, gain=.35))
code = ['']
def setc(t, c): ide.append(dict(t=t, op='set', code=c)); code[0] = c
def typ(t, new, dur=None):
    dur = dur or max(.6, min(4.5, .075 * abs(len(new) - len(code[0])) + .25))
    ide.append(dict(t=t, op='type', dur=dur, **{'from': code[0], 'to': new}))
    n = len(new) - len(code[0])
    for j in range(max(1, min(abs(n), 60))): sfx.append(dict(name='key', t=round(t + dur * j / max(1, min(abs(n), 60)), 3), gain=.45))
    code[0] = new; return t + dur
def run(t, kind='ok', wait=None):
    ptr.append(dict(t=t, sel='#run')); o = dict(t=t, op='run', sel='#run')
    if wait: o['wait'] = wait
    ide.append(o)
    sfx.append(dict(name='click', t=t, gain=.6)); sfx.append(dict(name='ding' if kind == 'ok' else 'buzz', t=t + .25, gain=.5 if kind == 'ok' else .35))
def click(t, sel, op='click'):
    ptr.append(dict(t=t, sel=sel)); ide.append(dict(t=t, op=op, sel=sel)); sfx.append(dict(name='click', t=t, gain=.6))
def clear(t): ide.append(dict(t=t, op='clear'))
def goto(t, lesson, i=0): ide.append(dict(t=t, op='goto', lesson=lesson, i=i))
def mark(t0, t1, line, c0, c1, text='', color='y', pos='above'):
    marks.append(dict(t0=t0, t1=t1, line=line, c0=c0, c1=c1, text=text, color=color, pos=pos)); sfx.append(dict(name='pop', t=t0, gain=.35))
def MK(t0, t1, sub, text='', color='y', pos='above', nth=0):
    lines = code[0].split('\n'); k = 0
    for li, ln in enumerate(lines):
        p0 = 0
        while True:
            c = ln.find(sub, p0)
            if c < 0: break
            if k == nth: mark(t0, t1, li, c, c + len(sub), text, color, pos); return
            k += 1; p0 = c + 1
    raise SystemExit('MK not found: ' + sub)
def ring(t0, t1, sel, text='', color='y', pad=6):
    rings.append(dict(t0=t0, t1=t1, sel=sel, text=text, color=color, pad=pad)); sfx.append(dict(name='pop', t=t0, gain=.35))
def chip(t0, t1, h, cls='', style=''):
    chips.append(dict(t0=t0, t1=t1, html=h, cls=cls, style=style)); sfx.append(dict(name='pop', t=t0, gain=.45))

slides = []
def A(kind, t, o=None, ok='fade'):
    s = f'data-a="{kind};{t}"' + (f' data-o="{o}" data-ok="{ok}"' if o is not None else '')
    if kind in ('pop', 'stamp', 'drop'): sfx.append(dict(name={'pop': 'pop', 'stamp': 'thud', 'drop': 'thud'}[kind], t=t + (.35 if kind == 'drop' else 0), gain=.4))
    return s
def pill(l, t, tt, text, cls='', kind='left', o=None, size=None):
    st = f'font-size:{size}px;padding:14px 26px' if size else ''
    return f'<div style="left:{l}px;top:{t}px" {A(kind, tt, o)}><span class="pill {cls}" style="{st}">{text}</span></div>'
def node(l, t, w, tt, emoji, title, small='', cls='', o=None, kind='pop'):
    return f'<div class="node {cls}" style="left:{l}px;top:{t}px;width:{w}px" {A(kind, tt, o)}><span class="big">{emoji}</span>{title}<small>{small}</small></div>'
def card(l, t, w, h, tt, emoji, title, body='', cls='', o=None, kind='up'):
    return f'<div class="card3 {cls}" style="left:{l}px;top:{t}px;width:{w}px;height:{h}px" {A(kind, tt, o)}><div class="emo">{emoji}</div><div class="t">{title}</div><div class="u">{body}</div></div>'
def cc(l, t, tt, text, size=26, kind='pop', o=None, extra=''):
    return f'<div class="codechip" style="left:{l}px;top:{t}px;font-size:{size}px;{extra}" {A(kind, tt, o)}>{text}</div>'
def h2(l, t, tt, text, size=46, o=None): return f'<div class="h2" style="left:{l}px;top:{t}px;font-size:{size}px" {A("up", tt, o)}>{text}</div>'
def kick(tt, num, text): return f'<div class="kicker" {A("down", tt)}><b>{num}</b>{text}</div>'
def arrow(l, t, tt, text='→', size=44, o=None, color='var(--purple)'): return f'<div class="mono" style="left:{l}px;top:{t}px;font-size:{size}px;color:{color}" {A("pop", tt, o)}>{text}</div>'
def bubble(l, t, w, tt, who, body, cls='', o=None, h=None):
    ht = f'height:{h}px;' if h else ''
    return f'<div class="card3 {cls}" style="left:{l}px;top:{t}px;width:{w}px;{ht}gap:8px" {A("up", tt, o)}><div class="u" style="font:800 15px var(--mono);letter-spacing:1px;color:var(--purple)">{who}</div><div style="font:600 21px/1.45 Inter,sans-serif;color:#fff">{body}</div></div>'
REAL = '🧪 ҷавоби воқеии Claude · матн'

# ---------- границы сцен ----------
T_HELP = N(45.2); T_HOW = N(88.2); T_CAN = N(135.9); T_R1 = N(174.6); T_ANS1 = N(261.5); T_IDEA = N(279.7); T_ANS2 = N(304.5); T_IDEB = N(324.7)
T_R3 = N(397.3); T_IDEC = N(411.3); T_PLAN = N(482.1); T_PROJ = N(506.2); T_IDED = N(574.1); T_ASK = N(590.3); T_WARN = N(652.6); T_DEV = N(692.3); T_LEARN = N(728.6); T_TASK = N(777.1)
T_SUM = N(842.6); T_ROAD = N(884.8); T_END = N(947.1)

# ---------- 0. Хук ----------
slides.append(f'''<section class="scene" id="s-hook">
{kick(.2, 'ДАРСИ 13 / 13', 'БАРНОМАСОЗӢ АЗ СИФР · JAVASCRIPT')}
<div class="h1" style="left:60px;top:70px;font-size:84px;line-height:1.05" {A('stamp', .6)}>ЗЕҲНИ СУНЪӢ<br>БАРОИ БАРНОМАСОЗ</div>
{pill(60, 330, N(7.7), '❓ Оё зеҳни сунъӣ ҷои барномасозро мегирад?', 'left', 'left', size=26)}
{pill(60, 400, N(15.0), '🤝 ёвар ✓', 'ok', 'pop', size=28)}
{pill(300, 400, N(16.5), '🚫 ҷонишин ✗', 'err', 'pop', size=28)}
{pill(60, 480, N(20.8), '1 · дақиқ пурсед', 'left', 'left', size=24)}
{pill(60, 540, N(22.2), '2 · кодро хонед ва бифаҳмед', 'left', 'left', size=24)}
{pill(60, 600, N(23.6), '3 · ҳатман иҷро кунед ва санҷед', 'left', 'left', size=24)}
<div style="left:600px;top:470px" {A('stamp', N(25.6), N(32.0))}><span class="pill accent" style="font-size:30px;padding:16px 32px">охирини силсила · 13 / 13</span></div>
{pill(600, 560, N(29.0), '🎯 санҷиши нав ҳаст', 'accent', 'pop', N(32.0))}
{card(600, 450, 620, 150, N(33.8), '🚫', 'на барои онҳост, ки мехоҳанд ҳамаро зеҳни сунъӣ кунад', '', '', N(38.2))}
{card(600, 450, 620, 150, N(38.5), '✅', 'барои онҳост, ки мехоҳанд барномасоз шаванд', 'ва аз ёвар дуруст истифода баранд', 'hl')}
</section>''')
S('s-hook', 0, T_HELP)

# ---------- 1. Ёвари ҷавон ----------
slides.append(f'''<section class="scene" id="s-help">
{kick(T_HELP + .1, '01', 'ЁВАРИ ҶАВОН')}
{h2(60, 90, T_HELP + .5, 'Тасаввур кунед: ёвари ҷавон', 46)}
{node(60, 200, 360, N(47.9), '⚡', 'зуд кор мекунад', 'ҳаргиз хаста намешавад')}
{node(450, 200, 360, N(52.8), '⚠️', 'баъзан хато мекунад', 'ва бо боварии том', 'no')}
{node(840, 200, 360, N(60.4), '✅', 'шумо месанҷед', 'пеш аз он ки ба одамон нишон диҳед', 'yes')}
{pill(60, 440, N(64.8), '🤖 зеҳни сунъӣ дар барномасозӣ = ёвар', 'accent', 'left', size=28)}
{pill(60, 510, N(72.3), '🧠 масъулият ҳамеша бар души шумост', 'ok', 'left', size=26)}
{pill(60, 580, N(80.3), '🔍 барои санҷидан бояд фаҳмед, ки код чӣ кор мекунад', 'left', 'left', size=24)}
<div style="left:700px;top:640px" {A('stamp', N(84.8))}><span class="pill accent" style="font-size:24px">12 дарс — барои ҳамин</span></div>
</section>''')
S('s-help', T_HELP, T_HOW)

# ---------- 2. Чӣ тавр кор мекунад ----------
slides.append(f'''<section class="scene" id="s-how">
{kick(T_HOW + .1, '02', 'ЗЕҲНИ СУНЪӢ ЧӢ ТАВР КОР МЕКУНАД?')}
{node(60, 160, 300, N(94.9), '📚', 'ҳазорон матн ва код', 'омӯхта шудааст')}
{arrow(380, 210, N(98.1), '→', 44)}
{node(470, 160, 300, N(102.1), '🎲', 'ҷавоби «эҳтимолан дуруст»', 'на фикр кардани одам')}
{arrow(790, 210, N(108.3), '→', 44)}
{node(880, 160, 340, N(108.9), '💬', 'ҷавоб', 'ба саволи шумо монанд')}
{card(60, 400, 560, 170, N(113.9), '✅', 'аксар вақт дуруст', 'чунин кодро бисёр дидааст', 'hl')}
{card(660, 400, 560, 170, N(119.2), '⚠️', 'гоҳо ба назар дуруст', 'дар асл не — бо ҳамон боварӣ', '')}
{pill(60, 600, N(126.2), '👁️ барномаи шуморо намебинад, агар нагӯед', 'left', 'left', size=24)}
{pill(700, 600, N(130.1), '▶️ кодро худаш иҷро намекунад', 'left', 'left', size=24)}
</section>''')
S('s-how', T_HOW, T_CAN)

# ---------- 3. Ёвар чӣ кор карда метавонад ----------
slides.append(f'''<section class="scene" id="s-can">
{kick(T_CAN + .1, '03', 'ЁВАР ЧӢ КОР КАРДА МЕТАВОНАД?')}
{h2(60, 80, T_CAN + .5, 'Ёвар бисёр чиз карда метавонад', 44)}
{card(60, 170, 360, 190, N(140.6), '📖', 'шарҳ додани код', 'ба забони оддӣ', 'hl')}
{card(450, 170, 360, 190, N(144.9), '🐞', 'паёми хато', 'сабабҳои имкониро мегӯяд', 'hl')}
{card(840, 170, 360, 190, N(149.2), '🧪', 'санҷишҳо пешниҳод мекунад', 'бо кадом қиматҳо', 'hl')}
{card(60, 390, 360, 190, N(154.0), '🏷️', 'номи фаҳмо', 'барои тағйирёбанда', '')}
{card(450, 390, 360, 190, N(157.5), '🔁', 'аз забон ба забон', 'мегардонад', '')}
{card(840, 390, 360, 190, N(160.8), '🎯', 'мисол ва машқ', 'барои омӯхтан', '')}
<div style="left:60px;top:620px" {A('stamp', N(164.9))}><span class="pill accent" style="font-size:28px;padding:16px 32px">ӯ пешниҳод мекунад — шумо қарор мегиред</span></div>
</section>''')
S('s-can', T_CAN, T_R1)

# ---------- 4. Қоидаи 1 ----------
P1 = 'Функсия бинавис, ки ду рақамро ҷамъ мекунад.'
P2 = 'Дар <span style="color:var(--teal)">JavaScript</span> функсияи <span style="color:var(--fn)">add</span> бо параметрҳои <span style="color:var(--fn)">a</span> ва <span style="color:var(--fn)">b</span> бинавис, ки ду рақамро ҷамъ мекунад ва ҷавобро <span style="color:var(--kw)">return</span> мекунад. Рақамҳо гоҳо ҳамчун матн меоянд, масалан <span style="color:var(--str)">"25"</span>.'
slides.append(f'''<section class="scene" id="s-r1">
{kick(T_R1 + .1, '04', 'ҚОИДАИ 1: ДАҚИҚ ПУРСЕД')}
{bubble(60, 110, 1160, N(185.9), 'ХОҲИШИ 1 · НОРАВШАН', P1, '', N(233.0), 90)}
{bubble(60, 240, 1160, N(190.9), 'ХОҲИШИ 2 · ДАҚИҚ', P2, 'hl', N(233.0), 190)}
{pill(60, 470, N(209.2), '1 · забон', 'ok', 'up', N(233.0), 24)}
{pill(240, 470, N(211.3), '2 · ном ва параметрҳо', 'ok', 'up', N(233.0), 24)}
{pill(590, 470, N(215.0), '3 · ҷавоб (return)', 'ok', 'up', N(233.0), 24)}
{pill(890, 470, N(216.9), '4 · ҳолати хос', 'ok', 'up', N(233.0), 24)}
{pill(60, 560, N(222.1), '🎲 норавшан → натиҷаи тасодуфӣ', 'err', 'left', N(233.0), 24)}
{pill(60, 622, N(225.4), '🎯 равшан → натиҷаи дуруст', 'ok', 'left', N(233.0), 24)}
<div class="h2" style="left:60px;top:90px;font-size:44px" {A('up', N(233.2), N(248.0))}>Хоҳиши хуб — панҷ сатр</div>
{pill(60, 190, N(236.9), '1 · забон', 'left', 'left', N(248.0), 28)}
{pill(60, 260, N(237.9), '2 · вазифа', 'left', 'left', N(248.0), 28)}
{pill(60, 330, N(239.4), '3 · маълумоти воридотӣ', 'left', 'left', N(248.0), 28)}
{pill(60, 400, N(241.0), '4 · натиҷаи интизорӣ', 'left', 'left', N(248.0), 28)}
{pill(60, 470, N(242.2), '5 · ҳолати хос', 'left', 'left', N(248.0), 28)}
<div class="h2" style="left:60px;top:90px;font-size:44px" {A('up', N(248.0))}>Агар навомӯз бошед — бигӯед</div>
{bubble(60, 200, 1160, N(252.9), 'ХОҲИШ', '«Ман навомӯзам, бо забони оддӣ шарҳ деҳ».', 'hl', None, 110)}
{pill(60, 360, N(256.1), '💡 ёвар на калимаҳои мураккаб, балки мисоли равшан медиҳад', 'ok', 'left', size=26)}
</section>''')
S('s-r1', T_R1, T_ANS1)

# ---------- 5. Ҷавоби воқеии 1 ----------
slides.append(f'''<section class="scene" id="s-ans1">
<div class="kicker" {A('down', T_ANS1 + .1)}><b>05</b>{REAL}</div>
{bubble(60, 90, 1160, N(263.3), 'ХОҶИШ (ШУМО)', P1, '', None, 90)}
<div class="card3 hl" style="left:60px;top:210px;width:1160px;height:360px;gap:10px" {A('up', N(266.0))}><div class="u" style="font:800 15px var(--mono);letter-spacing:1px;color:var(--purple)">ҶАВОБИ ВОҚЕИИ CLAUDE</div>
 <div style="font:600 20px Inter,sans-serif;color:#d4d4d4">Албатта! Ин функсия ду рақамро ҷамъ мекунад.</div>
 <div class="codechip" style="font-size:30px;white-space:pre;padding:18px 26px;width:620px" {A('pop', N(268.8))}><span class="k">function</span> <span class="f">sum</span>(a, b) {{
  <span class="k">return</span> a + b;
}}

console.<span class="f">log</span>(<span class="f">sum</span>(<span class="n">2</span>, <span class="n">3</span>)); <span class="c">// 5</span></div>
 <div style="display:flex;gap:16px;margin-top:6px"><span class="pill" style="font-size:20px" {A('pop', N(275.9))}>TypeScript ✓</span><span class="pill" style="font-size:20px" {A('pop', N(277.0))}>Python ✓</span><span class="pill ok" style="font-size:20px" {A('pop', N(277.8))}>воқеӣ · бе тағйир</span></div>
</div>
</section>''')
S('s-ans1', T_ANS1, T_IDEA)

# ---------- IDE: sum ----------
S('ide', T_IDEA, T_ANS2)
SUM0 = 'function sum(a, b) {\n  return a + b;\n}\n'
setc(T_IDEA, SUM0); clear(T_IDEA)
chip(T_IDEA + .1, T_IDEA + 2.0, '<span>🧪</span><div>Санҷиши ҷавоби ёвар<small>06 · sum(a, b)</small></div>', 'card')
SUM1 = SUM0 + 'console.log(sum(2, 3));'
typ(N(280.8), SUM1, 2.4)
run(N(284.0)); ring(N(284.6), N(285.6), '#out', '✅ 5', 'g', 2)
SUM2 = SUM0 + 'console.log(sum("25", 1));'
typ(N(287.0), SUM2, 1.8); clear(N(288.9))
run(N(289.6)); ring(N(290.2), N(304.0), '#out', '⚠️ 251', 'r', 2)
chip(N(292.3), N(297.0), '<span class="big">📦</span><div>дарси 8: <span class="mono">"25" + 1</span> = <span class="mono">"251"</span><small>матн плюс рақам — матн пайваст мешавад</small></div>', 'card', 'top:420px')
chip(N(297.3), N(303.5), '<div>хатои зеҳни сунъӣ нест<small>мо нагуфта будем, ки рақам гоҳо матн аст</small></div>', 'card', 'top:420px')

# ---------- Ҷавоби воқеии 2 ----------
slides.append(f'''<section class="scene" id="s-ans2">
<div class="kicker" {A('down', T_ANS2 + .1)}><b>07</b>{REAL}</div>
{bubble(60, 90, 1160, N(304.8), 'ХОҶИШИ 2 (ШУМО)', P2, '', None, 150)}
<div class="card3 hl" style="left:60px;top:270px;width:1160px;height:330px;gap:10px" {A('up', N(306.0))}><div class="u" style="font:800 15px var(--mono);letter-spacing:1px;color:var(--purple)">ҶАВОБИ ВОҚЕИИ CLAUDE</div>
 <div class="codechip" style="font-size:28px;white-space:pre;padding:16px 26px;width:700px" {A('pop', N(306.6))}><span class="k">function</span> <span class="f">add</span>(a, b) {{
  <span class="k">return</span> <span class="f">Number</span>(a) + <span class="f">Number</span>(b);
}}</div>
 <div style="font:600 21px/1.45 Inter,sans-serif;color:#d4d4d4" {A('up', N(311.4))}>«Шарҳ: агар <span class="mono" style="color:var(--kw)">+</span>-ро бевосита истифода барем, <span class="mono" style="color:var(--str)">"25" + 5</span> натиҷаи <span class="mono" style="color:var(--str)">"255"</span> (пайваст кардани матн) медиҳад. Барои ҳамин аввал <span class="mono" style="color:var(--fn)">Number()</span> ҳар ду параметрро ба рақам табдил медиҳад…»</div>
</div>
</section>''')
S('s-ans2', T_ANS2, T_IDEB)

# ---------- IDE: add + қоидаи 2 ----------
S('ide', T_IDEB, T_R3)
ADD0 = 'function add(a, b) {\n  return Number(a) + Number(b);\n}\n'
setc(T_IDEB, ''); clear(T_IDEB)
typ(N(324.8), ADD0 + 'console.log(add("25", 5));', 3.2)
run(N(328.0)); ring(N(328.8), N(331.8), '#out', '✅ 30', 'g', 2)
chip(T_IDEB + .1, T_IDEB + 1.9, '<span>🛠️</span><div>add — хоҳиши дақиқ<small>08 · ҷавоби дуруст</small></div>', 'card', 'top:560px')
chip(N(332.0), N(334.5), '<span class="big">📖</span><div>Қоидаи 2<small>кодро хонед ва бифаҳмед</small></div>', 'card')
chip(N(339.1), N(344.0), '«Ин кодро сатр ба сатр шарҳ деҳ»', 'side yel', 'top:90px')
MK(N(347.6), N(350.6), 'function', 'функсия — дарси 5', 'g')
MK(N(350.9), N(353.1), '(a, b)', 'параметрҳо', 'c', 'below')
MK(N(353.3), N(356.4), 'return', 'ҷавоб', 'y', 'below')
MK(N(358.6), N(367.0), 'Number', '❓ калимаи нав — пурсед', 'r')
chip(N(362.2), N(366.8), '«Number чист ва чаро лозим аст?»', 'side yel', 'top:90px')
chip(N(371.6), N(376.0), '«Чаро ту ин тавр навиштӣ?»', 'side yel', 'top:90px')
chip(N(376.7), N(383.5), '«Роҳи оддитар ҳаст?»', 'side yel', 'top:90px')
chip(N(388.4), N(396.5), '«Боз содда шарҳ деҳ»', 'side yel', 'top:90px')

# ---------- Қоидаи 3: хоҳиш ----------
P3 = 'Ман навомӯзам. Функсия бинавис, ки миёнаи рӯйхати рақамҳоро ҳисоб мекунад.'
slides.append(f'''<section class="scene" id="s-r3">
{kick(T_R3 + .1, '09', 'ҚОИДАИ 3: ҲАТМАН ИҶРО КУНЕД ВА САНҶЕД')}
{h2(60, 90, T_R3 + .5, 'Мисоли дуюм: миёнаи рӯйхат', 46)}
{bubble(60, 220, 1160, N(405.9), 'ХОҲИШИ 3 (ШУМО)', P3, 'hl', None, 110)}
{pill(60, 380, N(411.0), '🧪 ва ҷавоби воқеӣ ин аст…', 'accent', 'pop', size=28)}
</section>''')
S('s-r3', T_R3, T_IDEC)

# ---------- IDE: miyona ----------
S('ide', T_IDEC, T_PLAN)
MIY = 'function miyona(royhat) {\n  if (royhat.length === 0) {\n    return 0; // агар рӯйхат холӣ бошад\n  }\n\n  let jam = 0;\n  for (const raqam of royhat) {\n    jam += raqam;\n  }\n\n  return jam / royhat.length;\n}\n'
setc(T_IDEC, ''); clear(T_IDEC)
chip(T_IDEC + .1, T_IDEC + 2.0, '<span>🧪</span><div>ҷавоби воқеии Claude<small>10 · miyona(royhat)</small></div>', 'card')
typ(N(413.2), MIY, 17.0)
MK(N(419.7), N(423.0), 'royhat.length === 0', 'холӣ → return 0', 'g')
MK(N(424.1), N(429.6), 'const raqam of royhat', 'давр (дарси 3)', 'c', 'below')
chip(N(434.1), N(437.2), '<span class="big">✅</span><div>ҳолати холиро ӯ худаш ба назар гирифт<small>хуб!</small></div>', 'card', 'top:560px')
chip(N(437.4), N(445.0), '<div>калимаҳои нав: <span class="mono">for…of</span> · <span class="mono">reduce</span><small>қоидаи 2: калимаи нав — пурсед</small></div>', 'card', 'top:560px')
chip(N(445.2), N(449.0), '«reduce-ро баъдтар ҳатман омӯзед» — ӯ худаш', 'side yel', 'top:90px')
T1 = MIY + 'console.log(miyona([10, 20, 30]));'
typ(N(450.3), T1, 3.0)
run(N(453.6)); ring(N(454.0), N(454.9), '#out', '✅ 20', 'g', 2)
T2 = MIY + 'console.log(miyona([]));'
typ(N(455.1), T2, 1.4); clear(N(456.6))
run(N(456.8)); ring(N(457.2), N(457.8), '#out', '✅ 0', 'g', 2)
T3 = MIY + 'console.log(miyona(["10", "20"]));'
typ(N(457.9), T3, 3.0); clear(N(461.2))
run(N(462.8)); ring(N(463.3), N(482.0), '#out', '⚠️ 510', 'r', 2)
chip(N(469.9), N(476.0), '<div><span class="mono">0 + "10" + "20"</span> → <span class="mono">"01020"</span><small>нол плюс матн — матн пайваст мешавад; баъд ÷ 2 = 510</small></div>', 'card', 'top:420px')
FIX = MIY.replace('jam += raqam;', 'jam += Number(raqam);') + 'console.log(miyona(["10", "20"]));'
typ(N(477.0), FIX, 2.6); clear(N(479.7))
MK(N(477.4), N(481.6), 'Number(raqam)', 'Number — ислоҳ', 'g')
run(N(480.3)); ring(N(480.9), N(482.0), '#out', '✅ 15', 'g', 2)

# ---------- нақшаи санҷиш ----------
slides.append(f'''<section class="scene" id="s-plan">
{kick(T_PLAN + .1, '11', 'НАҚШАИ САНҶИШ')}
{h2(60, 90, T_PLAN + .5, 'Ҳатто ҷавоби хуб бояд санҷида шавад', 44)}
{card(60, 200, 360, 250, N(486.7), '✅', 'ҳолати оддӣ', 'он чизе ки интизор меравад<br><span class="mono">[10, 20, 30]</span>', 'hl')}
{card(450, 200, 360, 250, N(489.9), '📏', 'ҳолати канорӣ', 'нол · холӣ · хеле калон<br><span class="mono">[]</span>', '')}
{card(840, 200, 360, 250, N(493.9), '🧩', 'ҳолати нодуруст', 'матн ба ҷои рақам<br><span class="mono">["10", "20"]</span>', '')}
<div style="left:60px;top:490px" {A('stamp', N(497.0))}><span class="pill accent" style="font-size:30px;padding:16px 32px">бо рақам · бо матн · бо холӣ</span></div>
{pill(60, 590, N(500.4), '⏱️ 5 дақиқа санҷиш < 1 соат ҷустуҷӯи хато дар охир', 'ok', 'left', size=26)}
</section>''')
S('s-plan', T_PLAN, T_PROJ)

# ---------- лоиҳаи калон ----------
slides.append(f'''<section class="scene" id="s-proj">
{kick(T_PROJ + .1, '12', 'ЛОИҲАИ КАЛОН: ҚАДАМ БА ҚАДАМ')}
{h2(60, 90, T_PROJ + .5, 'Ҳамаашро якбора напурсед', 46, N(524.0))}
{bubble(60, 190, 1160, N(515.8), 'ХОҲИШИ БАД', '«Дафтарчаи пурраро бинавис» — ҷавоби калон ва бесанҷ', 'no', N(524.0), 100)}
<div class="h2" style="left:60px;top:90px;font-size:46px" {A('up', N(524.2))}>Беҳтар: қадам ба қадам</div>
{card(60, 200, 360, 200, N(526.5), '1️⃣', 'showTasks', 'иҷро → санҷ', 'hl')}
{card(450, 200, 360, 200, N(530.7), '2️⃣', 'addTask', 'иҷро → санҷ', 'hl')}
{card(840, 200, 360, 200, N(533.3), '3️⃣', 'completeTask', 'иҷро → санҷ', 'hl')}
{pill(60, 430, N(540.8), '📓 дарси 10: чор функсия — қадам ба қадам', 'ok', 'left', N(549.5), 24)}
{bubble(60, 430, 1160, N(553.2), 'ХОҲИШИ ХУБ БАРОИ ҚАДАМИ 2', 'Дар JavaScript функсияи <span class="mono" style="color:var(--fn)">addTask</span> бо параметри <span class="mono" style="color:var(--fn)">text</span> бинавис. Вай ба рӯйхати <span class="mono">tasks</span> объекти бо <span class="mono">text</span> ва <span class="mono">done</span> баробари <span class="mono">false</span> илова мекунад. Дар охир ҳеҷ чиз return намекунад.', 'hl', None, 200)}
{pill(60, 650, N(566.2), '✅ забон · ном · параметр · натиҷа · он чӣ бояд намешавад — ҳама ҳаст', 'ok', 'left', size=22)}
</section>''')
S('s-proj', T_PROJ, T_IDED)

# ---------- IDE: хато ----------
S('ide', T_IDED, T_ASK)
AVG = 'function average(list) {\n  let sum = 0;\n  for (let i = 0; i < list.length; i++) {\n    sum = sum + list[i];\n  }\n  return sum / list.length;\n}\n'
setc(T_IDED, ''); clear(T_IDED)
typ(N(574.6), AVG, 4.5)
typ(N(582.1), AVG + 'console.log(average());', 2.0)
run(N(584.9) + .4, 'bad')
ring(N(586.0), N(590.2), '#out', '⚠️ TypeError', 'r', 2)

# ---------- Хоҳиши хуб ва ҷавоби воқеии 4 ----------
slides.append(f'''<section class="scene" id="s-ask">
{kick(T_ASK + .1, '13', 'АГАР ХАТО ШУД')}
{h2(60, 90, T_ASK + .5, 'Хоҳиши хуб — чор қисм', 44, N(604.5))}
{card(60, 190, 275, 200, N(594.6), '📄', 'код', 'ҳамон ки хато медиҳад', 'hl', N(604.5))}
{card(355, 190, 275, 200, N(596.4), '🛑', 'паёми хато', 'ҳамон матн', 'hl', N(604.5))}
{card(650, 190, 275, 200, N(597.6), '🎯', 'интизор будед', 'нол ё паём', 'hl', N(604.5))}
{card(945, 190, 275, 200, N(599.0), '❓', '«Чаро?»', 'чаро мешавад ва чӣ тавр ислоҳ кунам', 'hl', N(604.5))}
{pill(60, 440, N(604.7), '📨 мо ин хоҳишро воқеан фиристодем', 'accent', 'left', N(606.0), 26)}
<div class="card3 hl" style="left:60px;top:130px;width:1160px;height:390px;gap:10px" {A('up', N(606.2), N(630.0))}><div class="u" style="font:800 15px var(--mono);letter-spacing:1px;color:var(--purple)">ҶАВОБИ ВОҚЕИИ CLAUDE · ХУЛОСА</div>
 <div style="font:600 24px/1.5 Inter,sans-serif;color:#fff" {A('up', N(607.6))}>🔎 average бе рӯйхат даъват шудааст — <span class="mono" style="color:var(--err)">list = undefined</span></div>
 <div style="font:600 24px/1.5 Inter,sans-serif;color:#fff" {A('up', N(611.5))}>1️⃣ рӯйхат гузаред: <span class="mono" style="color:var(--teal)">average([1, 2, 3])</span></div>
 <div style="font:600 24px/1.5 Inter,sans-serif;color:#fff" {A('up', N(613.5))}>2️⃣ ё санҷиш илова кунед: <span class="mono" style="color:var(--teal)">Array.isArray(list)</span></div>
 <div style="font:700 24px/1.5 Inter,sans-serif;color:var(--fn)" {A('pop', N(615.0))}>💡 «нол ё паём?» — ин қарор бо шумост</div>
</div>
{pill(60, 560, N(619.7), '🔁 пурс → санҷ → боз санҷ — кори ҳаррӯзаи барномасоз', 'ok', 'left', N(630.0), 26)}
<div class="h2" style="left:60px;top:90px;font-size:44px" {A('up', N(630.4))}>Агар ёвар такрор хато кунад</div>
{card(60, 200, 360, 230, N(634.7), '✂️', 'хоҳишро содда кунед', 'як қисми хурд, як савол', 'hl')}
{card(450, 200, 360, 230, N(639.5), '🖨️', 'console.log', 'қиматро худатон бубинед (дарси 8)', 'hl')}
{card(840, 200, 360, 230, N(645.4), '📝', 'хоҳишро беҳтар нависед', 'баъзан хато дар он аст, ки чӣ мехоҳед', 'hl')}
</section>''')
S('s-ask', T_ASK, T_WARN)

# ---------- Огоҳӣ ----------
slides.append(f'''<section class="scene" id="s-warn">
{kick(T_WARN + .1, '14', 'ОГОҲӢ: БА ЧӢ БОВАР НАКУНЕД')}
{card(60, 130, 560, 220, N(655.5), '🔑', 'рамз, калид, маълумоти шахсӣ', 'ба зеҳни сунъӣ нанависед: он чи ба хидмати онлайн мефиристед, дигар танҳо дар дасти шумо нест', 'no')}
{card(660, 130, 560, 220, N(669.9), '👻', 'чизи вуҷуднадошта', 'баъзан функсия ё китобхонаеро «меофарад», ки нест — дар ҳуҷҷатҳои расмӣ санҷед', '')}
{card(60, 380, 560, 220, N(682.2), '🕰️', 'маълумоти кӯҳна', 'ӯ метавонад кӯҳна бошад', '')}
{card(660, 380, 560, 220, N(686.1), '📋', 'нусхаи бефаҳм — не', 'ҳамон қоидаи 2: намефаҳмед — нагузоред', 'hl')}
</section>''')
S('s-warn', T_WARN, T_DEV)

# ---------- Барномасоз чӣ кор мекунад ----------
slides.append(f'''<section class="scene" id="s-dev">
{kick(T_DEV + .1, '15', 'БАРНОМАСОЗ ЧӢ КОР МЕКУНАД?')}
{h2(60, 90, T_DEV + .5, 'Танҳо код навиштан нест', 46)}
{node(60, 190, 270, N(698.5), '🧩', 'масъаларо мефаҳмад', 'одамон чӣ мехоҳанд')}
{node(350, 190, 270, N(702.3), '✂️', 'ба қисмҳо тақсим мекунад', 'мисли дафтарчаи вазифаҳо')}
{node(640, 190, 270, N(707.5), '🔍', 'ҳар қисмро месанҷад', '')}
{node(930, 190, 290, N(709.8), '🧠', 'масъулият мегирад', 'дуруст кор мекунад ё не')}
{pill(60, 470, N(715.5), '🤖 ёвар: навиштани қисмҳо ва шарҳ додан', 'left', 'left', size=26)}
<div style="left:60px;top:560px" {A('stamp', N(721.1))}><span class="pill accent" style="font-size:28px;padding:16px 32px">фаҳмидан, тақсим кардан ва масъулият — бо шумост</span></div>
</section>''')
S('s-dev', T_DEV, T_LEARN)

# ---------- Чӣ тавр омӯхтан ----------
slides.append(f'''<section class="scene" id="s-learn">
{kick(T_LEARN + .1, '16', 'ЧӢ ТАВР БО ЗЕҲНИ СУНЪӢ ОМӮХТАН')}
{card(60, 130, 360, 230, N(734.5), '1️⃣', 'худатон кӯшиш кунед', 'вазифаро худатон ҳал кунед, ҳатто агар хато шавад', 'hl')}
{card(450, 130, 360, 230, N(740.1), '2️⃣', 'баъд пурсед', '«Ин код чӣ мекунад?» · «Роҳи дигар ҳаст?» · «Машқҳои монанд деҳ»', 'hl')}
{card(840, 130, 360, 230, N(746.5), '3️⃣', 'аз нав бо дасти худ нависед', 'на нусха', 'hl')}
{pill(60, 400, N(752.7), '❓ ман ин ҷавобро шарҳ дода метавонам?  Агар не — ҳанӯз кор мондааст', 'accent', 'left', size=24)}
{pill(60, 480, N(759.8), '⏱️ ҳар рӯз 20 дақиқа > 3 соат дар як рӯзи ҳафта', 'ok', 'left', size=26)}
{pill(60, 550, N(764.6), '📚 як мавзӯъ · 🧪 як вазифа · 🐞 як хато бо дасти худ', 'left', 'left', size=24)}
</section>''')
S('s-learn', T_LEARN, T_TASK)

# ---------- Вазифаҳо ва санҷиш (IDE) ----------
S('ide', T_TASK, T_SUM)
chip(T_TASK + .1, N(779.6), '<span>🎯</span><div>Вазифаҳо барои шумо<small>17 · дарси 13 дар IDE</small></div>', 'card')
goto(N(779.9), 'l13', 0)
ST1 = 'function sum(a, b) {\n  return a + b;\n}\n\nconsole.log(sum(25, 1));\nconsole.log(sum("25", 1));\n'
SO1 = ST1.replace('return a + b;', 'return Number(a) + Number(b);')
setc(N(780.0), ST1)
ring(N(782.6), N(787.0), '#side', '📘 назария', 'c', 4)
ring(N(787.2), N(795.0), '#task', 'Вазифаи 1', 'y', 4)
typ(N(788.6), SO1, 3.4)
click(N(795.4), '#side button[data-i="1"]')
ST2 = 'function miyona(royhat) {\n  if (royhat.length === 0) {\n    return 0;\n  }\n  let jam = 0;\n  for (const raqam of royhat) {\n    jam += raqam;\n  }\n  return jam / royhat.length;\n}\n'
SO2 = ST2.replace('jam += raqam;', 'jam += Number(raqam);')
setc(N(795.45), ST2)
ring(N(795.8), N(801.6), '#task', 'Вазифаи 2', 'y', 4)
typ(N(797.0), SO2, 3.0)
click(N(801.9), '#side button[data-i="2"]')
ST3 = 'function double(n) {\n  return n + 2;\n}\n\nconsole.log(double(5));\nconsole.log(double(0));\nconsole.log(double(-3));\n'
SO3 = ST3.replace('n + 2', 'n * 2')
setc(N(801.95), ST3)
ring(N(802.3), N(806.5), '#task', 'Вазифаи 3', 'y', 4)
run(N(806.2) + .2, 'bad')
ring(N(807.0), N(809.2), '#out', '⚠️ хато дар double', 'r', 2)
typ(N(809.4), SO3, 1.6)
ring(N(810.3), N(811.6), '#check', '✓ Санҷиш', 'c', 6)
click(N(811.0), '#check', 'check'); sfx.append(dict(name='chime', t=N(811.9), gain=.6))

# ---------- санҷиш (квиз) ----------
goto(N(812.4), 'free', 0)
MAX0 = 'function max(a, b) {\n  if (a > b) {\n    return a;\n  }\n  return b;\n}\n'
setc(N(812.5), ''); clear(N(812.5))
typ(N(813.2), MAX0, 4.2)
typ(N(817.7), MAX0 + 'console.log(max("9", "10"));', 3.8)
g0 = V(GAP_Q) - PAUSE
qb = lambda sub: f'<div>max("9", "10") = ?<small>{sub}</small></div>'
chip(N(823.4), g0 - .3, '<span class="big">❓</span>' + qb('«нӯҳ» ё «даҳ»? видеоро пауза кунед ✍️'), 'card')
for k in range(5):
    chip(g0 + k + .02, g0 + k + .62, f'<span class="big">{5 - k}</span>' + qb('фикр кунед · баъд ҷавобро мебинем ✅'), 'card')
    sfx.append(dict(name='tick', t=g0 + k, gain=.8))
run(N(829.3) + .3)
ring(N(830.4), N(836.5), '#out', '⚠️ 9', 'r', 2)
chip(N(831.3), N(836.8), '<div><span class="mono">"9" &gt; "1"</span> — матнҳо ҳарф ба ҳарф муқоиса мешаванд<small>«9» аз «1» калонтар аст</small></div>', 'card', 'top:560px')
typ(N(836.9), MAX0 + 'console.log(max(Number("9"), Number("10")));', 3.0); clear(N(839.6))
MK(N(837.2), N(842.0), 'Number("9")', 'Number — ислоҳ', 'g')
run(N(840.0)); ring(N(840.6), N(842.5), '#out', '✅ 10', 'g', 2)

# ---------- Хулоса ----------
slides.append(f'''<section class="scene" id="s-sum">
{kick(T_SUM + .2, '18', 'ХУЛОСА')}
<div class="h1" style="left:60px;top:80px;font-size:80px;line-height:1.05" {A('stamp', N(844.1))}>ЁВАР,<br>НА ҶОНИШИН</div>
{pill(60, 330, N(849.1), '1 · дақиқ пурсед', 'ok', 'left', size=26)}
{pill(60, 396, N(851.4), '2 · кодро хонед ва бифаҳмед', 'ok', 'left', size=26)}
{pill(60, 462, N(853.2), '3 · ҳатман иҷро кунед ва санҷед', 'ok', 'left', size=26)}
{pill(60, 540, N(855.1), '🛑 хато → код + паёми хато + интизорӣ', 'left', 'left', size=24)}
{pill(60, 604, N(859.9), '🔑 рамз ва маълумоти шахсӣ — нафиристед', 'err', 'left', size=24)}
<div style="left:560px;top:330px" {A('stamp', N(863.3))}><span class="pill accent" style="font-size:30px;padding:18px 36px">охирин дарси силсила · 13 / 13</span></div>
{pill(560, 440, N(865.9), '📦 → … → 🌐 → 🤝', 'ok', 'pop', size=34)}
</section>''')
S('s-sum', T_SUM, T_ROAD)

# ---------- Роҳи тайкарда ----------
LESS = [('📦', 'тағйирёбанда'), ('🔀', 'шарт'), ('🔁', 'давр'), ('📋', 'рӯйхат'), ('⚙️', 'функсия'), ('🗂️', 'объект'), ('🐞', 'дебаг'), ('📓', 'лоиҳа'), ('🧱', 'HTML'), ('🎨', 'CSS'), ('⚡', 'JS'), ('🌐', 'сайт'), ('🤝', 'зеҳни сунъӣ')]
def T(phrase, after=0): return N(W[I(phrase, after)]['t0'])
a_age = T('Дар дарси якум'); a_if = T('Баъд шарт:'); a_loop = T('Баъд давр:', I('Баъд шарт:')); a_list = T('Баъд рӯйхат'); a_fn = T('Функсия — як маротиба'); a_obj = T('Объект — корти'); a_dbg = T('Дебаг — хаторо'); a_prj = T('Лоиҳа — ҳамаро'); a_web = T('эйч-ти-эм-эл, си-эс-эс, джаваскрипт —'); a_site = T('Ва дарси дувоздаҳум'); a_ai = T('Ва ҳоло — ёвар')
times = [a_age, a_if, a_loop, a_list, a_fn, a_obj, a_dbg, a_prj, a_web, a_web + .5, a_web + 1.0, a_site, a_ai]
cards = ''
for i, ((em, nm), tt) in enumerate(zip(LESS, times)):
    r, c = divmod(i, 7)
    cards += f'<div class="card3 {"hl" if i in (0, 12) else ""}" style="left:{60 + c * 168}px;top:{150 + r * 200}px;width:150px;height:170px" {A("pop", tt)}><div class="emo">{em}</div><div class="t" style="font-size:17px;line-height:1.25">{i + 1}<br>{nm}</div></div>'
slides.append(f'''<section class="scene" id="s-road">
{kick(T_ROAD + .1, '19', 'РОҲИ ТАЙКАРДА')}
{cards}
{pill(60, 590, T('Ва дар хотир доред'), '💪 хато — қисми роҳ аст; хатои худатон ёфтаед — беҳтар дар хотир мемонад', 'ok', 'left', size=24)}
</section>''')
S('s-road', T_ROAD, T_END)

slides.append(f'''<section class="scene" id="s-end">
{kick(T_END + .1, 'ДАРСИ 13 / 13', 'ОХИРИ СИЛСИЛА')}
<div class="h1" style="left:60px;top:100px;font-size:88px;line-height:1.05" {A('stamp', T_END + .3)}>ЛОИҲАИ<br>ХУДАТОН</div>
{pill(68, 400, T('Шпаргалкаи бепул'), '📘 Шпаргалка — дар тавсиф', 'ok', 'left', size=28)}
{pill(820, 170, T('Обуна шавед,'), '🔔 Обуна шавед', 'accent', 'pop', size=34)}
{pill(820, 270, T('Обуна шавед,') + .6, '@shahriyor_yunusov', 'left', 'pop', size=26)}
</section>''')
S('s-end', T_END, END + 1)

chapters = [dict(t=0, title='Хук'), dict(t=T_HELP, title='Ёвари ҷавон'), dict(t=T_HOW, title='Зеҳни сунъӣ чӣ тавр кор мекунад?'), dict(t=T_CAN, title='Ёвар чӣ кор карда метавонад?'), dict(t=T_R1, title='Қоидаи 1: дақиқ пурсед'),
            dict(t=T_ANS1, title='Мисол дар IDE: sum ва add'), dict(t=N(332.0), title='Қоидаи 2: кодро хонед ва бифаҳмед'), dict(t=T_R3, title='Қоидаи 3: ҳатман иҷро кунед ва санҷед'), dict(t=T_PROJ, title='Лоиҳаи калон: қадам ба қадам'),
            dict(t=T_IDED, title='Агар хато шуд'), dict(t=T_WARN, title='Огоҳӣ: ба чӣ бовар накунед'), dict(t=T_DEV, title='Барномасоз чӣ кор мекунад?'), dict(t=T_LEARN, title='Чӣ тавр бо зеҳни сунъӣ омӯхтан'),
            dict(t=T_TASK, title='Вазифаҳо ва санҷиш'), dict(t=T_SUM, title='Хулоса ва роҳи тайкарда')]
ide.sort(key=lambda o: o['t']); ptr.sort(key=lambda o: o['t'])

# ---------- субтитры (.srt) ----------
MAP = [(r'индекс нуқта эйч-ти-эм-эл', 'index.html'), (r'джейсон нуқта парс', 'JSON.parse'), (r'эйч-ти-эм-эл', 'HTML'), (r'си-эс-эс', 'CSS'), (r'джаваскрипт', 'JavaScript'), (r'тайпскрипт', 'TypeScript'), (r'пайтон', 'Python'),
       (r'ай-ди-и', 'IDE'), (r'консол лог', 'console.log'), (r'фанкшн', 'function'), (r'риторн', 'return'), (r'нампер', 'Number'), (r'эн-эй-эн', 'NaN'), (r'тайп-эрор', 'TypeError'), (r'андефайнд', 'undefined'), (r'редюс-ро', 'reduce-ро'), (r'редюс', 'reduce'),
       (r'мийона', 'miyona'), (r'ройхат', 'royhat'), (r'рақам', 'raqam'), (r'джам', 'jam'), (r'конст', 'const'), (r'фор', 'for'), (r'оф', 'of'), (r'эд-таск', 'addTask'), (r'комплит-таск', 'completeTask'), (r'шоу-таскс', 'showTasks'), (r'таскс', 'tasks'),
       (r'эвриж-ро', 'average-ро'), (r'эвриж', 'average'), (r'дабл', 'double'), (r'макс', 'max'), (r'сум', 'sum'), (r'эд', 'add'), (r'эйдж-ро', 'age-ро'), (r'текст', 'text'), (r'дан', 'done'), (r'фолс', 'false'), (r'ленгс', 'length'), (r'эй', 'a'), (r'би', 'b'), (r'Энтер-ро', 'Enter-ро')]
def disp(s):
    for a, b in MAP: s = re.sub(r'(?<![\w-])' + a + r'(?![\w-])', b, s)
    return s
caps = []; cur = []
def flush():
    if cur: caps.append(dict(t0=V(cur[0]['t0']), t1=V(cur[-1]['t1']), text=disp(' '.join(w['w'] for w in cur)))); cur.clear()
for w in W:
    cur.append(w)
    if w['w'][-1] in '.!?:' or len(cur) >= 9 or len(' '.join(x['w'] for x in cur)) > 62: flush()
flush()
for a, b in zip(caps, caps[1:]): a['t1'] = min(a['t1'] + .3, b['t0'])

TL = dict(end=END, scenes=scenes, ide=ide, marks=marks, rings=rings, ptr=ptr, chips=chips, zooms=zooms, caps=[], chapters=chapters, cd=[g0])

# ---------- страница ----------
IDE_DIR = os.path.abspath('../../../../public/ide')
src = open(IDE_DIR + '/index.html', encoding='utf8').read()
PTR = '<svg id="ptr" viewBox="0 0 24 24"><path d="M3 2l7.5 19 2.6-7.6L21 11z" fill="#fff" stroke="#111" stroke-width="1.4" stroke-linejoin="round"/></svg>'
inject_head = '<style>' + open('video.css', encoding='utf8').read() + '</style>'
inject_body = '<div id="ovl">' + PTR + '<div id="rip"></div></div>' + ''.join(slides)
src = src.replace('</head>', inject_head + '</head>', 1)
src = src.replace('<div class="app">', inject_body + '<div id="stagewrap"><div class="app">', 1)
src = src.replace('\n<script src="lessons/js.js"></script>\n<script src="lessons/web.js"></script>', '\n</div>\n<script src="file://' + IDE_DIR + '/lessons/js.js"></script>\n<script src="file://' + IDE_DIR + '/lessons/web.js"></script>', 1)
assert 'file://' in src
src = src.replace('function confetti() {', 'function confetti() { return;')
i = src.rindex('</body>')
src = src[:i] + '<script>window.TL=' + json.dumps(TL, ensure_ascii=False) + ';</script><script>' + open('video.js', encoding='utf8').read() + '</script>' + src[i:]
open('video.html', 'w', encoding='utf8').write(src)

sfx = [s for s in sfx if 0 <= s['t'] < END]
json.dump(dict(end=END, sfx=sorted(sfx, key=lambda s: s['t'])), open('sfx.json', 'w'), indent=0)
json.dump(dict(gaps=GAPS, end=END), open('gaps.json', 'w'))
def ts(t): h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60; return f'{h:02}:{m:02}:{int(s):02},{int(round((s % 1) * 1000)) % 1000:03}'
with open('../youtube-lesson-13.srt', 'w', encoding='utf8') as f:
    for k, c in enumerate(caps, 1): f.write(f"{k}\n{ts(c['t0'])} --> {ts(c['t1'])}\n{c['text']}\n\n")
with open('chapters.txt', 'w', encoding='utf8') as f:
    for c in chapters: f.write(f"{int(c['t'] // 60)}:{int(c['t'] % 60):02} {c['title']}\n")
print('END', END, 'scenes', len(scenes), 'ide ops', len(ide), 'sfx', len(sfx))
print(open('chapters.txt').read())
