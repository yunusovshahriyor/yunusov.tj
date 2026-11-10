# Собирает video.html (IDE + слайды + таймлайн), sfx.json, .srt (для YouTube; в видео субтитров НЕТ) и главы для YouTube-урока 9 «Лоиҳаи хурд: рӯйхати вазифаҳо».
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
S1_END = T('Тасаввур кунед, ки дафтарча')
S_IDE = T('Ба ай-ди-и')
S_PUSH = T('Вазифаи нав илова')
S_LOOP = T('Ҳоло ҳамаро чоп')
S_DONE = T('Ва акнун вазифаи аввалро')
S_DBG = T('Ва як хатои маъмул')
S_TASK = T('Ва акнун вазифа барои')
S_SUM = T('Хулоса мекунем.')
X_NEXT = T('Дарси оянда')

# --- 0. Хук ---
h_hi = T('Салом, дӯстон!'); h_a = T('Дафтари вазифаҳоро'); h_b = T('дар код'); h_c = T('нигоҳ доштан'); h_list = T('як рӯйхат'); h_loop = T('як давр'); h_first = T('Ин аввалин'); h_today = T('Имрӯз онро'); h_add = T('илова кардан,'); h_show = T('нишон додан'); h_done = T('иҷро шуд гуфтан'); h_quiz = T('Дар охир санҷиши')
slides.append(f'''<section class="scene" id="s-hook">
<div class="kicker" {A('down', .2)}><b>ДАРСИ 9</b>БАРНОМАСОЗӢ АЗ СИФР · JAVASCRIPT</div>
<div class="h1" style="left:60px;top:100px;font-size:104px;line-height:1.05" {A('stamp', .6)}>ЛОИҲАИ<br>ХУРД</div>
<div style="left:68px;top:350px" {A('bob', h_hi, h_list - .1, 'shrink')}><span class="pill accent" style="font-size:30px;padding:16px 30px">👋 Салом, дӯстон!</span></div>
<div class="codechip" style="left:68px;top:350px;font-size:26px" {A('pop', h_list)} data-tw="{h_list};2.2" data-text='let tasks = [ … ];'></div>
<div style="left:68px;top:440px" {A('left', h_list + .6)}><span class="pill">📋 рӯйхат</span></div>
<div style="left:68px;top:502px" {A('left', h_loop)}><span class="pill">🔁 давр</span></div>
<div style="left:68px;top:564px" {A('left', h_first)}><span class="pill accent">🎯 аввалин лоиҳа</span></div>

<div style="left:830px;top:150px" {A('drop', h_a)}><span class="pill ok" style="font-size:28px;padding:14px 28px">☑ нон харидан</span></div>
<div style="left:830px;top:220px" {A('drop', h_b)}><span class="pill" style="font-size:28px;padding:14px 28px">☐ дарс хондан</span></div>
<div style="left:830px;top:290px" {A('drop', h_c)}><span class="pill" style="font-size:28px;padding:14px 28px">☐ занг задан</span></div>
<div class="sub" style="left:830px;top:370px;font-size:24px" {A('up', h_today)}>аз сифр месозем:</div>
<div style="left:830px;top:420px" {A('left', h_today + 2.2)}><span class="pill">📋 рӯйхати вазифаҳо</span></div>
<div style="left:830px;top:484px" {A('left', h_add)}><span class="pill ok">➕ илова кардан</span></div>
<div style="left:830px;top:548px" {A('left', h_show)}><span class="pill">👀 нишон додан</span></div>
<div style="left:830px;top:612px" {A('left', h_done)}><span class="pill ok">☑ иҷро шуд</span></div>
<div style="left:68px;top:650px" {A('pop', h_quiz)}><span class="pill accent">🎯 Дар охир: санҷиши нав</span></div>
</section>''')
S('s-hook', 0, S1_END)

# --- 1. Образи дафтарча ва объект ---
n_a = T('нон харидан,'); n_b = T('дарс хондан.'); n_c = T('иҷро шуд ё не'); n_code = T('Дар барномасозӣ ҳам'); n_id = T('корти шиноснома'); n_text = T('Текст —'); n_dan = T('Дан —'); n_tf = T('тру ё фолс'); n_list = T('Ва объектҳо дар'); n_card = T('Рӯйхат —', n_list); n_row = T('объект — як сатри')
PA = n_code - .25; PB = n_list - .25
slides.append(f'''<section class="scene" id="s-note">
<div class="kicker" {A('down', S1_END + .1)}><b>01</b>ДАФТАРЧА ВА ОБЪЕКТ</div>
<div class="h2" style="left:60px;top:90px;font-size:48px" {A('up', S1_END + .3, PA)}>📓 Дафтарча</div>
<div class="row" style="left:60px;top:190px;width:560px" {A('left', n_a, PA)}><span class="op">☐</span><span class="mean">нон харидан</span></div>
<div class="row" style="left:60px;top:274px;width:560px" {A('left', n_b, PA)}><span class="op">☐</span><span class="mean">дарс хондан</span></div>
<div style="left:680px;top:200px" {A('pop', n_c, PA)}><span class="pill ok">☑ иҷро шуд</span></div>
<div style="left:680px;top:268px" {A('pop', n_c + .5, PA)}><span class="pill">☐ ё не</span></div>

<div class="h2" style="left:60px;top:90px;font-size:46px" {A('up', n_code, PB)}>Ҳар вазифа — объект</div>
<div class="node yes" style="left:60px;top:190px;width:300px" {A('pop', n_id, PB)}><span class="big">🪪</span>корти шиноснома<small>дарси 6</small></div>
<div class="codechip" style="left:420px;top:210px;font-size:30px" {A('up', n_id + .6, PB)}>{{ <span class="t">text</span>: <span class="s">"нон харидан"</span>, <span class="t">done</span>: <span class="k">false</span> }}</div>
<div style="left:420px;top:300px" {A('left', n_text, PB)}><span class="pill"><span class="mono" style="color:var(--teal)">text</span> — вазифа чист</span></div>
<div style="left:420px;top:368px" {A('left', n_dan, PB)}><span class="pill"><span class="mono" style="color:var(--teal)">done</span> — иҷро шуд ё не</span></div>
<div style="left:420px;top:436px" {A('left', n_tf, PB)}><span class="pill ok"><span class="mono">true</span> ё <span class="mono">false</span></span></div>

<div class="h2" style="left:60px;top:90px;font-size:46px" {A('up', n_list)}>Объектҳо дар рӯйхат 📋</div>
<div class="node" style="left:60px;top:200px;width:300px" {A('pop', n_list + .5)}><span class="mono acc" style="font-size:56px">0</span>нон харидан<small>объект</small></div>
<div class="node" style="left:400px;top:200px;width:300px" {A('pop', n_list + 1.1)}><span class="mono acc" style="font-size:56px">1</span>дарс хондан<small>объект</small></div>
<div style="left:60px;top:450px" {A('left', n_card)}><span class="pill accent">📓 рӯйхат = дафтарча</span></div>
<div style="left:60px;top:520px" {A('left', n_row)}><span class="pill">🧾 объект = як сатри он</span></div>
</section>''')
S('s-note', S1_END, S_IDE)

# --- 2. IDE ---
S('ide', S_IDE, S_SUM)
setc(S_IDE, ''); clear(S_IDE)
t_link = T('Пайванд дар тавсиф')
chip(t_link, t_link + 3.4, '🔗 yunusovshahriyor.github.io/yunusov.tj/ide', 'side yel', 'top:90px')
chip(S_IDE + .1, S_IDE + 2.0, '<span>📋</span><div>Аввалин рӯйхат дар IDE<small>02 · ҳамроҳи ман нависед</small></div>', 'card')
O1 = '  { text: "нон харидан", done: false },'
O2 = '  { text: "дарс хондан", done: false }'
O2c = '  { text: "дарс хондан", done: false },'
O3 = '  { text: "занг задан", done: false }'
K0 = 'let tasks = [\n];'
K1 = 'let tasks = [\n' + O1 + '\n];'
K2 = 'let tasks = [\n' + O1 + '\n' + O2 + '\n];'
K3 = K2 + '\nconsole.log(tasks[0].text);'
K4 = K3 + '\nconsole.log(tasks.length);'
a_let = T('лет таскс баробари'); a_in = T('Дар дохил —'); a_o1 = T('Якум: текст'); a_o2 = T('Дуюм: текст'); a_mine = T('Ин дафтарчаи мо'); a_first = T('Номи вазифаи аввал'); a_run = T('Иҷро.', a_first); a_nan = T('«Нон харидан»!', a_run); a_zero = T('Шумора аз сифр', a_nan); a_len = T('Ва консол лог, таскс'); a_two = T('ду.', a_len); a_two2 = T('Дар дафтарча ду')
zoom(a_let - .3, S_DBG - .3, 330, 250, 1.4)
typ(a_let, K0, 2.0)
mark(a_in, a_o1 - .1, 0, 4, 9, '📋 рӯйхат', 'c')
typ(a_o1, K1, 3.4)
typ(a_o2, K2, 3.4)
mark(a_mine, a_first - .1, 1, 2, len(O1), 'объект 1', 'y')
mark(a_mine + .6, a_first - .1, 2, 2, len(O2), 'объект 2', 'g', 'below')
typ(a_first + .8, K3, 4.4)
run(a_run + .3)
ring(a_nan, a_len - .1, '#out', '✅ нон харидан', 'g', 2)
mark(a_zero, a_len - .1, 4, 17, 20, 'аз сифр! (дарси 4)', 'c')
typ(a_len, K4, 2.4)
run(a_two + .35)
ring(a_two + .8, S_PUSH - .1, '#out', '✅ 2 вазифа', 'g', 2)

# --- илова кардан: push ---
chip(S_PUSH + .1, S_PUSH + 2.0, '<span>➕</span><div>Илова кардан: push<small>03 · tasks.push(...)</small></div>', 'card')
P1 = K4 + '\ntasks.push({ text: "занг задан", done: false });'
P2 = P1 + '\nconsole.log(tasks.length);'
b_push = T('Таскс нуқта пуш'); b_obj = T('объекти нав'); b_now = T('Ҳоло консол лог,')
b_three = T('се!'); b_grew = T('Дафтарча калон шуд')
typ(b_push, P1, 5.0)
mark(b_push + 1.2, b_obj + 1.5, 5, 0, 10, '➕ push — дарси 4', 'g')
typ(b_now, P2, 2.2)
run(b_three + .3)
ring(b_three + .8, S_LOOP - .1, '#out', '✅ 3 вазифа', 'g', 2)

# --- нишон додан: давр ---
setc(S_LOOP, ''); clear(S_LOOP)
chip(S_LOOP + .1, S_LOOP + 2.0, '<span>🔁</span><div>Нишон додан: давр<small>04 · for (дарси 3)</small></div>', 'card')
KF = 'let tasks = [\n' + O1 + '\n' + O2c + '\n' + O3 + '\n];'
setc(S_LOOP + .15, KF)
LP0 = KF + '\nfor (let i = 0; i < tasks.length; i++) {\n}'
LP1 = KF + '\nfor (let i = 0; i < tasks.length; i++) {\n  console.log(i + 1 + ". " + tasks[i].text);\n}'
l_for = T('Фор, лет ай'); l_pp = T('плюс плюс'); l_in = T('Дар дохил:', l_pp); l_why = T('Чаро ай плюс як'); l_run = T('Иҷро.', l_why); l_one = T('Як —'); l_all = T('Ҳамаи вазифаҳо як-як')
zoom(S_LOOP - .3, S_DONE - .3, 330, 250, 1.4)
typ(l_for, LP0, 5.8)
mark(l_for + .5, l_in - .1, 5, 0, 3, '🔁 давр (дарси 3)', 'g')
typ(l_in, LP1, 7.8)
mark(l_why, l_run - .1, 6, 14, 19, 'i + 1: «як, ду, се»', 'y', 'below')
run(l_run + .25)
ring(l_one, S_DONE - .2, '#out', '✅ 1 · 2 · 3', 'g', 2)

# --- иҷро шуд: done ва шарт ---
chip(S_DONE + .1, S_DONE + 2.0, '<span>☑</span><div>Иҷро шуд: done ва шарт<small>05 · tasks[0].done = true</small></div>', 'card')
LOOP_OLD = 'for (let i = 0; i < tasks.length; i++) {\n  console.log(i + 1 + ". " + tasks[i].text);\n}'
D1 = KF + '\ntasks[0].done = true;\n' + LOOP_OLD
D2a = KF + '\ntasks[0].done = true;\nfor (let i = 0; i < tasks.length; i++) {\n  if (tasks[i].done) {\n  }\n}'
D2b = KF + '\ntasks[0].done = true;\nfor (let i = 0; i < tasks.length; i++) {\n  if (tasks[i].done) {\n    console.log("☑ " + tasks[i].text);\n  }\n}'
D2c = KF + '\ntasks[0].done = true;\nfor (let i = 0; i < tasks.length; i++) {\n  if (tasks[i].done) {\n    console.log("☑ " + tasks[i].text);\n  } else {\n    console.log("☐ " + tasks[i].text);\n  }\n}'
d_do = T('иҷро мекунем:'); d_true = T('Нон харида шуд'); d_see = T('Барои дидан ҳолатро'); d_if = T('Иф,'); d_full = T('«квадрати пур»'); d_else = T('Вагарна:'); d_run = T('Иҷро.', d_else); d_f = T('Квадрати пур —'); d_alive = T('Дафтарча зинда')
zoom(S_DONE - .3, S_DBG - .3, 330, 250, 1.4)
typ(d_do, D1, 4.0)
mark(d_true, d_see - .1, 5, 16, 20, '✅ иҷро шуд', 'g')
typ(d_if, D2a, 2.8)
mark(d_if + 2.9, d_full - .1, 7, 2, 4, '❓ шарт (дарси 2)', 'y')
typ(d_full - .3, D2b, 3.0)
typ(d_else, D2c, 3.4)
run(d_run + .25)
ring(d_f, d_alive - .1, '#out', '☑ нон · ☐ дарс · ☐ занг', 'g', 2)

# --- хато ва дебаг ---
setc(S_DBG, KF); clear(S_DBG)
chip(S_DBG + .1, S_DBG + 2.0, '<span>🐞</span><div>Хато ва дебаг<small>06 · бубин · санҷ · ислоҳ</small></div>', 'card')
E1 = KF + '\nconsole.log(tasks[3].text);'
E2 = KF + '\nconsole.log(tasks.length);'
E3 = KF + '\nconsole.log(tasks[2].text);'
e_wr = T('Мо менависем:', S_DBG); e_run = T('Иҷро.', e_wr); e_err = T('Хато:'); e_back = T('Ба дарси ҳаштум'); e_see = T('Бубинед:'); e_t3 = T('таскс, се —'); e_chk = T('Санҷед:'); e_len = T('консол лог, таскс нуқта ленгс', e_chk); e_idx = T('Яъне шумораҳо'); e_fix = T('Ислоҳ:'); e_two = T('таскс, ду —', e_fix); e_run3 = T('Иҷро.', e_fix); e_zang = T('«Занг задан»!', e_run3); e_rule = T('Қоида:', e_zang)
zoom(e_wr - .3, S_TASK - .3, 330, 250, 1.4)
typ(e_wr + .1, E1, 3.6)
run(e_run + .3, 'bad')
ring(e_err, e_back - .1, '#out', '⚠️ TypeError: Cannot read properties', 'r', 2)
chip(e_see, e_chk - .1, '👀 Бубин: хато дар сатри 6', 'side yel', 'top:70px;left:1050px')
mark(e_t3, e_chk - .1, 5, 17, 20, 'tasks[3] — нест!', 'r')
chip(e_chk, e_fix - .1, '🔎 Санҷ: console.log', 'side yel', 'top:70px;left:1050px')
typ(e_len - .2, E2, 2.4)
run(e_idx - .6)
ring(e_idx - .2, e_fix - .1, '#out', '✅ 3 → индекс: 0, 1, 2', 'g', 2)
chip(e_fix, e_rule - .1, '🛠️ Ислоҳ кун', 'side yel', 'top:70px;left:1050px')
typ(e_fix + .2, E3, 2.0)
run(e_run3 + .25)
ring(e_zang, e_rule - .1, '#out', '✅ занг задан', 'g', 2)
chip(e_rule, e_rule + 4.0, '<span class="big">💡</span><div>Қоида<small>охирин шумора = length минус як</small></div>', 'card')

# --- вазифаҳо ва санҷиш ---
t_tab = T('ҷадвали «Озод»-ро'); t_t1 = T('Якум: вазифаи'); t_t1w = T('вазифаи чорумро'); t_t2 = T('Дуюм: вазифаи'); t_t2w = T('вазифаи дуюмро'); t_t3 = T('Саввум: давр'); t_t3w = T('давр нависед')
t_q = T('Ва санҷиши нав'); t_cl = T('Консол лог, таскс, як'); t_what = T('чӣ чоп мекунад'); t_rem = T('Ёдовар:'); t_pz = T('Видеоро пауза')
t_ans = T('Ҷавоб:', t_pz); t_ds = T('«дарс хондан».', t_ans); t_s0 = T('Сифр —', t_ans); t_s1 = T('як — дарс', t_s0); t_s2 = T('ду — занг', t_s1)
setc(S_TASK, KF); clear(S_TASK)
chip(S_TASK + .1, S_TASK + 2.0, '<span>🎯</span><div>Вазифаҳо барои шумо<small>07 · ҷадвали «Озод», кодҳо — худатон</small></div>', 'card')
chip(t_t1, t_t2 - .1, 'Вазифаи 1 / 3', 'side yel', 'top:70px;left:1050px')
zoom(t_t1w - .3, t_q - .4, 330, 250, 1.4)
V1 = KF + '\ntasks.push({ text: "хондани китоб", done: false });'
typ(t_t1w, V1, 2.6)
chip(t_t2, t_t3 - .1, 'Вазифаи 2 / 3', 'side yel', 'top:70px;left:1050px')
V2 = V1 + '\ntasks[1].done = true;'
typ(t_t2w, V2, 1.6)
chip(t_t3, t_q - .1, 'Вазифаи 3 / 3', 'side yel', 'top:70px;left:1050px')
V3 = V2 + '\nfor (let i = 0; i < tasks.length; i++) {\n  if (tasks[i].done) {\n    console.log("☑ " + tasks[i].text);\n  } else {\n    console.log("☐ " + tasks[i].text);\n  }\n}'
typ(t_t3w, V3, 2.5)
run(t_t3w + 2.65)
ring(t_t3w + 3.0, t_q - .1, '#out', '✅ ☐ ☑ ☐ ☐', 'g', 2)
setc(t_q + .12, KF); clear(t_q + .12)
Q1 = KF + '\nconsole.log(tasks[1].text);'
zoom(t_cl - .3, t_what - .2, 330, 250, 1.4)
typ(t_cl, Q1, 3.2)
mark(t_what, t_rem - .1, 5, 17, 20, '❓ чӣ чоп мекунад?', 'y')
mark(t_rem, t_pz - .2, 5, 17, 20, 'аз сифр: 0, 1, 2', 'c')
g0 = V(GAP_Q) - PAUSE
chip(t_pz, g0 - .3, '<span class="big">❓</span><div>tasks[1].text — чӣ чоп мешавад?<small>видеоро пауза кунед ✍️</small></div>', 'card')
for k in range(5):
    chip(g0 + k + .02, g0 + k + .62, f'<span class="big">{5 - k}</span><div>tasks[1].text — чӣ чоп мешавад?<small>фикр кунед · баъд ҷавобро мебинем ✅</small></div>', 'card')
    sfx.append(dict(name='tick', t=g0 + k, gain=.8))
run(t_ans + .3)
ring(t_ds, S_SUM - .3, '#out', '✅ дарс хондан', 'g', 2)
mark(t_s0, t_s1 - .1, 1, 2, len(O1), '0 — нон харидан', 'c')
mark(t_s1, t_s2 - .1, 2, 2, len(O2c), '1 — дарс хондан', 'g', 'below')
mark(t_s2, S_SUM - .3, 3, 2, len(O3), '2 — занг задан', 'c')

# --- 3. Хулоса ---
x_a = T('Ту-ду —'); x_b = T('Рӯйхат месозем'); x_c = T('пуш илова'); x_d = T('давр нишон'); x_e = T('шарт ҳолатро'); x_pdf = T('Шпаргалкаи бепул')
slides.append(f'''<section class="scene" id="s-sum">
<div class="kicker" {A('down', S_SUM + .2)}><b>08</b>ХУЛОСА</div>
<div class="h2" style="left:60px;top:90px;font-size:50px" {A('up', x_a)}>To-do = <span class="acc">рӯйхати объектҳо</span></div>
<div class="card3" style="left:60px;top:220px;width:280px;height:250px" {A('up', x_b)}><div class="emo">📋</div><div class="t">Рӯйхат</div><div class="codechip" style="font-size:20px">tasks = [ … ]</div></div>
<div class="card3" style="left:370px;top:220px;width:280px;height:250px" {A('up', x_c)}><div class="emo">➕</div><div class="t">push</div><div class="codechip" style="font-size:20px">tasks.push(…)</div></div>
<div class="card3" style="left:680px;top:220px;width:280px;height:250px" {A('up', x_d)}><div class="emo">🔁</div><div class="t">for</div><div class="codechip" style="font-size:20px">tasks[i].text</div></div>
<div class="card3" style="left:990px;top:220px;width:230px;height:250px" {A('up', x_e)}><div class="emo">❓</div><div class="t">if</div><div class="codechip" style="font-size:20px">.done</div></div>
<div style="left:60px;top:510px" {A('up', x_a + 1.0)}><span class="pill ok">🧾 ҳар вазифа: матн + ҳолат</span></div>
<div style="left:60px;top:580px" {A('up', x_pdf)}><span class="pill accent">📘 Шпаргалкаи бепул (PDF) — дар тавсифи видео</span></div>
</section>''')
S('s-sum', S_SUM, X_NEXT)

x_fn = T('вазифаҳоро бо функсия'); x_add = T('илова ва иҷро'); x_sub = T('Обуна шавед')
slides.append(f'''<section class="scene" id="s-next">
<div class="kicker" {A('down', X_NEXT + .1)}><b>ДАРСИ 10</b>НАВБАТӢ</div>
<div class="h1" style="left:60px;top:110px;font-size:104px;line-height:1.05" {A('stamp', X_NEXT + .3)}>ЛОИҲА<br>ҚИСМИ 2</div>
<div class="sub" style="left:68px;top:360px" {A('up', X_NEXT + 1.4)}>вазифаҳоро бо функсия илова ва иҷро мекунем</div>
<div style="left:68px;top:440px" {A('left', x_fn)}><span class="pill ok">➕ <span class="mono">addTask()</span></span></div>
<div style="left:68px;top:508px" {A('left', x_add + .3)}><span class="pill ok">☑ <span class="mono">completeTask()</span></span></div>
<div style="left:820px;top:170px" {A('pop', x_sub)}><span class="pill accent" style="font-size:34px;padding:20px 40px">🔔 Обуна шавед</span></div>
<div style="left:820px;top:270px" {A('pop', x_sub + .5)}><span class="pill" style="font-size:26px;padding:16px 30px">@shahriyor_yunusov</span></div>
</section>''')
S('s-next', X_NEXT, END + 1)

chapters = [dict(t=0, title='Хук'), dict(t=S1_END, title='Образи дафтарча ва объект'), dict(t=S_IDE, title='Аввалин рӯйхат дар IDE'), dict(t=S_PUSH, title='Илова кардан: push'),
            dict(t=S_LOOP, title='Нишон додан: давр'), dict(t=S_DONE, title='Иҷро шуд: done ва шарт'), dict(t=S_DBG, title='Хато ва дебаг'), dict(t=S_TASK, title='Вазифаҳо ва санҷиш'), dict(t=S_SUM, title='Хулоса')]
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
MAP = [(r'ай-ди-и', 'IDE'), (r'консол лог', 'console.log'), (r'тайп эрор', 'TypeError'), (r'кэннот рид пропертиз оф андефайнд', 'Cannot read properties of undefined'), (r'ту-ду', 'to-do'), (r'таскс', 'tasks'), (r'текст', 'text'), (r'ленгс', 'length'),
       (r'пуш', 'push'), (r'лет', 'let'), (r'фор', 'for'), (r'иф', 'if'), (r'дан', 'done'), (r'тру', 'true'), (r'фолс', 'false'), (r'ай', 'i'), (r'Инстаграм', 'Instagram')]
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
with open('../youtube-lesson-9.srt', 'w', encoding='utf8') as f:
    for k, c in enumerate(caps, 1): f.write(f"{k}\n{ts(c['t0'])} --> {ts(c['t1'])}\n{c['text']}\n\n")
with open('chapters.txt', 'w', encoding='utf8') as f:
    for c in chapters: f.write(f"{int(c['t'] // 60)}:{int(c['t'] % 60):02} {c['title']}\n")
print('END', END, 'scenes', len(scenes), 'ide ops', len(ide), 'sfx', len(sfx))
print(open('chapters.txt').read())
