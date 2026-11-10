# Собирает video.html (IDE + слайды + таймлайн), sfx.json, .srt (для YouTube; в видео субтитров НЕТ) и главы для YouTube-урока 10 «Лоиҳаи хурд, қисми 2: функсияҳо».
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
S1_END = T('Ёдатон ҳаст рецепт')
S_IDE = T('Ба ай-ди-и')
S_F2 = T('Функсияи дуюм')
S_F3 = T('Функсияи сеюм')
S_F4 = T('Ва функсияи чорум')
S_TASK = T('Ва акнун вазифа барои')
S_SUM = T('Хулоса мекунем.')
X_NEXT = T('Дарси оянда')

# --- 0. Хук ---
h_hi = T('Салом, дӯстон!'); h_nb = T('дафтарчаи вазифаҳоро'); h_add = T('илова кардан'); h_done = T('иҷро кардан'); h_again = T('аз нав'); h_btn = T('«тугма»'); h_fn = T('се функсия'); h_a = T('илова кардан,', h_fn); h_b = T('иҷро кардан', h_a); h_c = T('нишон додан', h_b); h_one = T('як сатр'); h_quiz = T('Дар охир санҷиши')
slides.append(f'''<section class="scene" id="s-hook">
<div class="kicker" {A('down', .2)}><b>ДАРСИ 10</b>БАРНОМАСОЗӢ АЗ СИФР · JAVASCRIPT</div>
<div class="h1" style="left:60px;top:100px;font-size:104px;line-height:1.05" {A('stamp', .6)}>ЛОИҲА<br>ҚИСМИ 2</div>
<div style="left:68px;top:370px" {A('bob', h_hi, h_nb, 'shrink')}><span class="pill accent" style="font-size:30px;padding:16px 30px">👋 Салом, дӯстон!</span></div>
<div style="left:68px;top:370px" {A('left', h_nb)}><span class="pill">📓 дафтарчаи вазифаҳо</span></div>
<div style="left:68px;top:440px" {A('left', h_add)}><span class="pill err">🔁 <span class="mono">push(…)</span> — ҳар дафъа аз нав</span></div>
<div style="left:68px;top:502px" {A('left', h_done)}><span class="pill err">🔁 <span class="mono">done = true</span> — аз нав</span></div>
<div style="left:68px;top:564px" {A('left', h_again)}><span class="pill err">🔁 <span class="mono">for (…)</span> — аз нав 😮‍💨</span></div>

<div style="left:830px;top:150px" {A('pop', h_btn)}><span class="pill accent" style="font-size:28px;padding:14px 28px">🔘 се «тугма» — се функсия</span></div>
<div class="codechip" style="left:830px;top:240px;font-size:26px" {A('pop', h_a)} data-tw="{h_a};1.4" data-text='addTask("занг задан");'></div>
<div class="codechip" style="left:830px;top:316px;font-size:26px" {A('pop', h_b)} data-tw="{h_b};1.2" data-text='completeTask(0);'></div>
<div class="codechip" style="left:830px;top:392px;font-size:26px" {A('pop', h_c)} data-tw="{h_c};1.0" data-text='showTasks();'></div>
<div style="left:830px;top:490px" {A('pop', h_one)}><span class="pill ok" style="font-size:28px;padding:14px 28px">⚡ ҳар амал — як сатр</span></div>
<div style="left:850px;top:650px" {A('pop', h_quiz)}><span class="pill accent">🎯 Дар охир: санҷиши нав</span></div>
</section>''')
S('s-hook', 0, S1_END)

# --- 1. Чаро функсия? ---
w_rec = T('рецепт аз'); w_once = T('Як маротиба менависем'); w_many = T('бисёр бор'); w_nb = T('Дафтарчаи мо ҳам'); w_push = T('Илова кардан ҳар'); w_for = T('Нишон додан ҳар'); w_tired = T('Агар ин кодро'); w_better = T('Беҳтар аст'); w_write = T('як маротиба дар функсия'); w_call = T('бо ном даъват')
PA = w_nb - .25; PB = w_better - .25
slides.append(f'''<section class="scene" id="s-why">
<div class="kicker" {A('down', S1_END + .1)}><b>01</b>ЧАРО ФУНКСИЯ?</div>
<div class="node yes" style="left:60px;top:150px;width:320px" {A('pop', w_rec, PA)}><span class="big">📖</span>рецепт<small>дарси 5</small></div>
<div style="left:60px;top:430px" {A('left', w_once, PA)}><span class="pill ok">✍️ як маротиба менависем</span></div>
<div style="left:60px;top:498px" {A('left', w_many, PA)}><span class="pill accent">🔁 бисёр бор истифода мебарем</span></div>

<div class="h2" style="left:60px;top:90px;font-size:46px" {A('up', w_nb, PB)}>📓 Дафтарчаи мо ҳам</div>
<div style="left:60px;top:200px" {A('left', w_push, PB)}><span class="pill" style="font-size:28px;padding:14px 26px">➕ илова кардан = <span class="mono" style="color:var(--teal)">push</span></span></div>
<div style="left:60px;top:276px" {A('left', w_for, PB)}><span class="pill" style="font-size:28px;padding:14px 26px">👀 нишон додан = <span class="mono" style="color:var(--teal)">for</span></span></div>
<div style="left:60px;top:380px" {A('left', w_tired, PB)}><span class="pill err" style="font-size:28px;padding:14px 26px">😮‍💨 3 бор нависем → хаста + хато</span></div>

<div class="h2" style="left:60px;top:90px;font-size:46px" {A('up', w_better)}>Беҳтар: функсия</div>
<div class="node yes" style="left:60px;top:200px;width:360px" {A('pop', w_write)}><span class="big">📦</span><span class="mono">function</span><small>як маротиба менависем</small></div>
<div class="h2" style="left:450px;top:260px;font-size:48px" {A('fade', w_call)}>→</div>
<div class="node" style="left:530px;top:200px;width:360px" {A('pop', w_call)}><span class="big">📞</span><span class="mono">showTasks()</span><small>бо ном даъват мекунем</small></div>
</section>''')
S('s-why', S1_END, S_IDE)

# --- 2. IDE ---
S('ide', S_IDE, S_SUM)
setc(S_IDE, ''); clear(S_IDE)
t_link = T('Пайванд дар тавсиф')
chip(t_link, t_link + 3.4, '🔗 yunusovshahriyor.github.io/yunusov.tj/ide', 'side yel', 'top:90px')
chip(S_IDE + .1, S_IDE + 2.0, '<span>👀</span><div>Функсияи 1: showTasks<small>02 · ҳамроҳи ман нависед</small></div>', 'card')
LIST = 'let tasks = [{ text: "нон харидан", done: false }, { text: "дарс хондан", done: false }];'
LIST3 = 'let tasks = [\n  { text: "нон харидан", done: false },\n  { text: "дарс хондан", done: false },\n  { text: "занг задан", done: false }\n];'
SH_HEAD = 'function showTasks() {\n'
SH_FOR = '  for (let i = 0; i < tasks.length; i++) {\n'
SH_IF = '    if (tasks[i].done) { console.log("☑ " + tasks[i].text); }\n'
SH_ELSE = '    else { console.log("☐ " + tasks[i].text); }\n'
SH_END = '  }\n}'
SHOW = SH_HEAD + SH_FOR + SH_IF + SH_ELSE + SH_END
M0 = LIST
SA = M0 + '\nfunction showTasks() {\n}'
SB = M0 + '\n' + SH_HEAD + SH_FOR + '  }\n}'
SC = M0 + '\n' + SH_HEAD + SH_FOR + SH_IF + '  }\n}'
SD = M0 + '\n' + SHOW
SE = SD + '\nshowTasks();'
a_list = T('Лет таскс'); a_fn = T('Фанкшн шоу'); a_for = T('фор, ай'); a_if = T('Иф таскс'); a_else = T('Вагарна'); a_wrote = T('Навиштем'); a_nothing = T('ҳеҷ чиз нашуд'); a_mem = T('Ёдатон ҳаст аз дарси панҷум?', a_nothing); a_wr = T('Навиштан як чиз'); a_call = T('Шоу таскс бо қавс'); a_run = T('Иҷро —'); a_two = T('ду вазифа')
zoom(a_list - .3, S_F2 - .3, 330, 230, 1.35)
typ(a_list, M0, 5.4)
typ(a_fn, SA, 2.2)
mark(a_fn + 1.2, a_for - .1, 1, 9, 18, '📦 функсия', 'c')
typ(a_for, SB, 3.0)
mark(a_for + .6, a_if - .1, 2, 2, 5, '🔁 давр (дарси 9)', 'g')
typ(a_if, SC, 4.2)
typ(a_else, SD, 2.4)
mark(a_if + 1.2, a_else - .1, 3, 4, 6, 'шарт (дарси 9)', 'y')
run(a_wrote + .8)
ring(a_nothing, a_mem - .1, '#out', '⚠️ ҳеҷ чиз!', 'r', 2)
chip(a_wr, a_call - .1, '<span class="big">✍️ ≠ 📞</span><div>навиштан ≠ даъват<small>навиштем — ҳоло даъват кунем</small></div>', 'card')
typ(a_call, SE, 1.2)
run(a_run + .25)
ring(a_two, S_F2 - .1, '#out', '✅ ду вазифа ☐ ☐', 'g', 2)

# --- функсияи 2: addTask ---
setc(S_F2, M0 + '\n' + SHOW); clear(S_F2)
chip(S_F2 + .1, S_F2 + 2.0, '<span>➕</span><div>Функсияи 2: addTask<small>03 · параметр text</small></div>', 'card')
AD0 = M0 + '\n' + SHOW + '\nfunction addTask(text) {\n}'
AD1 = M0 + '\n' + SHOW + '\nfunction addTask(text) {\n  tasks.push({ text: text, done: false });\n}'
AC1 = AD1 + '\naddTask("занг задан");\nshowTasks();'
AC2 = AD1 + '\naddTask("занг задан");\naddTask("хондани китоб");\nshowTasks();'
b_fn = T('Фанкшн эд'); b_par = T('параметр текст'); b_mem = T('Ёдатон ҳаст параметр'); b_in = T('таскс нуқта пуш'); b_same = T('текст — ҳамон'); b_now = T('Ҳоло эд таск'); b_run = T('Иҷро.', b_now); b_three = T('Се вазифа!'); b_one = T('Як сатр'); b_more = T('Ва ҳар қадар'); b_book = T('«хондани китоб»'); b_code = T('Код як')
zoom(b_fn - .3, S_F3 - .3, 330, 230, 1.35)
typ(b_fn, AD0, 2.3)
mark(b_par, b_in - .1, 7, 17, 21, '📦 параметр (дарси 5)', 'c')
typ(b_in, AD1, 5.5)
mark(b_same, b_now - .1, 8, 21, 25, 'text — параметр', 'g')
typ(b_now, AC1, 3.4)
run(b_run + .2)
ring(b_three, b_more, '#out', '✅ 3 вазифа', 'g', 2)
typ(b_more + 1.0, AC2, 1.6)
run(b_book + 1.8)
ring(b_book + 2.2, S_F3 - .1, '#out', '✅ 4 вазифа', 'g', 2)

# --- функсияи 3: completeTask ---
setc(S_F3, M0 + '\n' + SHOW); clear(S_F3)
chip(S_F3 + .1, S_F3 + 2.0, '<span>☑</span><div>Функсияи 3: completeTask<small>04 · индекс, шарт ва return</small></div>', 'card')
CT0 = M0 + '\n' + SHOW + '\nfunction completeTask(index) {\n}'
CT1 = M0 + '\n' + SHOW + '\nfunction completeTask(index) {\n  tasks[index].done = true;\n}'
CC1 = CT1 + '\ncompleteTask(0);\nshowTasks();'
CE = CT1 + '\ncompleteTask(5);'
IFLINE = '  if (index >= tasks.length) { console.log("Чунин вазифа нест"); return; }'
CT2 = M0 + '\n' + SHOW + '\nfunction completeTask(index) {\n' + IFLINE + '\n  tasks[index].done = true;\n}'
CE2 = CT2 + '\ncompleteTask(5);'
c_fn = T('Фанкшн комплит'); c_in = T('Дар дохил:', S_F3); c_call = T('Комплит таск, сифр'); c_run = T('Иҷро —', c_call); c_ate = T('нон харида шуд'); c_err = T('Комплит таск, панҷ'); c_no = T('вазифаи панҷум'); c_run2 = T('Иҷро.', c_err); c_bad = T('Хато:', c_run2); c_mem = T('Ёдатон ҳаст аз дарси нӯҳум')
c_fix = T('Пеш аз ҳама санҷем'); c_big = T('индекс калон'); c_ret = T('ва риторн'); c_stop = T('Риторн функсияро'); c_run3 = T('Иҷро.', c_stop); c_msg = T('«Чунин вазифа нест».', c_run3); c_ok = T('Барнома хато накард')
zoom(c_fn - .3, S_F4 - .3, 330, 230, 1.35)
typ(c_fn, CT0, 2.0)
typ(c_in, CT1, 3.6)
typ(c_call, CC1, 2.4)
run(c_run + .2)
ring(c_ate, c_err - .1, '#out', '✅ нон харида шуд ☑', 'g', 2)
typ(c_err, CE, 2.2)
mark(c_no, c_run2 - .1, 10, 13, 14, '⚠️ вазифаи 5 нест', 'r')
run(c_run2 + .3, 'bad')
ring(c_bad, c_mem - .1, '#out', '⚠️ TypeError', 'r', 2)
typ(c_fix + .5, CE2, 8.0)
mark(c_big, c_big + 3.6, 8, 6, 27, '❓ шарт (дарси 2)', 'y')
mark(c_ret, c_stop - .1, 8, IFLINE.index('return'), IFLINE.index('return') + 6, 'return — қатъ', 'g', 'below')
chip(c_stop, c_stop + 4.2, '<span class="big">↩️</span><div>return — функсияро фавран қатъ мекунад<small>(дарси 5)</small></div>', 'card')
run(c_run3 + .2)
ring(c_msg, c_ok + 2.6, '#out', '✅ «Чунин вазифа нест» — паём!', 'g', 2)

# --- функсияи 4: countDone ---
setc(S_F4, LIST3 + '\ntasks[0].done = true;'); clear(S_F4)
chip(S_F4 + .1, S_F4 + 2.0, '<span>🔢</span><div>Функсияи 4: countDone<small>05 · return — ҷавоб</small></div>', 'card')
BASE4 = LIST3 + '\ntasks[0].done = true;'
D0 = BASE4 + '\nfunction countDone() {\n}'
D1 = BASE4 + '\nfunction countDone() {\n  let count = 0;\n}'
D2 = BASE4 + '\nfunction countDone() {\n  let count = 0;\n  for (let i = 0; i < tasks.length; i++) {\n  }\n}'
D3 = BASE4 + '\nfunction countDone() {\n  let count = 0;\n  for (let i = 0; i < tasks.length; i++) {\n    if (tasks[i].done) { count = count + 1; }\n  }\n}'
D4 = BASE4 + '\nfunction countDone() {\n  let count = 0;\n  for (let i = 0; i < tasks.length; i++) {\n    if (tasks[i].done) { count = count + 1; }\n  }\n  return count;\n}'
D5 = D4 + '\nconsole.log(countDone());'
d_fn = T('Фанкшн каунт'); d_let = T('лет каунт баробари'); d_loop = T('Давр —'); d_if = T('ва агар вазифа'); d_ret = T('Дар охир риторн'); d_log = T('консол лог нишон медиҳад'); d_retw = T('риторн ҷавоб'); d_need = T('Ин ҷо ҷавоб'); d_call = T('Консол лог, каунт дан'); d_run = T('Иҷро —', d_call); d_one = T('як.', d_run); d_all = T('Ҳамаи вазифаҳо');
zoom(d_fn - .3, S_TASK - .3, 330, 230, 1.35)
typ(d_fn, D0, 1.4)
typ(d_let, D1, 2.0)
typ(d_loop, D2, 2.0)
typ(d_if, D3, 3.8)
typ(d_ret, D4, 2.2)
mark(d_ret + 1.4, d_log - .1, 11, 2, 8, 'return', 'g')
chip(d_log, d_need - .1, '<span class="big">📣</span><div>console.log — нишон медиҳад<small>return — ҷавоб бармегардонад</small></div>', 'card')
typ(d_call, D5, 2.2)
run(d_run + .2)
ring(d_one, S_TASK - .2, '#out', '✅ 1 (аз 3)', 'g', 2)

# --- 3. Вазифаҳо ---
t_tab = T('ҷадвали «Озод»-ро'); t_t1 = T('Якум: ба рӯйхат'); t_t1w = T('эд таск илова'); t_t2 = T('Дуюм: функсияи'); t_t2w = T('анкомплит таск нависед'); t_t3 = T('Саввум: функсияи'); t_t3w = T('каунт лефт нависед')
t_q = T('Ва санҷиши нав'); t_cc = T('Комплит таск, сифр', t_q); t_what = T('Чӣ чоп мешавад'); t_pz = T('Видеоро пауза'); t_ans = T('Ҷавоб:', t_pz); t_one = T('як.', t_ans); t_zero = T('Вазифаи сифр'); t_true = T('дан аз тру')
TBASE = LIST + '\nfunction addTask(text) {\n  tasks.push({ text: text, done: false });\n}\nfunction completeTask(index) { tasks[index].done = true; }'
setc(S_TASK, TBASE); clear(S_TASK)
chip(S_TASK + .1, S_TASK + 2.0, '<span>🎯</span><div>Вазифаҳо барои шумо<small>06 · ҷадвали «Озод», кодҳо — худатон</small></div>', 'card')
chip(t_t1, t_t2 - .1, 'Вазифаи 1 / 3', 'side yel', 'top:70px;left:1050px')
zoom(t_t1w - .3, t_q - .4, 330, 230, 1.35)
V1 = TBASE + '\naddTask("хондани китоб");\ncompleteTask(1);'
typ(t_t1w, V1, 4.2)
chip(t_t2, t_t3 - .1, 'Вазифаи 2 / 3', 'side yel', 'top:70px;left:1050px')
V2 = V1 + '\nfunction uncompleteTask(index) {\n  tasks[index].done = false;\n}'
typ(t_t2w, V2, 3.6)
chip(t_t3, t_q - .1, 'Вазифаи 3 / 3', 'side yel', 'top:70px;left:1050px')
V3 = V2 + '\nfunction countLeft() {\n  let left = 0;\n  for (let i = 0; i < tasks.length; i++) {\n    if (tasks[i].done === false) { left = left + 1; }\n  }\n  return left;\n}'
typ(t_t3w, V3, 5.0)
QB = LIST3 + '\nfunction completeTask(index) { tasks[index].done = true; }\nfunction countDone() {\n  let count = 0;\n  for (let i = 0; i < tasks.length; i++) {\n    if (tasks[i].done) { count = count + 1; }\n  }\n  return count;\n}'
setc(t_q + .12, QB); clear(t_q + .12)
Q1 = QB + '\ncompleteTask(0);\ncompleteTask(0);\nconsole.log(countDone());'
zoom(t_cc - .3, t_what - .2, 330, 230, 1.35)
typ(t_cc, Q1, 6.2)
mark(t_what, t_pz - .3, 15, 0, 25, '❓ чӣ чоп мешавад?', 'y')
g0 = V(GAP_Q) - PAUSE
chip(t_pz, g0 - .3, '<span class="big">❓</span><div>completeTask(0) ×2 — countDone()?<small>видеоро пауза кунед ✍️</small></div>', 'card')
for k in range(5):
    chip(g0 + k + .02, g0 + k + .62, f'<span class="big">{5 - k}</span><div>completeTask(0) ×2 — countDone()?<small>фикр кунед · баъд ҷавобро мебинем ✅</small></div>', 'card')
    sfx.append(dict(name='tick', t=g0 + k, gain=.8))
run(t_ans + .3)
ring(t_one, S_SUM - .3, '#out', '✅ 1', 'g', 2)
mark(t_zero, t_true - .1, 13, 0, 15, 'сифр — бори 1', 'c')
mark(t_zero + 1.0, t_true - .1, 14, 0, 15, 'сифр — бори 2', 'c', 'below')
mark(t_true, S_SUM - .3, 5, QB.split('\n')[5].index('true'), QB.split('\n')[5].index('true') + 4, 'true → true: як вазифа', 'y')

# --- 4. Хулоса ---
x_a = T('нишон додан,', S_SUM); x_b = T('илова кардан,', x_a); x_c = T('иҷро кардан', x_b); x_d = T('ҳисоб кардан'); x_p = T('Параметр —'); x_r = T('риторн —', x_p); x_s = T('шарт ҳифз'); x_pdf = T('Шпаргалкаи бепул')
slides.append(f'''<section class="scene" id="s-sum">
<div class="kicker" {A('down', S_SUM + .2)}><b>07</b>ХУЛОСА</div>
<div class="h2" style="left:60px;top:90px;font-size:50px" {A('up', S_SUM + .6)}>4 функсия = <span class="acc">4 «тугма»</span></div>
<div class="card3" style="left:60px;top:220px;width:280px;height:250px" {A('up', x_a)}><div class="emo">👀</div><div class="t">нишон додан</div><div class="codechip" style="font-size:20px">showTasks()</div></div>
<div class="card3" style="left:370px;top:220px;width:280px;height:250px" {A('up', x_b)}><div class="emo">➕</div><div class="t">илова кардан</div><div class="codechip" style="font-size:20px">addTask(text)</div></div>
<div class="card3" style="left:680px;top:220px;width:280px;height:250px" {A('up', x_c)}><div class="emo">☑</div><div class="t">иҷро кардан</div><div class="codechip" style="font-size:20px">completeTask(i)</div></div>
<div class="card3" style="left:990px;top:220px;width:230px;height:250px" {A('up', x_d)}><div class="emo">🔢</div><div class="t">ҳисоб</div><div class="codechip" style="font-size:20px">countDone()</div></div>
<div style="left:60px;top:500px" {A('left', x_p)}><span class="pill">📦 параметр — қимат мегирад</span></div>
<div style="left:60px;top:560px" {A('left', x_r)}><span class="pill">↩️ return — ҷавоб бармегардонад</span></div>
<div style="left:60px;top:620px" {A('left', x_s)}><span class="pill ok">🛡️ шарт — аз шумораи нодуруст ҳифз мекунад</span></div>
<div style="left:700px;top:560px" {A('up', x_pdf)}><span class="pill accent">📘 Шпаргалка — дар тавсиф</span></div>
</section>''')
S('s-sum', S_SUM, X_NEXT)

x_html = T('ейч-ти-эм-эл,'); x_css = T('си-эс-эс'); x_js = T('ҷаваскрипт'); x_sub = T('Обуна шавед')
slides.append(f'''<section class="scene" id="s-next">
<div class="kicker" {A('down', X_NEXT + .1)}><b>ДАРСИ 11</b>НАВБАТӢ</div>
<div class="h1" style="left:60px;top:110px;font-size:92px;line-height:1.05" {A('stamp', X_NEXT + .3)}>САЙТ ЧӢ ТАВР<br>КОР МЕКУНАД?</div>
<div style="left:68px;top:380px" {A('left', x_html)}><span class="pill" style="font-size:28px;padding:14px 28px">🧱 HTML</span></div>
<div style="left:68px;top:456px" {A('left', x_css)}><span class="pill" style="font-size:28px;padding:14px 28px">🎨 CSS</span></div>
<div style="left:68px;top:532px" {A('left', x_js)}><span class="pill ok" style="font-size:28px;padding:14px 28px">⚙️ JavaScript</span></div>
<div style="left:820px;top:170px" {A('pop', x_sub)}><span class="pill accent" style="font-size:34px;padding:20px 40px">🔔 Обуна шавед</span></div>
<div style="left:820px;top:270px" {A('pop', x_sub + .5)}><span class="pill" style="font-size:26px;padding:16px 30px">@shahriyor_yunusov</span></div>
</section>''')
S('s-next', X_NEXT, END + 1)

chapters = [dict(t=0, title='Хук'), dict(t=S1_END, title='Чаро функсия?'), dict(t=S_IDE, title='Функсияи 1: showTasks'), dict(t=S_F2, title='Функсияи 2: addTask'),
            dict(t=S_F3, title='Функсияи 3: completeTask'), dict(t=S_F4, title='Функсияи 4: countDone, return'), dict(t=S_TASK, title='Вазифаҳо ва санҷиш'), dict(t=S_SUM, title='Хулоса')]
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
MAP = [(r'ай-ди-и', 'IDE'), (r'консол лог', 'console.log'), (r'тайп эрор', 'TypeError'), (r'шоу таскс', 'showTasks'), (r'эд таскро', 'addTask-ро'), (r'эд таск', 'addTask'), (r'комплит таскро', 'completeTask-ро'), (r'комплит таск', 'completeTask'), (r'анкомплит таск', 'uncompleteTask'),
       (r'каунт дан', 'countDone'), (r'каунт лефт', 'countLeft'), (r'таскс', 'tasks'), (r'текст', 'text'), (r'индекс', 'index'), (r'каунт', 'count'), (r'ленгс', 'length'), (r'пуш', 'push'), (r'лет', 'let'), (r'фор', 'for'), (r'иф', 'if'), (r'дан', 'done'), (r'тру', 'true'), (r'фолс', 'false'), (r'фанкшн', 'function'), (r'риторн', 'return'), (r'ай', 'i'), (r'ейч-ти-эм-эл', 'HTML'), (r'си-эс-эс', 'CSS'), (r'ҷаваскрипт', 'JavaScript')]
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
with open('../youtube-lesson-10.srt', 'w', encoding='utf8') as f:
    for k, c in enumerate(caps, 1): f.write(f"{k}\n{ts(c['t0'])} --> {ts(c['t1'])}\n{c['text']}\n\n")
with open('chapters.txt', 'w', encoding='utf8') as f:
    for c in chapters: f.write(f"{int(c['t'] // 60)}:{int(c['t'] % 60):02} {c['title']}\n")
print('END', END, 'scenes', len(scenes), 'ide ops', len(ide), 'sfx', len(sfx))
print(open('chapters.txt').read())
