# Собирает video.html (IDE + слайды + таймлайн), sfx.json, .srt (для YouTube; в видео субтитров НЕТ) и главы для YouTube-урока 8 «Хатогӣ ва дебаг».
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
S1_END = T('Хатои барномаро')
S_IDE = T('Ба ай-ди-и')
S_E2 = T('Мисоли дуюм')
S_TASK = T('Ва акнун вазифа')
S_SUM = T('Хулоса мекунем.')
X_NEXT = T('Дарси оянда')

# --- 0. Хук ---
h_hi = T('Салом, дӯстон!'); h_code = T('Бисту панҷ плюс як'); h_251 = T('дусаду панҷоҳу як'); h_26 = T('Мо бисту шаш'); h_pc = T('Компютер хато накард'); h_bug = T('хато дар код аст'); h_how = T('чӣ тавр чунин'); h_dbg = T('Ин дебаг аст'); h_quiz = T('Дар охир санҷиши')
slides.append(f'''<section class="scene" id="s-hook">
<div class="kicker" {A('down', .2)}><b>ДАРСИ 8</b>БАРНОМАСОЗӢ АЗ СИФР · JAVASCRIPT</div>
<div class="h1" style="left:60px;top:100px;font-size:104px;line-height:1.05" {A('stamp', .6)}>ХАТОГӢ ВА<br>ДЕБАГ</div>
<div style="left:68px;top:370px" {A('bob', h_hi, h_code - .1, 'shrink')}><span class="pill accent" style="font-size:30px;padding:16px 30px">👋 Салом, дӯстон!</span></div>
<div class="codechip" style="left:68px;top:370px;font-size:28px" {A('pop', h_code)} data-tw="{h_code};2.4" data-text='let age = "25" + 1;'></div>
<div class="node no" style="left:830px;top:140px;width:340px" {A('drop', h_251)}><span class="big">😵</span><span class="mono" style="font-size:64px;color:var(--err)">251</span><small>натиҷа</small></div>
<div class="node yes" style="left:830px;top:390px;width:340px" {A('pop', h_26)}><span class="big">🎯</span><span class="mono" style="font-size:64px;color:var(--teal)">26</span><small>мо интизор будем</small></div>
<div style="left:68px;top:450px" {A('left', h_pc)}><span class="pill ok">🤖 компютер хато накард</span></div>
<div style="left:68px;top:512px" {A('left', h_bug)}><span class="pill err">🐞 хато дар код аст</span></div>
<div style="left:68px;top:574px" {A('left', h_how)}><span class="pill">🔎 чӣ тавр ёфтан?</span></div>
<div style="left:68px;top:636px" {A('bob', h_dbg)}><span class="pill accent" style="font-size:28px;padding:14px 28px">🛠️ ДЕБАГ</span></div>
<div style="left:850px;top:650px" {A('pop', h_quiz)}><span class="pill accent">🎯 Дар охир: санҷиши нав</span></div>
</section>''')
S('s-hook', 0, S1_END)

# --- 1. Баг ва механик ---
g_bug = T('«баг»'); g_find = T('Ёфтан ва ислоҳ'); g_dbg = T('дебаг мебошад'); g_imag = T('Тасаввур кунед'); g_car = T('мошини шумо'); g_stop = T('ҳаракат намекунад'); g_mech = T('Механик чӣ кор'); g_look = T('Аввал мебинад'); g_test = T('Баъд қисм ба қисм')
g_acc = T('аккумулятор,'); g_fuel = T('сӯзишворӣ,'); g_wheel = T('чарх.'); g_fix = T('таъмир мекунад'); g_code = T('Дар код ҳам'); g_three = T('Се қадам'); g_1 = T('бубин, санҷ'); g_2 = T('санҷ, ислоҳ'); g_3 = T('ислоҳ кун.')
PA = g_imag - .25; PB = g_code - .25
slides.append(f'''<section class="scene" id="s-bug">
<div class="kicker" {A('down', S1_END + .1)}><b>01</b>БАГ ВА ДЕБАГ</div>
<div class="h1" style="left:60px;top:130px;font-size:128px" {A('stamp', g_bug, PA)}>БАГ</div>
<div style="left:70px;top:290px" {A('pop', g_bug + .3, PA)}><span class="pill err" style="font-size:30px;padding:16px 30px">🐞 хатои барнома</span></div>
<div class="h2" style="left:480px;top:170px;font-size:64px" {A('fade', g_find, PA)}>→</div>
<div class="h1 acc" style="left:580px;top:130px;font-size:128px" {A('stamp', g_find, PA)}>ДЕБАГ</div>
<div style="left:580px;top:290px" {A('pop', g_find + .5, PA)}><span class="pill ok" style="font-size:30px;padding:16px 30px">🔎 ёфтан + 🛠️ ислоҳ</span></div>

<div class="node no" style="left:60px;top:140px;width:300px" {A('pop', g_car, PB)}><span class="big">🚗</span>мошин<small>ҳаракат намекунад</small></div>
<div style="left:60px;top:380px" {A('left', g_stop, PB)}><span class="pill err">🔴 чароғи хато</span></div>
<div class="node yes" style="left:430px;top:140px;width:300px" {A('pop', g_mech, PB)}><span class="big">🧑‍🔧</span>механик<small>чӣ кор мекунад?</small></div>
<div style="left:430px;top:380px" {A('left', g_look, PB)}><span class="pill">👀 аввал мебинад</span></div>
<div style="left:430px;top:448px" {A('left', g_test, PB)}><span class="pill">🔎 қисм ба қисм месанҷад</span></div>
<div style="left:800px;top:150px" {A('left', g_acc, PB)}><span class="pill">🔋 аккумулятор</span></div>
<div style="left:800px;top:218px" {A('left', g_fuel, PB)}><span class="pill">⛽ сӯзишворӣ</span></div>
<div style="left:800px;top:286px" {A('left', g_wheel, PB)}><span class="pill">🛞 чарх</span></div>
<div style="left:430px;top:516px" {A('left', g_fix, PB)}><span class="pill ok">🛠️ таъмир мекунад</span></div>

<div class="h2" style="left:60px;top:90px;font-size:48px" {A('up', g_code)}>Дар код ҳам ҳамин тавр</div>
<div class="card3" style="left:60px;top:220px;width:360px;height:260px" {A('up', g_1)}><div class="emo">👀</div><div class="t">1 · Бубин</div><div class="u">чӣ гирифтем, чӣ мехостем</div></div>
<div class="card3" style="left:460px;top:220px;width:360px;height:260px" {A('up', g_2)}><div class="emo">🔎</div><div class="t">2 · Санҷ</div><div class="u">бо console.log</div></div>
<div class="card3" style="left:860px;top:220px;width:360px;height:260px" {A('up', g_3)}><div class="emo">🛠️</div><div class="t">3 · Ислоҳ кун</div><div class="u">як чиз ва санҷиши дубора</div></div>
</section>''')
S('s-bug', S1_END, S_IDE)

# --- 2. IDE ---
S('ide', S_IDE, S_SUM)
setc(S_IDE, ''); clear(S_IDE)
t_link = T('Пайванд дар тавсиф')
chip(t_link, t_link + 3.4, '🔗 yunusovshahriyor.github.io/yunusov.tj/ide', 'side yel', 'top:90px')
chip(S_IDE + .1, S_IDE + 2.0, '<span>🐞</span><div>Дебаг: бубин · санҷ · ислоҳ<small>02 · ҳамроҳи ман нависед</small></div>', 'card')
A0 = 'let age = "25" + 1;'
A1 = A0 + '\nconsole.log(age);'
A2 = A1 + '\nconsole.log(typeof age);'
A3 = 'let age = Number("25") + 1;\nconsole.log(age);\nconsole.log(typeof age);'
a_let = T('лет эйдж баробари'); a_log = T('Консол лог, эйдж.'); a_run = T('Иҷро.', a_log); a_251 = T('Дусаду панҷоҳу як!'); a_s1 = T('Қадами якум'); a_got = T('Чӣ гирифтем?'); a_want = T('Чӣ мехостем?'); a_att = T('Диққат: паёми хато'); a_s2 = T('Қадами дуюм'); a_type = T('Консол лог, тайп-оф'); a_run2 = T('Иҷро.', a_type); a_str = T('Стринг'); a_why = T('Чаро?')
a_q = T('Дар қавс «бисту'); a_cat = T('компютер онҳоро'); a_box = T('Ин ҳамон қуттии'); a_tip = T('Маслиҳат:'); a_s3 = T('Қадами сеюм'); a_num = T('Намбер, дар қавс'); a_run3 = T('Иҷро.', a_num); a_26 = T('Бисту шаш!', a_run3); a_numw = T('Намбер матнро'); a_check = T('Ва акнун санҷед'); a_cmp = T('натиҷаро бо')
zoom(a_let - .3, S_E2 - .3, 330, 250, 1.4)
typ(a_let, A0, 3.4)
typ(a_log, A1, 1.2)
run(a_run + .3)
ring(a_251, a_want, '#out', '⚠️ 251', 'r', 2)
chip(a_s1, a_att - .2, '👀 Қадами 1 · бубин', 'side yel', 'top:70px;left:1050px')
chip(a_got, a_want + 2.0, 'Чӣ гирифтем — 251', 'side red', 'top:130px;left:1050px')
chip(a_want, a_want + 3.6, 'Чӣ мехостем — 26', 'side grn', 'top:190px;left:1050px')
chip(a_att + .1, a_att + 3.8, '⚠️ Паёми хато нест!<small>барнома кор кард — лекин нодуруст</small>', 'card')
chip(a_s2, a_tip - .2, '🔎 Қадами 2 · санҷ', 'side yel', 'top:70px;left:1050px')
typ(a_type - .3, A2, 2.2)
run(a_run2 + .2)
ring(a_str, a_box - .1, '#out', '✅ string — матн!', 'g', 2)
mark(a_q, a_cat - .1, 0, 10, 14, '"25" — матн, на рақам', 'c')
mark(a_cat, a_box - .1, 0, 15, 16, 'часпонидан', 'y', 'below')
chip(a_box, a_tip - .2, '<span class="big">📦</span><div>age = "25"<small>қуттии матнӣ (дарси 1)</small></div>', 'card')
chip(a_tip, a_s3 - .2, '<span class="big">💡</span><div>Маслиҳат<small>шубҳа дорӣ — console.log гузор</small></div>', 'card')
chip(a_s3, a_check, '🛠️ Қадами 3 · ислоҳ', 'side yel', 'top:70px;left:1050px')
typ(a_num, A3, 3.0)
mark(a_numw, a_run3 - .1, 0, 10, 22, '🔧 Number → рақам', 'g')
run(a_run3 + .15)
ring(a_26, a_check, '#out', '✅ 26 · number', 'g', 2)
chip(a_cmp - .6, a_cmp + 2.0, '<span class="big">🔁</span><div>санҷиши дубора<small>натиҷа = чӣ мехостем? 26 ✅</small></div>', 'card')

# --- мисоли дуюм ---
setc(S_E2, ''); clear(S_E2)
chip(S_E2 + .1, S_E2 + 2.0, '<span>🧮</span><div>Мисоли дуюм: функсия<small>03 · average(a, b)</small></div>', 'card')
F0 = 'function average(a, b) {\n}'
F1 = 'function average(a, b) {\n  return a + b / 2;\n}'
F2 = F1 + '\nconsole.log(average(10, 20));'
F3 = F2 + '\nconsole.log(20 / 2);'
F4 = 'function average(a, b) {\n  return (a + b) / 2;\n}\nconsole.log(average(10, 20));\nconsole.log(20 / 2);'
f_fn = T('фанкшн эверейҷ'); f_ret = T('Риторн: эй плюс би'); f_call = T('Даъват: эверейҷ'); f_run = T('Иҷро —'); f_20 = T('бист!', f_run); f_s1 = T('Қадами якум:', f_run); f_s2 = T('Қадами дуюм:', f_run); f_cl = T('Консол лог, бист тақсим')
f_ten = T('даҳ.', f_cl); f_div = T('тақсим пеш аз плюс'); f_pc1 = T('Компютер аввал'); f_pc2 = T('баъд даҳро'); f_s3 = T('Қадами сеюм:', f_run); f_par = T('Дар қавс эй плюс би'); f_run3 = T('Иҷро —', f_par); f_15 = T('понздаҳ!', f_run3); f_thus = T('Ҳамин тавр:', f_run3)
zoom(f_fn - .3, S_TASK - .3, 330, 250, 1.4)
typ(f_fn, F0, 2.5)
typ(f_ret, F1, 3.0)
typ(f_call - .1, F2, 2.6)
run(f_run + .2)
ring(f_20, f_s2 - .1, '#out', '⚠️ 20 (мехостем 15)', 'r', 2)
chip(f_s1, f_s2 - .1, '👀 Қадами 1 · бубин', 'side yel', 'top:70px;left:1050px')
chip(f_s2, f_s3 - .1, '🔎 Қадами 2 · санҷ', 'side yel', 'top:70px;left:1050px')
typ(f_cl - .3, F3, 2.2)
run(f_ten + .15)
ring(f_ten + .6, f_div - .1, '#out', '10 = 20 / 2', 'c', 2)
mark(f_div, f_pc1 - .1, 1, 13, 18, '➗ аввал тақсим', 'r')
mark(f_pc1, f_pc2 - .1, 1, 13, 18, 'b / 2 = 10', 'c')
mark(f_pc2, f_s3 - .1, 1, 9, 18, 'a + 10 = 20', 'y', 'below')
chip(f_s3, f_thus - .1, '🛠️ Қадами 3 · ислоҳ', 'side yel', 'top:70px;left:1050px')
typ(f_par, F4, 2.4)
mark(f_par + 2.5, f_run3 - .05, 1, 9, 16, 'қавс — аввал ҷамъ', 'g')
run(f_run3 + .15)
ring(f_15, f_thus - .1, '#out', '✅ 15', 'g', 2)
chip(f_thus, S_TASK - .4, '<span class="big">👀 → 🔎 → 🛠️</span><div>бубин · санҷ · ислоҳ<small>ҳамин тавр дебаг мекунем</small></div>', 'card')

# --- 3. Вазифаҳо ---
t_tab = T('ҷадвали «Озод»-ро'); t_three = T('Се барномаи'); t_t1 = T('Якум: нарх'); t_t1w = T('нарх ба «сад»'); t_ok1 = T('Бояд саду бист'); t_t2 = T('Дуюм: давр'); t_t2w = T('давр, ки ҷамъро'); t_bad2 = T('вале сифр'); t_t3 = T('Саввум:', t_t2); t_t3w = T('ҳамон эверейҷ')
t_q = T('Ва санҷиши нав'); t_cl = T('консол лог, «даҳ»'); t_what = T('Чӣ чоп мекунад'); t_rem = T('Ёдовар:'); t_pz = T('Видеоро пауза')
t_ans = T('Ҷавоб:', t_pz); t_105 = T('саду панҷ'); t_cat = T('Матн плюс рақам', t_ans); t_fixw = T('Агар мехоҳед ҷамъ'); t_numw = T('намбер, даҳ,', t_fixw); t_15 = T('понздаҳ.', t_numw)
chip(S_TASK + .1, S_TASK + 2.0, '<span>🎯</span><div>Вазифаҳо барои шумо<small>04 · ҷадвали «Озод», кодҳо дар тавсиф</small></div>', 'card')
click(t_tab + .6, '#tabs .tab:nth-child(1)')
setc(t_tab + .62, ''); clear(t_tab + .62)
chip(t_three, t_t1 - .2, '🐞 3 барномаи хатодор', 'side red', 'top:70px;left:1050px')
chip(t_t1, t_t2 - .1, 'Вазифаи 1 / 3', 'side yel', 'top:70px;left:1050px')
V1 = 'let price = "100";\nlet total = price + 20;\nconsole.log(total);'
setc(t_t1 + .05, ''); clear(t_t1 + .05)
zoom(t_t1w - .3, t_t2 - .5, 330, 250, 1.4)
typ(t_t1w, V1, 3.2)
run(t_ok1 + .5)
ring(t_ok1 + 1.0, t_t2 - .1, '#out', '⚠️ 10020 — на 120', 'r', 2)
chip(t_t2, t_t3 - .1, 'Вазифаи 2 / 3', 'side yel', 'top:70px;left:1050px')
V2 = 'let sum = 0;\nfor (let i = 1; i <= 3; i++) {\n  sum + i;\n}\nconsole.log(sum);'
setc(t_t2 + .05, ''); clear(t_t2 + .05)
zoom(t_t2w - .3, t_t3 - .5, 330, 250, 1.4)
typ(t_t2w, V2, 2.3)
run(t_bad2 + .5)
ring(t_bad2 + 0.9, t_t3 - .1, '#out', '⚠️ 0 — на 6', 'r', 2)
chip(t_t3, t_q - .1, 'Вазифаи 3 / 3', 'side yel', 'top:70px;left:1050px')
V3 = 'function average(a, b) {\n  return a + b / 2;\n}\nconsole.log(average(10, 20));'
setc(t_t3 + .05, ''); clear(t_t3 + .05)
zoom(t_t3w - .3, t_q - .5, 330, 250, 1.4)
typ(t_t3w, V3, 1.6)
run(t_t3w + 1.9)
ring(t_t3w + 2.3, t_q - .1, '#out', '⚠️ 20 — на 15', 'r', 2)
Q0 = 'console.log("10" + 5);'
setc(t_q + .12, ''); clear(t_q + .12)
zoom(t_cl - .3, t_what - .2, 330, 250, 1.4)
typ(t_cl, Q0, 3.0)
mark(t_what, t_rem - .1, 0, 12, 20, '❓ чӣ чоп мекунад?', 'y')
mark(t_rem, t_pz - .2, 0, 12, 16, '"10" — матн!', 'c')
g0 = V(GAP_Q) - PAUSE
chip(t_pz, g0 - .3, '<span class="big">❓</span><div>"10" + 5 — чӣ чоп мекунад?<small>видеоро пауза кунед ✍️</small></div>', 'card')
for k in range(5):
    chip(g0 + k + .02, g0 + k + .62, f'<span class="big">{5 - k}</span><div>"10" + 5 — чӣ чоп мекунад?<small>фикр кунед · баъд ҷавобро мебинем ✅</small></div>', 'card')
    sfx.append(dict(name='tick', t=g0 + k, gain=.8))
run(t_ans + .3)
ring(t_105, S_SUM - .3, '#out', '✅ 105', 'g', 2)
mark(t_cat, t_fixw - .1, 0, 17, 18, 'часпонидан, на ҷамъ', 'y', 'below')
Q1 = 'console.log(Number("10") + 5);'
typ(t_fixw + 1.0, Q1, 2.2)
run(t_15 - .3)
ring(t_15, S_SUM - .3, '#out', '✅ 15', 'g', 2)

# --- 4. Хулоса ---
x_see = T('Бубин —', S_SUM); x_chk = T('Санҷ —', S_SUM); x_fix = T('Ислоҳ —', S_SUM); x_err = T('Хатогиҳо дар код'); x_pdf = T('Шпаргалкаи бепул')
slides.append(f'''<section class="scene" id="s-sum">
<div class="kicker" {A('down', S_SUM + .2)}><b>05</b>ХУЛОСА</div>
<div class="h2" style="left:60px;top:90px;font-size:50px" {A('up', S_SUM + .6)}>Дебаг = <span class="acc">бубин · санҷ · ислоҳ кун</span></div>
<div class="card3" style="left:60px;top:220px;width:360px;height:250px" {A('up', x_see)}><div class="emo">👀</div><div class="t">Бубин</div><div class="u">чӣ гирифтем ва чӣ мехостем</div></div>
<div class="card3" style="left:460px;top:220px;width:360px;height:250px" {A('up', x_chk)}><div class="emo">🔎</div><div class="t">Санҷ</div><div class="codechip" style="font-size:22px">console.log(<span class="e">…</span>)</div></div>
<div class="card3" style="left:860px;top:220px;width:360px;height:250px" {A('up', x_fix)}><div class="emo">🛠️</div><div class="t">Ислоҳ кун</div><div class="u">як чиз ва санҷиши дубора</div></div>
<div style="left:60px;top:510px" {A('up', x_err)}><span class="pill ok">🌱 хатогиҳо — роҳи фаҳмиш ва омӯзиш</span></div>
<div style="left:60px;top:580px" {A('up', x_pdf)}><span class="pill accent">📘 Шпаргалкаи бепул (PDF) — дар тавсифи видео</span></div>
</section>''')
S('s-sum', S_SUM, X_NEXT)

x_list = T('рӯйхати вазифаҳо'); x_sub = T('Обуна шавед')
slides.append(f'''<section class="scene" id="s-next">
<div class="kicker" {A('down', X_NEXT + .1)}><b>ДАРСИ 9</b>НАВБАТӢ</div>
<div class="h1" style="left:60px;top:110px;font-size:104px;line-height:1.05" {A('stamp', X_NEXT + .3)}>ЛОИҲАИ<br>ХУРД</div>
<div class="sub" style="left:68px;top:360px" {A('up', X_NEXT + 1.4)}>рӯйхати вазифаҳо</div>
<div style="left:68px;top:440px" {A('left', x_list)}><span class="pill ok">✅ дарс хондан</span></div>
<div style="left:68px;top:508px" {A('left', x_list + .5)}><span class="pill">⬜ код навиштан</span></div>
<div style="left:68px;top:576px" {A('left', x_list + 1.0)}><span class="pill">⬜ дебаг кардан</span></div>
<div style="left:820px;top:170px" {A('pop', x_sub)}><span class="pill accent" style="font-size:34px;padding:20px 40px">🔔 Обуна шавед</span></div>
<div style="left:820px;top:270px" {A('pop', x_sub + .5)}><span class="pill" style="font-size:26px;padding:16px 30px">@shahriyor_yunusov</span></div>
</section>''')
S('s-next', X_NEXT, END + 1)

chapters = [dict(t=0, title='Хук'), dict(t=S1_END, title='Баг ва механик'), dict(t=S_IDE, title='Қадами 1: бубин'), dict(t=a_s2, title='Қадами 2: санҷ'), dict(t=a_s3, title='Қадами 3: ислоҳ кун'),
            dict(t=S_E2, title='Мисоли дуюм: функсия'), dict(t=S_TASK, title='Вазифаҳо ва санҷиш'), dict(t=S_SUM, title='Хулоса')]
ide.sort(key=lambda o: o['t']); ptr.sort(key=lambda o: o['t'])
# зум: пеш аз «Иҷро» экран ба андозаи пурра бармегардад, то «Натича» дида шавад; бо навиштани навбатӣ боз зум мешавад
_runs = sorted(o['t'] for o in ide if o['op'] in ('run', 'check'))
_types = sorted(o['t'] for o in ide if o['op'] == 'type')
_out = []
for z in zooms:
    segs = [(z['t0'], z['t1'])]
    for r in _runs:
        nxt = next((t for t in _types if t > r + .3), 1e9)
        c0, c1 = r - 1.0, nxt - .2
        ns = []
        for a, c in segs:
            if c1 <= a or c0 >= c: ns.append((a, c)); continue
            if a < c0: ns.append((a, c0))
            if c1 < c: ns.append((c1, c))
        segs = ns
    _out += [dict(z, t0=a, t1=c) for a, c in segs if c - a >= 1.2]
zooms[:] = _out


# ---------- субтитры (.srt для YouTube; в самом видео субтитров НЕТ) ----------
MAP = [(r'ай-ди-и', 'IDE'), (r'консол лог', 'console.log'), (r'тайп-оф', 'typeof'), (r'стринг', 'string'), (r'намбер', 'Number'), (r'фанкшн', 'function'), (r'эверейҷ', 'average'), (r'риторн', 'return'),
       (r'лет', 'let'), (r'эйдж', 'age'), (r'эй', 'a'), (r'би', 'b'), (r'Инстаграм', 'Instagram')]
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
with open('../youtube-lesson-8.srt', 'w', encoding='utf8') as f:
    for k, c in enumerate(caps, 1): f.write(f"{k}\n{ts(c['t0'])} --> {ts(c['t1'])}\n{c['text']}\n\n")
with open('chapters.txt', 'w', encoding='utf8') as f:
    for c in chapters: f.write(f"{int(c['t'] // 60)}:{int(c['t'] % 60):02} {c['title']}\n")
print('END', END, 'scenes', len(scenes), 'ide ops', len(ide), 'sfx', len(sfx))
print(open('chapters.txt').read())
