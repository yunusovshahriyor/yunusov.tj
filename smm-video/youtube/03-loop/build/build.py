# Собирает video.html (IDE + слайды + таймлайн), sfx.json, .srt (для YouTube; в видео субтитров НЕТ) и главы для YouTube-урока 3 «Давр».
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
def box_nums(vals, t0, step, label='i', zoomv=1.0, left=''):
    nums = ''
    for k, v in enumerate(vals):
        a = t0 + k * step; o = a + step if k + 1 < len(vals) else None
        nums += f'<div class="num" {A("drop", a, o, "flyout")}>{v}</div>'
    return (f'<div class="box" style="position:relative;zoom:{zoomv}" {A("pop", t0 - .3)}><div class="back"></div>{nums}'
            f'<div class="front"><div class="tag" {A("stamp", t0 - .1)}>{label}</div></div></div>')

# ключевые моменты
S1_END = T('Дар варзиш мураббӣ')
S2_END = T('Ба ай-ди-и')
S3_END = T('Бубинем, дар дохили давр')
S4_END = T('Қадам ҳамеша як нест')
S5_END = T('Ҳоло як мисоли муфид')
S6_END = T('Се хатои маъмули')
S7_END = T('Ва акнун вазифа')
S8_END = T('Хулоса мекунем.')
X_NEXT = T('Дарси оянда')

# --- 0. Хук ---
h_100 = T('сад бор'); h_hand = T('Дастӣ'); h_pc = T('Компютер ин корро'); h_vid = T('Дар ин видео'); h_quiz = T('Дар охир санҷиши')
slides.append(f'''<section class="scene" id="s-hook">
<div class="kicker" {A('down', .2)}><b>ДАРСИ 3</b>БАРНОМАСОЗӢ АЗ СИФР · JAVASCRIPT</div>
<div class="h1" style="left:60px;top:110px;font-size:150px" {A('stamp', .6)}>ДАВР</div>
<div class="mono acc" style="left:66px;top:290px;font-size:60px;font-weight:800" {A('up', h_vid)}>for · loop</div>
<div class="sub" style="left:68px;top:370px" {A('up', h_vid + .3)}>як амал — чандин маротиба</div>
<div style="left:68px;top:430px" {A('left', h_100)}><span class="pill">📝 «Салом» × <span class="mono" data-cnt="0;100;{h_100 + .3};1.8">0</span></span></div>
<div style="left:68px;top:498px" {A('left', h_hand)}><span class="pill err">😮‍💨 дастӣ — хаста мешавед</span></div>
<div style="left:68px;top:566px" {A('left', h_pc)}><span class="pill ok">⚡ компютер — як лаҳза</span></div>
<div style="left:880px;top:130px">{box_nums([1, 2, 3, 4, 5, 6], 1.0, 1.15, zoomv=1.25)}</div>
<div style="left:850px;top:640px" {A('pop', h_quiz)}><span class="pill accent">🎯 Дар охир: санҷиши нав</span></div>
</section>''')
S('s-hook', 0, S1_END)

# --- 1. Образи мураббӣ ---
c_tr = T('Дар варзиш мураббӣ'); c_cnt = T('як, ду, се…'); c_def = T('Ана ҳамин давр'); c_pc = T('Мо ба компютер'); c_a = T('аз куҷо оғоз кун'); c_b = T('то кай давом'); c_c = T('ҳар бор чӣ қадар')
c_every = T('Давр дар ҳама ҷо'); c_ig = T('лентаи Инстаграм'); c_game = T('бозӣ экранро'); c_all = T('Ҳамаи инҳо')
for k in range(10): sfx.append(dict(name='tick', t=round(c_cnt + k * .3, 3), gain=.8))
slides.append(f'''<section class="scene" id="s-coach">
<div class="kicker" {A('down', c_tr)}><b>01</b>ДАВР ЧИСТ?</div>
<div class="node" style="left:60px;top:120px;width:560px;text-align:left" {A('up', c_tr + .3, c_pc - .3)}><span style="font-size:48px">🏋️</span> Мураббӣ<small>«даҳ бор нишаст-хез кунед»</small></div>
<div class="mono" style="left:720px;top:90px;font-size:190px;font-weight:900;color:#fff;line-height:1" {A('fade', c_cnt - .3, c_pc - .3)}><span data-cnt="1;10;{c_cnt};2.7">1</span></div>
<div style="left:60px;top:400px" {A('pop', c_def, c_pc - .3)}><span class="pill accent" style="font-size:26px">ДАВР = як амал, чанд маротиба</span></div>
<div class="h2" style="left:60px;top:100px;font-size:44px" {A('up', c_pc, c_every - .3)}>Ба компютер мегӯем:</div>
<div class="node yes" style="left:60px;top:210px;width:360px" {A('up', c_a, c_every - .3)}><span class="big">🚩</span>Аз куҷо оғоз?</div>
<div class="node" style="left:460px;top:210px;width:360px" {A('up', c_b, c_every - .3)}><span class="big">🏁</span>То кай давом?</div>
<div class="node no" style="left:860px;top:210px;width:360px" {A('up', c_c, c_every - .3)}><span class="big">👣</span>Ҳар бор чӣ қадар?</div>
<div class="h2" style="left:60px;top:100px;font-size:44px" {A('up', c_every + .2)}>Давр дар ҳама ҷо ҳаст</div>
<div class="node" style="left:60px;top:230px;width:540px" {A('up', c_ig)}><span class="big">📱</span>Лентаи Инстаграм<small>постҳо як-як</small></div>
<div class="node" style="left:660px;top:230px;width:540px" {A('up', c_game)}><span class="big">🎮</span>Экрани бозӣ<small>дар як сония чандин бор нав мешавад</small></div>
<div style="left:410px;top:500px" {A('stamp', c_all)}><span class="pill accent" style="font-size:30px">ҳамаи инҳо — давр 🔁</span></div>
</section>''')
S('s-coach', S1_END, S2_END)

# --- 2. Аввалин давр дар IDE ---
S('ide', S2_END, S3_END)
setc(S2_END, ''); clear(S2_END)
chip(S2_END + .1, S2_END + 2.0, '<span>💻</span><div>Аввалин давр дар IDE<small>02 · ҳамроҳи ман нависед</small></div>', 'card')
t_link = T('Пайванд дар тавсиф')
chip(t_link, t_link + 3.6, '🔗 yunusovshahriyor.github.io/yunusov.tj/ide', 'side yel', 'top:90px')
Ca = 'for () {\n}'
Cb = 'for (let i = 1; ) {\n}'
Cc = 'for (let i = 1; i <= 5; ) {\n}'
Cd = 'for (let i = 1; i <= 5; i++) {\n}'
Ce = 'for (let i = 1; i <= 5; i++) {\n  console.log("Нишаст-хез " + i);\n}'
p_for = T('фор, дар қавс'); p_let = T('лет ай баробари'); p_in = T('Ин ай ҳамон'); p_cond = T('Дуюм:', p_let); p_cond2 = T('Ин ҳамон шарт'); p_step = T('Саввум:', p_cond); p_body = T('Дар дохили қавсҳои'); p_cl = T('консол лог,', p_body)
p_run = T('Иҷро мекунем.'); p_res = T('Нишаст-хез як'); p_five = T('Панҷ бор!'); p_th = T('Ҳоло панҷро'); p_run2 = T('Иҷро.', p_th); p_thousand = T('Ҳазор сатр'); p_wow = T('Ана қуввати')
zoom(p_for - .4, p_run - .3, 330, 250, 1.4)
typ(p_for + .2, Ca, .8)
typ(p_let - .1, Cb, 1.6)
mark(p_let + .2, p_in - .1, 0, 5, 15, '🚩 оғоз', 'c')
mark(p_in, p_cond - .2, 0, 9, 10, '📦 ҳамон қуттӣ (дарси 1)', 'y', 'below')
typ(p_cond + .1, Cc, 1.6)
mark(p_cond + .3, p_cond2 - .1, 0, 16, 23, '❓ шарт', 'y')
mark(p_cond2, p_step - .3, 0, 16, 23, 'аз дарси 2', 'c', 'below')
typ(p_step + .1, Cd, 1.0)
mark(p_step + .3, p_body - .2, 0, 24, 27, '👣 қадам: +1', 'g')
typ(p_body + .9, Ce, 3.4)
run(p_run + .6)
ring(p_res + .4, p_five + 1.8, '#out', '✅ панҷ бор', 'g', 2)
zoom(p_th - .3, p_run2 - .3, 330, 250, 1.4)
typ(p_th + .1, Ce.replace('<= 5', '<= 1000'), .7)
run(p_run2 + .3)
ring(p_thousand, p_wow + 1.6, '#out', '⚡ 1000 сатр · < 1 с', 'g', 2)

# --- 3. Давр қадам ба қадам (слайд) ---
t_ex = T('Мисоли хурд'); r1 = T('Ай мешавад як'); r1b = T('Шартро месанҷем'); r1c = T('Ҳа — кор'); r2 = T('ай мешавад ду'); r2b = T('Боз шарт'); r3 = T('Баъд ай мешавад се'); r4 = T('Баъд ай мешавад чор'); r4b = T('Чор аз се'); r_end = T('Давр тамом')
t_sum = T('Хулоса:'); t_trio = T('шарт, кор, қадам.')
rows3 = [('i = 1', '1 &lt;= 3 ?', 'ҳа ✓', 'иҷро · i++ → 2', r1), ('i = 2', '2 &lt;= 3 ?', 'ҳа ✓', 'иҷро · i++ → 3', r2), ('i = 3', '3 &lt;= 3 ?', 'ҳа ✓', 'иҷро · i++ → 4', r3), ('i = 4', '4 &lt;= 3 ?', 'не ✗', 'давр тамом ■', r4)]
rr = ''
for k, (op, q, ans, act, ta) in enumerate(rows3):
    bad = k == 3
    tq = ta + 1.0 if k == 0 else ta + .8
    rr += (f'<div class="row{" hit" if bad else ""}" style="left:100px;top:{190 + 84 * k}px;width:1080px;{"background:var(--panel)" if bad else ""}" {A("up", ta)}><span class="op">{op}</span>'
           f'<span class="mean mono" style="font-size:26px"><span {A("fade", tq)}>{q}</span> <span class="{"t-err" if bad else "t-ok"}" {A("pop", tq + .3)}>{ans}</span></span>'
           f'<span class="res" style="min-width:280px;color:{"var(--err)" if bad else "var(--text)"}" {A("fade", tq + .7)}>{act}</span></div>')
slides.append(f'''<section class="scene" id="s-trace">
<div class="kicker" {A('down', S3_END + .2)}><b>03</b>ДАВР ҚАДАМ БА ҚАДАМ</div>
<div class="codechip" style="left:100px;top:100px;font-size:30px" {A('up', t_ex)}><span class="k">for</span> (<span class="k">let</span> i = <span class="n">1</span>; i &lt;= <span class="n">3</span>; i++) {{ … }}</div>
{rr}
<div style="left:100px;top:560px" {A('stamp', t_sum)}><span class="pill accent" style="font-size:28px">шарт → кор → қадам · шарт → кор → қадам</span></div>
</section>''')
S('s-trace', S3_END, S4_END)

# --- 4. IDE: қадам, ҷамъ, хатогиҳо, вазифаҳо ---
S('ide', S4_END, S8_END)
setc(S4_END, ''); clear(S4_END)
chip(S4_END + .1, S4_END + 1.8, '<span>🔢</span><div>Қадам ҳамеша як нест<small>04 · += ва --</small></div>', 'card')
v_p = T('ай плюс баробари ду'); v_res = T('дуву чор'); v_m = T('Ва ай минус минус'); v_back = T('аз даҳ то як')
V1 = 'for (let i = 2; i <= 10; i += 2) {\n  console.log(i);\n}'
V2 = 'for (let i = 10; i >= 1; i--) {\n  console.log(i);\n}'
zoom(S4_END + 1.9, v_res - .5, 330, 250, 1.4)
typ(S4_END + 2.0, V1, 2.6)
mark(v_p + .3, v_res - .3, 0, 25, 31, '👣 қадам: +2', 'g')
run(v_res - .2)
ring(v_res + .6, v_m - .2, '#out', '2, 4, 6, 8, 10', 'g', 2)
zoom(v_m - .3, v_m + 3.2, 330, 250, 1.4)
typ(v_m + .1, V2, 2.6)
mark(v_m + 1.0, v_m + 3.0, 0, 25, 29, '👣 қадам: −1', 'c')
run(v_back - .3)
ring(v_back + .4, S5_END - .3, '#out', '10 → 1', 'g', 2)

setc(S5_END, ''); clear(S5_END)
chip(S5_END + .1, S5_END + 1.8, '<span>➕</span><div>Ҷамъ аз 1 то 100<small>05 · қуттии sum</small></div>', 'card')
s_box = T('Қуттии сум'); s_loop = T('Баъд давр аз як'); s_in = T('Дар дохил:'); s_sum = T('сум баробари'); s_log = T('Ба охир'); s_run = T('Иҷро.', s_log); s_res = T('Панҷ ҳазору'); s_hand = T('Дастӣ ҳисоб')
SU0 = 'let sum = 0;'
SU1 = SU0 + '\nfor (let i = 1; i <= 100; i++) {\n}'
SU2 = SU0 + '\nfor (let i = 1; i <= 100; i++) {\n  sum = sum + i;\n}'
SU3 = SU2 + '\nconsole.log(sum);'
zoom(s_box - .3, s_run - .3, 330, 250, 1.4)
typ(s_box + .1, SU0, 1.4)
mark(s_box + .3, s_loop - .2, 0, 4, 7, '📦 қуттӣ: сум = 0', 'c')
typ(s_loop + .1, SU1, 2.0)
typ(s_sum - .1, SU2, 2.6)
mark(s_sum + .8, s_sum + 3.6, 3, 2, 16, '➕ ба сумма i-ро илова кун', 'g', 'below')
typ(s_log + .1, SU3, 1.6)
run(s_run - .3)
ring(s_res, s_hand + 3.0, '#out', '🎉 5050', 'g', 2)

setc(S6_END, ''); clear(S6_END)
chip(S6_END + .1, S6_END + 2.0, '<span>🐞</span><div>Се хатои маъмул<small>06 · ҳама хато мекунанд — ин муқаррарӣ аст</small></div>', 'card')
e1 = T('Якум:', I('Се хатои маъмули')); e1w = T('Агар нависем'); e1att = T('Диққат ба аломат')
e2 = T('Дуюм:', e1att); e2f = T('қадамро фаромӯш'); e2w = T('Агар ай мондааст'); e2inf = T('Ин даври бепоён'); e2ide = T('ай-ди-и мо')
e3 = T('Саввум:', e2ide); e3w = T('ай-ро берун'); e3box = T('Қуттии ай танҳо'); e3x = T('Берун — хатои')
E1 = 'for (let i = 1; i < 5; i++) {\n  console.log(i);\n}'
chip(e1 + .1, e1 + 2.3, 'Хатои 1 / 3', 'side red', 'top:70px;left:1090px')
zoom(e1w - .3, e1w + 3.2, 330, 250, 1.4)
typ(e1w + .1, E1, 3.0)
run(e1w + 3.5)
ring(e1w + 4.0, e1att - .1, '#out', '1, 2, 3, 4 — панҷ нест!', 'r', 2)
mark(e1att, e2 - .3, 0, 18, 19, '⚠️ &lt; ≠ &lt;=', 'r')
chip(e2 + .1, e2 + 2.3, 'Хатои 2 / 3', 'side red', 'top:70px;left:1090px')
E2 = 'for (let i = 1; i <= 5; ) {\n}'
zoom(e2f - .3, e2inf - .3, 330, 250, 1.4)
typ(e2f + .2, E2, 2.0)
mark(e2f + 1.2, e2w + 4.0, 0, 23, 26, '⚠️ қадам нест', 'r')
run(e2inf, 'bad', 3300)
ring(e2inf + .6, e2ide + 4.0, '#out', '♾️ IDE ҳифз кард', 'y', 2)
chip(e3 + .1, e3 + 2.3, 'Хатои 3 / 3', 'side red', 'top:70px;left:1090px')
E3 = 'for (let i = 1; i <= 3; i++) {\n}\nconsole.log(i);'
typ(e3w, E3, 2.4)
mark(e3w + .8, e3x - .2, 2, 12, 13, '⚠️ i берун аз давр', 'r')
run(e3x - .3, 'bad')
ring(e3x + .4, S7_END - .3, '#out .l.e', 'i is not defined', 'c', 4)

# --- 5. Вазифаҳо ---
t_tab = T('ҷадвали', S7_END); t_three = T('Се вазифа ҳаст'); t_t1 = T('Якум:', t_three); t_t1w = T('рақамҳои аз як'); t_t2 = T('Дуюм:', t_t1); t_t2w = T('ҷамъи аз як то садро'); t_t3 = T('Саввум:', t_t2); t_t3w = T('ҳисоби баръакс', t_t3); t_chk = T('Ай-ди-и месанҷад')
t_q = T('Ва санҷиши нав'); t_qcode = T('фор, дар қавс лет ай баробари сифр'); t_zero = T('лет ай баробари сифр'); t_cond = T('шарт ай хурд'); t_step = T('қадам ай плюс'); t_what = T('Барнома чанд бор'); t_pz = T('Видеоро пауза')
t_ans = T('Ҷавоб:', t_pz); t_three_t = T('се бор.', t_ans); t_vals = T('ай мешавад сифр'); t_no = T('Ва ҳангоми се'); t_zero_c = T('Сифр ҳам')
chip(S7_END + .1, S7_END + 2.0, '<span>🎯</span><div>Вазифаҳо барои шумо<small>07 · дар IDE, ҷадвали «3 · Давр»</small></div>', 'card')
click(t_tab + .9, '#tabs .tab:nth-child(4)')
ST1 = '// давр нависед\n'; ST2 = 'let sum = 0;\n\n// давр нависед\n\nconsole.log(sum);\n'; ST3 = '// ҳисоби баръакс\n'
setc(t_tab + .92, ST1)
ring(t_tab + 1.4, t_three - .2, '#tabs .tab:nth-child(4)', '', 'y', 4)
ring(t_three, t_t1 - .1, '#side', '📘 назария', 'c', 4)
ring(t_t1, t_t2 - .1, '#task', 'Вазифаи 1', 'y', 4)
SOL1 = 'for (let i = 1; i <= 5; i++) {\n  console.log(i);\n}\n'
typ(t_t1w, SOL1, 2.8)
click(t_t2 + .3, '#side button[data-i="1"]'); setc(t_t2 + .32, ST2)
ring(t_t2 + .8, t_t3 - .1, '#task', 'Вазифаи 2', 'y', 4)
SOL2 = 'let sum = 0;\nfor (let i = 1; i <= 100; i++) {\n  sum = sum + i;\n}\nconsole.log(sum);\n'
typ(t_t2w, SOL2, 4.0)
click(t_t3 + .3, '#side button[data-i="2"]'); setc(t_t3 + .32, ST3)
ring(t_t3 + .8, t_chk - .1, '#task', 'Вазифаи 3', 'y', 4)
SOL3 = 'for (let i = 10; i >= 1; i--) {\n  console.log(i);\n}\n'
typ(t_t3w + .1, SOL3, 2.2)
ring(t_chk - .3, t_chk + .9, '#check', '✓ Санҷиш', 'c', 6)
click(t_chk + .5, '#check', 'check'); sfx.append(dict(name='chime', t=t_chk + .9, gain=.6))
ring(t_chk + 1.0, t_q - .3, '#checks', '', 'g', 4)
# санҷиш: ҷадвали «Озод», код бо i = 0; i < 3
QZ = 'for (let i = 0; i < 3; i++) {\n  console.log("Салом");\n}'
click(t_q + .1, '#tabs .tab:nth-child(1)'); setc(t_q + .12, '')
zoom(t_qcode - .3, t_what - .2, 330, 250, 1.4)
typ(t_qcode, QZ, 6.0)
mark(t_zero, t_cond - .2, 0, 5, 15, 'оғоз: 0', 'c')
mark(t_cond, t_step - .2, 0, 16, 22, 'шарт: i &lt; 3', 'y')
mark(t_step, t_what - .2, 0, 23, 26, 'қадам: +1', 'g')
g0 = V(GAP_Q) - PAUSE
chip(t_what, g0 - .3, '<span class="big">❓</span><div>Барнома чанд бор «Салом» мегӯяд?<small>i = 0; i &lt; 3 · видеоро пауза кунед ✍️</small></div>', 'card')
for k in range(5):
    chip(g0 + k + .02, g0 + k + .62, f'<span class="big">{5 - k}</span><div>Барнома чанд бор «Салом» мегӯяд?<small>фикр кунед · баъд ҷавобро мебинем ✅</small></div>', 'card')
    sfx.append(dict(name='tick', t=g0 + k, gain=.8))
run(t_ans - .3)
ring(t_three_t, t_vals - .2, '#out', '✅ 3 бор', 'g', 2)
mark(t_vals, t_no - .2, 0, 13, 14, '0 → 1 → 2', 'c')
mark(t_no, t_zero_c - .2, 0, 16, 22, '3 &lt; 3 ? не ✗', 'r', 'below')
mark(t_zero_c, S8_END - .3, 0, 13, 14, '0 ҳам ҳисоб', 'g')

# --- 6. Хулоса ---
x1 = T('Давр — такрори'); x2 = T('Се қисм:'); x_o = T('оғоз,', x2); x_s = T('шарт ва қадам'); x_q = T('ва қадам', x_o) + .15; x_ok = T('То шарт дуруст'); x_pdf = T('Шпаргалкаи бепул')
slides.append(f'''<section class="scene" id="s-sum">
<div class="kicker" {A('down', S8_END + .2)}><b>08</b>ХУЛОСА</div>
<div class="h2" style="left:60px;top:90px;font-size:54px" {A('up', x1)}>Давр = <span class="acc">оғоз + шарт + қадам</span></div>
<div class="card3" style="left:60px;top:220px;width:360px;height:270px" {A('up', x_o)}><div class="emo">🚩</div><div class="t">Оғоз</div><div class="codechip" style="font-size:24px"><span class="k">let</span> i = <span class="n">1</span></div></div>
<div class="card3" style="left:460px;top:220px;width:360px;height:270px" {A('up', x_s)}><div class="emo">❓</div><div class="t">Шарт</div><div class="codechip" style="font-size:24px">i &lt;= <span class="n">5</span></div></div>
<div class="card3" style="left:860px;top:220px;width:360px;height:270px" {A('up', x_q)}><div class="emo">👣</div><div class="t">Қадам</div><div class="codechip" style="font-size:24px">i++</div></div>
<div style="left:60px;top:530px" {A('up', x_ok)}><span class="pill ok">то шарт дуруст — давр кор мекунад 🔁</span></div>
<div style="left:60px;top:600px" {A('up', x_pdf)}><span class="pill accent">📘 Шпаргалкаи бепул (PDF) — дар тавсифи видео</span></div>
</section>''')
S('s-sum', S8_END, X_NEXT)

x_sub = T('Обуна шавед')
slides.append(f'''<section class="scene" id="s-next">
<div class="kicker" {A('down', X_NEXT + .1)}><b>ДАРСИ 4</b>НАВБАТӢ</div>
<div class="h1" style="left:60px;top:130px;font-size:140px" {A('stamp', X_NEXT + .3)}>РӮЙХАТ</div>
<div class="mono acc" style="left:66px;top:300px;font-size:56px;font-weight:800" {A('up', X_NEXT + .8)}>array</div>
<div class="sub" style="left:68px;top:380px" {A('up', X_NEXT + 1.2)}>бисёр қуттиҳо — як ҷо</div>
<div class="codechip" style="left:68px;top:470px;font-size:30px" {A('up', X_NEXT + 2.4)}><span class="k">let</span> fruits = [<span class="s">"себ"</span>, <span class="s">"нок"</span>, <span class="s">"ангур"</span>];</div>
<div style="left:820px;top:170px" {A('pop', x_sub)}><span class="pill accent" style="font-size:34px;padding:20px 40px">🔔 Обуна шавед</span></div>
<div style="left:820px;top:270px" {A('pop', x_sub + .5)}><span class="pill" style="font-size:26px;padding:16px 30px">@shahriyor_yunusov</span></div>
</section>''')
S('s-next', X_NEXT, END + 1)

chapters = [dict(t=0, title='Хук'), dict(t=S1_END, title='Давр чист?'), dict(t=S2_END, title='Аввалин давр дар IDE'), dict(t=S3_END, title='Давр қадам ба қадам'),
            dict(t=S5_END, title='Ҷамъ аз 1 то 100'), dict(t=S6_END, title='Хатогиҳои маъмул'), dict(t=S7_END, title='Вазифаҳо ва санҷиш'), dict(t=S8_END, title='Хулоса')]
ide.sort(key=lambda o: o['t']); ptr.sort(key=lambda o: o['t'])

# ---------- субтитры (.srt для YouTube; в самом видео субтитров НЕТ) ----------
MAP = [(r'ай-ди-и', 'IDE'), (r'консол лог', 'console.log'), (r'фор', 'for'), (r'лет', 'let'), (r'эррей', 'array'), (r'сум', 'sum'), (r'ай из нот дефайнд', 'i is not defined'),
       (r'ай', 'i'), (r'Инстаграм', 'Instagram'), (r'сифр', '0'), (r'панҷ ҳазору панҷоҳ', '5050')]
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
with open('../youtube-lesson-3.srt', 'w', encoding='utf8') as f:
    for k, c in enumerate(caps, 1): f.write(f"{k}\n{ts(c['t0'])} --> {ts(c['t1'])}\n{c['text']}\n\n")
with open('chapters.txt', 'w', encoding='utf8') as f:
    for c in chapters: f.write(f"{int(c['t'] // 60)}:{int(c['t'] % 60):02} {c['title']}\n")
print('END', END, 'scenes', len(scenes), 'ide ops', len(ide), 'sfx', len(sfx))
print(open('chapters.txt').read())
