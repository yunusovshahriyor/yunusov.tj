# Собирает video.html (IDE + слайды + таймлайн), sfx.json, .srt (для YouTube; в видео субтитров НЕТ) и главы для YouTube-урока 5 «Функсия».
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
S1_END = T('Тасаввур кунед, ки рецепти палав')
S2_END = T('Ба ай-ди-и')
S3_END = T('Ҳоло вуруд илова')
S4_END = T('Баъзан функсия бояд')
S5_END = T('Функсия бо шарт аз дарси')
S6_END = T('Се хатои маъмули')
S7_END = T('Ва акнун вазифа')
S8_END = T('Хулоса мекунем.')
X_NEXT = T('Дарси оянда')

# --- 0. Хук ---
h_name = T('бо номаш'); h_copy = T('Оё ҳар дафъа'); h_one = T('Як маротиба менависем'); h_func = T('Ин функсия аст'); h_quiz = T('Дар охир санҷиши')
slides.append(f'''<section class="scene" id="s-hook">
<div class="kicker" {A('down', .2)}><b>ДАРСИ 5</b>БАРНОМАСОЗӢ АЗ СИФР · JAVASCRIPT</div>
<div class="h1" style="left:60px;top:110px;font-size:128px" {A('stamp', .6)}>ФУНКСИЯ</div>
<div class="mono acc" style="left:66px;top:268px;font-size:58px;font-weight:800" {A('up', h_func)}>function</div>
<div class="sub" style="left:68px;top:350px" {A('up', h_func + .3)}>як маротиба менависем — бисёр бор истифода мебарем</div>
<div style="left:68px;top:430px" {A('left', h_copy)}><span class="pill err">📋 ҳар дафъа нусха кардан? Не!</span></div>
<div style="left:68px;top:498px" {A('left', h_one)}><span class="pill ok">⚙️ як маротиба менависем</span></div>
<div style="left:68px;top:566px" {A('left', h_func + .8)}><span class="pill">🔁 ва бисёр бор даъват мекунем</span></div>
<div style="left:830px;top:150px" {A('pop', h_name)}><span class="pill">👋 «Салом, Нигина!»</span></div>
<div style="left:830px;top:218px" {A('pop', h_name + .5)}><span class="pill">👋 «Салом, Фарҳод!»</span></div>
<div style="left:830px;top:286px" {A('pop', h_name + 1.0)}><span class="pill">👋 «Салом, Зарина!»</span></div>
<div class="node" style="left:830px;top:400px;width:340px" {A('pop', h_one)}><span class="big">⚙️</span><span class="mono">greet(name)</span><small>як рецепт</small></div>
<div style="left:850px;top:640px" {A('pop', h_quiz)}><span class="pill accent">🎯 Дар охир: санҷиши нав</span></div>
</section>''')
S('s-hook', 0, S1_END)

# --- 1. Образи рецепт ---
r_pal = S1_END; r_once = T('Рецептро як маротиба'); r_use = T('ҳамон рецептро'); r_three = T('Рецепт се чиз'); r_med = T('Ҷузъҳоро медиҳем'); r_works = T('рецепт кор мекунад'); r_out = T('натиҷа мебарояд')
r_func = T('Функсия ҳам ҳамин'); r_in = T('онҳоро «вуруд»'); r_ret = T('натиҷа бармегардонад'); r_ex = T('Яке аз мисолҳои'); r_calc = T('калкулятор'); r_btn = T('Рақам медиҳем')
slides.append(f'''<section class="scene" id="s-recipe">
<div class="kicker" {A('down', r_pal)}><b>01</b>ФУНКСИЯ ЧИСТ?</div>
<div class="node" style="left:380px;top:150px;width:520px" {A('pop', r_pal + .3, r_three - .3)}><span class="big">📖</span>Рецепти палав</div>
<div style="left:140px;top:400px" {A('pop', r_once, r_three - .3)}><span class="pill ok">✍️ навиштан: як маротиба</span></div>
<div style="left:700px;top:400px" {A('pop', r_use, r_three - .3)}><span class="pill accent">🔁 истифода: бисёр бор</span></div>
<div class="h2" style="left:60px;top:90px;font-size:44px" {A('up', r_three, r_ex - .3)}>Рецепт: ҷузъҳо → кор → натиҷа</div>
<div class="node" style="left:60px;top:200px;width:320px" {A('up', r_med, r_ex - .3)}><span class="big">🍚🥩🥕</span>ҷузъҳо<small>вуруд</small></div>
<div class="h2" style="left:410px;top:235px;font-size:44px" {A('fade', r_works, r_ex - .3)}>→</div>
<div class="node yes" style="left:480px;top:200px;width:320px" {A('up', r_works, r_ex - .3)}><span class="big">⚙️</span>рецепт<small>функсия</small></div>
<div class="h2" style="left:830px;top:235px;font-size:44px" {A('fade', r_out, r_ex - .3)}>→</div>
<div class="node" style="left:900px;top:200px;width:320px" {A('up', r_out, r_ex - .3)}><span class="big">🍲</span>палав<small>натиҷа</small></div>
<div style="left:60px;top:470px" {A('left', r_func, r_ex - .3)}><span class="pill">вуруд = <span class="mono" style="color:var(--purple)">параметр</span></span></div>
<div style="left:60px;top:538px" {A('left', r_in + 1.2, r_ex - .3)}><span class="pill">рецепт = <span class="mono" style="color:var(--purple)">function</span></span></div>
<div style="left:60px;top:606px" {A('left', r_ret, r_ex - .3)}><span class="pill">натиҷа = <span class="mono" style="color:var(--purple)">return</span></span></div>
<div class="h2" style="left:60px;top:110px;font-size:46px" {A('up', r_ex + .1)}>Мисоли оддӣ: калкулятор 🧮</div>
<div class="node" style="left:60px;top:260px;width:300px" {A('up', r_btn)}><span class="mono" style="font-size:72px">5</span><small>вуруд</small></div>
<div class="h2" style="left:395px;top:290px;font-size:44px" {A('fade', r_btn + .3)}>→</div>
<div class="node yes" style="left:470px;top:260px;width:360px" {A('pop', r_btn + .4)}><span class="mono" style="font-size:44px">× 2</span><small>«ду баробар»</small></div>
<div class="h2" style="left:865px;top:290px;font-size:44px" {A('fade', r_btn + .8)}>→</div>
<div class="node" style="left:940px;top:260px;width:280px" {A('pop', r_btn + 1.2)}><span class="mono" style="font-size:72px;color:var(--teal)">10</span><small>натиҷа</small></div>
</section>''')
S('s-recipe', S1_END, S2_END)

# --- 2. Аввалин функсия дар IDE ---
S('ide', S2_END, S8_END)
setc(S2_END, ''); clear(S2_END)
chip(S2_END + .1, S2_END + 2.0, '<span>💻</span><div>Аввалин функсия дар IDE<small>02 · ҳамроҳи ман нависед</small></div>', 'card')
t_link = T('Пайванд дар тавсиф')
chip(t_link, t_link + 3.6, '🔗 yunusovshahriyor.github.io/yunusov.tj/ide', 'side yel', 'top:90px')
SH0 = 'function sayHello() {\n}'
SH1 = 'function sayHello() {\n  console.log("Салом!");\n}'
a_fn = T('фанкшн, ном'); a_body = T('консол лог, «Салом!»'); a_run = T('Иҷро мекунем.'); a_none = T('Ҳеҷ чиз нашуд'); a_why = T('Мо рецептро навиштем'); a_call = T('Функсияро даъват'); a_call2 = T('сей хелло бо қавс'); a_run2 = T('Иҷро.', a_call2); a_ok = T('«Салом!».', a_run2)
a_two = T('Ду бор нависем'); a_three = T('Се бор — се бор'); a_rule = T('Қоида:'); a_once = T('навиштан — як бор'); a_any = T('даъват — ҳар қадар')
zoom(a_fn - .3, a_run - .3, 330, 250, 1.4)
typ(a_fn, SH0, 2.6)
typ(a_body - .4, SH1, 2.2)
run(a_run + .4)
ring(a_none, a_why - .1, '#out', '⚠️ ҳеҷ чиз!', 'r', 2)
mark(a_why, a_call - .2, 0, 0, 8, '📖 рецепт навишта шуд', 'c')
C1 = SH1 + '\nsayHello();'
typ(a_call2 - .6, C1, 1.2)
run(a_run2 - .2)
ring(a_ok, a_two - .1, '#out', '✅ Салом!', 'g', 2)
C2 = C1 + '\nsayHello();'
typ(a_two, C2, .8)
run(a_two + 1.0)
ring(a_two + 1.5, a_three - .1, '#out', '2 бор', 'g', 2)
C3 = C2 + '\nsayHello();'
typ(a_three, C3, .8)
run(a_three + 1.0)
ring(a_three + 1.5, a_rule - .1, '#out', '3 бор', 'g', 2)
mark(a_once, a_any - .1, 0, 0, 19, '✍️ навиштан: як бор', 'c')
mark(a_any, S3_END - .3, 3, 0, 11, '🔁 даъват: ҳар қадар', 'g', 'below')

# --- 3. Параметр ---
setc(S3_END, ''); clear(S3_END)
chip(S3_END + .1, S3_END + 1.8, '<span>📦</span><div>Параметр<small>03 · функсия бо вуруд</small></div>', 'card')
GR0 = 'function greet(name) {\n}'
GR1 = 'function greet(name) {\n  console.log("Салом, " + name + "!");\n}'
b_par = T('Дар қавс ном менависем'); b_isp = T('Ин параметр аст'); b_same = T('Ҳамон қуттии нейм'); b_in = T('Дар дохил:', b_isp); b_plus = T('Матнҳоро бо плюс'); b_call = T('Даъват:', b_plus); b_g1 = T('грит, дар қавс «Нигина»'); b_run = T('Иҷро.', b_g1); b_g2 = T('Ва грит'); b_run2 = T('«Салом, Фарҳод!».'); b_same2 = T('Код як')
zoom(b_par - .3, b_run - .4, 330, 250, 1.4)
typ(b_par + .2, GR0, 2.6)
mark(b_isp, b_same - .1, 0, 15, 19, '📦 параметр', 'c')
mark(b_same, b_in - .1, 0, 15, 19, 'ҳамон қуттӣ (дарси 1)', 'y', 'below')
typ(b_in + .1, GR1, 3.6)
mark(b_plus, b_call - .1, 1, 14, 36, 'матн + матн (дарси 1)', 'g', 'below')
G2 = GR1 + '\ngreet("Нигина");'
typ(b_call + .4, G2, 1.8)
run(b_run - .2)
ring(b_run + 1.0, b_g2 - .1, '#out', '✅ Салом, Нигина!', 'g', 2)
G3 = G2 + '\ngreet("Фарҳод");'
typ(b_g2 - .2, G3, 1.6)
run(b_run2 - .3)
ring(b_run2, S4_END - .2, '#out', '2 натиҷа — як код', 'g', 2)

# --- 4. return ---
setc(S4_END, ''); clear(S4_END)
chip(S4_END + .1, S4_END + 1.8, '<span>↩️</span><div>return: ҷавоб бармегардонем<small>04 · double(x)</small></div>', 'card')
DB0 = 'function double(x) {\n}'
DB1 = 'function double(x) {\n  return x * 2;\n}'
c_fn = T('фанкшн дабл'); c_body = T('риторн, икс'); c_call = T('консол лог, дабл, дар қавс панҷ'); c_run = T('Иҷро.', c_call); c_ten = T('Даҳ!'); c_ret = T('Риторн — ҷавоб'); c_box = T('лет резалт'); c_plus = T('резалт плюс як'); c_diff = T('Фарқ:'); c_log = T('консол лог — нишон'); c_retw = T('риторн — баргардонад')
zoom(c_fn - .3, c_run - .3, 330, 250, 1.4)
typ(c_fn, DB0, 1.4)
typ(c_body - .2, DB1, 1.6)
mark(c_body + .3, c_call - .2, 1, 2, 8, '↩️ ҷавоб бармегардонад', 'g')
D2 = DB1 + '\nconsole.log(double(5));'
typ(c_call - .4, D2, 2.2)
run(c_run - .2)
ring(c_ten, c_ret - .1, '#out', '✅ 10', 'g', 2)
mark(c_ret, c_box - .2, 3, 12, 21, '← ҷавоб ба ин ҷо', 'c', 'below')
D3 = DB1 + '\nlet result = double(4);\nconsole.log(result + 1);'
typ(c_box - .3, D3, 2.6)
mark(c_box + 1.0, c_plus - .1, 3, 4, 10, '📦 қуттӣ', 'y')
run(c_plus + .9)
ring(c_plus + 1.4, c_diff - .1, '#out', '9', 'g', 2)
mark(c_log, c_retw - .1, 4, 0, 11, 'нишон медиҳад', 'c', 'below')
mark(c_retw, S5_END - .3, 1, 2, 8, 'баргардонад', 'g')

# --- 5. Функсия бо шарт ---
setc(S5_END, ''); clear(S5_END)
chip(S5_END + .1, S5_END + 1.8, '<span>❓</span><div>Функсия бо шарт<small>05 · isAdult(age)</small></div>', 'card')
AD0 = 'function isAdult(age) {\n}'
AD1 = 'function isAdult(age) {\n  return age >= 18;\n}'
d_fn = T('из эдалт, параметр'); d_ret = T('Риторн: эйдж калон'); d_call = T('Даъват:', d_ret); d_run = T('Иҷро.', d_call); d_res = T('тру, тру, фолс'); d_kid = T('Ҳаждаҳсола ҳам')
typ(d_fn, AD0, 1.8)
typ(d_ret + .1, AD1, 2.4)
mark(d_ret + 1.0, d_call - .2, 1, 9, 18, '❓ шарт аз дарси 2', 'y')
AD2 = AD1 + '\nconsole.log(isAdult(20), isAdult(18), isAdult(17));'
typ(d_call + .4, AD2, 3.2)
run(d_run - .2)
ring(d_res, d_kid + 2.8, '#out', '✅ true true false', 'g', 2)

# --- 6. Хатогиҳои маъмул ---
setc(S6_END, ''); clear(S6_END)
chip(S6_END + .1, S6_END + 2.0, '<span>🐞</span><div>Се хатои маъмул<small>06 · ҳама хато мекунанд — ин муқаррарӣ аст</small></div>', 'card')
e1 = T('Якум:', S6_END); e1c = T('фаромӯш кардани даъват'); e1n = T('аммо даъват нашуд'); e2 = T('Дуюм:', e1c); e2w = T('риторн-ро нанавиштан'); e2u = T('ҷавоб андефайнд'); e2l = T('Риторн лозим'); e3 = T('Саввум:', e2l); e3w = T('вуруд надодан'); e3u = T('«Салом, андефайнд!»'); e3p = T('Параметр қимат интизор')
chip(e1 + .1, e1 + 2.3, 'Хатои 1 / 3', 'side red', 'top:70px;left:1090px')
zoom(e1c, e1n + 1.2, 330, 250, 1.4)
typ(e1c + .2, SH1, 2.6)
run(e1n + 2.2, 'bad', None)
ring(e1n + 2.8, e2 - .2, '#out', '⚠️ ҳеҷ чиз — даъват нашуд', 'r', 2)
chip(e2 + .1, e2 + 2.3, 'Хатои 2 / 3', 'side red', 'top:70px;left:1090px')
E2 = 'function double(x) {\n  x * 2;\n}\nconsole.log(double(5));'
zoom(e2w - .2, e2u + .3, 330, 250, 1.4)
typ(e2w + .1, E2, 3.2)
mark(e2w + 1.3, e2l, 1, 2, 7, '⚠️ return нест!', 'r')
run(e2u + .8)
ring(e2u + 1.4, e3 - .2, '#out', '⚠️ undefined', 'r', 2)
chip(e3 + .1, e3 + 2.3, 'Хатои 3 / 3', 'side red', 'top:70px;left:1090px')
E3 = 'function greet(name) {\n  console.log("Салом, " + name + "!");\n}\ngreet();'
zoom(e3w, e3u - .3, 330, 250, 1.4)
typ(e3w + .2, E3, 3.2)
mark(e3w + 2.0, e3u + 1.0, 3, 5, 7, '⚠️ ном нест', 'r')
run(e3u + .3)
ring(e3u + 1.0, S7_END - .3, '#out', '⚠️ Салом, undefined!', 'r', 2)

# --- 7. Вазифаҳо ---
t_tab = T('ҷадвали', S7_END); t_three = T('Се вазифа ҳаст'); t_t1 = T('Якум:', t_three); t_t1w = T('функсияи дабл нависед'); t_t2 = T('Дуюм:', t_t1); t_t2w = T('из эдалт — агар'); t_t3 = T('Саввум:', t_t2); t_t3w = T('грит —', t_t3); t_chk = T('Ай-ди-и месанҷад')
t_q = T('Ва санҷиши нав'); t_dbl = T('ҳамон функсияи дабл'); t_cl = T('Консол лог, дабл, дар дохил'); t_what = T('Чӣ мешавад?'); t_pz = T('Видеоро пауза')
t_ans = T('Ҷавоб:', t_pz); t_12 = T('дувоздаҳ.', t_ans); t_in = T('Аввал дарун'); t_out = T('Баъд берун'); t_fin = T('Функсияро ба функсия')
chip(S7_END + .1, S7_END + 2.0, '<span>🎯</span><div>Вазифаҳо барои шумо<small>07 · дар IDE, ҷадвали «5 · Функсия»</small></div>', 'card')
click(t_tab + .9, '#tabs .tab:nth-child(6)')
ST1 = 'function double(x) {\n  // return ...\n}\n'; ST2 = 'function isAdult(age) {\n  // ...\n}\n'; ST3 = 'function greet(name) {\n  // ...\n}\n'
setc(t_tab + .92, ST1)
ring(t_tab + 1.4, t_three - .2, '#tabs .tab:nth-child(6)', '', 'y', 4)
ring(t_three, t_t1 - .1, '#side', '📘 назария', 'c', 4)
ring(t_t1, t_t2 - .1, '#task', 'Вазифаи 1', 'y', 4)
SOL1 = 'function double(x) {\n  return x * 2;\n}\n'
typ(t_t1w, SOL1, 3.6)
click(t_t2 + .3, '#side button[data-i="1"]'); setc(t_t2 + .32, ST2)
ring(t_t2 + .8, t_t3 - .1, '#task', 'Вазифаи 2', 'y', 4)
SOL2 = 'function isAdult(age) {\n  return age >= 18;\n}\n'
typ(t_t2w, SOL2, 4.0)
click(t_t3 + .3, '#side button[data-i="2"]'); setc(t_t3 + .32, ST3)
ring(t_t3 + .8, t_chk - .1, '#task', 'Вазифаи 3', 'y', 4)
SOL3 = 'function greet(name) {\n  return "Салом, " + name + "!";\n}\n'
typ(t_t3w, SOL3, 3.0)
ring(t_chk - .3, t_chk + .9, '#check', '✓ Санҷиш', 'c', 6)
click(t_chk + .5, '#check', 'check'); sfx.append(dict(name='chime', t=t_chk + .9, gain=.6))
ring(t_chk + 1.0, t_q - .3, '#checks', '', 'g', 4)
QZ0 = 'function double(x) {\n  return x * 2;\n}\n'
QZ1 = QZ0 + 'console.log(double(double(3)));'
click(t_q + .1, '#tabs .tab:nth-child(1)'); setc(t_q + .12, '')
zoom(t_dbl - .3, t_what - .2, 330, 250, 1.4)
typ(t_dbl + .1, QZ0, 2.4)
typ(t_cl + .1, QZ1, 3.0)
mark(t_what, t_pz - .3, 3, 12, 29, '❓ чӣ мешавад?', 'y')
g0 = V(GAP_Q) - PAUSE
chip(t_what, g0 - .3, '<span class="big">❓</span><div>double(double(3)) — чӣ мешавад?<small>видеоро пауза кунед ✍️</small></div>', 'card')
for k in range(5):
    chip(g0 + k + .02, g0 + k + .62, f'<span class="big">{5 - k}</span><div>double(double(3)) — чӣ мешавад?<small>фикр кунед · баъд ҷавобро мебинем ✅</small></div>', 'card')
    sfx.append(dict(name='tick', t=g0 + k, gain=.8))
run(t_ans + .3)
ring(t_12, t_fin - .1, '#out', '✅ 12', 'g', 2)
mark(t_in, t_out - .1, 3, 19, 28, 'дарун: double(3) = 6', 'c', 'below')
mark(t_out, t_fin - .1, 3, 12, 29, 'берун: double(6) = 12', 'g')

# --- 8. Хулоса ---
x1 = T('Функсия — рецепти барнома', S8_END); x2 = T('як маротиба менависем', x1); x3 = T('Вуруд — параметр', S8_END); x_pdf = T('Шпаргалкаи бепул')
slides.append(f'''<section class="scene" id="s-sum">
<div class="kicker" {A('down', S8_END + .2)}><b>08</b>ХУЛОСА</div>
<div class="h2" style="left:60px;top:90px;font-size:50px" {A('up', x1)}>Функсия = <span class="acc">ном + вуруд + return</span></div>
<div class="card3" style="left:60px;top:220px;width:360px;height:250px" {A('up', x2)}><div class="emo">🏷️</div><div class="t">Ном</div><div class="codechip" style="font-size:22px"><span class="k">function</span> <span class="f">double</span></div></div>
<div class="card3" style="left:460px;top:220px;width:360px;height:250px" {A('up', x3)}><div class="emo">📥</div><div class="t">Вуруд (параметр)</div><div class="codechip" style="font-size:22px">(<span class="k">x</span>)</div></div>
<div class="card3" style="left:860px;top:220px;width:360px;height:250px" {A('up', x3 + 1.6)}><div class="emo">📤</div><div class="t">Ҷавоб</div><div class="codechip" style="font-size:22px"><span class="k">return</span> x * <span class="n">2</span>;</div></div>
<div style="left:60px;top:510px" {A('up', x2 + 1.5)}><span class="pill ok">навиштан — як бор · даъват — ҳар қадар 🔁</span></div>
<div style="left:60px;top:580px" {A('up', x_pdf)}><span class="pill accent">📘 Шпаргалкаи бепул (PDF) — дар тавсифи видео</span></div>
</section>''')
S('s-sum', S8_END, X_NEXT)

x_sub = T('Обуна шавед')
slides.append(f'''<section class="scene" id="s-next">
<div class="kicker" {A('down', X_NEXT + .1)}><b>ДАРСИ 6</b>НАВБАТӢ</div>
<div class="h1" style="left:60px;top:130px;font-size:130px" {A('stamp', X_NEXT + .3)}>ОБЪЕКТ</div>
<div class="mono acc" style="left:66px;top:290px;font-size:56px;font-weight:800" {A('up', X_NEXT + .8)}>object</div>
<div class="sub" style="left:68px;top:370px" {A('up', X_NEXT + 1.2)}>маълумоти як чиз — дар як ҷо</div>
<div class="codechip" style="left:68px;top:460px;font-size:28px;line-height:1.5" {A('up', X_NEXT + 2.4)}><span class="k">let</span> person = {{<br>&nbsp;&nbsp;name: <span class="s">"Нигина"</span>,<br>&nbsp;&nbsp;age: <span class="n">20</span><br>}};</div>
<div style="left:820px;top:170px" {A('pop', x_sub)}><span class="pill accent" style="font-size:34px;padding:20px 40px">🔔 Обуна шавед</span></div>
<div style="left:820px;top:270px" {A('pop', x_sub + .5)}><span class="pill" style="font-size:26px;padding:16px 30px">@shahriyor_yunusov</span></div>
</section>''')
S('s-next', X_NEXT, END + 1)

chapters = [dict(t=0, title='Хук'), dict(t=S1_END, title='Функсия чист?'), dict(t=S2_END, title='Аввалин функсия дар IDE'), dict(t=S3_END, title='Параметр'),
            dict(t=S4_END, title='return: ҷавоб бармегардонем'), dict(t=S5_END, title='Функсия бо шарт'), dict(t=S6_END, title='Хатогиҳои маъмул'), dict(t=S7_END, title='Вазифаҳо ва санҷиш'), dict(t=S8_END, title='Хулоса')]
ide.sort(key=lambda o: o['t']); ptr.sort(key=lambda o: o['t'])

# ---------- субтитры (.srt для YouTube; в самом видео субтитров НЕТ) ----------
MAP = [(r'ай-ди-и', 'IDE'), (r'консол лог', 'console.log'), (r'сей хелло', 'sayHello'), (r'из эдалт', 'isAdult'), (r'грит-ро', 'greet-ро'), (r'грит', 'greet'), (r'дабл', 'double'), (r'резалт', 'result'),
       (r'фанкшн', 'function'), (r'риторн-ро', 'return-ро'), (r'риторн', 'return'), (r'андефайнд', 'undefined'), (r'нейм', 'name'), (r'эйдж', 'age'), (r'тру', 'true'), (r'фолс', 'false'), (r'лет', 'let'), (r'икс', 'x'), (r'Инстаграм', 'Instagram')]
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
with open('../youtube-lesson-5.srt', 'w', encoding='utf8') as f:
    for k, c in enumerate(caps, 1): f.write(f"{k}\n{ts(c['t0'])} --> {ts(c['t1'])}\n{c['text']}\n\n")
with open('chapters.txt', 'w', encoding='utf8') as f:
    for c in chapters: f.write(f"{int(c['t'] // 60)}:{int(c['t'] % 60):02} {c['title']}\n")
print('END', END, 'scenes', len(scenes), 'ide ops', len(ide), 'sfx', len(sfx))
print(open('chapters.txt').read())
