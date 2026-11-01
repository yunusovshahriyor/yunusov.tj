# Собирает video.html (IDE + слайды + таймлайн), sfx.json, .srt (для YouTube; в видео субтитров НЕТ) и главы для YouTube-урока 4 «Рӯйхат».
import json, re, html
WJ = json.load(open('words.json')); W = WJ['words']; NARR_END = WJ['total']
toks = [re.sub(r'[^\w-]', '', w['w']).lower() for w in W]

def find(phrase, after=0):
    if isinstance(after, float):  # время видео -> индекс слова
        after = next((k for k, w in enumerate(W) if V(w['t0']) >= after - .01), len(W))
    seq = [re.sub(r'[^\w-]', '', x).lower() for x in phrase.split()]
    for i in range(after, len(W) - len(seq) + 1):
        if toks[i:i + len(seq)] == seq: return i
    raise SystemExit('not found: ' + phrase)

GAPS = []
def V(nt): return nt + sum(d for g, d in GAPS if g <= nt)
def T(phrase, after=0, end=False, off=0.0):
    i = find(phrase, after); n = len(phrase.split())
    return round(V(W[i + n - 1]['t1'] if end else W[i]['t0']) + off, 3)
def I(phrase, after=0): return find(phrase, after)

PAUSE = 5.0
GAP_Q = W[I('фикр кунед.', I('Ва санҷиши нав')) + 1]['t1'] + 0.05; GAPS.append((GAP_Q, PAUSE))
END = round(V(NARR_END) + 0.8, 2)

# ---------- таймлайн ----------
scenes, ide, marks, rings, ptr, chips, zooms, sfx = [], [], [], [], [], [], [], []
def S(id, t0, t1): scenes.append(dict(id=id, t0=t0, t1=t1)); sfx.append(dict(name='whoosh', t=t0 - .15, gain=.35))
code = ['']
def setc(t, c): ide.append(dict(t=t, op='set', code=c)); code[0] = c
def typ(t, new, dur=None):
    dur = dur or max(.6, min(4.5, .075 * abs(len(new) - len(code[0])) + .25))
    ide.append(dict(t=t, op='type', dur=dur, **{'from': code[0], 'to': new}))
    n = len(new) - len(code[0])
    for j in range(max(1, abs(n))): sfx.append(dict(name='key', t=round(t + dur * j / max(1, abs(n)), 3), gain=.5))
    code[0] = new; return t + dur
def run(t, kind='ok', wait=None):
    ptr.append(dict(t=t, sel='#run')); o = dict(t=t, op='run', sel='#run')
    if wait: o['wait'] = wait
    ide.append(o)
    sfx.append(dict(name='click', t=t, gain=.6)); sfx.append(dict(name='ding' if kind == 'ok' else 'buzz', t=t + .25, gain=.5 if kind == 'ok' else .35))
def click(t, sel, op='click'):
    ptr.append(dict(t=t, sel=sel)); ide.append(dict(t=t, op=op, sel=sel)); sfx.append(dict(name='click', t=t, gain=.6))
def clear(t): ide.append(dict(t=t, op='clear'))
def mark(t0, t1, line, c0, c1, text='', color='y', pos='above'):
    marks.append(dict(t0=t0, t1=t1, line=line, c0=c0, c1=c1, text=text, color=color, pos=pos)); sfx.append(dict(name='pop', t=t0, gain=.35))
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

# ключевые моменты
S1_END = T('Тасаввур кунед, ки рӯйхати харид')
S2_END = T('Ба ай-ди-и')
S3_END = T('Ҳоло қимати нав')
S4_END = T('Рӯйхат ва давр')
S5_END = T('Се хатои маъмули')
S6_END = T('Ва акнун вазифа')
S7_END = T('Хулоса мекунем.')
X_NEXT = T('Дарси оянда')

# --- 0. Хук ---
h_100 = T('сад рақам'); h_tired = T('ин хаста'); h_one = T('Як рӯйхат кифоя'); h_vid = T('Дар ин видео'); h_quiz = T('Дар охир санҷиши')
tiny = ''.join(f'<div class="tinybox" {A("pop", h_100 + .2 + k * .12, h_one - .3)}>a{k + 1}</div>' for k in range(12))
slides.append(f'''<section class="scene" id="s-hook">
<div class="kicker" {A('down', .2)}><b>ДАРСИ 4</b>БАРНОМАСОЗӢ АЗ СИФР · JAVASCRIPT</div>
<div class="h1" style="left:60px;top:110px;font-size:140px" {A('stamp', .6)}>РӮЙХАТ</div>
<div class="mono acc" style="left:66px;top:285px;font-size:60px;font-weight:800" {A('up', h_vid)}>array</div>
<div class="sub" style="left:68px;top:365px" {A('up', h_vid + .3)}>якчанд қимат — як ҷо</div>
<div style="left:68px;top:430px" {A('left', h_100)}><span class="pill">🔢 сад рақам → сад тағйирёбанда?</span></div>
<div style="left:68px;top:498px" {A('left', h_tired)}><span class="pill err">😮‍💨 ин хаста мекунад</span></div>
<div style="left:68px;top:566px" {A('left', h_one)}><span class="pill ok">📋 як рӯйхат кифоя аст</span></div>
<div style="left:760px;top:140px;width:480px;display:flex;flex-wrap:wrap;gap:14px">{tiny}</div>
<div class="shelf" style="left:1145px;top:400px;gap:10px;zoom:.62" {A('pop', h_one)}>
 <div class="slot"><div class="idx">0</div><div class="cell">12</div></div><div class="slot"><div class="idx">1</div><div class="cell">7</div></div><div class="slot"><div class="idx">2</div><div class="cell">31</div></div><div class="slot"><div class="idx">3</div><div class="cell">…</div></div></div>
<div style="left:850px;top:640px" {A('pop', h_quiz)}><span class="pill accent">🎯 Дар охир: санҷиши нав</span></div>
</section>''')
S('s-hook', 0, S1_END)

# --- 1. Образи рӯйхати харид ---
l_non = T('нон,', S1_END); l_shir = T('шир,', S1_END); l_tuhm = T('тухм,', S1_END); l_seb = T('себ,', S1_END); l_nok = T('нок.', S1_END)
l_arr = T('Номаш эррей'); l_box = T('Ин ҳамон қуттии'); l_num = T('Ва ҳар ҷой шумора'); l_zero = T('шумора аз сифр оғоз', l_num); l_n0 = T('Нон —', S1_END); l_n1 = T('шир —', l_n0); l_n2 = T('тухм —', l_n0)
l_life = T('Дар ҳаёт рӯйхатҳо'); l_mus = T('рӯйхати мусиқӣ'); l_pic = T('суратҳо дар галерея'); l_ig = T('обуначиёни Инстаграм')
items = [('нон', l_non), ('шир', l_shir), ('тухм', l_tuhm), ('себ', l_seb), ('нок', l_nok)]
idx_t = [l_num + .3 + k * .45 for k in range(5)]
cells = ''
for k, (nm, tt) in enumerate(items):
    hit_t = [l_n0, l_n1, l_n2, None, None][k]
    cells += (f'<div class="slot" id="sl{k}"><div class="idx" {A("pop", idx_t[k], l_life - .3)}>{k}</div>'
              f'<div class="cell" {A("drop", tt, l_life - .3)}>{nm}</div></div>')
    if hit_t: cells += ''
hits = ''.join(f'<div style="left:{129 + k * 208}px;top:322px;width:190px;height:130px;border:4px solid var(--purple);border-radius:16px;box-shadow:0 0 30px rgba(189,147,249,.5)" {A("pop", t, l_life - .3)}></div>' for k, t in enumerate([l_n0, l_n1, l_n2]))
slides.append(f'''<section class="scene" id="s-list">
<div class="kicker" {A('down', S1_END + .1)}><b>01</b>РӮЙХАТ ЧИСТ?</div>
<div class="h2" style="left:60px;top:90px;font-size:48px" {A('up', S1_END + .3, l_life - .3)}>Рӯйхати харид 🛒</div>
<div class="shelf" style="left:129px;top:260px" >{cells}</div>
{hits}
<div style="left:700px;top:96px" {A('pop', l_arr, l_life - .3)}><span class="pill accent mono" style="font-size:26px">array = рӯйхат</span></div>
<div style="left:129px;top:500px" {A('pop', l_box, l_life - .3)}><span class="pill">📦 қуттии дарси 1 + раф: ҳар қимат — ҷои худро дорад</span></div>
<div style="left:129px;top:575px" {A('stamp', l_zero + .5, l_life - .3)}><span class="pill accent" style="font-size:28px">шумора аз 0 оғоз мешавад!</span></div>
<div class="h2" style="left:60px;top:100px;font-size:46px" {A('up', l_life + .1)}>Рӯйхатҳо дар ҳама ҷо ҳастанд</div>
<div class="node" style="left:60px;top:240px;width:360px" {A('up', l_mus)}><span class="big">🎵</span>Рӯйхати мусиқӣ</div>
<div class="node" style="left:460px;top:240px;width:360px" {A('up', l_pic)}><span class="big">🖼️</span>Суратҳо дар галерея</div>
<div class="node" style="left:860px;top:240px;width:360px" {A('up', l_ig)}><span class="big">📱</span>Обуначиёни Инстаграм</div>
</section>''')
S('s-list', S1_END, S2_END)

# --- 2. Аввалин рӯйхат дар IDE ---
S('ide', S2_END, S7_END)
setc(S2_END, ''); clear(S2_END)
chip(S2_END + .1, S2_END + 2.0, '<span>💻</span><div>Аввалин рӯйхат дар IDE<small>02 · ҳамроҳи ман нависед</small></div>', 'card')
t_link = T('Пайванд дар тавсиф')
chip(t_link, t_link + 3.6, '🔗 yunusovshahriyor.github.io/yunusov.tj/ide', 'side yel', 'top:90px')
F0 = 'let fruits = ["себ", "нок", "ангур"];'
t_w = T('лет фрутс баробари'); t_vals = T('«себ», «нок»', t_w); t_comma = T('Қиматҳо бо вергул'); t_quote = T('матн дар нохунак'); t_get = T('Барои гирифтани қимат'); t_cl = T('консол лог, фрутс', t_get)
t_run = T('Иҷро.', t_cl); t_seb = T('«Себ»!', t_run); t_first = T('Ба ҷои як'); t_one = T('Ҳоло як:'); t_nok = T('«нок».', t_one); t_two = T('Ду:', t_one); t_ang = T('«ангур».', t_two); t_ask = T('Ва агар донистан'); t_len = T('фрутс нуқта лэнгс', t_ask); t_run3 = T('Иҷро.', t_len); t_se = T('Се!', t_run3)
zoom(t_w - .3, t_run - .4, 330, 250, 1.4)
typ(t_w + .1, F0, 5.0)
mark(t_vals, t_comma - .1, 0, 13, 37, '📋 рӯйхат: се қимат', 'c')
mark(t_comma, t_quote - .1, 0, 19, 20, 'вергул ,', 'y')
mark(t_quote, t_get - .2, 0, 14, 19, 'матн — дар нохунак', 'g')
F1 = F0 + '\nconsole.log(fruits[0]);'
typ(t_cl - .2, F1, 3.4)
run(t_run - .2)
ring(t_seb, t_one - .1, '#out', '✅ себ', 'g', 2)
mark(t_first, t_one - .2, 1, 18, 21, '0 = аввалин', 'y', 'below')
typ(t_one - .1, F0 + '\nconsole.log(fruits[1]);', .5)
run(t_one + .8)
typ(t_two - .1, F0 + '\nconsole.log(fruits[2]);', .5)
run(t_two + .65)
typ(t_ask + .8, F0 + '\nconsole.log(fruits.length);', 2.0)
run(t_run3 - .2)
ring(t_se, S3_END - .1, '#out', '🎉 3 қимат', 'g', 2)

# --- 3. push ---
chip(S3_END + .1, S3_END + 1.8, '<span>➕</span><div>Илова кардан: push<small>03 · ба охири рӯйхат</small></div>', 'card')
p_push = T('фрутс нуқта пуш'); p_anor = T('Ин «анор»-ро'); p_bz = T('Боз лэнгс'); p_run = T('Иҷро.', p_bz); p_four = T('Чор!'); p_know = T('Донистан хуб аст'); p_last = T('шумораи охирин'); p_four2 = T('Дар мо чор қимат')
G1 = F0 + '\nfruits.push("анор");\nconsole.log(fruits.length);'
zoom(p_push - .3, p_run - .4, 330, 250, 1.4)
typ(p_push, G1, 3.0)
mark(p_push + .6, p_anor - .1, 1, 7, 11, '➕ илова мекунад', 'g')
mark(p_anor, p_bz - .2, 1, 12, 19, '→ ба охири рӯйхат', 'c')
run(p_run - .2)
ring(p_four, p_know - .2, '#out', '🎉 4 қимат', 'g', 2)
G2 = F0 + '\nfruits.push("анор");\nconsole.log(fruits[fruits.length - 1]);'
typ(p_last - .6, G2, 2.4)
mark(p_four2 - .5, p_four2 + 2.6, 2, 26, 38, 'охирин = length − 1', 'y')
run(p_four2 + 3.0)
ring(p_four2 + 3.6, S4_END - .2, '#out', '✅ анор', 'g', 2)

# --- 4. Рӯйхат ва давр ---
chip(S4_END + .1, S4_END + 1.8, '<span>🔁</span><div>Рӯйхат ва давр<small>04 · for + array</small></div>', 'card')
BASE = F0 + '\nfruits.push("анор");'
d_dars3 = T('Давр аз дарси се'); d_for = T('фор.'); d_let = T('лет ай баробари сифр'); d_cond = T('ай хурд аз фрутс'); d_step = T('ай плюс плюс'); d_body = T('консол лог, фрутс, дар'); d_i = T('ай-и нав'); d_run = T('Иҷро.', d_i); d_res = T('Себ, нок, ангур, анор'); d_all = T('Ҳамаи қиматҳо'); d_thou = T('Дар рӯйхат ҳазор')
zoom(d_for - .3, d_run - .4, 330, 250, 1.4)
typ(d_for - .2, BASE + '\nfor () {\n}', .7)
typ(d_let - .1, BASE + '\nfor (let i = 0; ) {\n}', 1.6)
mark(d_let + .2, d_cond - .1, 2, 5, 15, '🚩 оғоз: 0', 'c')
typ(d_cond, BASE + '\nfor (let i = 0; i < fruits.length; ) {\n}', 2.2)
mark(d_cond + .3, d_step - .1, 2, 16, 34, '❓ то охири рӯйхат', 'y')
typ(d_step, BASE + '\nfor (let i = 0; i < fruits.length; i++) {\n}', .9)
mark(d_step + .2, d_body - .1, 2, 35, 38, '👣 +1', 'g')
typ(d_body, BASE + '\nfor (let i = 0; i < fruits.length; i++) {\n  console.log(fruits[i]);\n}', 3.2)
mark(d_i - .2, d_run - .2, 3, 21, 22, '🔁 ҳар бор нав', 'c')
run(d_run - .2)
ring(d_res, d_thou - .1, '#out', '✅ ҳамаи қиматҳо як-як', 'g', 2)

# --- 5. Хатогиҳои маъмул ---
setc(S5_END, ''); clear(S5_END)
chip(S5_END + .1, S5_END + 2.0, '<span>🐞</span><div>Се хатои маъмул<small>05 · ҳама хато мекунанд — ин муқаррарӣ аст</small></div>', 'card')
e1 = T('Якум:', S5_END); e1w = T('Дар рӯйхати се қимат'); e1u = T('андефайнд', e1w); e1last = T('Охирин қимат дар'); e2 = T('Дуюм:', e1last); e2w = T('дар давр хурд'); e2code = T('Агар нависем ай хурд'); e2u = T('охирин сатр'); e2att = T('Диққат ба аломат')
e3 = T('Саввум:', e2att); e3w = T('лэнгс-ро бо қавс'); e3prop = T('лэнгс — ин хосият'); e3err = T('Агар нависем фрутс'); e3none = T('Қавс лозим нест')
chip(e1 + .1, e1 + 2.3, 'Хатои 1 / 3', 'side red', 'top:70px;left:1090px')
E1 = F0 + '\nconsole.log(fruits[3]);'
zoom(e1 + 1.0, e1u - .3, 330, 250, 1.4)
typ(e1 + 1.3, E1, 4.0)
mark(e1w + 2.5, e1u, 1, 18, 21, '⚠️ шумора 3 нест!', 'r')
run(e1u - .1, 'bad')
ring(e1u + .5, e1last - .1, '#out', '❓ undefined — ҷои се нест', 'r', 2)
typ(e1last + .3, F0 + '\nconsole.log(fruits[2]);', .6)
mark(e1last + .6, e2 - .6, 1, 18, 21, '✅ охирин = 2', 'g')
run(e1last + 1.6)
chip(e2 + .1, e2 + 2.3, 'Хатои 2 / 3', 'side red', 'top:70px;left:1090px')
E2 = F0 + '\nfor (let i = 0; i <= fruits.length; i++) {\n  console.log(fruits[i]);\n}'
zoom(e2w - .2, e2u - .2, 330, 250, 1.4)
typ(e2w + .1, E2, 4.2)
mark(e2code + .6, e2att, 1, 18, 21, '⚠️ &lt;= ≠ &lt;', 'r')
run(e2u + .2, 'bad')
ring(e2u + .8, e2att + 1.6, '#out', '⚠️ охирин: undefined', 'r', 2)
chip(e3 + .1, e3 + 2.3, 'Хатои 3 / 3', 'side red', 'top:70px;left:1090px')
E3 = F0 + '\nconsole.log(fruits.length());'
zoom(e3w - .2, e3err + 1.2, 330, 250, 1.4)
typ(e3w + .1, E3, 3.0)
mark(e3prop, e3none - .1, 1, 25, 27, '⚠️ () лозим нест', 'r')
run(e3err + 4.4, 'bad')
ring(e3err + 5.0, S6_END - .3, '#out .l.e', 'is not a function', 'c', 4)

# --- 6. Вазифаҳо ---
t_tab = T('ҷадвали', S6_END); t_three = T('Се вазифа ҳаст'); t_t1 = T('Якум:', S6_END + 3.0); t_t1w = T('рӯйхати се хӯроки'); t_t2 = T('Дуюм:', t_t1); t_t2w = T('бо пуш'); t_t3 = T('Саввум:', t_t2); t_t3w = T('бо давр ҳар'); t_chk = T('Ай-ди-и месанҷад')
t_q = T('Ва санҷиши нав'); t_list = T('ҳамон рӯйхати харид'); t_tuhm = T('«Тухм» бо кадом'); t_what = T('бо кадом шумора'); t_pz = T('Видеоро пауза')
t_ans = T('Ҷавоб:', t_pz); t_z0 = T('Нон —', t_ans); t_z1 = T('шир —', t_z0); t_z2 = T('тухм —', t_z0); t_zero = T('Шумора аз сифр', t_z2)
chip(S6_END + .1, S6_END + 2.0, '<span>🎯</span><div>Вазифаҳо барои шумо<small>06 · дар IDE, ҷадвали «4 · Рӯйхат»</small></div>', 'card')
click(t_tab + .9, '#tabs .tab:nth-child(5)')
ST1 = '// let foods = [ ... ];\n'; ST2 = 'let fruits = ["себ", "нок", "ангур"];\n\n// push ва length\n'; ST3 = 'let fruits = ["себ", "нок", "ангур"];\n\n// давр нависед\n'
setc(t_tab + .92, ST1)
ring(t_tab + 1.4, t_three - .2, '#tabs .tab:nth-child(5)', '', 'y', 4)
ring(t_three, t_t1 - .1, '#side', '📘 назария', 'c', 4)
ring(t_t1, t_t2 - .1, '#task', 'Вазифаи 1', 'y', 4)
SOL1 = 'let foods = ["палав", "самбуса", "ошташ"];\nconsole.log(foods[1]);\n'
typ(t_t1w, SOL1, 4.5)
click(t_t2 + .3, '#side button[data-i="1"]'); setc(t_t2 + .32, ST2)
ring(t_t2 + .8, t_t3 - .1, '#task', 'Вазифаи 2', 'y', 4)
SOL2 = 'let fruits = ["себ", "нок", "ангур"];\nfruits.push("анор");\nconsole.log(fruits.length);\n'
typ(t_t2w, SOL2, 4.0)
click(t_t3 + .3, '#side button[data-i="2"]'); setc(t_t3 + .32, ST3)
ring(t_t3 + .8, t_chk - .1, '#task', 'Вазифаи 3', 'y', 4)
SOL3 = 'let fruits = ["себ", "нок", "ангур"];\nfor (let i = 0; i < fruits.length; i++) {\n  console.log(fruits[i]);\n}\n'
typ(t_t3w, SOL3, 3.2)
ring(t_chk - .3, t_chk + .9, '#check', '✓ Санҷиш', 'c', 6)
click(t_chk + .5, '#check', 'check'); sfx.append(dict(name='chime', t=t_chk + .9, gain=.6))
ring(t_chk + 1.0, t_q - .3, '#checks', '', 'g', 4)
QZ = 'let list = ["нон", "шир", "тухм", "себ", "нок"];'
click(t_q + .1, '#tabs .tab:nth-child(1)'); setc(t_q + .12, '')
zoom(t_list - .3, t_tuhm - .2, 330, 250, 1.4)
typ(t_list, QZ, 4.5)
mark(t_tuhm, t_pz - .3, 0, 26, 32, '❓ тухм', 'y')
g0 = V(GAP_Q) - PAUSE
chip(t_what, g0 - .3, '<span class="big">❓</span><div>«Тухм» бо кадом шумора истодааст?<small>нон, шир, тухм, себ, нок · видеоро пауза кунед ✍️</small></div>', 'card')
for k in range(5):
    chip(g0 + k + .02, g0 + k + .62, f'<span class="big">{5 - k}</span><div>«Тухм» бо кадом шумора истодааст?<small>фикр кунед · баъд ҷавобро мебинем ✅</small></div>', 'card')
    sfx.append(dict(name='tick', t=g0 + k, gain=.8))
typ(t_ans, QZ + '\nconsole.log(list[2]);', 1.4)
run(t_z0 - .3)
mark(t_z0, t_z1 - .1, 0, 12, 18, '0', 'c')
mark(t_z1, t_z2 - .1, 0, 19, 25, '1', 'c')
mark(t_z2, t_zero - .1, 0, 26, 32, '2 = тухм', 'g')
ring(t_z2 + .3, S7_END - .3, '#out', '✅ list[2] = тухм', 'g', 2)

# --- 7. Хулоса ---
x1 = T('Рӯйхат — қуттӣ бо', S7_END); x2 = T('Шумора аз сифр оғоз мешавад.', S7_END); x3 = T('лэнгс мегӯяд', S7_END); x4 = T('Ва бо давр', S7_END); x_pdf = T('Шпаргалкаи бепул')
slides.append(f'''<section class="scene" id="s-sum">
<div class="kicker" {A('down', S7_END + .2)}><b>07</b>ХУЛОСА</div>
<div class="h2" style="left:60px;top:90px;font-size:50px" {A('up', x1)}>Рӯйхат = <span class="acc">якчанд қимат + шумора аз 0</span></div>
<div class="card3" style="left:60px;top:220px;width:360px;height:250px" {A('up', x2)}><div class="emo">0️⃣</div><div class="t">Шумора аз 0</div><div class="codechip" style="font-size:22px">fruits<span class="k">[0]</span></div></div>
<div class="card3" style="left:460px;top:220px;width:360px;height:250px" {A('up', x3)}><div class="emo">🔢</div><div class="t">Чанд қимат?</div><div class="codechip" style="font-size:22px">fruits.<span class="f">length</span></div></div>
<div class="card3" style="left:860px;top:220px;width:360px;height:250px" {A('up', x3 + 1.6)}><div class="emo">➕</div><div class="t">Ба охир илова</div><div class="codechip" style="font-size:22px">fruits.<span class="f">push</span>(<span class="s">"анор"</span>)</div></div>
<div style="left:60px;top:510px" {A('up', x4)}><span class="pill ok">бо давр — ҳар қимат як-як 🔁</span></div>
<div style="left:60px;top:580px" {A('up', x_pdf)}><span class="pill accent">📘 Шпаргалкаи бепул (PDF) — дар тавсифи видео</span></div>
</section>''')
S('s-sum', S7_END, X_NEXT)

x_sub = T('Обуна шавед')
slides.append(f'''<section class="scene" id="s-next">
<div class="kicker" {A('down', X_NEXT + .1)}><b>ДАРСИ 5</b>НАВБАТӢ</div>
<div class="h1" style="left:60px;top:130px;font-size:130px" {A('stamp', X_NEXT + .3)}>ФУНКСИЯ</div>
<div class="mono acc" style="left:66px;top:290px;font-size:56px;font-weight:800" {A('up', X_NEXT + .8)}>function</div>
<div class="sub" style="left:68px;top:370px" {A('up', X_NEXT + 1.2)}>«рецепт»-и барнома</div>
<div class="codechip" style="left:68px;top:460px;font-size:28px;line-height:1.5" {A('up', X_NEXT + 2.4)}><span class="k">function</span> <span class="f">sayHello</span>() {{<br>&nbsp;&nbsp;<span class="f">console.log</span>(<span class="s">"Салом!"</span>);<br>}}</div>
<div style="left:820px;top:170px" {A('pop', x_sub)}><span class="pill accent" style="font-size:34px;padding:20px 40px">🔔 Обуна шавед</span></div>
<div style="left:820px;top:270px" {A('pop', x_sub + .5)}><span class="pill" style="font-size:26px;padding:16px 30px">@shahriyor_yunusov</span></div>
</section>''')
S('s-next', X_NEXT, END + 1)

chapters = [dict(t=0, title='Хук'), dict(t=S1_END, title='Рӯйхат чист?'), dict(t=S2_END, title='Аввалин рӯйхат дар IDE'), dict(t=S3_END, title='Илова кардан: push'),
            dict(t=S4_END, title='Рӯйхат ва давр'), dict(t=S5_END, title='Хатогиҳои маъмул'), dict(t=S6_END, title='Вазифаҳо ва санҷиш'), dict(t=S7_END, title='Хулоса')]
ide.sort(key=lambda o: o['t']); ptr.sort(key=lambda o: o['t'])

# ---------- субтитры (.srt для YouTube; в самом видео субтитров НЕТ) ----------
MAP = [(r'ай-ди-и', 'IDE'), (r'консол лог', 'console.log'), (r'фор', 'for'), (r'лет', 'let'), (r'эррей', 'array'), (r'фрутс', 'fruits'), (r'лэнгс-ро', 'length-ро'), (r'лэнгс', 'length'),
       (r'пуш', 'push'), (r'андефайнд', 'undefined'), (r'из нот э фанкшн', 'is not a function'), (r'ай-и', 'i-и'), (r'ай', 'i'), (r'Инстаграм', 'Instagram'), (r'сифр', '0')]
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

TL = dict(end=END, scenes=scenes, ide=ide, marks=marks, rings=rings, ptr=ptr, chips=chips, zooms=zooms, caps=[], chapters=chapters, cd=[g0])

# ---------- страница ----------
src = open('../../../ide/index.html', encoding='utf8').read()
PTR = '<svg id="ptr" viewBox="0 0 24 24"><path d="M3 2l7.5 19 2.6-7.6L21 11z" fill="#fff" stroke="#111" stroke-width="1.4" stroke-linejoin="round"/></svg>'
inject_head = '<style>' + open('video.css', encoding='utf8').read() + '</style>'
inject_body = '<div id="ovl">' + PTR + '<div id="rip"></div></div>' + ''.join(slides)
src = src.replace('</head>', inject_head + '</head>', 1)
src = src.replace('<div class="app">', inject_body + '<div id="stagewrap"><div class="app">', 1)
src = src.replace('\n<script>\n(function () {', '\n</div>\n<script>\n(function () {', 1)
src = src.replace('function confetti() {', 'function confetti() { return;')
src = src.replace('["#B4472E", "#E9B949", "#3E7C59", "#1F3F44"]', '["#BD93F9", "#FF79C6", "#4EC9B0", "#DCDCAA"]')
src = src.replace('</body>', '<script>window.TL=' + json.dumps(TL, ensure_ascii=False) + ';</script><script>' + open('video.js', encoding='utf8').read() + '</script></body>', 1)
open('video.html', 'w', encoding='utf8').write(src)

# ---------- sfx / srt / главы ----------
sfx = [s for s in sfx if 0 <= s['t'] < END]
json.dump(dict(end=END, sfx=sorted(sfx, key=lambda s: s['t'])), open('sfx.json', 'w'), indent=0)
json.dump(dict(gaps=GAPS, end=END), open('gaps.json', 'w'))
def ts(t): h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60; return f'{h:02}:{m:02}:{int(s):02},{int(round((s % 1) * 1000)) % 1000:03}'
with open('../youtube-lesson-4.srt', 'w', encoding='utf8') as f:
    for k, c in enumerate(caps, 1): f.write(f"{k}\n{ts(c['t0'])} --> {ts(c['t1'])}\n{c['text']}\n\n")
with open('chapters.txt', 'w', encoding='utf8') as f:
    for c in chapters: f.write(f"{int(c['t'] // 60)}:{int(c['t'] % 60):02} {c['title']}\n")
print('END', END, 'scenes', len(scenes), 'ide ops', len(ide), 'sfx', len(sfx))
print(open('chapters.txt').read())
