# Собирает video.html (IDE + слайды + таймлайн), sfx.json, .srt (для YouTube; в видео субтитров НЕТ) и главы для YouTube-урока 12 «Сайт чӣ тавр кор мекунад?»
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
def N(nt): return round(V(nt), 3)          # время повествования -> время видео
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
def zoom(t0, t1, x, y, s): zooms.append(dict(t0=t0, t1=t1, x=x, y=y, s=s))

slides = []
def A(kind, t, o=None, ok='fade'):
    s = f'data-a="{kind};{t}"' + (f' data-o="{o}" data-ok="{ok}"' if o is not None else '')
    if kind in ('pop', 'stamp', 'drop'): sfx.append(dict(name={'pop': 'pop', 'stamp': 'thud', 'drop': 'thud'}[kind], t=t + (.35 if kind == 'drop' else 0), gain=.4))
    return s
def pill(l, t, tt, text, cls='', kind='left', o=None, size=None):
    st = f';font-size:{size}px;padding:14px 26px' if size else ''
    return f'<div style="left:{l}px;top:{t}px" {A(kind, tt, o)}><span class="pill {cls}" style="{st[1:]}">{text}</span></div>'
def node(l, t, w, tt, emoji, title, small='', cls='', o=None, kind='pop'):
    return f'<div class="node {cls}" style="left:{l}px;top:{t}px;width:{w}px" {A(kind, tt, o)}><span class="big">{emoji}</span>{title}<small>{small}</small></div>'
def card(l, t, w, h, tt, emoji, title, body='', cls='', o=None, kind='up'):
    return f'<div class="card3 {cls}" style="left:{l}px;top:{t}px;width:{w}px;height:{h}px" {A(kind, tt, o)}><div class="emo">{emoji}</div><div class="t">{title}</div><div class="u">{body}</div></div>'
def cc(l, t, tt, text, size=26, kind='pop', o=None, extra=''):
    return f'<div class="codechip" style="left:{l}px;top:{t}px;font-size:{size}px;{extra}" {A(kind, tt, o)}>{text}</div>'
def h2(l, t, tt, text, size=46, o=None): return f'<div class="h2" style="left:{l}px;top:{t}px;font-size:{size}px" {A("up", tt, o)}>{text}</div>'
def kick(tt, num, text): return f'<div class="kicker" {A("down", tt)}><b>{num}</b>{text}</div>'
def arrow(l, t, tt, text='→', size=44, o=None, color='var(--purple)'): return f'<div class="mono" style="left:{l}px;top:{t}px;font-size:{size}px;color:{color}" {A("pop", tt, o)}>{text}</div>'

# ---------- границы сцен (время повествования -> видео) ----------
T_REST = N(40.2); T_URL = N(98.0); T_DNS = N(166.9); T_REQ = N(219.3); T_IDE1 = N(229.1); T_GP = N(246.6); T_SRV = N(273.7); T_IDE2 = N(289.6); T_STAT = N(354.2)
T_THREE = N(393.9); T_FB = N(458.6); T_LIKE = N(518.0); T_IDE3 = N(549.6); T_SLOW = N(598.0); T_HTTPS = N(649.2); T_ERR = N(681.3); T_REC = N(724.7); T_TASK = N(786.0); T_SUM = N(861.2); T_NEXT = N(907.8)

# ---------- 0. Хук ----------
slides.append(f'''<section class="scene" id="s-hook">
{kick(.2, 'ДАРСИ 12', 'БАРНОМАСОЗӢ АЗ СИФР · JAVASCRIPT')}
<div class="h1" style="left:60px;top:70px;font-size:96px;line-height:1.05" {A('stamp', .6)}>САЙТ ЧӢ ТАВР<br>КОР МЕКУНАД?</div>
<div style="left:60px;top:290px;width:640px;height:300px;border-radius:16px;background:#2D2D30;border:1px solid #3C3C3C;box-shadow:0 20px 60px rgba(0,0,0,.45);overflow:hidden" {A('up', 1.2)}>
  <div style="background:#3a3a3d;padding:10px 14px;display:flex;gap:10px;align-items:center"><span style="color:#8B949E;font:600 16px Inter">🔒</span><span class="mono" style="background:#1E1E1E;border-radius:999px;padding:8px 18px;color:#fff;font-size:22px;min-width:360px" data-tw="{N(1.8)};2.2" data-text="yunusov.tj"></span><span style="margin-left:auto" {A('pop', N(4.6))}><span class="pill accent" style="font-size:18px;padding:6px 14px">Enter ↵</span></span></div>
  <div style="padding:34px 30px" {A('up', N(6.4))}><div style="font:800 44px Inter;color:#fff">Салом!</div><div style="font:600 22px Inter;color:#8B949E;margin-top:10px">Ман барномасоз мешавам.</div></div>
</div>
{pill(730, 300, N(8.0), '⏱ ≈ як лаҳза', 'ok', 'pop', size=28)}
{pill(730, 380, N(9.5), '❓ даҳҳо қадам дар ин лаҳза', 'err', 'pop', size=26)}
{pill(730, 450, N(15.0), '📍 суроға · домен', 'left', 'left', size=22)}
{pill(730, 504, N(18.4), '🖥️ сервер · 📨 ҷавоб', 'left', 'left', size=22)}
{pill(730, 558, N(21.0), '📄 се файл аз дарси 11', 'left', 'left', size=22)}
{cc(730, 618, N(25.0), 'function server(req) { … }', 24)}
{pill(60, 640, N(36.4), '🎯 Дар охир: санҷиши нав', 'accent', 'pop')}
</section>''')
S('s-hook', 0, T_REST)

# ---------- 1. Ресторан ----------
slides.append(f'''<section class="scene" id="s-rest">
{kick(T_REST + .1, '01', 'ОБРАЗИ РЕСТОРАН')}
{h2(60, 90, T_REST + .5, 'Дар ресторан нишастаед…', 46, N(71.7))}
{node(60, 190, 330, N(40.8), '🙋', 'меҳмон', 'шумо', o=N(71.7))}
{node(475, 190, 330, N(46.4), '🛎️', 'официант', 'мебарад ва меорад', o=N(71.7))}
{node(890, 190, 330, N(43.6), '🧑‍🍳', 'ошхона', 'ош мепазад', o=N(71.7))}
<div class="mono" style="left:402px;top:230px;font-size:42px;color:var(--purple)" {A('pop', N(48.4), N(71.7))}>→</div>
<div class="mono" style="left:818px;top:230px;font-size:42px;color:var(--purple)" {A('pop', N(48.9), N(71.7))}>→</div>
{pill(60, 400, N(53.8), '🌐 меҳмон = браузер (клиент)', 'accent', 'left', N(71.7))}
{pill(60, 470, N(60.8), '🖥️ ошхона = сервер', 'accent', 'left', N(71.7))}
{pill(60, 540, N(67.1), '🛎️ официант = интернет', 'accent', 'left', N(71.7))}
<div style="left:560px;top:420px" {A('pop', N(46.7), N(52.0))}><span class="pill" style="font-size:26px;padding:14px 26px">💬 «Ман ошро мехоҳам»</span></div>
<div class="h2" style="left:60px;top:90px;font-size:46px" {A('up', N(71.9), N(86.8))}>Ду калимаи асосӣ</div>
{card(60, 200, 560, 260, N(73.8), '❓', 'ДАРХОСТ', 'вақте ки браузер чизе мепурсад', 'hl', N(86.8))}
{card(660, 200, 560, 260, N(77.2), '📦', 'ҶАВОБ', 'вақте ки сервер чизе медиҳад', 'hl', N(86.8))}
<div style="left:60px;top:520px" {A('stamp', N(83.1), N(86.8))}><span class="pill accent" style="font-size:34px;padding:18px 36px">сайт = дархост + ҷавоб</span></div>
<div class="h2" style="left:60px;top:90px;font-size:46px" {A('up', N(87.0))}>Ёдатон ҳаст дарси 11?</div>
{cc(60, 230, N(89.1), '<span class="t">index.html</span>', 30)}
{cc(60, 310, N(90.6), '<span class="t">style.css</span>', 30)}
{cc(60, 390, N(92.0), '<span class="t">script.js</span>', 30)}
{pill(60, 500, N(93.3), '📨 ҳамин се файл дар ҷавоб меоянд', 'ok', 'left', size=26)}
</section>''')
S('s-rest', T_REST, T_URL)

# ---------- 2. Суроға ----------
URLX = 90
slides.append(f'''<section class="scene" id="s-url">
{kick(T_URL + .1, '02', 'СУРОҒА')}
{h2(60, 90, T_URL + .5, 'Суроға аз чанд қисм иборат аст', 44)}
<div class="codechip" style="left:60px;top:190px;font-size:46px;padding:22px 30px;white-space:nowrap" {A('up', N(100.5))}>
 <span style="color:var(--kw)" {A('fade', N(108.2))}>https://</span><span style="color:var(--str)" {A('fade', N(111.0))}>yunusov.tj</span><span style="color:var(--fn)" {A('fade', N(114.6))}>/ide/</span><span style="color:var(--teal)" {A('fade', N(150.9))}>#dars-12</span></div>
<div style="left:90px;top:298px;width:221px;text-align:center" {A('up', N(117.9))}><span class="pill" style="font-size:22px;border-color:var(--kw)">протокол</span></div>
<div style="left:311px;top:298px;width:276px;text-align:center" {A('up', N(132.2))}><span class="pill" style="font-size:22px;border-color:var(--str)">домен</span></div>
<div style="left:587px;top:298px;width:138px;text-align:center" {A('up', N(139.2))}><span class="pill" style="font-size:22px;border-color:var(--fn)">роҳ</span></div>
<div style="left:725px;top:298px;width:221px;text-align:center" {A('up', N(150.9))}><span class="pill" style="font-size:22px;border-color:var(--teal)">ҳаш</span></div>
{pill(60, 372, N(122.0), '💬 «забон»-и гуфтугӯ: бо кадом қоидаҳо', 'left', 'left', N(127.4), 22)}
{pill(60, 372, N(127.6), '🔒 s — бехатар (баъд мегӯем)', 'ok', 'left', N(132.0), 22)}
{pill(60, 372, N(136.4), '🏙️ номи сайт, мисли номи шаҳр', 'left', 'left', N(139.0), 22)}
{pill(60, 372, N(142.2), '📍 ҷои дақиқ: мисли кӯча ва хона', 'left', 'left', N(147.0), 22)}
{pill(60, 372, N(147.2), '🏠 роҳ нест → саҳифаи асосӣ', 'ok', 'left', N(150.8), 22)}
{pill(60, 372, N(156.0), '↘ ба сервер намеравад: браузер худаш', 'left', 'left', N(159.5), 22)}
{card(60, 450, 360, 200, N(160.2), '🏙️', 'шаҳр', '= домен', '')}
{card(450, 450, 360, 200, N(162.4), '🛣️', 'кӯча', '= роҳ', '')}
{card(840, 450, 360, 200, N(163.7), '🏠', 'хона', '= саҳифа ё файл', '')}
<div style="left:850px;top:372px" {A('stamp', N(164.6))}><span class="pill accent" style="font-size:24px">аз бузург ба хурд</span></div>
</section>''')
S('s-url', T_URL, T_DNS)

# ---------- 3. Домен ва DNS ----------
slides.append(f'''<section class="scene" id="s-dns">
{kick(T_DNS + .1, '03', 'ДОМЕН ВА DNS')}
{h2(60, 90, T_DNS + .5, 'Номҳо ≠ рақамҳо', 46, N(188.8))}
{pill(60, 200, N(168.3), '🧠 компютерҳо номҳоро намефаҳманд', 'err', 'left', N(188.8), 26)}
{pill(60, 272, N(170.6), '🔢 онҳо танҳо рақамҳоро мефаҳманд', 'ok', 'left', N(188.8), 26)}
{cc(60, 360, N(173.0), '203.0.113.10', 54, 'pop', N(188.8))}
{pill(60, 470, N(173.4), 'IP — суроғаи рақамии сервер (мисол)', 'left', 'left', N(188.8), 24)}
{pill(60, 536, N(182.8), '😮‍💨 IP-ро ёд кардан душвор', 'err', 'left', N(188.8), 24)}
{pill(60, 602, N(185.6), '🏷️ домен — барои одам', 'ok', 'left', N(188.8), 24)}
<div class="h2" style="left:60px;top:90px;font-size:46px" {A('up', N(189.0))}>Пеш аз дархост — як савол</div>
{node(60, 210, 300, N(189.4), '🌐', 'браузер', '')}
{node(490, 210, 300, N(194.5), '📖', 'DNS', 'китоби телефон')}
{node(920, 210, 300, N(204.2), '🖥️', 'сервер', '203.0.113.10')}
<div style="left:70px;top:420px" {A('pop', N(192.3))}><span class="pill" style="font-size:24px">❓ yunusov.tj = ?</span></div>
<div style="left:420px;top:420px" {A('pop', N(202.0))}><span class="pill ok" style="font-size:24px">💬 203.0.113.10</span></div>
{arrow(372, 256, N(192.6), '→', 44)}
{arrow(802, 256, N(204.3), '→', 44)}
{pill(60, 510, N(200.0), '📖 ном медиҳед — рақам мегиред', 'accent', 'left', size=26)}
{pill(60, 580, N(207.4), '⏱ қадами 1 — як миллисония нагузашта', 'left', 'left', size=22)}
<div style="left:700px;top:580px" {A('stamp', N(212.5))}><span class="pill ok" style="font-size:24px">домен → одам · рақам → компютер</span></div>
</section>''')
S('s-dns', T_DNS, T_REQ)

# ---------- 4. Дархост ----------
slides.append(f'''<section class="scene" id="s-req">
{kick(T_REQ + .1, '04', 'ДАРХОСТ')}
{h2(60, 90, T_REQ + .5, 'Дархост — паёми браузер ба сервер', 44)}
{node(60, 230, 280, T_REQ + 1.0, '🌐', 'браузер', '')}
{arrow(360, 280, N(221.8), '✉️ →', 50)}
{node(540, 230, 280, N(222.4), '🖥️', 'сервер', '')}
{card(60, 450, 540, 170, N(225.4), '🛠️', 'усул (method)', 'чӣ мехоҳем', 'hl')}
{card(640, 450, 540, 170, N(227.0), '📍', 'роҳ (url)', 'аз куҷо', 'hl')}
</section>''')
S('s-req', T_REQ, T_IDE1)

# ---------- IDE: объект request ----------
S('ide', T_IDE1, T_GP)
setc(T_IDE1, ''); clear(T_IDE1)
chip(T_IDE1 + .1, T_IDE1 + 2.2, '<span>💻</span><div>Дархост — объект<small>05 · дарси 6</small></div>', 'card')
REQ = 'let request = { method: "GET", url: "/" };'
typ(N(234.5), REQ, 5.0)
MK(N(238.3), N(242.2), 'method', 'усул — чӣ мехоҳем', 'c')
MK(N(244.3), N(246.4), 'url', 'роҳ — аз куҷо', 'g', 'below')

# ---------- GET / POST ----------
slides.append(f'''<section class="scene" id="s-gp">
{kick(T_GP + .1, '05', 'GET ВА POST')}
{h2(60, 90, T_GP + .5, 'Ду усули асосӣ', 46)}
{card(60, 200, 560, 330, N(248.5), '📥', 'GET — «ба ман деҳ»', 'саҳифа мекушоем, сурат мебинем', 'hl')}
{card(660, 200, 560, 330, N(254.2), '📤', 'POST — «ман мефиристам»', 'шакл, тугмаи «Лайк»', 'hl')}
{cc(90, 400, N(250.4), 'GET /', 30)}
{cc(690, 400, N(264.9), 'POST /like', 30)}
{pill(690, 470, N(257.0), '📝 шакл → «Фиристодан»', 'left', 'left', size=22)}
{pill(90, 470, N(250.8), '🖼️ сурат · 📄 саҳифа', 'left', 'left', size=22)}
<div style="left:60px;top:580px" {A('stamp', N(270.0))}><span class="pill accent" style="font-size:30px;padding:16px 32px">GET — мегирем · POST — мефиристем</span></div>
</section>''')
S('s-gp', T_GP, T_SRV)

# ---------- 5. Сервер: намуна ----------
slides.append(f'''<section class="scene" id="s-srv">
{kick(T_SRV + .1, '06', 'СЕРВЕР ДАРХОСТРО МЕГИРАД')}
{h2(60, 90, T_SRV + .5, 'Сервер дархостро гирифт', 46)}
{node(60, 220, 330, N(274.0), '🖥️', 'сервер', 'ҷавоб тайёр мекунад…')}
{cc(450, 250, N(275.2), 'GET /about', 34)}
{arrow(410, 252, N(275.0), '←', 44)}
{pill(60, 420, N(278.0), '🏢 сервери воқеӣ — барномаи калон', 'left', 'left', size=26)}
{pill(60, 490, N(281.3), '🧪 мо — намунаи хурд бо JavaScript', 'ok', 'left', size=26)}
<div style="left:60px;top:580px" {A('stamp', N(286.2))}><span class="pill accent" style="font-size:28px;padding:16px 32px">сервери воқеӣ нест — аммо принсип ҳамон</span></div>
</section>''')
S('s-srv', T_SRV, T_IDE2)

# ---------- IDE: функсияи server ----------
S('ide', T_IDE2, T_STAT)
SV0 = 'function server(req) {\n}'
SV1 = 'function server(req) {\n  if (req.url === "/") {\n    return { status: 200, body: "<h1>Салом!</h1>" };\n  }\n}'
SV2 = 'function server(req) {\n  if (req.url === "/") {\n    return { status: 200, body: "<h1>Салом!</h1>" };\n  }\n  if (req.url === "/about") {\n    return { status: 200, body: "<p>Ман барномасоз мешавам.</p>" };\n  }\n}'
SV3 = 'function server(req) {\n  if (req.url === "/") {\n    return { status: 200, body: "<h1>Салом!</h1>" };\n  }\n  if (req.url === "/about") {\n    return { status: 200, body: "<p>Ман барномасоз мешавам.</p>" };\n  }\n  return { status: 404, body: "Саҳифа ёфт нашуд" };\n}'
setc(T_IDE2, SV0 and ''); clear(T_IDE2)
chip(T_IDE2 + .1, T_IDE2 + 2.0, '<span>🖥️</span><div>Сервери намунавӣ<small>06 · function, if, return</small></div>', 'card')
typ(N(291.3), SV0, 2.4)
typ(N(296.0), SV1, 9.0); MK(N(297.0), N(301.8), 'req.url', 'роҳи дархост', 'c'); MK(N(302.3), N(306.0), 'return', 'return — ҷавоб', 'g', 'below'); MK(N(304.2), N(308.4), 'status', 'статус-код', 'y')
typ(N(309.9), SV2, 8.0); MK(N(310.4), N(316.0), '"/about"', 'роҳи дуюм', 'c', 'below')
typ(N(320.4), SV3, 6.5); MK(N(323.8), N(327.8), '404', 'ёфт нашуд', 'r', 'below')
chip(N(327.9), N(335.5), '<span class="big">↩️</span><div>return — ҷавоб бармегардонад<small>(дарси 5)</small></div>', 'card')
QUERY1 = SV3 + '\nconsole.log(server({ method: "GET", url: "/" }));'
typ(N(337.0), QUERY1, 4.6)
run(N(341.9) + .2)
ring(N(342.8), N(346.8), '#out', '✅ status 200', 'g', 2)
QUERY2 = SV3 + '\nconsole.log(server({ method: "GET", url: "/shop" }));'
typ(N(348.2), QUERY2, 1.6)
clear(N(350.0))
run(N(350.6) + .2)
ring(N(351.4), N(354.0), '#out', '⚠️ 404', 'r', 2)

# ---------- статус-код ----------
slides.append(f'''<section class="scene" id="s-stat">
{kick(T_STAT + .1, '07', 'СТАТУС-КОД')}
{h2(60, 90, T_STAT + .5, 'Дар ҷавоб ҳамеша як рақам ҳаст', 44)}
{card(60, 190, 275, 300, N(361.5), '✅', '200', 'ҳамааш хуб', 'hl')}
{card(355, 190, 275, 300, N(363.2), '🔍', '404', 'саҳифа ёфт нашуд: суроға нодуруст ё файл нест', '')}
{card(650, 190, 275, 300, N(368.4), '🔥', '500', 'хатои худи сервер — хатои ошхона', '')}
{card(945, 190, 275, 300, N(376.8), '↪️', '301', 'саҳифа ба ҷои дигар гузашт — браузер худаш меравад', '')}
<div style="left:60px;top:540px" {A('stamp', N(388.6))}><span class="pill accent" style="font-size:28px;padding:16px 32px">404 — танҳо ҷавоби сервер: «Чунин чизе надорам»</span></div>
</section>''')
S('s-stat', T_STAT, T_THREE)

# ---------- 6. Се файл ва F12 ----------
slides.append(f'''<section class="scene" id="s-three">
{kick(T_THREE + .1, '08', 'БРАУЗЕР ҶАМЪ МЕКУНАД')}
{h2(60, 90, T_THREE + .5, 'Се файл — як саҳифа', 46, N(429.8))}
{node(60, 200, 300, N(394.5), '🌐', 'браузер', '', o=N(429.8))}
{node(920, 200, 300, N(395.0), '🖥️', 'сервер', '', o=N(429.8))}
{pill(400, 215, N(399.9), '← index.html', 'ok', 'left', N(429.8), 28)}
{cc(400, 290, N(408.2), '&lt;link href="<span class="s">style.css</span>"&gt;', 24, 'pop', N(429.8))}
{cc(400, 350, N(409.8), '&lt;script src="<span class="s">script.js</span>"&gt;', 24, 'pop', N(429.8))}
{pill(400, 430, N(413.4), '→ style.css? → script.js?', 'accent', 'left', N(429.8), 26)}
{pill(400, 500, N(416.3), '← style.css ← script.js', 'ok', 'left', N(429.8), 26)}
{pill(60, 590, N(421.2), '🧱 HTML — деворҳо', 'left', 'left', N(429.8), 22)}
{pill(430, 590, N(422.8), '🎨 CSS — ранг', 'left', 'left', N(429.8), 22)}
{pill(740, 590, N(424.8), '⚡ JS — барқ', 'left', 'left', N(429.8), 22)}
<div style="left:960px;top:590px" {A('stamp', N(427.7), N(429.8))}><span class="pill ok" style="font-size:22px">саҳифаи зинда 🏠</span></div>
<div class="h2" style="left:60px;top:90px;font-size:46px" {A('up', N(429.9))}>F12 → Network</div>
<div style="left:60px;top:170px;width:1160px;height:330px;background:#1E1E1E;border:1px solid #3C3C3C;border-radius:14px;box-shadow:0 20px 60px rgba(0,0,0,.5);overflow:hidden" {A('up', N(431.2))}>
 <div style="display:flex;gap:26px;padding:12px 20px;background:#2D2D30;color:#8B949E;font:700 18px Inter"><span style="color:#fff">Elements</span><span>Console</span><span style="color:#BD93F9;border-bottom:3px solid #BD93F9">Network</span></div>
 <div style="display:grid;grid-template-columns:2.2fr 1fr 1fr 1fr;padding:12px 20px;color:#8B949E;font:700 17px Inter;border-bottom:1px solid #3C3C3C"><span>Name</span><span>Status</span><span>Size</span><span>Time</span></div>
 <div style="display:grid;grid-template-columns:2.2fr 1fr 1fr 1fr;padding:16px 20px;font:600 22px var(--mono);border-bottom:1px solid #2d2d30" {A('fade', N(436.4))}><span style="color:var(--teal)">index.html</span><span style="color:#4EC9B0">200</span><span>…</span><span>…</span></div>
 <div style="display:grid;grid-template-columns:2.2fr 1fr 1fr 1fr;padding:16px 20px;font:600 22px var(--mono);border-bottom:1px solid #2d2d30" {A('fade', N(437.6))}><span style="color:var(--teal)">style.css</span><span style="color:#4EC9B0">200</span><span>…</span><span>…</span></div>
 <div style="display:grid;grid-template-columns:2.2fr 1fr 1fr 1fr;padding:16px 20px;font:600 22px var(--mono)" {A('fade', N(438.6))}><span style="color:var(--teal)">script.js</span><span style="color:#4EC9B0">200</span><span>…</span><span>…</span></div>
</div>
<div style="left:60px;top:530px" {A('pop', N(444.1))}><span class="pill err" style="font-size:24px">🧪 схема — намунавӣ; ҳақиқиашро дар браузери худатон мебинед</span></div>
<div style="left:60px;top:600px" {A('pop', N(450.0))}><span class="pill accent" style="font-size:26px">⌨️ F12 — «рентген»-и ҳар сайт</span></div>
</section>''')
S('s-three', T_THREE, T_FB)

# ---------- 7. Фронтенд ва бекенд ----------
slides.append(f'''<section class="scene" id="s-fb">
{kick(T_FB + .1, '09', 'ФРОНТЕНД ВА БЕКЕНД')}
{h2(60, 90, T_FB + .5, 'Дар ресторан: зал ва ошхона', 46)}
{card(60, 190, 560, 340, N(462.6), '🙋', 'ЗАЛ → фронтенд', 'он чизе, ки мебинед ва пахш мекунед', 'hl')}
{card(660, 190, 560, 340, N(480.6), '🧑‍🍳', 'ОШХОНА → бекенд', 'он чизе, ки намебинед', '')}
{cc(90, 400, N(473.6), '<span class="t">HTML</span> · <span class="t">CSS</span> · <span class="f">JS</span>', 26)}
{pill(90, 470, N(477.5), 'дар браузер', 'ok', 'left', size=22)}
{pill(690, 350, N(484.1), '📨 қабули дархост', 'left', 'left', size=22)}
{pill(690, 404, N(485.8), '🧮 ҳисоб (масалан лайк)', 'left', 'left', size=22)}
{pill(690, 458, N(488.0), '🗄️ база: нигоҳ доштани маълумот', 'left', 'left', size=22)}
<div style="left:60px;top:570px" {A('stamp', N(497.9))}><span class="pill accent" style="font-size:28px;padding:16px 32px">JavaScript — ҳам дар браузер, ҳам дар сервер</span></div>
<div style="left:960px;top:640px" {A('pop', N(514.3))}><span class="pill ok" style="font-size:26px">full-stack 🧑‍💻</span></div>
</section>''')
S('s-fb', T_FB, T_LIKE)

# ---------- 8. Сайти зинда: JSON ----------
slides.append(f'''<section class="scene" id="s-like">
{kick(T_LIKE + .1, '10', 'САЙТИ ЗИНДА')}
{h2(60, 90, T_LIKE + .5, 'Тугмаи «Лайк» чӣ тавр кор мекунад?', 44)}
{pill(60, 220, N(520.2), '📄 саҳифаи оддӣ — ҳамеша як хел', 'left', 'left', N(527.5), 26)}
{node(60, 230, 300, N(527.7), '👍', 'Лайк', '25', 'hl')}
{arrow(380, 290, N(529.0), '→', 46)}
{cc(450, 285, N(531.0), 'POST /like', 28)}
{arrow(760, 290, N(532.4), '→', 46)}
{node(850, 230, 300, N(534.5), '🖥️', 'сервер', 'лайкро менависад')}
{cc(450, 430, N(538.0), '{"likes": 26, "liked": true}', 30)}
{arrow(380, 440, N(537.8), '←', 46)}
{pill(60, 540, N(541.5), '📝 JSON — матн бо қоидаи махсус', 'accent', 'left', size=26)}
{pill(60, 610, N(546.0), '🧩 JSON = объект, танҳо дар шакли матн (дарси 6)', 'ok', 'left', size=24)}
</section>''')
S('s-like', T_LIKE, T_IDE3)

S('ide', T_IDE3, T_SLOW)
setc(T_IDE3, ''); clear(T_IDE3)
chip(T_IDE3 + .1, T_IDE3 + 2.0, '<span>🧩</span><div>JSON дар IDE<small>07 · parse ва stringify</small></div>', 'card')
J1 = 'let answer = \'{"likes": 25, "liked": false}\';'
J2 = J1 + '\nlet data = JSON.parse(answer);'
J3 = J2 + '\nconsole.log(data.likes);'
J4 = J3 + '\ndata.likes = data.likes + 1;\ndata.liked = true;'
J5 = J4 + '\nconsole.log(JSON.stringify(data));'
typ(N(551.2), J1, 5.2); MK(N(553.6), N(557.6), '"likes"', 'матн аз сервер', 'c', 'below')
typ(N(560.3), J2, 4.4); MK(N(564.0), N(568.0), 'JSON.parse', 'матн → объект', 'g')
typ(N(568.2), J3, 3.2)
run(N(571.4))
ring(N(571.8), N(573.2), '#out', '✅ 25', 'g', 2)
typ(N(573.5), J4, 6.2); MK(N(574.0), N(580.0), 'data.likes + 1', 'плюс як', 'y', 'below')
typ(N(580.8), J5, 3.6); MK(N(582.7), N(585.0), 'JSON.stringify', 'объект → матн', 'c')
run(N(585.0) + .2)
ring(N(585.8), N(598.0), '#out', '✅ likes 26', 'g', 2)
chip(N(588.8), N(596.0), '<span class="big">📦</span><div>25 → 26<small>қуттии дарси 1 — ҳоло «лайк»</small></div>', 'card', 'top:330px')

# ---------- 9. Чаро гоҳо суст ----------
slides.append(f'''<section class="scene" id="s-slow">
{kick(T_SLOW + .1, '11', 'ЧАРО ГОҲО САЙТ СУСТ МЕКУШОЯД?')}
{h2(60, 90, T_SLOW + .5, 'Ба назар як лаҳза, аммо…', 46)}
{card(60, 200, 360, 300, N(611.8), '📏', 'сервер дур аст', 'ҷавоб мисли нома: ҳар қадар дуртар, ҳамон қадар дертар', '')}
{card(450, 200, 360, 300, N(619.8), '🖼️', 'файлҳо калон', 'як сурати вазнин аз даҳҳо саҳифаи матн вазнинтар', '')}
{card(840, 200, 360, 300, N(629.6), '🍽️', 'меҳмонҳо бисёр', 'ресторан пур: сервер ба садҳо ҳазор нафар ҷавоб медиҳад', '')}
{pill(60, 560, N(625.8), '🗜️ суратҳоро хурд мекунанд', 'ok', 'left', size=24)}
{pill(60, 620, N(639.0), '🌍 нусха дар шаҳрҳои гуногун — ба меҳмон наздиктар', 'accent', 'left', size=24)}
</section>''')
S('s-slow', T_SLOW, T_HTTPS)

# ---------- 10. HTTPS ----------
slides.append(f'''<section class="scene" id="s-https">
{kick(T_HTTPS + .1, '12', 'ҚУЛФ ДАР СУРОҒА')}
{h2(60, 90, T_HTTPS + .5, 'http ва https', 46)}
{card(60, 190, 560, 300, N(652.3), '📮', 'http — открытка', 'ҳар кас аз паҳлӯ хонда метавонад', '')}
{card(660, 190, 560, 300, N(661.6), '✉️', 'https — конверти пӯшида', 'танҳо сервер мекушояд', 'hl')}
{cc(90, 400, N(653.0), 'http://…', 28)}
{cc(690, 400, N(662.4), '🔒 https://…', 28)}
{pill(60, 540, N(669.2), '🔑 рамз · рақами корт — танҳо дар сайтҳои бо 🔒', 'ok', 'left', size=26)}
{pill(60, 608, N(676.9), '⚠️ қулф нест — маълумоти муҳим ворид накунед', 'err', 'left', size=26)}
</section>''')
S('s-https', T_HTTPS, T_ERR)

# ---------- 11. Хатогиҳо ----------
slides.append(f'''<section class="scene" id="s-err">
{kick(T_ERR + .1, '13', 'СЕ ХАТОИ МАЪМУЛ')}
{card(60, 115, 1160, 175, N(684.4), '1️⃣', '«Сайти ман дар компютери ман аст — пас ҳама мебинанд»', '✅ Не: файлҳо бояд дар сервер бошанд', 'hl')}
{card(60, 310, 1160, 175, N(696.3), '2️⃣', '«404 — сайт вайрон шуд»', '✅ Аксар вақт: суроға нодуруст аст ё файл дар ҷои дигар', 'hl')}
{card(60, 505, 1160, 175, N(707.4), '3️⃣', 'Ном ва роҳ дақиқ навишта мешаванд', '✅ <span class="mono">/about</span> ≠ <span class="mono">/About</span> — сервер онҳоро ду чизи гуногун мешуморад', 'hl')}
</section>''')
S('s-err', T_ERR, T_REC)

# ---------- 12. Ҳафт қадам ----------
def step(l, t, tt, n, emoji, title, small): return card(l, t, 275, 190, tt, emoji, f'{n} · {title}', small, 'hl' if n in (1, 7) else '')
slides.append(f'''<section class="scene" id="s-rec">
{kick(T_REC + .1, '14', 'РОҲИ ЯК ДАРХОСТ')}
{h2(60, 80, T_REC + .5, 'Ҳафт қадам — як лаҳза', 44)}
{step(60, 160, N(734.5), 1, '📍', 'суроға', 'протокол · домен · роҳ')}
{step(355, 160, N(741.3), 2, '📖', 'DNS', 'ном → рақам')}
{step(650, 160, N(746.1), 3, '📨', 'дархост', 'GET + роҳ')}
{step(945, 160, N(752.1), 4, '🖥️', 'сервер', 'ҷавоб тайёр мекунад')}
{step(60, 370, N(757.1), 5, '📦', 'ҷавоб', 'статус 200 + index.html')}
{step(355, 370, N(765.3), 6, '📎', 'файлҳо', 'style.css + script.js')}
{step(650, 370, N(774.7), 7, '🏠', 'саҳифа', 'браузер ҷамъ мекунад')}
<div style="left:945px;top:400px;width:275px" {A('stamp', N(782.4))}><span class="pill accent" style="font-size:24px;padding:14px 22px">7 қадам — як лаҳза ⚡</span></div>
{pill(60, 600, N(778.6), '👆 тугмаро пахш кунед — дархости нав сар мешавад', 'ok', 'left', size=24)}
</section>''')
S('s-rec', T_REC, T_TASK)

# ---------- 13. Вазифаҳо ва санҷиш (IDE) ----------
S('ide', T_TASK, T_SUM)
chip(T_TASK + .1, N(788.4), '<span>🎯</span><div>Вазифаҳо барои шумо<small>08 · дарси 12 дар IDE</small></div>', 'card')
goto(N(788.7), 'l12', 0)
ST1 = 'function server(req) {\n  if (req.url === "/") {\n    return { status: 200, body: "<h1>Салом!</h1>" };\n  }\n  if (req.url === "/about") {\n    return { status: 200, body: "<p>Ман барномасоз мешавам.</p>" };\n  }\n  // роҳи /contact-ро илова кунед\n  return { status: 404, body: "Саҳифа ёфт нашуд" };\n}\n'
SO1 = ST1.replace('  // роҳи /contact-ро илова кунед\n', '  if (req.url === "/contact") {\n    return { status: 200, body: "Телефон" };\n  }\n')
setc(N(788.8), ST1)
ring(N(791.4), N(793.0), '#side', '📘 назария', 'c', 4)
ring(N(793.0), N(801.2), '#task', 'Вазифаи 1', 'y', 4)
typ(N(794.4), SO1, 5.0)
click(N(801.5), '#side button[data-i="1"]')
ST2 = 'let text = \'{"name": "Нигина", "age": 25}\';\n\n// JSON.parse ва console.log\n'
setc(N(801.55), ST2)
ring(N(801.8), N(810.3), '#task', 'Вазифаи 2', 'y', 4)
typ(N(803.4), 'let text = \'{"name": "Нигина", "age": 25}\';\nlet data = JSON.parse(text);\nconsole.log(data.name);\n', 4.4)
click(N(810.6), '#side button[data-i="2"]')
ST3 = 'function server(req) {\n  if (req.url === "/") {\n    return { status: 200, body: "<h1>Салом!</h1>" };\n  }\n  // ба роҳи номаълум ҷавоб илова кунед\n}\nconsole.log(server({ method: "GET", url: "/xyz" }).status);\n'
SO3 = ST3.replace('  // ба роҳи номаълум ҷавоб илова кунед\n', '  return { status: 404, body: "Саҳифа ёфт нашуд" };\n')
setc(N(810.65), ST3)
ring(N(810.9), N(818.0), '#task', 'Вазифаи 3', 'y', 4)
typ(N(812.4), SO3, 3.8)
chip(N(818.3), N(834.6), '<span class="big">🧠</span><div>аввал фикр кунед, баъд иҷро<small>қоғаз ё дар ақл: сервер ба ҳар роҳ кадом статус медиҳад?</small></div>', 'card', 'top:300px')
ring(N(831.0), N(832.4), '#check', '✓ Санҷиш', 'c', 6)
click(N(832.6), '#check', 'check'); sfx.append(dict(name='chime', t=N(833.6), gain=.6))
ring(N(833.8), N(835.3), '#checks', '', 'g', 4)

# ---------- санҷиш (квиз) ----------
t_q = N(835.5)
goto(t_q + .02, 'free', 0)
QB = SV3
setc(t_q + .12, QB); clear(t_q + .12)
Q1 = QB + '\nconsole.log(server({ method: "GET", url: "/contact" }).status);'
typ(N(839.5), Q1, 6.0)
MK(N(846.6), N(848.0), '"/contact"', '❓ чӣ чоп мешавад?', 'y', 'below')
g0 = V(GAP_Q) - PAUSE
qbody = lambda sub: f'<div>server({{ GET, "/contact" }}).status?<small>{sub}</small></div>'
chip(N(847.9), g0 - .3, '<span class="big">❓</span>' + qbody('видеоро пауза кунед ✍️'), 'card')
for k in range(5):
    chip(g0 + k + .02, g0 + k + .62, f'<span class="big">{5 - k}</span>' + qbody('фикр кунед · баъд ҷавобро мебинем ✅'), 'card')
    sfx.append(dict(name='tick', t=g0 + k, gain=.8))
run(N(851.3) + .3)
ring(N(852.4), N(860.8), '#out', '✅ 404', 'g', 2)
chip(N(853.6), N(860.6), '<div>роҳи <span class="mono">/contact</span> нест → охирин <span class="mono">return</span><small>«Саҳифа ёфт нашуд»</small></div>', 'card', 'top:620px')

# ---------- 14. Хулоса ----------
slides.append(f'''<section class="scene" id="s-sum">
{kick(T_SUM + .2, '15', 'ХУЛОСА')}
{h2(60, 80, T_SUM + .6, 'Сайт = <span class="acc">дархост + ҷавоб</span>', 50)}
{pill(60, 190, N(862.5), '📍 суроға: протокол · домен · роҳ', 'left', 'left', size=26)}
{pill(60, 256, N(866.7), '📖 DNS: домен → рақам', 'left', 'left', size=26)}
{pill(60, 322, N(870.0), '📨 дархост: GET — мегирад · POST — мефиристад', 'left', 'left', size=26)}
{pill(60, 388, N(875.7), '📦 ҷавоб + статус-код: 200 · 404 · 500', 'left', 'left', size=26)}
{pill(60, 454, N(882.1), '🧩 ҷавоб — се файл ё маълумот (JSON)', 'left', 'left', size=26)}
<div style="left:60px;top:540px" {A('stamp', N(886.4))}><span class="pill accent" style="font-size:32px;padding:18px 36px">Ин ҳамаи он чизест, ки дар паси ҳар сайт меистад</span></div>
{pill(60, 624, N(892.5), '🧱 дарси 11: саҳифа сохтем · дарси 12: чӣ тавр мерасад', 'ok', 'left', size=22)}
{pill(800, 454, N(903.8), '📘 Шпаргалка — дар тавсиф', 'accent', 'up', size=24)}
</section>''')
S('s-sum', T_SUM, T_NEXT)

slides.append(f'''<section class="scene" id="s-next">
{kick(T_NEXT + .1, 'ДАРСИ 13', 'НАВБАТӢ')}
<div class="h1" style="left:60px;top:110px;font-size:92px;line-height:1.05" {A('stamp', T_NEXT + .3)}>AI БАРОИ<br>БАРНОМАСОЗ</div>
{pill(68, 380, N(909.0), 'ёвар, на ҷонишин 🤝', 'ok', 'left', size=28)}
{pill(68, 456, N(911.3), '⚙️ код менависем ва санҷида мебинем', 'left', 'left', size=26)}
{pill(820, 170, N(916.1), '🔔 Обуна шавед', 'accent', 'pop', size=34)}
{pill(820, 270, N(917.0), '@shahriyor_yunusov', 'left', 'pop', size=26)}
</section>''')
S('s-next', T_NEXT, END + 1)

chapters = [dict(t=0, title='Хук'), dict(t=T_REST, title='Образи ресторан'), dict(t=T_URL, title='Суроға: аз чӣ иборат аст?'), dict(t=T_DNS, title='Домен ва DNS'), dict(t=T_REQ, title='Дархост: GET ва POST'),
            dict(t=T_SRV, title='Сервер ва ҷавоб: статус-код'), dict(t=T_THREE, title='Браузер ҷамъ мекунад: се файл'), dict(t=T_FB, title='Фронтенд ва бекенд'), dict(t=T_LIKE, title='Сайти зинда: JSON ва «Лайк»'),
            dict(t=T_SLOW, title='Чаро гоҳо сайт суст мекушояд'), dict(t=T_HTTPS, title='Қулф дар суроға'), dict(t=T_ERR, title='Хатогиҳои маъмул'), dict(t=T_REC, title='Роҳи як дархост'), dict(t=T_TASK, title='Вазифаҳо ва санҷиш'), dict(t=T_SUM, title='Хулоса')]
ide.sort(key=lambda o: o['t']); ptr.sort(key=lambda o: o['t'])

# ---------- субтитры (.srt для YouTube; в самом видео субтитров НЕТ) ----------
MAP = [(r'индекс нуқта эйч-ти-эм-эл', 'index.html'), (r'стайл нуқта си-эс-эс', 'style.css'), (r'скрипт нуқта джей-эс', 'script.js'), (r'юнусов нуқта ту-джей', 'yunusov.tj'),
       (r'джейсон нуқта стрингифай', 'JSON.stringify'), (r'джейсон нуқта парс', 'JSON.parse'), (r'рек нуқта ю-эр-эл', 'req.url'), (r'дейта нуқта лайкс', 'data.likes'), (r'дейта нуқта лайкд', 'data.liked'),
       (r'хати ҷаҳида эбаут', '/about'), (r'хати ҷаҳида Эбаут', '/About'), (r'хати ҷаҳида контакт', '/contact'), (r'хати ҷаҳида шоп', '/shop'), (r'хати ҷаҳида лайк', '/like'),
       (r'эйч-ти-ти-пи-эс', 'HTTPS'), (r'эйч-ти-ти-пи', 'HTTP'), (r'эйч-ти-эм-эл-ро', 'HTML-ро'), (r'эйч-ти-эм-эл', 'HTML'), (r'си-эс-эс', 'CSS'), (r'джаваскрипт', 'JavaScript'), (r'джей-эс', 'JS'),
       (r'ди-эн-эс', 'DNS'), (r'ай-пи-ро', 'IP-ро'), (r'ай-пи', 'IP'), (r'ю-эр-эл', 'url'), (r'ай-ди-и', 'IDE'), (r'эй-ай', 'AI'), (r'джейсон-ро', 'JSON-ро'), (r'джейсон', 'JSON'),
       (r'консол лог', 'console.log'), (r'фанкшн', 'function'), (r'риторн', 'return'), (r'лет', 'let'), (r'реквест', 'request'), (r'метод', 'method'), (r'ансвер', 'answer'), (r'дейта', 'data'),
       (r'лайкс', 'likes'), (r'лайкд', 'liked'), (r'гет', 'GET'), (r'пост', 'POST'), (r'эф-дувоздаҳ-ро', 'F12-ро'), (r'эф-дувоздаҳ', 'F12'), (r'нетворк-ро', 'Network-ро'), (r'нетворк', 'Network'),
       (r'эйч-ван', 'h1'), (r'статус', 'status'), (r'бодӣ', 'body'), (r'рек', 'req'), (r'тру', 'true'), (r'фолс', 'false'), (r'парс', 'parse'), (r'фулл-стек', 'full-stack'), (r'Энтер-ро', 'Enter-ро'), (r'ту-джей', 'tj')]
def disp(s):
    for a, b in MAP: s = re.sub(r'(?<![\w-])' + a + r'(?![\w-])', b, s, flags=re.I)
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

# ---------- sfx / srt / главы ----------
sfx = [s for s in sfx if 0 <= s['t'] < END]
json.dump(dict(end=END, sfx=sorted(sfx, key=lambda s: s['t'])), open('sfx.json', 'w'), indent=0)
json.dump(dict(gaps=GAPS, end=END), open('gaps.json', 'w'))
def ts(t): h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60; return f'{h:02}:{m:02}:{int(s):02},{int(round((s % 1) * 1000)) % 1000:03}'
with open('../youtube-lesson-12.srt', 'w', encoding='utf8') as f:
    for k, c in enumerate(caps, 1): f.write(f"{k}\n{ts(c['t0'])} --> {ts(c['t1'])}\n{c['text']}\n\n")
with open('chapters.txt', 'w', encoding='utf8') as f:
    for c in chapters: f.write(f"{int(c['t'] // 60)}:{int(c['t'] % 60):02} {c['title']}\n")
print('END', END, 'scenes', len(scenes), 'ide ops', len(ide), 'sfx', len(sfx))
print(open('chapters.txt').read())
