# Собирает video.html (IDE + слайды + таймлайн), sfx.json, .srt (для YouTube; в видео субтитров НЕТ) и главы для YouTube-урока 7 «3 хатои рӯзи аввал».
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
S1_END = T('Тасаввур кунед, ки бо мошин')
S_IDE = T('Ба ай-ди-и')
S_READ = T('Ва маслиҳати асосӣ')
S_TASK = T('Ва акнун вазифа')
S_SUM = T('Хулоса мекунем.')
X_NEXT = T('Дарси оянда')
S_E1 = T('Хатои якум аз дарси')

# --- 0. Хук ---
h_hi = T('Салом, дӯстон!'); h_nav = T('Ҳар навкор дар рӯзи'); h_err = T('хато мекунад'); h_norm = T('ин муқаррарӣ'); h_three = T('Аммо се хато'); h_a = T('такрор мешавад'); h_b = T('онҳоро якҷоя'); h_c = T('меёбем')
h_msg = T('паёми хаторо хонем'); h_quiz = T('Дар охир санҷиши')
slides.append(f'''<section class="scene" id="s-hook">
<div class="kicker" {A('down', .2)}><b>ДАРСИ 7</b>БАРНОМАСОЗӢ АЗ СИФР · JAVASCRIPT</div>
<div class="h1" style="left:60px;top:100px;font-size:104px;line-height:1.05" {A('stamp', .6)}>3 ХАТОИ<br>РӮЗИ АВВАЛ</div>
<div style="left:68px;top:370px" {A('bob', h_hi, h_nav - .1, 'shrink')}><span class="pill accent" style="font-size:30px;padding:16px 30px">👋 Салом, дӯстон!</span></div>
<div class="codechip" style="left:68px;top:370px;font-size:26px;color:var(--cm)" {A('pop', h_nav, h_three - .1, 'shrink')} data-tw="{h_nav + .2};2.4" data-text="// рӯзи аввал — ҳама хато мекунанд"></div>

<div class="node no" style="left:830px;top:150px;width:340px" {A('drop', h_err, h_three - .1, 'shrink')}><span class="big">⛔</span><span class="mono" style="font-size:44px;color:var(--err)">Error</span><small>хато мекунад</small></div>
<div style="left:830px;top:370px" {A('left', h_norm, h_three - .1, 'shrink')}><span class="pill ok">✅ ин муқаррарӣ аст</span></div>

<div class="node yes" style="left:830px;top:150px;width:340px" {A('pop', h_three)}><span class="big">🐞</span><span class="mono" style="font-size:56px"><span data-cnt="0;3;{h_three};1.2">0</span> хато</span><small>ҳамеша такрор мешавад</small></div>
<div style="left:68px;top:440px" {A('drop', h_a)}><span class="pill err"><span class="mono">=</span> ба ҷои <span class="mono">===</span></span></div>
<div style="left:68px;top:502px" {A('drop', h_b)}><span class="pill err"><span class="mono">City</span> ≠ <span class="mono">city</span></span></div>
<div style="left:68px;top:564px" {A('drop', h_c)}><span class="pill err"><span class="mono">console.log("Салом"</span> — қавс нест</span></div>
<div class="node" style="left:830px;top:400px;width:340px" {A('bob', h_msg)}><span class="big">📨</span>паёми хато<small>чӣ тавр хонем?</small></div>
<div style="left:850px;top:650px" {A('pop', h_quiz)}><span class="pill accent">🎯 Дар охир: санҷиши нав</span></div>
</section>''')
S('s-hook', 0, S1_END)

# --- 1. Хато — роҳнамост ---
n_car = T('бо мошин'); n_nav = T('Навигатор мегӯяд'); n_back = T('«Баргардед!».'); n_friend = T('ин ёвар'); n_pc = T('Компютер мегӯяд'); n_line = T('сатрро нишон'); n_three = T('Паёми хато се қисм'); n_type = T('навъи хато,'); n_why = T('сабаб ва'); n_row = T('рақами сатр.'); n_each = T('ҳар дафъа ин паёмро'); n_gone = T('Хатогие')
n_l2 = T('аз дарси дуюм')
PA = n_gone - .25; PB = S_E1 - .25
slides.append(f'''<section class="scene" id="s-nav">
<div class="kicker" {A('down', S1_END + .1)}><b>01</b>ХАТО — РОҲНАМОСТ</div>
<div class="node" style="left:60px;top:170px;width:300px" {A('pop', n_car, PA)}><span class="big">🚗</span>шумо<small>роҳро гум кардед</small></div>
<div class="h2" style="left:385px;top:215px;font-size:44px" {A('fade', n_nav, PA)}>→</div>
<div class="node yes" style="left:455px;top:170px;width:300px" {A('pop', n_nav, PA)}><span class="big">🧭</span>навигатор<small>роҳ нишон медиҳад</small></div>
<div style="left:60px;top:430px" {A('left', n_back, PA)}><span class="pill err" style="font-size:30px;padding:16px 28px">⛔ «Баргардед!»</span></div>
<div style="left:60px;top:520px" {A('left', n_friend, PA)}><span class="pill ok" style="font-size:28px;padding:14px 26px">🤝 душман нест — ёвар аст</span></div>

<div class="h2" style="left:60px;top:90px;font-size:46px" {A('up', n_pc, PB)}>Компютер ҳам ҳамин тавр 💬</div>
<div style="left:60px;top:190px" {A('left', n_pc + .3, PB)}><span class="pill err" style="font-size:28px;padding:14px 26px">⚠️ ин ҷо чизе нодуруст аст</span></div>
<div style="left:60px;top:268px" {A('left', n_line, PB)}><span class="pill" style="font-size:28px;padding:14px 26px">📍 ва сатрро нишон медиҳад</span></div>
<div class="h2" style="left:60px;top:380px;font-size:40px" {A('up', n_three, PB)}>Паёми хато — се қисм</div>
<div class="card3" style="left:60px;top:450px;width:360px;height:190px" {A('up', n_type, PB)}><div class="emo">🏷️</div><div class="t">1 · навъи хато</div></div>
<div class="card3" style="left:460px;top:450px;width:360px;height:190px" {A('up', n_why, PB)}><div class="emo">💬</div><div class="t">2 · сабаб</div></div>
<div class="card3" style="left:860px;top:450px;width:360px;height:190px" {A('up', n_row, PB)}><div class="emo">📍</div><div class="t">3 · рақами сатр</div></div>

<div class="h1" style="left:60px;top:120px;font-size:110px" {A('stamp', S_E1 + .2)}>ХАТОИ 1</div>
<div class="mono acc" style="left:66px;top:270px;font-size:72px;font-weight:800" {A('up', S_E1 + .7)}>= ≠ ===</div>
<div class="sub" style="left:68px;top:380px" {A('up', n_l2)}>аз дарси 2: шарт (if)</div>
<div style="left:68px;top:450px" {A('left', n_l2 + .6)}><span class="pill accent">🔎 паёми хато нест!</span></div>
</section>''')
S('s-nav', S1_END, S_IDE)

# --- 2. IDE: хатои 1, 2, 3 ---
S('ide', S_IDE, S_READ)
setc(S_IDE, ''); clear(S_IDE)
t_link = T('пайванд дар тавсиф')
chip(t_link, t_link + 3.4, '🔗 yunusovshahriyor.github.io/yunusov.tj/ide', 'side yel', 'top:90px')
chip(S_IDE + .1, S_IDE + 2.0, '<span>🐞</span><div>Хатои 1: = ба ҷои ===<small>02 · ҳамроҳи ман нависед</small></div>', 'card')
A0 = 'let age = 15;'
A1 = 'let age = 15;\nif (age = 18) {\n}'
A2 = 'let age = 15;\nif (age = 18) {\n  console.log("Калон");\n}'
A3 = 'let age = 15;\nif (age === 18) {\n  console.log("Калон");\n}'
a_let = T('лет эйдж баробари понздаҳ'); a_if = T('Иф, дар қавс'); a_in = T('Дар дохил:'); a_run = T('Иҷро.', S_IDE); a_kal = T('«Калон»!'); a_why = T('Чаро?'); a_eq = T('Як баробар қимат'); a_gave = T('Мо ба эйдж'); a_18 = T('ва ҳаждаҳ ҳамеша')
a_att = T('Диққат: паёми хато'); a_good = T('Барои муқоиса'); a_fix = T('эйдж се баробар'); a_run2 = T('Иҷро —'); a_none = T('ҳеҷ чиз'); a_rule = T('Қоида:', a_none); a_eq1 = T('як баробар —', a_rule); a_eq3 = T('се баробар —', a_eq1)
S_E2 = T('Хатои дуюм')
zoom(a_let - .3, a_rule - .3, 330, 250, 1.4)
typ(a_let, A0, 1.6)
typ(a_if, A1, 2.8)
typ(a_in, A2, 2.2)
run(a_run + .3)
ring(a_kal, a_why + .2, '#out', '⚠️ «Калон»?! (15 < 18)', 'r', 2)
mark(a_eq, a_gave - .1, 1, 8, 9, '= гузоштан, на муқоиса', 'r')
mark(a_18, a_att - .1, 1, 10, 12, 'ҳаждаҳ = «дуруст»', 'y', 'below')
chip(a_att + .1, a_att + 2.8, '⚠️ Паёми хато нест!<small>барнома оромона нодуруст кор мекунад</small>', 'card')
typ(a_fix, A3, 1.6)
mark(a_fix + 1.7, a_run2 - .1, 1, 8, 11, '=== муқоиса', 'g')
run(a_run2 + .3)
ring(a_none, a_rule - .1, '#out', '✅ ҳеҷ чиз — дуруст', 'g', 2)
chip(a_eq1, a_eq3 - .1, '<span class="big">=</span><div>гузоштан<small>қимат медиҳад</small></div>', 'card')
chip(a_eq3, S_E2 - .4, '<span class="big">===</span><div>муқоиса<small>мепурсад: баробар аст?</small></div>', 'card')

# --- хатои 2 ---
setc(S_E2, ''); clear(S_E2)
chip(S_E2 + .1, S_E2 + 2.0, '<span>🔤</span><div>Хатои 2: ҳарфи калон ва хурд<small>03 · City ≠ city</small></div>', 'card')
B1 = 'let city = "Душанбе";'
B2 = 'let city = "Душанбе";\nconsole.log(City);'
b_let = T('лет сити баробари'); b_log = T('Консол лог, сити'); b_cap = T('бо ҳарфи калон.'); b_run = T('Иҷро.', b_log); b_bad = T('Хато!', b_run); b_read = T('Паёмро мехонем'); b_ref = T('референс эрор'); b_def = T('сити из нот дефайнд'); b_l2 = T('сатри ду')
b_two = T('Барои компютер'); b_small = T('сити бо ҳарфи хурд'); b_big = T('сити бо ҳарфи калон'); b_nig = T('Ҳамон тавр'); b_cl = T('Ҳамин тавр консол'); b_cb = T('консол бо ҳарфи калон'); b_cs = T('консол бо ҳарфи хурд'); b_ok = T('кор мекунад.', b_cs); b_rule = T('Қоида:', b_ok)
chip(S_E2 + 2.4, S_E2 + 4.6, 'Хатои 2 / 3', 'side red', 'top:70px;left:1090px')
zoom(b_let - .3, b_rule - .3, 330, 250, 1.4)
typ(b_let, B1, 2.2)
typ(b_log, B2, 2.4)
mark(b_cap, b_run - .2, 1, 12, 13, 'C — калон!', 'r')
run(b_run + .3, 'bad')
ring(b_bad, b_two - .2, '#out', '⚠️ City is not defined', 'r', 2)
mark(b_def, b_l2 - .1, 1, 12, 16, '⚠️ City ≠ city', 'r')
mark(b_l2, b_l2 + 2.0, 1, 0, 18, 'сатри 2', 'y', 'below')
mark(b_small, b_big - .1, 0, 4, 8, 'city', 'c')
mark(b_big, b_nig - .1, 1, 12, 16, 'City', 'r')
chip(b_nig, b_cl - .1, '<span>👤</span><div>Нигина ≠ нигина<small>ҳарфи калон ва хурд — ду ном</small></div>', 'card')
B3 = 'Console.log("Салом");'
B4 = 'console.log("Салом");'
typ(b_cl + .3, B3, 1.4)
mark(b_cb, b_cs - .1, 0, 0, 1, 'C — хато', 'r')
typ(b_cs, B4, .8)
run(b_ok + .15)
ring(b_ok + .6, b_rule - .1, '#out', '✅ Салом', 'g', 2)

# --- хатои 3 ---
S_E3 = T('Хатои сеюм')
setc(S_E3, ''); clear(S_E3)
chip(S_E3 + .1, S_E3 + 2.0, '<span>❌</span><div>Хатои 3: қавси фаромӯшшуда<small>04 · SyntaxError</small></div>', 'card')
chip(S_E3 + 2.4, S_E3 + 4.6, 'Хатои 3 / 3', 'side red', 'top:70px;left:1090px')
C1 = 'console.log("Салом"'
C2 = 'console.log("Салом");'
c_men = T('Менависем:', S_E3); c_none = T('қавси пӯшанда нест'); c_run = T('Иҷро.', c_none); c_syn = T('Синтакс эрор:'); c_yaane = T('Яъне:', c_syn); c_syn2 = T('Синтакс эрор', c_yaane); c_add = T('Қавси пӯшанда илова'); c_works = T('кор мекунад.', c_add); c_rule = T('Қоида:', c_works); c_pair = T('ҳар қавси кушода'); c_quote = T('ҳар нохунак')
zoom(c_men + .5, c_rule - .3, 330, 250, 1.4)
typ(c_men + .1, C1, 4.2)
mark(c_none - .3, c_run - .1, 0, 13, 19, '⚠️ қавси ) нест', 'r')
run(c_run + .3, 'bad')
ring(c_syn, c_add - .2, '#out', '⚠️ SyntaxError: missing )', 'r', 2)
mark(c_syn + .3, c_yaane - .1, 0, 0, 19, 'сатри 1', 'y', 'below')
typ(c_add, C2, 1.0)
mark(c_add + 1.1, c_works - .1, 0, 19, 21, '✅ )', 'g')
run(c_works + .3)
ring(c_works + .8, c_rule - .1, '#out', '✅ Салом', 'g', 2)
chip(c_pair, S_READ - .4, '<span class="big">( )</span><div>қавс — ҷуфт-ҷуфт<small>ва нохунак ҳам ҷуфт: " "</small></div>', 'card')

# --- 3. Паёми хаторо мехонем (слайд) ---
S('s-read', S_READ, S_TASK)
r_s1 = T('Қадами якум'); r_s2 = T('Қадами дуюм'); r_s3 = T('Қадами сеюм'); r_up = T('Баъзан хатои асосӣ'); r_lamp = T('ишораи лампа')
slides.append(f'''<section class="scene" id="s-read">
<div class="kicker" {A('down', S_READ + .1)}><b>05</b>ПАЁМИ ХАТОРО ЧӢ ТАВР МЕХОНЕМ</div>
<div class="h2" style="left:60px;top:90px;font-size:50px" {A('up', S_READ + .3)}>Паёми хаторо <span class="acc">хонед</span></div>
<div class="codechip" style="left:60px;top:200px;font-size:34px;display:flex;gap:18px;padding:22px 30px">
<span style="display:inline-block;color:var(--purple)" {A('pop', r_s1)}>ReferenceError:</span>
<span style="display:inline-block;color:var(--teal)" {A('pop', r_s2)}>City is not defined</span>
<span style="display:inline-block;color:var(--fn)" {A('pop', r_s3)}>(line 2)</span></div>
<div class="card3" style="left:60px;top:340px;width:360px;height:200px" {A('up', r_s1)}><div class="emo">🏷️</div><div class="t">1 · навъи хато</div><div class="u">ReferenceError ё SyntaxError</div></div>
<div class="card3" style="left:460px;top:340px;width:360px;height:200px" {A('up', r_s2)}><div class="emo">💬</div><div class="t">2 · сабаб</div><div class="u">ба ҷумла нигаред</div></div>
<div class="card3" style="left:860px;top:340px;width:360px;height:200px" {A('up', r_s3)}><div class="emo">📍</div><div class="t">3 · рақами сатр</div><div class="u">ба ҳамон ҷо равед</div></div>
<div style="left:60px;top:580px" {A('left', r_up)}><span class="pill err">⬆️ баъзан хато як сатр боло аст</span></div>
<div style="left:620px;top:580px" {A('left', r_lamp)}><span class="pill ok">💡 дар IDE: ишора, чӣ тавр ислоҳ кунед</span></div>
</section>''')

# --- 4. Вазифаҳо ---
S('ide', S_TASK, S_SUM)
t_tab = T('ҷадвали «ҳафт,'); t_four = T('Чор вазифа'); t_t1 = T('Якум: қавси'); t_t1w = T('қавси гумшуда'); t_t2 = T('Дуюм: давре'); t_t2w = T('давре, ки хотима'); t_t3 = T('Саввум:', t_t2); t_t3w = T('конст-ро иваз'); t_t4 = T('Чорум: шумораи'); t_t4w = T('шумораи нодуруст'); t_chk = T('Ай-ди-и месанҷад')
t_q = T('Ва санҷиши нав'); t_x = T('лет икс баробари панҷ'); t_if = T('Иф, дар қавс', t_q); t_log2 = T('Баъд консол лог'); t_what = T('Чӣ чоп мешавад'); t_pz = T('Видеоро пауза')
t_ans = T('Ҷавоб:', t_pz); t_ha = T('«ҳа» ва даҳ'); t_gave = T('Як баробар ба икс'); t_true = T('даҳ «дуруст»'); t_xnow = T('Ва икс акнун')
chip(S_TASK + .1, S_TASK + 2.0, '<span>🎯</span><div>Вазифаҳо барои шумо<small>06 · дар IDE, ҷадвали «7 · Хатогиро ёб»</small></div>', 'card')
click(t_tab + .9, '#tabs .tab:nth-child(8)')
ST1 = 'let temperature = 34;\nif (temperature > 30) {\n  console.log("Гарм аст");\n} else {\n  console.log("Хунук аст");\n'
ST2 = 'for (let i = 1; i <= 3; ) {\n  console.log(i);\n}\n'
ST3 = 'const total = 0;\nfor (let i = 1; i <= 5; i++) {\n  total = total + i;\n}\nconsole.log(total);\n'
ST4 = 'let shopping = ["нон", "шир", "тухм"];\nconsole.log(shopping[3]);\n'
setc(t_tab + .92, ST1)
ring(t_tab + 1.4, t_four - .2, '#tabs .tab:nth-child(8)', '', 'y', 4)
ring(t_four, t_t1 - .1, '#side', '📘 назария', 'c', 4)
ring(t_t1, t_t2 - .1, '#task', 'Вазифаи 1', 'y', 4)
typ(t_t1w, ST1 + '}\n', 1.4)
click(t_t2 + .3, '#side button[data-i="1"]'); setc(t_t2 + .32, ST2)
typ(t_t2w, 'for (let i = 1; i <= 3; i++) {\n  console.log(i);\n}\n', 1.4)
click(t_t3 + .3, '#side button[data-i="2"]'); setc(t_t3 + .32, ST3)
typ(t_t3w, 'let total = 0;\nfor (let i = 1; i <= 5; i++) {\n  total = total + i;\n}\nconsole.log(total);\n', 1.2)
click(t_t4 + .3, '#side button[data-i="3"]'); setc(t_t4 + .32, ST4)
ring(t_t4 + .8, t_chk - .1, '#task', 'Вазифаи 4', 'y', 4)
typ(t_t4w, 'let shopping = ["нон", "шир", "тухм"];\nconsole.log(shopping[2]);\n', 1.2)
ring(t_chk - .3, t_chk + .9, '#check', '✓ Санҷиш', 'c', 6)
click(t_chk + .5, '#check', 'check'); sfx.append(dict(name='chime', t=t_chk + .9, gain=.6))
ring(t_chk + 1.0, t_q - .3, '#checks', '', 'g', 4)
Q0 = 'let x = 5;'
Q1 = 'let x = 5;\nif (x = 10) {\n  console.log("ҳа");\n}'
Q2 = Q1 + '\nconsole.log(x);'
click(t_q + .1, '#tabs .tab:nth-child(1)'); setc(t_q + .12, '')
zoom(t_x - .3, t_what - .2, 330, 250, 1.4)
typ(t_x, Q0, 1.4)
typ(t_if, Q1, 3.6)
typ(t_log2, Q2, 1.2)
mark(t_what, t_pz - .3, 4, 0, 15, '❓ чӣ чоп мешавад?', 'y')
g0 = V(GAP_Q) - PAUSE
chip(t_what, g0 - .3, '<span class="big">❓</span><div>if (x = 10) … чӣ чоп мешавад?<small>видеоро пауза кунед ✍️</small></div>', 'card')
for k in range(5):
    chip(g0 + k + .02, g0 + k + .62, f'<span class="big">{5 - k}</span><div>if (x = 10) … чӣ чоп мешавад?<small>фикр кунед · баъд ҷавобро мебинем ✅</small></div>', 'card')
    sfx.append(dict(name='tick', t=g0 + k, gain=.8))
run(t_ans + .3)
ring(t_ha, S_SUM - .3, '#out', '✅ ҳа · 10', 'g', 2)
mark(t_gave, t_true - .1, 1, 4, 10, 'x = 10 (гузоштан)', 'r')
mark(t_true, t_xnow - .1, 1, 4, 10, '10 = «дуруст»', 'y', 'below')
mark(t_xnow, S_SUM - .3, 4, 12, 13, 'x акнун 10', 'g')

# --- 5. Хулоса ---
x_a = T('як баробар ба ҷои', S_SUM); x_b = T('ҳарфи калон ва хурд,', x_a); x_c = T('қавси фаромӯшшуда.', x_b); x_d = T('Ва асоси кор'); x_e = T('Хато душман'); x_pdf = T('Шпаргалкаи бепул')
slides.append(f'''<section class="scene" id="s-sum">
<div class="kicker" {A('down', S_SUM + .2)}><b>07</b>ХУЛОСА</div>
<div class="h2" style="left:60px;top:90px;font-size:50px" {A('up', S_SUM + .6)}>Се хато — <span class="acc">як роҳнамо</span></div>
<div class="card3" style="left:60px;top:220px;width:360px;height:250px" {A('up', x_a)}><div class="emo">🟰</div><div class="t">= ба ҷои ===</div><div class="codechip" style="font-size:22px"><span class="e">=</span> гузоштан · <span class="t">===</span> муқоиса</div></div>
<div class="card3" style="left:460px;top:220px;width:360px;height:250px" {A('up', x_b)}><div class="emo">🔤</div><div class="t">Ҳарфи калон/хурд</div><div class="codechip" style="font-size:22px"><span class="e">City</span> ≠ <span class="t">city</span></div></div>
<div class="card3" style="left:860px;top:220px;width:360px;height:250px" {A('up', x_c)}><div class="emo">❌</div><div class="t">Қавси фаромӯшшуда</div><div class="codechip" style="font-size:22px">log(<span class="s">"Салом"</span><span class="t">)</span></div></div>
<div style="left:60px;top:510px" {A('up', x_d)}><span class="pill ok">📨 паёми хаторо хонед: навъ · сабаб · сатр</span></div>
<div style="left:60px;top:580px" {A('up', x_pdf)}><span class="pill accent">📘 Шпаргалкаи бепул (PDF) — дар тавсифи видео</span></div>
</section>''')
S('s-sum', S_SUM, X_NEXT)

x_steps = T('қадам ба қадам'); x_sub = T('Обуна шавед')
slides.append(f'''<section class="scene" id="s-next">
<div class="kicker" {A('down', X_NEXT + .1)}><b>ДАРСИ 8</b>НАВБАТӢ</div>
<div class="h1" style="left:60px;top:110px;font-size:104px;line-height:1.05" {A('stamp', X_NEXT + .3)}>ХАТОГӢ ВА<br>ДЕБАГ</div>
<div class="sub" style="left:68px;top:360px" {A('up', X_NEXT + 1.4)}>чӣ тавр хатоҳоро қадам ба қадам меёбем</div>
<div style="left:68px;top:440px" {A('left', x_steps)}><span class="pill ok">👀 бубин</span></div>
<div style="left:68px;top:508px" {A('left', x_steps + .5)}><span class="pill">🔎 санҷ</span></div>
<div style="left:68px;top:576px" {A('left', x_steps + 1.0)}><span class="pill accent">🛠️ ислоҳ кун</span></div>
<div style="left:820px;top:170px" {A('pop', x_sub)}><span class="pill accent" style="font-size:34px;padding:20px 40px">🔔 Обуна шавед</span></div>
<div style="left:820px;top:270px" {A('pop', x_sub + .5)}><span class="pill" style="font-size:26px;padding:16px 30px">@shahriyor_yunusov</span></div>
</section>''')
S('s-next', X_NEXT, END + 1)

chapters = [dict(t=0, title='Хук'), dict(t=S1_END, title='Хато — роҳнамост'), dict(t=S_E1, title='Хатои 1: = ба ҷои ==='), dict(t=S_E2, title='Хатои 2: ҳарфи калон ва хурд'),
            dict(t=S_E3, title='Хатои 3: қавси фаромӯшшуда'), dict(t=S_READ, title='Паёми хаторо чӣ тавр мехонем'), dict(t=S_TASK, title='Вазифаҳо ва санҷиш'), dict(t=S_SUM, title='Хулоса')]
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
MAP = [(r'ай-ди-и', 'IDE'), (r'консол лог', 'console.log'), (r'референс эрор', 'ReferenceError'), (r'синтакс эрор', 'SyntaxError'), (r'сити из нот дефайнд', 'City is not defined'),
       (r'мисинг қавси пӯшанда афтер аргумент лист', 'missing ) after argument list'), (r'конст-ро', 'const-ро'), (r'консол', 'console'), (r'лет', 'let'), (r'эйдж', 'age'), (r'иф', 'if'), (r'сити', 'city'), (r'икс', 'x'), (r'Инстаграм', 'Instagram')]
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
with open('../youtube-lesson-7.srt', 'w', encoding='utf8') as f:
    for k, c in enumerate(caps, 1): f.write(f"{k}\n{ts(c['t0'])} --> {ts(c['t1'])}\n{c['text']}\n\n")
with open('chapters.txt', 'w', encoding='utf8') as f:
    for c in chapters: f.write(f"{int(c['t'] // 60)}:{int(c['t'] % 60):02} {c['title']}\n")
print('END', END, 'scenes', len(scenes), 'ide ops', len(ide), 'sfx', len(sfx))
print(open('chapters.txt').read())
