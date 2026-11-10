# Собирает video.html (IDE + слайды + таймлайн), sfx.json, .srt (для YouTube; в видео субтитров НЕТ) и главы для YouTube-урока 6 «Объект».
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
S1_END = T('Тасаввур кунед, ки корти')
S2_END = T('Ба ай-ди-и')
S3_END = T('Ҳоло қиматро иваз')
S4_END = T('Агар бисёр одам')
S5_END = T('Се хатои маъмули')
S6_END = T('Ва акнун вазифа')
S7_END = T('Хулоса мекунем.')
X_NEXT = T('Дарси оянда')

# --- 0. Хук ---
h_three = T('Оё се тағйирёбанда'); h_more = T('боз се?'); h_tired = T('Хаста мешавем'); h_card = T('Як корт кифоя'); h_obj = T('Ин обжект аст'); h_quiz = T('Дар охир санҷиши')
slides.append(f'''<section class="scene" id="s-hook">
<div class="kicker" {A('down', .2)}><b>ДАРСИ 6</b>БАРНОМАСОЗӢ АЗ СИФР · JAVASCRIPT</div>
<div class="h1" style="left:60px;top:110px;font-size:128px" {A('stamp', .6)}>ОБЪЕКТ</div>
<div class="mono acc" style="left:66px;top:268px;font-size:58px;font-weight:800" {A('up', h_obj)}>object</div>
<div class="sub" style="left:68px;top:350px" {A('up', h_obj + .3)}>маълумоти як чиз — дар як ҷо</div>
<div style="left:68px;top:430px" {A('left', h_three)}><span class="pill err">📦 <span class="mono">name1, age1, city1</span></span></div>
<div style="left:68px;top:498px" {A('left', h_more)}><span class="pill err">📦 <span class="mono">name2, age2, city2</span> …</span></div>
<div style="left:68px;top:566px" {A('left', h_tired)}><span class="pill err">😮‍💨 хаста мешавем</span></div>
<div class="node yes" style="left:830px;top:150px;width:340px" {A('pop', h_card)}><span class="big">🪪</span><span class="mono">person</span><small>як корт — се хусусият</small></div>
<div style="left:830px;top:400px" {A('left', h_obj + .3)}><span class="pill ok"><span class="mono">name:</span> «Нигина»</span></div>
<div style="left:830px;top:468px" {A('left', h_obj + .8)}><span class="pill ok"><span class="mono">age:</span> 20</span></div>
<div style="left:830px;top:536px" {A('left', h_obj + 1.3)}><span class="pill ok"><span class="mono">city:</span> «Душанбе»</span></div>
<div style="left:850px;top:640px" {A('pop', h_quiz)}><span class="pill accent">🎯 Дар охир: санҷиши нав</span></div>
</section>''')
S('s-hook', 0, S1_END)

# --- 1. Образи корт ---
c_r1 = T('дар он ном'); c_r2 = T('синну сол ва шаҳр'); c_r3 = T('шаҳр навишта'); c_each = T('Ҳар хат ном'); c_val = T('ва дар паҳлӯяш қимат'); c_obj = T('Обжект ҳамин'); c_key = T('калид, ва қимат')
c_diff = T('Аз дарси чорум'); c_list = T('дар рӯйхат қиматҳоро'); c_idx = T('сифр, як, ду'); c_obj2 = T('Дар обжект'); c_nm = T('нейм, эйдж'); c_life = T('Дар ҳаёт ҳам'); c_insta = T('профили Инстаграм'); c_prod = T('корти маҳсулот'); c_music = T('пайванди мусиқӣ')
PA = c_diff - .25; PB = c_life - .25
slides.append(f'''<section class="scene" id="s-card">
<div class="kicker" {A('down', S1_END + .1)}><b>01</b>ОБЪЕКТ ЧИСТ?</div>
<div class="h2" style="left:60px;top:100px;font-size:46px" {A('up', S1_END + .3, PA)}>🪪 Корти шиноснома</div>
<div class="row" style="left:60px;top:190px;width:560px" {A('left', c_r1, PA)}><span class="op">ном</span><span class="mean"></span><span class="res" style="color:var(--str)">«Нигина»</span></div>
<div class="row" style="left:60px;top:274px;width:560px" {A('left', c_r2, PA)}><span class="op">синну сол</span><span class="mean"></span><span class="res" style="color:var(--num)">20</span></div>
<div class="row" style="left:60px;top:358px;width:560px" {A('left', c_r3, PA)}><span class="op">шаҳр</span><span class="mean"></span><span class="res" style="color:var(--str)">«Душанбе»</span></div>
<div style="left:680px;top:200px" {A('pop', c_each, PA)}><span class="pill accent">🔑 ном = калид</span></div>
<div style="left:680px;top:284px" {A('pop', c_val, PA)}><span class="pill ok">💎 дар паҳлӯяш = қимат</span></div>
<div style="left:680px;top:368px" {A('pop', c_obj, PA)}><span class="pill">🪪 обжект = корт бо хусусиятҳо</span></div>
<div style="left:60px;top:500px" {A('up', c_key, PA)}><span class="pill accent" style="font-size:30px;padding:16px 30px">калид + қимат = <span class="mono">object</span></span></div>

<div class="h2" style="left:60px;top:90px;font-size:38px" {A('up', c_diff, PB)}>Аз дарси 4 фарқ</div>
<div class="h2" style="left:60px;top:190px;font-size:34px" {A('up', c_list, PB)}>Рӯйхат — бо шумора</div>
<div class="node" style="left:60px;top:260px;width:150px" {A('pop', c_idx, PB)}><span class="mono acc" style="font-size:56px">0</span><small>сифр</small></div>
<div class="node" style="left:230px;top:260px;width:150px" {A('pop', c_idx + .7, PB)}><span class="mono acc" style="font-size:56px">1</span><small>як</small></div>
<div class="node" style="left:400px;top:260px;width:150px" {A('pop', c_idx + 1.3, PB)}><span class="mono acc" style="font-size:56px">2</span><small>ду</small></div>
<div class="h2" style="left:680px;top:190px;font-size:34px" {A('up', c_obj2, PB)}>Обжект — бо ном</div>
<div class="node yes" style="left:680px;top:260px;width:230px" {A('pop', c_nm, PB)}><span class="mono" style="font-size:44px;color:var(--purple)">name</span><small>ном</small></div>
<div class="node yes" style="left:940px;top:260px;width:230px" {A('pop', c_nm + .55, PB)}><span class="mono" style="font-size:44px;color:var(--purple)">age</span><small>эйдж</small></div>
<div class="sub" style="left:60px;top:470px" {A('up', c_nm + 1.2, PB)}>person[0]  →  person.name</div>

<div class="h2" style="left:60px;top:100px;font-size:46px" {A('up', c_life)}>Обжектҳо ҳама ҷо ҳастанд</div>
<div class="node" style="left:60px;top:230px;width:340px" {A('pop', c_insta)}><span class="big">📸</span>профили Instagram</div>
<div class="node" style="left:470px;top:230px;width:340px" {A('pop', c_prod)}><span class="big">🛍️</span>корти маҳсулот<small>дар дукон</small></div>
<div class="node" style="left:880px;top:230px;width:340px" {A('pop', c_music)}><span class="big">🎵</span>пайванди мусиқӣ</div>
</section>''')
S('s-card', S1_END, S2_END)

# --- 2. Аввалин объект дар IDE ---
S('ide', S2_END, S7_END)
setc(S2_END, ''); clear(S2_END)
chip(S2_END + .1, S2_END + 2.0, '<span>💻</span><div>Аввалин обжект дар IDE<small>02 · ҳамроҳи ман нависед</small></div>', 'card')
t_link = T('Пайванд дар тавсиф')
chip(t_link, t_link + 3.6, '🔗 yunusovshahriyor.github.io/yunusov.tj/ide', 'side yel', 'top:90px')
P0 = 'let person = {\n};'
P1 = 'let person = {\n  name: "Нигина",\n};'
P2 = 'let person = {\n  name: "Нигина",\n  age: 20\n};'
a_let = T('лет персон баробари'); a_name = T('нейм, ду нуқта, «Нигина»'); a_age = T('Эйдж, ду нуқта, бисту'); a_box = T('Ин ҳамон қуттии'); a_feat = T('дохилаш якчанд хусусият'); a_get = T('Барои гирифтани қимат')
a_log = T('Консол лог, персон нуқта нейм'); a_run1 = T('Иҷро.', a_log); a_nig = T('«Нигина»!', a_run1); a_age2 = T('Ва персон нуқта эйдж'); a_dot = T('Нуқта — ин')
zoom(a_let - .3, a_dot - .2, 330, 250, 1.4)
typ(a_let, P0, 2.4)
typ(a_name, P1, 1.8)
typ(a_age, P2, 1.4)
mark(a_box, a_feat - .1, 0, 4, 10, '📦 ҳамон қуттӣ (дарси 1)', 'y')
mark(a_feat, a_get - .1, 1, 2, 17, 'хусусият 1', 'c', 'below')
mark(a_feat + .6, a_get - .1, 2, 2, 9, 'хусусият 2', 'g', 'below')
PL1 = P2 + '\nconsole.log(person.name);'
typ(a_log - .2, PL1, 2.2)
mark(a_get + 1.5, a_log + .6, 1, 2, 6, 'калид', 'y')
run(a_run1 + .3)
ring(a_nig, a_age2 - .1, '#out', '✅ Нигина', 'g', 2)
PL2 = PL1 + '\nconsole.log(person.age);'
typ(a_age2 - .1, PL2, 1.8)
a_20 = T('бисту.', a_age2)
run(a_20 + .15)
ring(a_20 + .7, a_dot - .1, '#out', '✅ 20', 'g', 2)
mark(a_dot, S3_END - .3, 5, 18, 19, '. = «дар дохили ин корт»', 'c', 'below')

# --- 3. Иваз кардан ва илова кардан ---
setc(S3_END, P2); clear(S3_END)
chip(S3_END + .1, S3_END + 1.8, '<span>✏️</span><div>Иваз ва илова кардан<small>03 · person.age, person.city</small></div>', 'card')
b_age = T('Персон нуқта эйдж баробари'); b_yaani = T('Яъне ба синну'); b_run1 = T('Иҷро.', b_yaani); b_21 = T('Бисту як!', b_yaani); b_new = T('Ва хусусияти нав'); b_city = T('персон нуқта сити баробари')
b_dotw = T('Нуқта, ном ва қимат'); b_log = T('Консол лог, персон нуқта сити'); b_runC = T('Иҷро.', b_log); b_dsh = T('«Душанбе»!', b_runC); b_grew = T('Корт калон шуд')
zoom(b_age - .3, b_dsh + 1.0, 330, 250, 1.4)
C1 = P2 + '\nperson.age = person.age + 1;'
typ(b_age, C1, 3.4)
mark(b_yaani, b_run1 - .2, 4, 13, 27, '+1 ба синну сол', 'g')
C1L = C1 + '\nconsole.log(person.age);'
typ(b_yaani + .2, C1L, 1.6)
run(b_run1 + .3)
ring(b_21, b_new - .1, '#out', '✅ 21', 'g', 2)
C2 = P2 + '\nperson.city = "Душанбе";'
typ(b_city - .4, C2, 2.6)
mark(b_new + .3, b_dotw - .2, 4, 0, 11, '🆕 хусусияти нав', 'c')
mark(b_dotw, b_dotw + 1.3, 4, 6, 7, 'нуқта', 'y', 'below')
mark(b_dotw + .8, b_log - .2, 4, 7, 11, 'ном', 'c')
mark(b_dotw + 1.5, b_log - .2, 4, 14, 23, 'қимат', 'g', 'below')
C2L = C2 + '\nconsole.log(person.city);'
typ(b_log, C2L, 1.8)
run(b_runC + .3)
ring(b_dsh, b_grew - .1, '#out', '✅ Душанбе', 'g', 2)
chip(b_grew, b_grew + 3.0, '<span>🪪</span><div>Корт калон шуд<small>ном · синну сол · шаҳр</small></div>', 'card')

# --- 4. Рӯйхати объектҳо ---
setc(S4_END, ''); clear(S4_END)
chip(S4_END + .1, S4_END + 2.2, '<span>📋</span><div>Рӯйхати обжектҳо<small>04 · дарси 4 + дарси 3</small></div>', 'card')
L0 = 'let people = [\n];'
L1 = 'let people = [\n  { name: "Нигина", age: 20 },\n];'
L2 = 'let people = [\n  { name: "Нигина", age: 20 },\n  { name: "Фарҳод", age: 25 }\n];'
l_let = T('Лет пипл баробари'); l_two = T('ду корт,'); l_far = T('Фарҳод бисту панҷ'); l_get = T('Барои гирифтани номи дуюм'); l_pl = T('пипл, қавси чоркунҷа, як'); l_runA = T('Иҷро.', l_pl); l_farA = T('«Фарҳод»!', l_runA)
l_idx0 = T('Шумора аз сифр'); l_for = T('Ва давр аз дарси'); l_cl = T('Консол лог, пипл'); l_runB = T('Иҷро.', l_cl); l_names = T('Нигина, Фарҳод.', l_runB); l_real = T('Дар барномаҳои воқеӣ')
zoom(l_let - .3, l_real, 330, 250, 1.4)
typ(l_let, L0, 2.0)
typ(l_two, L1, 1.2)
typ(l_far, L2, 1.4)
L3 = L2 + '\nconsole.log(people[1].name);'
typ(l_pl - .8, L3, 2.6)
mark(l_pl + 1.0, l_runA - .1, 4, 18, 21, '[1] = корти дуюм', 'y')
run(l_runA + .3)
ring(l_farA, l_idx0 - .1, '#out', '✅ Фарҳод', 'g', 2)
mark(l_idx0, l_for - .1, 4, 18, 21, 'аз сифр!', 'c', 'below')
LF1 = L2 + '\nfor (let i = 0; i < people.length; i++) {\n}'
typ(l_for + .2, LF1, 5.2)
mark(l_for + .5, l_cl - .1, 4, 0, 3, '🔁 давр (дарси 3)', 'g')
LF2 = L2 + '\nfor (let i = 0; i < people.length; i++) {\n  console.log(people[i].name);\n}'
typ(l_cl, LF2, 2.4)
mark(l_cl + 2.0, l_runB - .1, 5, 14, 23, 'корти i-ум', 'c', 'below')
run(l_runB + .3)
ring(l_names, l_real - .1, '#out', '✅ Нигина, Фарҳод', 'g', 2)

# --- 5. Хатогиҳои маъмул ---
setc(S5_END, ''); clear(S5_END)
chip(S5_END + .1, S5_END + 2.0, '<span>🐞</span><div>Се хатои маъмул<small>05 · ҳама хато мекунанд — ин муқаррарӣ аст</small></div>', 'card')
e1 = T('Якум:', S5_END); e1w = T('Агар нависем'); e1_typo = T('ҳарфҳо ҷой иваз'); e1_undef = T('ҷавоб андефайнд'); e1_care = T('Диққат ба имло')
e2 = T('Дуюм:', e1_care); e2w = T('Нейм, ду нуқта, Нигина', e2); e2_err = T('хатои «Нигина', e2w); e2_rule = T('Матн ҳамеша дар нохунак')
e3 = T('Саввум:', e2_rule); e3w = T('Агар байни нейм'); e3_err = T('хатои «анэкспектид', e3w); e3_rule = T('Хусусиятҳо бо вергул')
chip(e1 + .1, e1 + 2.3, 'Хатои 1 / 3', 'side red', 'top:70px;left:1090px')
E1 = 'let person = { name: "Нигина", age: 20 };\nconsole.log(person.nmae);'
zoom(e1w, e1_care, 330, 250, 1.4)
typ(e1w, E1, 2.6)
mark(e1_typo, e1_care - .1, 1, 19, 23, '⚠️ nmae ≠ name', 'r')
run(e1_undef - .2, 'bad')
ring(e1_undef + .4, e2 - .2, '#out', '⚠️ undefined', 'r', 2)
chip(e2 + .1, e2 + 2.3, 'Хатои 2 / 3', 'side red', 'top:70px;left:1090px')
E2 = 'let person = { name: Нигина, age: 20 };\nconsole.log(person.name);'
zoom(e2w, e2_rule + 1.0, 330, 250, 1.4)
typ(e2w, E2, 2.8)
mark(e2w + 1.6, e2_rule - .1, 0, 21, 27, '⚠️ нохунак нест', 'r')
run(e2_err - .2, 'bad')
ring(e2_err + .5, e3 - .2, '#out', '⚠️ Нигина is not defined', 'r', 2)
chip(e3 + .1, e3 + 2.3, 'Хатои 3 / 3', 'side red', 'top:70px;left:1090px')
E3 = 'let person = {\n  name: "Нигина"\n  age: 20\n};'
zoom(e3w, e3_rule + 1.0, 330, 250, 1.4)
typ(e3w, E3, 3.0)
mark(e3w + 2.2, e3_rule - .1, 1, 8, 16, '⚠️ вергул нест', 'r')
run(e3_err - .2, 'bad')
ring(e3_err + .6, S6_END - .3, '#out', '⚠️ Unexpected identifier', 'r', 2)

# --- 6. Вазифаҳо ---
t_tab = T('ҷадвали', S6_END); t_three = T('Се вазифа ҳаст'); t_t1 = T('Якум:', t_three); t_t1w = T('обжекти персон созед'); t_t2 = T('Дуюм:', t_t1); t_t2w = T('синну солро як зиёд'); t_t3 = T('Саввум:', t_t2); t_t3w = T('хусусияти сити илова'); t_chk = T('Ай-ди-и месанҷад')
t_q = T('Ва санҷиши нав'); t_prs = T('персон дорад нейм'); t_wr = T('Мо менависем'); t_cl = T('Ва консол лог, персон нуқта эйдж'); t_what = T('Чӣ мешавад?'); t_pz = T('Видеоро пауза')
t_ans = T('Ҷавоб:', t_pz); t_42 = T('чил ва ду.', t_ans); t_first = T('Аввал синну сол', t_ans); t_then = T('Баъд бисту як', t_ans)
chip(S6_END + .1, S6_END + 2.0, '<span>🎯</span><div>Вазифаҳо барои шумо<small>06 · дар IDE, ҷадвали «6 · Объект»</small></div>', 'card')
click(t_tab + .9, '#tabs .tab:nth-child(7)')
ST1 = 'let person = {\n  \n};\n'
ST2 = 'let person = { name: "Нигина", age: 20 };\n\n// синну солро 1 зиёд кунед ва нишон диҳед\n'
ST3 = 'let person = { name: "Нигина", age: 20 };\n\n// city илова кунед\n'
setc(t_tab + .92, ST1)
ring(t_tab + 1.4, t_three - .2, '#tabs .tab:nth-child(7)', '', 'y', 4)
ring(t_three, t_t1 - .1, '#side', '📘 назария', 'c', 4)
ring(t_t1, t_t2 - .1, '#task', 'Вазифаи 1', 'y', 4)
SOL1 = 'let person = {\n  name: "Нигина",\n  age: 20\n};\n'
typ(t_t1w, SOL1, 3.2)
click(t_t2 + .3, '#side button[data-i="1"]'); setc(t_t2 + .32, ST2)
ring(t_t2 + .8, t_t3 - .1, '#task', 'Вазифаи 2', 'y', 4)
SOL2 = 'let person = { name: "Нигина", age: 20 };\nperson.age = person.age + 1;\nconsole.log(person.age);\n'
typ(t_t2w, SOL2, 3.2)
click(t_t3 + .3, '#side button[data-i="2"]'); setc(t_t3 + .32, ST3)
ring(t_t3 + .8, t_chk - .1, '#task', 'Вазифаи 3', 'y', 4)
SOL3 = 'let person = { name: "Нигина", age: 20 };\nperson.city = "Душанбе";\nconsole.log(person.city);\n'
typ(t_t3w, SOL3, 3.0)
ring(t_chk - .3, t_chk + .9, '#check', '✓ Санҷиш', 'c', 6)
click(t_chk + .5, '#check', 'check'); sfx.append(dict(name='chime', t=t_chk + .9, gain=.6))
ring(t_chk + 1.0, t_q - .3, '#checks', '', 'g', 4)
Q0 = 'let person = { name: "Нигина", age: 20 };'
Q1 = Q0 + '\nperson.age = person.age + 1;'
Q2 = Q1 + '\nconsole.log(person.age * 2);'
click(t_q + .1, '#tabs .tab:nth-child(1)'); setc(t_q + .12, '')
zoom(t_prs - .3, t_what - .2, 330, 250, 1.4)
typ(t_prs + .1, Q0, 2.0)
typ(t_wr + .2, Q1, 2.6)
typ(t_cl + .1, Q2, 2.4)
mark(t_what, t_pz - .3, 2, 12, 26, '❓ чӣ мешавад?', 'y')
g0 = V(GAP_Q) - PAUSE
chip(t_what, g0 - .3, '<span class="big">❓</span><div>person.age * 2 — чӣ мешавад?<small>видеоро пауза кунед ✍️</small></div>', 'card')
for k in range(5):
    chip(g0 + k + .02, g0 + k + .62, f'<span class="big">{5 - k}</span><div>person.age * 2 — чӣ мешавад?<small>фикр кунед · баъд ҷавобро мебинем ✅</small></div>', 'card')
    sfx.append(dict(name='tick', t=g0 + k, gain=.8))
run(t_ans + .3)
ring(t_42, S7_END - .3, '#out', '✅ 42', 'g', 2)
mark(t_first, t_then - .1, 1, 13, 27, 'аввал: 20 + 1 = 21', 'c', 'below')
mark(t_then, S7_END - .3, 2, 12, 26, 'баъд: 21 × 2 = 42', 'g')

# --- 7. Хулоса ---
x1 = T('корт бо якчанд хусусият:', S7_END); x2 = T('калид ва қимат', S7_END); x3 = T('Қиматро бо нуқта', S7_END); x4 = T('Хусусияти нав ҳам', S7_END); x5 = T('Ва обжектҳоро метавон', S7_END); x_pdf = T('Шпаргалкаи бепул')
slides.append(f'''<section class="scene" id="s-sum">
<div class="kicker" {A('down', S7_END + .2)}><b>07</b>ХУЛОСА</div>
<div class="h2" style="left:60px;top:90px;font-size:50px" {A('up', x1)}>Обжект = <span class="acc">калид + қимат</span></div>
<div class="card3" style="left:60px;top:220px;width:360px;height:250px" {A('up', x2)}><div class="emo">🔑</div><div class="t">Калид</div><div class="codechip" style="font-size:22px"><span class="t">name</span>: <span class="s">"Нигина"</span></div></div>
<div class="card3" style="left:460px;top:220px;width:360px;height:250px" {A('up', x3)}><div class="emo">📍</div><div class="t">Нуқта: гирифтан</div><div class="codechip" style="font-size:22px">person<span class="e">.</span><span class="t">name</span></div></div>
<div class="card3" style="left:860px;top:220px;width:360px;height:250px" {A('up', x4)}><div class="emo">✏️</div><div class="t">Иваз / илова кардан</div><div class="codechip" style="font-size:22px">person.<span class="t">age</span> = <span class="n">21</span></div></div>
<div style="left:60px;top:510px" {A('up', x5)}><span class="pill ok">📋 рӯйхати обжектҳо — ҳамон рӯйхат + давр</span></div>
<div style="left:60px;top:580px" {A('up', x_pdf)}><span class="pill accent">📘 Шпаргалкаи бепул (PDF) — дар тавсифи видео</span></div>
</section>''')
S('s-sum', S7_END, X_NEXT)

x_ev = T('ҳамон хатоҳое'); x_sub = T('Обуна шавед')
slides.append(f'''<section class="scene" id="s-next">
<div class="kicker" {A('down', X_NEXT + .1)}><b>ДАРСИ 7</b>НАВБАТӢ</div>
<div class="h1" style="left:60px;top:110px;font-size:104px;line-height:1.05" {A('stamp', X_NEXT + .3)}>3 ХАТОИ<br>РӮЗИ АВВАЛ</div>
<div class="sub" style="left:68px;top:360px" {A('up', X_NEXT + 1.2)}>ҳамон хатоҳое, ки ҳар навомӯз мекунад</div>
<div style="left:68px;top:440px" {A('left', x_ev)}><span class="pill err">🐞 хатои 1</span></div>
<div style="left:68px;top:508px" {A('left', x_ev + .5)}><span class="pill err">🐞 хатои 2</span></div>
<div style="left:68px;top:576px" {A('left', x_ev + 1.0)}><span class="pill err">🐞 хатои 3</span></div>
<div style="left:820px;top:170px" {A('pop', x_sub)}><span class="pill accent" style="font-size:34px;padding:20px 40px">🔔 Обуна шавед</span></div>
<div style="left:820px;top:270px" {A('pop', x_sub + .5)}><span class="pill" style="font-size:26px;padding:16px 30px">@shahriyor_yunusov</span></div>
</section>''')
S('s-next', X_NEXT, END + 1)

chapters = [dict(t=0, title='Хук'), dict(t=S1_END, title='Объект чист? Образи корт'), dict(t=S2_END, title='Аввалин объект дар IDE'), dict(t=S3_END, title='Иваз кардан ва илова кардан'),
            dict(t=S4_END, title='Рӯйхати объектҳо'), dict(t=S5_END, title='Хатогиҳои маъмул'), dict(t=S6_END, title='Вазифаҳо ва санҷиш'), dict(t=S7_END, title='Хулоса')]
ide.sort(key=lambda o: o['t']); ptr.sort(key=lambda o: o['t'])

# ---------- субтитры (.srt для YouTube; в самом видео субтитров НЕТ) ----------
MAP = [(r'ай-ди-и', 'IDE'), (r'консол лог', 'console.log'), (r'эн-эм-эй-и', 'nmae'), (r'из нот дефайнд', 'is not defined'), (r'анэкспектид айдентифайер', 'Unexpected identifier'),
       (r'обжектҳоро', 'objectҳоро'), (r'обжектҳо', 'objectҳо'), (r'обжекти', 'object-и'), (r'обжект', 'object'), (r'персон', 'person'), (r'пипл', 'people'), (r'ленгс', 'length'),
       (r'андефайнд', 'undefined'), (r'нейм', 'name'), (r'эйдж', 'age'), (r'сити', 'city'), (r'фор', 'for'), (r'лет', 'let'), (r'ай', 'i'), (r'Инстаграм', 'Instagram')]
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
with open('../youtube-lesson-6.srt', 'w', encoding='utf8') as f:
    for k, c in enumerate(caps, 1): f.write(f"{k}\n{ts(c['t0'])} --> {ts(c['t1'])}\n{c['text']}\n\n")
with open('chapters.txt', 'w', encoding='utf8') as f:
    for c in chapters: f.write(f"{int(c['t'] // 60)}:{int(c['t'] % 60):02} {c['title']}\n")
print('END', END, 'scenes', len(scenes), 'ide ops', len(ide), 'sfx', len(sfx))
print(open('chapters.txt').read())
