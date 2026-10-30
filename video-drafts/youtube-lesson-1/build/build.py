# Собирает video.html (IDE + слайды + таймлайн), sfx.json, субтитры .srt и главы для YouTube-урока 1.
import json, re, html
W = json.load(open('words.json'))['words']
NARR_END = json.load(open('words.json'))['total']
toks = [re.sub(r'[^\w-]', '', w['w']).lower() for w in W]

def find(phrase, after=0):
    seq = [re.sub(r'[^\w-]', '', x).lower() for x in phrase.split()]
    for i in range(after, len(W) - len(seq) + 1):
        if toks[i:i + len(seq)] == seq: return i
    raise SystemExit('not found: ' + phrase)

# паузы без голоса (время повествования -> длительность вставки)
GAPS = []
def V(nt): return nt + sum(d for g, d in GAPS if g <= nt)
def T(phrase, after=0, end=False, off=0.0):
    i = find(phrase, after); n = len(phrase.split())
    return round(V(W[i + n - 1]['t1'] if end else W[i]['t0']) + off, 3)
def I(phrase, after=0): return find(phrase, after)

GAP_TRY = W[I('чӣ мешавад.', I('Шумо ҳам кӯшиш'))+1]['t1'] + 0.05; GAPS.append((GAP_TRY, 4.0))
GAP_PAUSE = W[I('интизор мешавам.')+1]['t1'] + 0.05; GAPS.append((GAP_PAUSE, 13.0))
END = round(V(NARR_END) + 0.6, 2)

# ---------- субтитры ----------
caps = []; i = 0
for ln in open('cues.txt', encoding='utf8'):
    ln = ln.strip()
    if not ln: continue
    ph, _, disp = ln.partition(' || '); disp = disp or ph; n = len(ph.split())
    caps.append(dict(t0=V(W[i]['t0']), t1=V(W[i + n - 1]['t1']), text=disp)); i += n
for a, b in zip(caps, caps[1:]): a['t1'] = min(max(a['t1'] + 0.35, a['t1']), b['t0'])
def cap_html(s):
    s = html.escape(s, quote=False)
    return re.sub(r'(let age = 2[56];|age = 26;|let 2age|age2|const pi = 3\.14;?|pi = 3|let a = [12]|&quot;Салом, &quot; \+ name \+ &quot;!&quot;|isStudent = true|console\.log|&quot;5&quot; \+ 1|\blet\b|\bconst\b|\bage\b|\bname\b|\btrue\b|\bfalse\b|\bif\b|\belse\b|\bpi\b)', r'<code>\1</code>', s)
for c in caps: c['html'] = cap_html(c['text'])

# ---------- таймлайн ----------
scenes, ide, marks, rings, ptr, chips, zooms, sfx = [], [], [], [], [], [], [], []
def S(id, t0, t1): scenes.append(dict(id=id, t0=t0, t1=t1)); sfx.append(dict(name='whoosh', t=t0 - .15, gain=.35))
code = ['']
def setc(t, c): ide.append(dict(t=t, op='set', code=c)); code[0] = c
def typ(t, new, dur=None):
    dur = dur or max(.6, min(4.5, .075 * abs(len(new) - len(code[0])) + .25))
    ide.append(dict(t=t, op='type', dur=dur, **{'from': code[0], 'to': new}))
    k = 0; n = sum(1 for _ in new) - len(code[0])
    for j in range(max(1, abs(n))): sfx.append(dict(name='key', t=round(t + dur * j / max(1, abs(n)), 3), gain=.5))
    code[0] = new; return t + dur
def run(t, kind='ok'):
    ptr.append(dict(t=t, sel='#run')); ide.append(dict(t=t, op='run', sel='#run'))
    sfx.append(dict(name='click', t=t, gain=.6)); sfx.append(dict(name='ding' if kind == 'ok' else 'buzz', t=t + .25, gain=.5 if kind == 'ok' else .35))
def click(t, sel, op='click'):
    ptr.append(dict(t=t, sel=sel)); ide.append(dict(t=t, op=op, sel=sel)); sfx.append(dict(name='click', t=t, gain=.6))
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
def box(label, val, cls='', ta=0, tl=0, tv=0, extra=''):
    return (f'<div class="box" style="position:relative" {A("pop", ta)}><div class="back"></div>'
            f'<div class="num {cls}" {A("drop", tv)}>{val}</div>{extra}<div class="front"><div class="tag" {A("stamp", tl)}>{label}</div></div></div>')

# --- 0. Хук ---
t_box = T('тағйирёбанда.', I('Салом,'))
h1 = T('Баъд аз ин'); h_code = T('аввалин коди'); h_run = T('иҷро мекунед'); h_err = T('хато медиҳад.')
h_no = T('Ҳеҷ чиз'); h_br = T('Танҳо браузер.'); h_go = T('Оғоз мекунем!')
S1_END = T('Тасаввур кунед,')
slides.append(f'''<section class="scene" id="s-hook">
<div class="kicker" {A('down', .2)}><b>ДАРСИ 1</b>БАРНОМАСОЗӢ АЗ СИФР · JAVASCRIPT</div>
<div style="left:110px;top:150px;zoom:1.35">
 <div class="box" style="position:relative" {A('pop', .4)}><div class="back"></div>
  <div class="num" {A('drop', .9, 2.6, 'flyout')}>25</div><div class="num" {A('drop', 3.0)}>26</div>
  <div class="front"><div class="tag" {A('stamp', .6)}>age</div></div></div></div>
<div class="h1" style="left:470px;top:150px" {A('stamp', t_box)}>ТАҒЙИРЁБАНДА</div>
<div class="sub" style="left:474px;top:238px;font-size:30px" {A('up', t_box + .4)}>variable · аз сифр, бо мисолҳо</div>
<div style="left:474px;top:310px;display:flex;flex-direction:column;gap:14px">
 <span class="pill" {A('left', h_code)}>✍️ Аввалин кодатонро менависед</span>
 <span class="pill" {A('left', h_run)}>▶️ Онро иҷро мекунед</span>
 <span class="pill" {A('left', h_err)}>⚠️ Мефаҳмед, ки чаро хато мешавад</span>
</div>
<div style="left:120px;top:520px" {A('pop', h_no)}><span class="pill gold">🌐 Ҳеҷ чиз насб намекунем — танҳо браузер</span></div>
</section>''')
S('s-hook', 0, S1_END)

# --- 1. Образи қуттӣ ---
b_box = T('қуттӣ доред.'); b_tag = T('тамға'); b_age = T('синну сол.'); b_25 = T('рақами бисту панҷро')
b_var = T('Ана ҳамин'); b_nom = T('ном', I('Ду чиз дорад')); b_qim = T('қимат', I('ва қимат —'))
b_year = T('Як сол'); b_out = T('мебарорем'); b_26 = T('бисту шашро'); b_same = T('Қуттӣ ҳамон,'); b_q = T('танҳо қимат иваз шуд.')
b_def = T('Барои ҳамин онро'); L_life = T('Дар ҳаёт ҳам'); L1 = T('холи бозӣ,'); L2 = T('бақияи ҳисоби'); L3 = T('шумораи пайравонатон'); L_all = T('Ҳамаи инҳо')
S2_END = T('Акнун ба амал')
slides.append(f'''<section class="scene" id="s-box">
<div class="kicker" {A('down', b_box)}><b>01</b>ТАҒЙИРЁБАНДА ЧИСТ?</div>
<div class="h2" style="left:56px;top:90px" {A('up', b_var, L_life - .2)}>Тағйирёбанда = <span style="color:var(--rust)">ном</span> + <span style="color:var(--leaf)">қимат</span></div>
<div style="left:400px;top:150px;zoom:1.3" {A('fade', b_box, L_life - .2)}>
 <div class="box" style="position:relative" {A('pop', b_box)}><div class="back"></div>
  <div class="num" {A('drop', b_25 - .2, b_out, 'flyout')}>25</div><div class="num" {A('drop', b_26)}>26</div>
  <div class="front"><div class="tag" {A('stamp', b_tag)}>age</div></div></div></div>
<div class="arrow" style="left:290px;top:432px" {A('right', b_nom, L_life - .2)}>НОМ (тамға) <span style="font-size:34px">→</span></div>
<div class="sub" style="left:560px;top:548px" {A('left', b_age, L_life - .2)}>age = «синну сол»</div>
<div class="arrow" style="left:880px;top:300px;color:var(--leaf)" {A('left', b_qim, L_life - .2)}><span style="font-size:34px">←</span> ҚИМАТ (дар дохил)</div>
<div style="left:56px;top:470px" {A('pop', b_year, b_out + .3)}><span class="pill ink">📅 +1 сол мегузарад…</span></div>
<div style="left:56px;top:470px;display:flex;gap:12px" {A('up', b_same, L_life - .2)}><span class="pill">📦 Қуттӣ ҳамон <b class="ok">✓</b></span><span class="pill">🏷️ Ном ҳамон <b class="ok">✓</b></span><span class="pill rust" {A('pop', b_q)}>🔄 Қимат иваз шуд</span></div>
<div style="left:56px;top:540px" {A('up', b_def, L_life - .2)}><span class="pill gold">тағйирёбанда = чизе, ки тағйир меёбад</span></div>
<div class="h2" style="left:56px;top:90px" {A('up', L_life + .2)}>Дар ҳаёт ҳам чунин «қуттиҳо» зиёданд</div>
<div style="left:56px;top:190px" class="card3" {A('up', L1)}><div class="emo">🎮</div><div class="t">Холи бозӣ</div><div class="v" data-cnt="1250;1980;{L1 + .3};3.5">1250</div><div class="u">score</div></div>
<div style="left:470px;top:190px" class="card3" {A('up', L2)}><div class="emo">💳</div><div class="t">Бақияи бонк</div><div class="v" data-cnt="340;520;{L2 + .3};3.5">340</div><div class="u">сомонӣ · balance</div></div>
<div style="left:884px;top:190px" class="card3" {A('up', L3)}><div class="emo">📱</div><div class="t">Пайравон дар Instagram</div><div class="v" data-cnt="1492;1530;{L3 + .3};3.5">1492</div><div class="u">followers</div></div>
<div style="left:56px;top:520px" {A('stamp', L_all)}><span class="pill rust">👉 ҳамаи инҳо — тағйирёбанда!</span></div>
</section>''')
S('s-box', S1_END, S2_END)

# --- 2. Аввалин код дар IDE ---
S3_END = T('Дар қуттӣ на танҳо')
S('ide', S2_END, S3_END)
chip(S2_END + .1, S2_END + 2.4, '<span>💻</span><div>Аввалин код дар IDE<small>02 · ҳамроҳи ман нависед</small></div>', 'card')
setc(S2_END, '')
ide.append(dict(t=S2_END, op='clear'))
t_link = T('пайванд дар тавсифи')
chip(t_link, t_link + 3.8, '🔗 yunusovshahriyor.github.io/yunusov.tj/ide', 'side yel', 'top:90px')
t_w = T('лет эйдж баробари бисту панҷ.', I('Менависем:'))
zoom(t_w - .3, T('Пахш мекунем «Иҷро».') - .4, 330, 140, 1.5)
e = typ(t_w, 'let age = 25;', 3.0)
i_let = I('«лет»', I('Менависем:')); t_let = V(W[i_let]['t0'])
t_ejd = T('«эйдж» — ном.'); t_eq = T('Аломати баробар'); t_25 = T('бисту панҷ — қимат.'); t_sc = T('Охирин нуқтавергул.')
mark(t_let, t_ejd - .1, 0, 0, 3, '📦 «қуттии нав месозам»', 'c')
mark(t_ejd, t_eq - .1, 0, 4, 7, '🏷️ ном', 'y')
mark(t_eq, t_25 - .1, 0, 8, 9, '➡️ «дар дохилаш гузор»', 'g')
mark(t_25, t_sc - .1, 0, 10, 12, '🔢 қимат', 'y')
mark(t_sc, t_sc + 1.6, 0, 12, 13, 'нуқтавергул ; — охири фармон', 'r', 'below')
t_cl = T('консол лог, дар қавс эйдж.')
typ(t_cl, 'let age = 25;\nconsole.log(age);', 3.2)
t_cl2 = T('консол лог — ин'); mark(t_cl2, t_cl2 + 3.0, 1, 0, 11, '🖥️ «ба экран нишон деҳ»', 'c', 'below')
t_run = T('Пахш мекунем «Иҷро».', end=False) + .9
run(t_run); ring(t_run + .5, t_run + 3, '#out', '✅ натиҷа: 25', 'g', 2)
t_new = T('эйдж баробари бисту шаш.', I('Қимати навро'))
zoom(t_new - .4, T('Иҷро. Бисту шаш!') - .6, 330, 160, 1.45)
typ(t_new, 'let age = 25;\nconsole.log(age);\nage = 26;', 1.6)
t_att = T('Диққат: акнун'); mark(t_att, t_att + 4.6, 2, 0, 3, '⚠️ бе let — қуттӣ аллакай ҳаст', 'r', 'below')
t_b = T('Боз консол лог.'); typ(t_b, 'let age = 25;\nconsole.log(age);\nage = 26;\nconsole.log(age);', 1.4)
t_r2 = T('Иҷро. Бисту шаш!'); run(t_r2); ring(t_r2 + .5, t_r2 + 3.2, '#out', '🎉 26!', 'g', 2)
t_try = T('Шумо ҳам кӯшиш кунед:'); chip(t_try, T('чӣ мешавад.', I('Шумо ҳам кӯшиш'), end=True), '✍️ Навбати шумо: 26 → 100', 'side yel', 'top:80px')
g0 = V(GAP_TRY) - 4.0 + .2
typ(g0, 'let age = 25;\nconsole.log(age);\nage = 100;\nconsole.log(age);', 1.2)
run(g0 + 1.7); ring(g0 + 2.2, g0 + 3.9, '#out', '100 ✓', 'g', 2)

# --- 3. Се навъи қимат ---
n1 = T('Якум — рақам.'); n_calc = T('Бо рақам ҳисоб'); n2 = T('Дуюм — матн.'); n_cat = T('Матнҳоро бо плюс'); n_res = T('мешавад «Салом,', I('Матнҳоро бо плюс'))
n3 = T('Саввум — ҳа ё не,'); n_is = T('Масалан, из студент')
S4_END = T('Ва як хусусияти аҷиб:')
slides.append(f'''<section class="scene" id="s-types">
<div class="kicker" {A('down', S3_END + .2)}><b>03</b>СЕ НАВЪИ ҚИМАТ</div>
<div class="h2" style="left:56px;top:84px" {A('up', S3_END + .3)}>Дар қуттӣ чӣ гузоштан мумкин?</div>
<div style="left:70px;top:170px">{box('number', '26', '', n1, n1 + .3, n1 + .5)}</div>
<div style="left:510px;top:170px">{box('string', '"Шаҳриёр"', 's', n2, n2 + .3, n2 + .9)}</div>
<div style="left:950px;top:170px">{box('boolean', 'true', 'b', n3, n3 + .3, n3 + .5)}</div>
<div class="pill ink" style="left:100px;top:452px" {A('up', n1 + .2)}>рақам</div>
<div class="pill rust" style="left:560px;top:452px" {A('up', n2 + .2)}>матн "…"</div>
<div class="pill" style="left:960px;top:452px;background:var(--leaf);color:#fff" {A('up', n3 + .2)}>ҳа / не</div>
<div class="codechip" style="left:56px;top:530px;font-size:21px" {A('up', n_calc)}><span class="n">10</span> * <span class="n">3</span> → <span class="n" data-cnt="0;30;{n_calc + 2.5};1.5">0</span></div>
<div class="codechip" style="left:330px;top:530px;font-size:19px" {A('up', n_cat)}><span class="s">"Салом, "</span> + name + <span class="s">"!"</span> → <span class="s" data-tw="{n_res};1.2" data-text='"Салом, Шаҳриёр!"'></span></div>
<div class="codechip" style="left:930px;top:530px;font-size:19px" {A('up', n_is)}>isStudent = <span class="k">true</span> 🎓</div>
</section>''')
S('s-types', S3_END, S4_END)

# --- 3b. "5" + 1 в IDE ---
S5_END = T('Ду хел қуттӣ')
S('ide', S4_END, S5_END)
setc(S4_END, 'console.log(5 + 1);'); ide.append(dict(t=S4_END, op='clear'))
zoom(S4_END + .2, S5_END, 480, 345, 1.3)
run(S4_END + .9); ring(S4_END + 1.4, T('рақами «панҷ» дар нохунак') - .1, '#out', '5 + 1 = 6', 'g', 2)
t5 = T('рақами «панҷ» дар нохунак'); typ(t5, 'console.log("5" + 1);', 1.0)
mark(t5 + 1.0, T('Агар «панҷ» плюс') - .1, 0, 12, 15, '"5" — ин матн аст!', 'r')
t_51 = T('на шаш, балки'); run(t_51 - .5, 'bad')
ring(t_51 + .1, S5_END - .3, '#out', '🤯 "51" — матн, на рақам', 'r', 2)

# --- 4. let ва const ---
lc_let = T('лет — қуттии одӣ:'); lc_ch = T('қиматро иваз кардан мумкин.', I('лет — қуттии одӣ:')); lc_c = T('конст — қуттии'); lc_lock = T('қуфлшуда:')
lc_pi = T('Масалан, конст пай'); lc_no = T('Ин рақам иваз намешавад.'); lc_rule = T('Қоидаи оддӣ:'); lc_r1 = T('конст нависед.'); lc_r2 = T('Агар тағйир меёбад,')
S6_END = T('Ҳама хато мекунанд,')
slides.append(f'''<section class="scene" id="s-lc">
<div class="kicker" {A('down', S5_END + .2)}><b>04</b>LET ВА CONST</div>
<div class="h2" style="left:56px;top:84px" {A('up', S5_END + .3)}>Ду хел қуттӣ</div>
<div style="left:120px;top:150px">
 <div class="box" style="position:relative" {A('pop', lc_let)}><div class="back"></div>
  <div class="num" {A('drop', lc_let + .4, lc_ch + .6, 'flyout')}>10</div><div class="num" {A('drop', lc_ch + .8, lc_ch + 2.0, 'flyout')}>20</div><div class="num" {A('drop', lc_ch + 2.2)}>30</div>
  <div class="front"><div class="tag" {A('stamp', lc_let + .2)}>score</div></div></div></div>
<div class="pill ink" style="left:150px;top:440px" {A('up', lc_let + .3)}>let — қимат иваз мешавад 🔄</div>
<div style="left:760px;top:150px">
 <div class="box" style="position:relative" {A('pop', lc_c)}><div class="back"></div>
  <div class="num" style="font-size:40px" {A('drop', lc_c + .4)}>3.14</div>
  <div class="front"><div class="tag" {A('stamp', lc_c + .2)}>pi</div></div><div class="lock" style="left:190px;top:-10px" {A('stamp', lc_lock)}>🔒</div></div></div>
<div class="pill rust" style="left:770px;top:440px" {A('up', lc_c + .3)}>const — қимат доимист 🔒</div>
<div class="codechip" style="left:740px;top:520px" {A('up', lc_pi)}><span class="k">const</span> pi = <span class="n">3.14</span>;</div>
<div style="left:1000px;top:250px;font-size:80px;color:#d33" {A('stamp', lc_no, lc_rule - .2)}>✕</div>
<div class="codechip" style="left:120px;top:520px" {A('up', lc_ch)}><span class="k">let</span> score = <span class="n" data-cnt="10;30;{lc_ch + .6};2.2">10</span>;</div>
</section>
<section class="scene" id="s-rule">
<div class="kicker" {A('down', lc_rule)}><b>04</b>ҚОИДАИ ОДДӢ</div>
<div style="left:140px;top:150px;width:1000px" class="card3" {A('up', lc_rule + .2)}>
 <div style="display:flex;align-items:center;gap:22px;font:800 34px Inter" {A('left', lc_r1 - .6)}>Қимат тағйир <u>намеёбад</u> → <span class="codechip" style="font-size:32px"><span class="k">const</span> 🔒</span></div>
 <div style="height:40px"></div>
 <div style="display:flex;align-items:center;gap:22px;font:800 34px Inter" {A('left', lc_r2)}>Қимат тағйир <u>меёбад</u> → <span class="codechip" style="font-size:32px"><span class="k">let</span> 🔄</span></div>
 <div class="u" style="margin-top:24px;font-size:22px" {A('up', lc_r2 + 1.2)}>масалан: <b>const</b> pi, <b>let</b> score (холи бозӣ)</div>
</div>
</section>''')
S('s-lc', S5_END, lc_rule); S('s-rule', lc_rule, S6_END)

# --- 5. Хатогиҳо в IDE ---
S7_END = T('Ва акнун вазифа')
S('ide', S6_END, S7_END)
setc(S6_END, ''); ide.append(dict(t=S6_END, op='clear'))
chip(S6_END + .1, S6_END + 3.6, '<span>🐞</span><div>Хатогиҳои маъмул<small>05 · ҳама хато мекунанд — ин муқаррарӣ аст</small></div>', 'card')
e1 = T('Якум: конст-ро'); chip(e1, e1 + 2.2, 'Хатои 1 / 3', 'side red', 'top:70px;left:1120px')
zoom(e1 + .3, S7_END - .2, 480, 345, 1.3)
e1w = T('Менависем конст пай'); typ(e1w, 'const pi = 3.14;\npi = 3;\nconsole.log(pi);', 4.0)
e1x = T('Хато: «Эсайнмент'); run(e1x - .4, 'bad'); ring(e1x + .2, T('Ҳал: лет') - .1, '#out .l.e', 'TypeError: const иваз намешавад', 'r', 4)
e1f = T('Ҳал: лет'); typ(e1f, 'let pi = 3.14;\npi = 3;\nconsole.log(pi);', 1.2); mark(e1f + 1.2, e1f + 3.5, 0, 0, 3, '✅ let', 'g')
run(e1f + 1.9); ring(e1f + 2.4, T('Дуюм: ном бо') - .1, '#out', 'кор кард: 3', 'g', 2)
e2 = T('Дуюм: ном бо'); chip(e2, e2 + 2.2, 'Хатои 2 / 3', 'side red', 'top:70px;left:1120px')
typ(e2 + .3, 'let 2age = 25;\nconsole.log(2age);', 2.6)
e2x = T('лет ду эйдж'); run(e2x + .3, 'bad'); mark(e2x + .8, T('Номро бо ҳарф') - .1, 0, 4, 8, '✕ ном бо рақам оғоз намешавад', 'r', 'below')
e2f = T('Номро бо ҳарф'); typ(e2f + .4, 'let age2 = 25;\nconsole.log(2age);', .9); typ(e2f + 1.4, 'let age2 = 25;\nconsole.log(age2);', .8); run(e2f + 2.6)
mark(e2f + 2.3, T('Саввум: лет-ро') - .1, 0, 4, 8, '✅ age2', 'g', 'below')
e3 = T('Саввум: лет-ро'); chip(e3, e3 + 2.2, 'Хатои 3 / 3', 'side red', 'top:70px;left:1120px')
e3w = T('лет эй баробари як,'); typ(e3w, 'let a = 1;\nlet a = 2;\nconsole.log(a);', 3.4)
e3x = T('Хато: «Айдентифаер'); run(e3x - .4, 'bad'); ring(e3x + .2, T('Дубора лет лозим') - .1, '#out .l.e', 'SyntaxError: ин ном аллакай ҳаст', 'r', 4)
e3f = T('Дубора лет лозим'); typ(e3f + .2, 'let a = 1;\na = 2;\nconsole.log(a);', 1.0); mark(e3f + 1.2, e3f + 3.6, 1, 0, 1, '✅ бе let', 'g', 'below')
t_hint = T('Хуб аст, ки ай-ди-и'); ring(t_hint + .3, T('дар кадом сатр') - .1, '#out .hint', '💡 шарҳ ба тоҷикӣ', 'y', 4)
ring(T('дар кадом сатр'), S7_END - .2, '#out .l.e', '📍 рақами сатр', 'c', 4)
run(S7_END - 1.0)

# --- 6. Вазифаҳо ---
t_tab = T('ҷадвали «як,'); t_tk1 = T('Якум: тағйирёбандаи'); t_tk2 = T('Дуюм: тағйирёбандаи'); t_chk = T('Баъд тугмаи'); t_hlp = T('тугмаи «Кӯмак»'); t_pz = T('Видеоро пауза кунед')
S8_END = T('Хулоса мекунем.')
S('ide', S7_END, S8_END)
chip(S7_END + .1, S7_END + 2.6, '<span>🎯</span><div>Вазифаҳо барои шумо<small>06 · дар IDE, ҷадвали «1 · Тағйирёбанда»</small></div>', 'card')
ptr.append(dict(t=t_tab - .2, sel=None))
click(t_tab + .6, '#tabs .tab:nth-child(2)'); setc(t_tab + .62, '// Тағйирёбандаи age-ро созед ва ба 26 иваз кунед\n')
ring(t_tab + 1.0, t_tk1 - .2, '#tabs .tab:nth-child(2)', '', 'y', 4)
ring(t_tk1, t_tk2 - .2, '#task', 'Вазифаи 1', 'y', 4)
click(t_tk2 + .2, '#side button[data-i="1"]'); setc(t_tk2 + .22, '// Тағйирёбандаи name-ро созед\n'); ring(t_tk2 + .7, t_chk - .2, '#task', 'Вазифаи 2', 'y', 4)
ring(t_chk, t_hlp - .2, '#check', '✓ Санҷиш', 'c', 6); ptr.append(dict(t=t_chk + .3, sel='#check'))
ring(t_hlp, t_pz - .2, '#hintb', '💡 Кӯмак', 'y', 6); ptr.append(dict(t=t_hlp + .3, sel='#hintb'))
g1 = V(GAP_PAUSE) - 13.0
cd0 = g1 + .4
chip(t_pz, cd0 - .05, '<span class="big">⏸</span><div>Видеоро пауза кунед<small>ва худатон кӯшиш кунед ✍️</small></div>', 'card')
for k in range(5):
    chip(cd0 + k, cd0 + k + .9, f'<span class="big">{5 - k}</span><div>Пауза кунед ва кӯшиш кунед<small>баъд ҷавобро мебинем ✅</small></div>', 'card')
    sfx.append(dict(name='tick', t=cd0 + k, gain=.8))
click(g1 + 5.6, '#side button[data-i="0"]'); zoom(g1 + 6.0, S8_END, 300, 300, 1.3)
chip(g1 + 5.8, g1 + 7.6, '✅ Ҷавоби вазифаи 1', 'side grn', 'top:80px')
setc(g1 + 6.2, '// Тағйирёбандаи age-ро созед ва ба 26 иваз кунед\n')
typ(g1 + 6.4, '// Тағйирёбандаи age-ро созед ва ба 26 иваз кунед\nlet age = 25;\nage = 26;\nconsole.log(age);', 2.8)
run(g1 + 9.6); click(g1 + 10.6, '#check', 'check'); sfx.append(dict(name='chime', t=g1 + 10.9, gain=.6))
ring(g1 + 11.0, S8_END - .2, '#checks', '🎉 Офарин!', 'g', 4)

# --- 7. Хулоса ---
x1 = T('Тағйирёбанда — қуттӣ бо ном', I('Хулоса мекунем.')); x2 = T('Се навъи асосӣ:'); x3 = T('лет — барои')
x_pdf = T('Шпаргалкаи бепул'); x_cm = T('дар шарҳи ролик'); x_next = T('Дарси оянда'); x_sub = T('обуна шавед'); x_sh = T('пайвандро ба дӯсте'); x_bye = T('То дидори нав!')
slides.append(f'''<section class="scene" id="s-sum">
<div class="kicker" {A('down', S8_END + .2)}><b>07</b>ХУЛОСА</div>
<div style="left:56px;top:110px" class="card3" {A('up', x1)}><div class="emo">📦</div><div class="t">Тағйирёбанда</div><div class="u" style="font-size:22px">ном + қимат<br>қиматро иваз кардан мумкин</div><div class="codechip" style="font-size:20px"><span class="k">let</span> age = <span class="n">26</span>;</div></div>
<div style="left:470px;top:110px" class="card3" {A('up', x2)}><div class="emo">🧩</div><div class="t">Се навъ</div><div class="u" style="font-size:22px">рақам · матн · ҳа/не</div><div class="codechip" style="font-size:20px"><span class="n">26</span> <span class="s">"Салом"</span> <span class="k">true</span></div></div>
<div style="left:884px;top:110px" class="card3" {A('up', x3)}><div class="emo">🔒</div><div class="t">let ва const</div><div class="u" style="font-size:22px">let — иваз мешавад<br>const — доимист</div><div class="codechip" style="font-size:20px"><span class="k">const</span> pi = <span class="n">3.14</span>;</div></div>
<div style="left:56px;top:460px;display:flex;gap:14px;align-items:center" {A('up', x_pdf)}><span class="pill gold">📘 Шпаргалкаи бепул (PDF)</span><span class="pill">дар тавсиф ё Instagram</span></div>
<div style="left:56px;top:530px;display:flex;gap:14px;align-items:center" {A('up', x_cm)}><span class="pill ink">💬 Шарҳ: <b style="color:var(--gold)" data-tw="{x_cm + .5};1.0" data-text="РӮЙХАТ"></b></span><span class="pill">@shahriyor_yunusov</span></div>
</section>
<section class="scene" id="s-next">
<div class="kicker" {A('down', x_next + .1)}><b>ДАРСИ 2</b>НАВБАТӢ</div>
<div class="h1" style="left:56px;top:110px;font-size:68px" {A('up', x_next + .3)}>Шарт: <span class="mono" style="color:var(--rust)">if / else</span></div>
<div class="sub" style="left:60px;top:200px;font-size:28px" {A('up', x_next + .8)}>чӣ тавр барнома қарор қабул мекунад 🚦</div>
<div class="codechip" style="left:60px;top:270px;font-size:24px;line-height:1.5" {A('up', x_next + 1.4)}><span class="k">if</span> (age &gt;= <span class="n">18</span>) {{<br>&nbsp;&nbsp;<span class="f">console.log</span>(<span class="s">"Хуш омадед!"</span>);<br>}} <span class="k">else</span> {{ … }}</div>
<div style="left:800px;top:260px" {A('pop', x_sub)}><span class="pill rust" style="font-size:30px;padding:18px 34px">🔔 Обуна шавед</span></div>
<div style="left:800px;top:350px" {A('pop', x_sh)}><span class="pill" style="font-size:26px;padding:16px 30px">📤 Ба дӯст фиристед</span></div>
<div class="h1" style="left:56px;top:480px;font-size:64px" {A('stamp', x_bye)}>То дидори нав! 👋</div>
</section>''')
S('s-sum', S8_END, x_next); S('s-next', x_next, END + 1)

chapters = [dict(t=0, title='Хук'), dict(t=S1_END, title='Тағйирёбанда чист?'), dict(t=S2_END, title='Аввалин код дар IDE'),
            dict(t=S3_END, title='Се навъи қимат'), dict(t=S5_END, title='let ва const'), dict(t=S6_END, title='Хатогиҳои маъмул'),
            dict(t=S7_END, title='Вазифаҳо'), dict(t=S8_END, title='Хулоса')]
ide.sort(key=lambda o: o['t']); ptr.sort(key=lambda o: o['t'])
TL = dict(end=END, scenes=scenes, ide=ide, marks=marks, rings=rings, ptr=ptr, chips=chips, zooms=zooms, caps=caps, chapters=chapters, cd=[cd0])

# ---------- страница ----------
src = open('../../games/ide/index.html', encoding='utf8').read()
PTR = '<svg id="ptr" viewBox="0 0 24 24"><path d="M3 2l7.5 19 2.6-7.6L21 11z" fill="#fff" stroke="#111" stroke-width="1.4" stroke-linejoin="round"/></svg>'
inject_head = '<style>' + open('video.css', encoding='utf8').read() + '</style>'
inject_body = ('<div id="ovl">' + PTR + '<div id="rip"></div></div>' + ''.join(slides) +
               '<div id="band"><div id="chap"></div><div id="cap"></div><div id="prog"></div></div>')
src = src.replace('</head>', inject_head + '</head>', 1)
src = src.replace('<div class="app">', inject_body + '<div id="stagewrap"><div class="app">', 1)
src = src.replace('\n<script>\n(function () {', '\n</div>\n<script>\n(function () {', 1)
src = src.replace('</body>', '<script>window.TL=' + json.dumps(TL, ensure_ascii=False) + ';</script><script>' + open('video.js', encoding='utf8').read() + '</script></body>', 1)
open('video.html', 'w', encoding='utf8').write(src)

# countdown hook: число в чипе паузы
# ---------- sfx / srt / главы ----------
sfx = [s for s in sfx if 0 <= s['t'] < END]
json.dump(dict(end=END, sfx=sorted(sfx, key=lambda s: s['t'])), open('sfx.json', 'w'), indent=0)
json.dump(dict(gaps=GAPS, end=END), open('gaps.json', 'w'))
def ts(t): h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60; return f'{h:02}:{m:02}:{int(s):02},{int(round((s % 1) * 1000)) % 1000:03}'
with open('../youtube-lesson-1.srt', 'w', encoding='utf8') as f:
    for k, c in enumerate(caps, 1): f.write(f"{k}\n{ts(c['t0'])} --> {ts(c['t1'])}\n{c['text']}\n\n")
with open('chapters.txt', 'w', encoding='utf8') as f:
    for c in chapters: f.write(f"{int(c['t'] // 60)}:{int(c['t'] % 60):02} {c['title']}\n")
print('END', END, 'scenes', len(scenes), 'ide ops', len(ide), 'sfx', len(sfx))
print(open('chapters.txt').read())
