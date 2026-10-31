# Собирает video.html (IDE + слайды + таймлайн), sfx.json, .srt (для загрузки на YouTube, в видео субтитров НЕТ) и главы для YouTube-урока 2 «Шарт».
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

# паузы без голоса (время повествования -> длительность вставки)
GAPS = []
def V(nt): return nt + sum(d for g, d in GAPS if g <= nt)
def T(phrase, after=0, end=False, off=0.0):
    i = find(phrase, after); n = len(phrase.split())
    return round(V(W[i + n - 1]['t1'] if end else W[i]['t0']) + off, 3)
def I(phrase, after=0): return find(phrase, after)

PAUSE = 5.0
GAP_Q = W[I('фикр кунед.', I('Ва ҳамон')) + 1]['t1'] + 0.05; GAPS.append((GAP_Q, PAUSE))
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
def run(t, kind='ok'):
    ptr.append(dict(t=t, sel='#run')); ide.append(dict(t=t, op='run', sel='#run'))
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
def box(val, ta=0, tl=0, tv=0, o=None, label='age', ok='flyout', zoomv=1):
    return (f'<div class="box" style="position:relative;zoom:{zoomv}" {A("pop", ta)}><div class="back"></div>'
            f'<div class="num" {A("drop", tv, o, ok)}>{val}</div><div class="front"><div class="tag" {A("stamp", tl)}>{label}</div></div></div>')

# ключевые моменты
S1_END = T('Аз хона мебароед.')
S2_END = T('Ба ай-ди-и')
S3_END = T('Барои савол додан')
S4_END = T('Шарт дар ҳама ҷо')
S5_END = T('Гоҳо ду роҳ')
S6_END = T('Се хатои маъмули')
S7_END = T('Акнун вазифа')
S8_END = T('Хулоса мекунем.')
X_NEXT = T('Дарси оянда')

# --- 0. Хук ---
h_dec = T('қарор қабул'); h_rain = T('борон борад'); h_price = T('нарх қимат'); h_prog = T('Ҳар барнома'); h_vid = T('Дар ин видео'); h_quiz = T('санҷиши ҷиддӣ')
slides.append(f'''<section class="scene" id="s-hook">
<div class="kicker" {A('down', .2)}><b>ДАРСИ 2</b>БАРНОМАСОЗӢ АЗ СИФР · JAVASCRIPT</div>
<div class="h1" style="left:60px;top:110px;font-size:150px" {A('stamp', .6)}>ШАРТ</div>
<div class="mono acc" style="left:66px;top:290px;font-size:60px;font-weight:800" {A('up', h_dec - .4)}>if / else</div>
<div class="sub" style="left:68px;top:370px" {A('up', h_dec + .2)}>чӣ тавр компютер қарор қабул мекунад</div>
<div style="left:68px;top:440px" {A('left', h_rain)}><span class="pill">☔ борон борад → чатр мегирем</span></div>
<div style="left:68px;top:508px" {A('left', h_price)}><span class="pill">🏷️ нарх қимат бошад → намехарем</span></div>
<div style="left:68px;top:576px" {A('left', h_prog)}><span class="pill">🤖 барнома ҳам ҳамин тавр кор мекунад</span></div>
<div style="left:880px;top:130px">{box('15', .4, .6, 1.0, label='age', zoomv=1.25)}</div>
<div class="node" style="left:860px;top:520px;width:340px" {A('pop', h_vid)}>Хуш омадед?<small>ҳа ✓ &nbsp;·&nbsp; не ✗</small></div>
<div style="left:850px;top:640px" {A('pop', h_quiz)}><span class="pill accent">🎯 Дар охир: санҷиши ҷиддӣ</span></div>
</section>''')
S('s-hook', 0, S1_END)

# --- 1. Образи субҳ ---
m_door = S1_END; m_if = T('Агар борон борад'); m_else = T('Вагарна', m_if); m_sh = T('Ана ҳамин шарт'); m_q = T('Шарт — ин савол')
m_sav = T('Савол:'); m_br = T('борон меборад?'); m_yn = T('Агар ҳа'); m_kw = T('Дар барномасозӣ ду калима'); m_if_w = T('иф', I('Дар барномасозӣ ду калима')); m_else_w = T('элс', I('Дар барномасозӣ ду калима'))
m_fin = T('Ҳамааш ҳамин')
slides.append(f'''<section class="scene" id="s-morn">
<div class="kicker" {A('down', m_door)}><b>01</b>ШАРТ ЧИСТ?</div>
<div class="node" style="left:420px;top:90px;width:440px" {A('up', m_door + .3)}><span style="font-size:44px">🚪</span> Аз хона мебароед</div>
<div class="node" style="left:420px;top:230px;width:440px;border-color:var(--purple);box-shadow:0 0 0 4px rgba(189,147,249,.16),0 0 30px rgba(189,147,249,.25)" {A('pop', m_if - .1)}>❓ Борон меборад?</div>
<svg style="left:0;top:0;width:1280px;height:720px" viewBox="0 0 1280 720" fill="none">
 <path d="M640 312 C640 380 330 360 330 424" stroke="#4EC9B0" stroke-width="4" stroke-linecap="round" {A('fade', m_if + .4)}/>
 <path d="M640 312 C640 380 950 360 950 424" stroke="#F48771" stroke-width="4" stroke-linecap="round" {A('fade', m_else)}/>
</svg>
<div style="left:395px;top:343px" {A('pop', m_yn)}><span class="pill ok">ҳа ✓</span></div>
<div style="left:870px;top:343px" {A('pop', m_yn + .5)}><span class="pill err">не ✗</span></div>
<div class="node yes" style="left:130px;top:430px;width:400px" {A('up', m_if + .5)}><span class="big">🌧️ → ☂️</span>Чатр мегирам</div>
<div class="node no" style="left:750px;top:430px;width:400px" {A('up', m_else + .2)}><span class="big">☀️ → 🕶️</span>Айнаки офтобӣ</div>
<div style="left:130px;top:600px" {A('pop', m_if_w)}><span class="codechip"><span class="k">if</span> = агар</span></div>
<div style="left:750px;top:600px" {A('pop', m_else_w)}><span class="codechip"><span class="k">else</span> = вагарна</span></div>
<div style="left:410px;top:640px" {A('pop', m_q)}><span class="pill accent" style="font-size:24px">Шарт = савол + ду роҳ</span></div>
</section>''')
S('s-morn', S1_END, S2_END)

# --- 2. Аввалин шарт дар IDE ---
S('ide', S2_END, S3_END)
setc(S2_END, ''); clear(S2_END)
chip(S2_END + .1, S2_END + 2.3, '<span>💻</span><div>Аввалин шарт дар IDE<small>02 · ҳамроҳи ман нависед</small></div>', 'card')
t_link = T('Пайванд дар тавсиф')
chip(t_link, t_link + 3.8, '🔗 yunusovshahriyor.github.io/yunusov.tj/ide', 'side yel', 'top:90px')
t_w = T('лет эйдж баробари', I('Менависем:'))
C0 = 'let age = 25;'
C1 = C0 + '\n\nif (age >= 18) {\n}'
C2 = C0 + '\n\nif (age >= 18) {\n  console.log("Хуш омадед!");\n}'
C3a = C2 + ' else {\n}'
C3 = C0 + '\n\nif (age >= 18) {\n  console.log("Хуш омадед!");\n} else {\n  console.log("Ҳанӯз барвақт");\n}'
t_if = T('иф,', I('Акнун шарт')); t_cl1 = T('консол лог,', t_if); t_els = T('Баъд элс'); t_cl2 = T('консол лог,', t_els)
t_run1 = T('Иҷро мекунем.')
zoom(t_w - .3, t_run1 - .3, 330, 250, 1.4)
typ(t_w, C0, 2.0)
mark(t_w + .3, t_w + 2.6, 0, 0, 13, '📦 қуттии age (аз дарси 1)', 'c')
typ(t_if - .1, C1, 2.4)
mark(T('калон ё баробари', t_if), T('Яъне синну сол') + 1.6, 2, 3, 14, '❓ савол', 'y')
typ(t_cl1, C2, 2.0)
typ(t_els, C3a, 1.2)
typ(t_cl2, C3, 2.2)
run(t_run1 + .7)
t_res = T('Натиҷа:')
ring(t_res + .2, T('Чаро?') - .1, '#out', '✅ Хуш омадед!', 'g', 2)
t_cmp = T('Компютер санҷид:'); t_cmpq = T('бисту панҷ аз ҳаждаҳ')
mark(t_cmpq, T('Ҳа.', t_cmpq) + .9, 2, 3, 14, '25 >= 18 → ҳа ✓', 'g', 'below')
t_15 = T('Ҳоло эйдж-ро'); t_else2_ = T('Компютер санҷид,', t_15)
zoom(t_15 - .4, T('Иҷро.', t_15) - .3, 330, 250, 1.4)
typ(t_15, C3.replace('25', '15'), 1.3)
run(T('Иҷро.', t_15) - .1)
ring(T('Иҷро.', t_15) + .5, t_else2_ - .1, '#out', '🙅 Ҳанӯз барвақт', 'r', 2)
t_else2 = T('Компютер санҷид,', t_15)
mark(t_else2 + 1.2, t_else2 + 4.4, 4, 2, 6, '→ роҳи else', 'c', 'below')
t_rule = T('дар қавс', I('Қоидаро дар хотир доред'))
mark(t_rule, t_rule + 2.4, 2, 3, 14, '❓ дар қавс — савол', 'y')
mark(T('дар қавси фигурӣ', t_rule), T('Барои савол додан') - .3, 3, 2, 29, '▶ дар { } — кор', 'g', 'below')

# --- 3. Аломатҳои муқоиса ---
o1 = T('Калон:'); o2 = T('Хурд:'); o3 = T('Калон ё баробар', o2); o4 = T('Хурд ё баробар'); o5 = T('Ва се баробарӣ')
o_att = T('Диққат ба фарқи'); o_age = T('Агар эйдж баробари ҳаждаҳ'); o_big = T('«калон»-и ҳаждаҳ'); o_geq = T('Аммо'); o_same = T('Барои ҳамин шарти'); o_tf = T('Ҷавоби ҳар муқоиса'); o_dec = T('Ҳамин ҷавоб қарорро')
ops = [('&gt;', 'аз 18 калон', 'age &gt; 18', 'false', o1, o_big, True), ('&lt;', 'аз 18 хурд', 'age &lt; 18', 'false', o2, o_same, False),
       ('&gt;=', 'калон ё баробар', 'age &gt;= 18', 'true', o3, o_geq, True), ('&lt;=', 'хурд ё баробар', 'age &lt;= 18', 'true', o4, o_same + .5, False),
       ('===', 'айнан баробар', 'age === 18', 'true', o5, o_same + 1.0, False)]
rows = ''
for k, (op, mean, ex, val, ta, tr, hit) in enumerate(ops):
    rows += (f'<div class="row" style="left:100px;top:{150 + 84 * k}px;width:1080px" {A("up", ta)}><span class="op">{op}</span><span class="mean">{mean}</span>'
             f'<span class="res" {A("pop", tr)}><span style="color:var(--muted)">{ex} →</span> <span class="{"t-ok" if val == "true" else "t-err"}">{val}</span></span></div>')
    if hit: rows += f'<div class="row hit" style="left:100px;top:{150 + 84 * k}px;width:1080px;background:transparent" {A("fade", tr + .1, o_tf - .2)}></div>'
slides.append(f'''<section class="scene" id="s-ops">
<div class="kicker" {A('down', S3_END + .2)}><b>03</b>АЛОМАТҲОИ МУҚОИСА</div>
<div class="h2" style="left:60px;top:70px;font-size:40px" {A('up', S3_END + .3)}>Панҷ аломат барои савол</div>
<div style="left:930px;top:62px" {A('pop', o_age)}><span class="pill accent">age = 18</span></div>
{rows}
<div style="left:100px;top:600px" {A('pop', o_tf)}><span class="pill">ҷавоб ҳамеша: <span class="t-ok mono">true</span> / <span class="t-err mono">false</span></span></div>
<div style="left:640px;top:600px" {A('pop', o_dec)}><span class="pill accent">→ ҳамин ҷавоб қарорро муайян мекунад</span></div>
</section>''')
S('s-ops', S3_END, S4_END)

# --- 4. Шарт дар ҳаёт ---
l_sv = T('Светофор'); l_g = T('мегузарем'); l_r = T('меистем'); l_pw = T('Парол дуруст'); l_ok = T('ворид мешавед'); l_bad = T('нодуруст бошад'); l_eq = T('Барои парол'); l_code = T('иф пасс')
slides.append(f'''<section class="scene" id="s-life">
<div class="kicker" {A('down', S4_END + .2)}><b>04</b>ШАРТ ДАР ҲАЁТ</div>
<div class="card3" style="left:70px;top:110px;width:540px;height:400px" {A('up', S4_END + .5)}>
 <div class="emo">🚦</div><div class="t">Светофор</div>
 <div class="node yes" style="margin-top:14px;text-align:left" {A('left', l_sv + .4)}>🟢 сабз бошад<small>→ мегузарем</small></div>
 <div class="node no" style="margin-top:6px;text-align:left" {A('left', l_g + .2)}>🔴 вагарна<small>→ меистем</small></div>
</div>
<div class="card3" style="left:670px;top:110px;width:540px;height:400px" {A('up', l_pw - .4)}>
 <div class="emo">🔐</div><div class="t">Парол</div>
 <div class="node yes" style="margin-top:14px;text-align:left" {A('left', l_pw + .4)}>✓ дуруст бошад<small>→ ворид мешавед</small></div>
 <div class="node no" style="margin-top:6px;text-align:left" {A('left', l_bad)}>✗ нодуруст бошад<small>→ хато</small></div>
</div>
<div style="left:670px;top:610px" {A('pop', l_code)}><span class="codechip" style="font-size:28px"><span class="k">if</span> (pass <span class="e">===</span> <span class="s">"1234"</span>) {{ … }}</span></div>
</section>''')
S('s-life', S4_END, S5_END)

# --- 5. else if в IDE ---
S('ide', S5_END, S8_END)
setc(S5_END, ''); clear(S5_END)
chip(S5_END + .1, S5_END + 1.7, '<span>🌡️</span><div>Бисёр роҳ: else if<small>05 · ҳарорат</small></div>', 'card')
EI0 = 'let temperature = 20;'
EI1 = EI0 + '\n\nif (temperature > 30) {\n  console.log("Гарм");\n}'
EI2 = EI1 + ' else if (temperature > 15) {\n  console.log("Мӯътадил");\n}'
EI3 = EI2 + ' else {\n  console.log("Хунук");\n}'
ei_t = T('Масалан, ҳарорат.'); ei_g = T('Агар аз сӣ'); ei_m = T('Вагарна агар'); ei_h = T('Вагарна', I('Вагарна агар') + 1); ei_c = T('Дар код:'); ei_f = T('Роҳҳо аз боло')
zoom(ei_t - .2, ei_f, 330, 270, 1.3)
typ(ei_t + .1, EI0, 1.8)
typ(ei_g - .2, EI1, 2.2)
typ(ei_m - .2, EI2, 2.4)
typ(ei_h - .2, EI3, 1.8)
t_a = T('иф,', ei_c); t_b = T('элс иф,', ei_c); t_c = T('элс.', t_b + .3)
mark(t_a, t_a + 1.5, 2, 0, 2, '1 · if', 'y')
mark(t_b, t_b + 1.7, 4, 2, 9, '2 · else if', 'c')
mark(t_c, t_c + 1.5, 6, 2, 6, '3 · else', 'g')
run(ei_f + 1.0)
ring(ei_f + 1.6, S6_END - .2, '#out', '20 > 30? не · 20 > 15? ҳа → Мӯътадил', 'g', 2)

# --- 6. Хатогиҳо ---
setc(S6_END, ''); clear(S6_END)
chip(S6_END + .1, S6_END + 2.0, '<span>🐞</span><div>Се хатои маъмул<small>06 · ҳама хато мекунанд — ин муқаррарӣ аст</small></div>', 'card')
e1 = T('Якум:', I('Се хатои маъмули')); e1w = T('Агар нависед'); e1x = T('Компютер ба эйдж'); e1f = T('Барои савол', e1x); e1g = T('Як баробарӣ', e1f)
e2 = T('Дуюм:', e1g); e2w = T('Панҷ ва'); e2n = T('дар нохунак'); e2x = T('ин ҳамон нест'); e2g = T('Дарси гузашта дидем')
e3 = T('Саввум:', e2g); e3w = T('фаромӯш кардани'); e3x = T('Ай-ди-и хаторо'); e3r = T('Ҳамеша аввал')
chip(e1 + .1, e1 + 2.3, 'Хатои 1 / 3', 'side red', 'top:70px;left:1090px')
zoom(e1w - .3, e1x - .2, 330, 250, 1.35)
E1 = 'let age = 15;\nif (age = 18) {\n  console.log("Хуш омадед!");\n} else {\n  console.log("Ҳанӯз барвақт");\n}'
typ(e1w, E1, 4.2)
mark(T('як аломат'), T('ин «гузор»') + .4, 1, 8, 9, '⚠️ як баробарӣ = «гузор»', 'r')
run(e1x - .1, 'bad')
ring(e1x + .6, e1f - .1, '#out', '🤯 age = 15, аммо «Хуш омадед!»', 'r', 2)
typ(e1f + .2, E1.replace('age = 18', 'age === 18'), .9)
mark(e1f + 1.1, e1f + 3.0, 1, 8, 11, '✅ се баробарӣ ===', 'g')
run(e1g - .2)
ring(e1g + .4, e2 - .2, '#out', '✅ 15 ≠ 18 → Ҳанӯз барвақт', 'g', 2)
chip(e2 + .1, e2 + 2.3, 'Хатои 2 / 3', 'side red', 'top:70px;left:1090px')
zoom(e2 + .8, e2x - .2, 330, 250, 1.35)
typ(e2 + .9, 'console.log(5 === "5");', 2.2)
mark(e2w, e2w + 1.0, 0, 12, 13, '🔢 рақам', 'c')
mark(e2n - .2, e2x - .2, 0, 18, 21, '🔤 матн', 'r')
run(e2x - .2)
ring(e2x + .5, e2g - .2, '#out', 'false: рақам ≠ матн', 'r', 2)
mark(e2g + 1.4, e3 - .3, 0, 18, 21, 'нохунак — навъро иваз мекунад', 'y', 'below')
chip(e3 + .1, e3 + 2.3, 'Хатои 3 / 3', 'side red', 'top:70px;left:1090px')
E3 = 'let age = 15;\nif (age >= 18) {\n  console.log("Хуш омадед!");\n'
typ(e3w - .2, E3, 3.0)
run(e3x - .5, 'bad')
ring(e3x + .2, T('сатрро нишон медиҳад') + .2, '#out .hint', '💡 шарҳ ба тоҷикӣ', 'y', 4)
ring(T('сатрро нишон медиҳад'), e3r - .1, '#out .l.e', '📍 рақами сатр', 'c', 4)
ring(e3r, S7_END - .3, '#out', '📖 аввал хабарро хонед', 'c', 2)
typ(S7_END - 1.9, E3 + '}', .6)

# --- 7. Вазифаҳо ---
t_tab = T('ҷадвали', S7_END); t_two = T('Ду вазифа ҳаст'); t_tk1 = T('Якум:', S7_END); t_tk1w = T('Агар температура'); t_tk2 = T('Дуюм:', t_tk1); t_tk2w = T('Агар эйдж калон', t_tk2); t_chk = T('Ай-ди-и бо якчанд')
t_quiz = T('Ва ҳамон санҷиши'); t_age15 = T('эйдж баробари понздаҳ'); t_what = T('Барнома чӣ мегӯяд'); t_pz = T('Видеоро пауза кунед')
t_ans = T('Ҷавоб:', I('Видеоро пауза кунед')); t_late = T('«Ҳанӯз барвақт»', t_ans); t_less = T('Понздаҳ аз ҳаждаҳ'); t_to = T('барнома ба элс')
chip(S7_END + .1, S7_END + 2.1, '<span>🎯</span><div>Вазифаҳо барои шумо<small>07 · дар IDE, ҷадвали «2 · Шарт»</small></div>', 'card')
click(t_tab + .8, '#tabs .tab:nth-child(3)')
ST1 = 'let temperature = 34;\n\n// if / else нависед\n'; ST2 = 'let age = 15;\n\n// if / else нависед\n'
setc(t_tab + .82, ST1)
ring(t_tab + 1.3, t_two - .2, '#tabs .tab:nth-child(3)', '', 'y', 4)
ring(t_two, t_tk1 - .2, '#side', '📘 назария', 'c', 4)
ring(t_tk1, t_tk2 - .1, '#task', 'Вазифаи 1', 'y', 4)
SOL1 = 'let temperature = 34;\n\nif (temperature > 30) {\n  console.log("Гарм аст");\n} else {\n  console.log("Хунук аст");\n}\n'
typ(t_tk1w, SOL1, 5.0)
click(t_tk2 + .3, '#side button[data-i="1"]'); setc(t_tk2 + .32, ST2)
ring(t_tk2 + .8, t_tk2w - .1, '#task', 'Вазифаи 2', 'y', 4)
SOL2 = 'let age = 15;\n\nif (age >= 18) {\n  console.log("Хуш омадед!");\n} else {\n  console.log("Ҳанӯз барвақт");\n}\n'
typ(t_tk2w + .1, SOL2, 5.5)
ring(t_chk - .3, t_chk + .9, '#check', '✓ Санҷиш', 'c', 6)
click(t_chk + .5, '#check', 'check'); sfx.append(dict(name='chime', t=t_chk + .9, gain=.6))
ring(t_chk + 1.0, t_quiz - .2, '#checks', '', 'g', 4)
mark(t_age15, t_what, 0, 4, 12, 'age = 15', 'y')
# пауза: обратный отсчёт 5…1 (голоса нет)
g0 = V(GAP_Q) - PAUSE
chip(t_what, g0 - .3, '<span class="big">❓</span><div>Барнома чӣ мегӯяд?<small>age = 15 · видеоро пауза кунед ✍️</small></div>', 'card')
for k in range(5):
    chip(g0 + k + .02, g0 + k + .62, f'<span class="big">{5 - k}</span><div>Барнома чӣ мегӯяд?<small>фикр кунед · баъд ҷавобро мебинем ✅</small></div>', 'card')
    sfx.append(dict(name='tick', t=g0 + k, gain=.8))
run(t_ans - .3)
ring(t_late - .1, S8_END - .3, '#out', '✅ Ҳанӯз барвақт', 'g', 2)
mark(t_less, t_to - .1, 2, 4, 14, '15 >= 18 → не ✗', 'r', 'below')
mark(t_to, t_to + 2.6, 4, 2, 6, '→ else', 'c', 'below')

# --- 8. Хулоса ---
x1 = T('Шарт — савол ва ду роҳ'); x2 = T('Иф — агар'); x3 = T('Барои савол — аломатҳои'); x_pdf = T('Шпаргалкаи бепул')
slides.append(f'''<section class="scene" id="s-sum">
<div class="kicker" {A('down', S8_END + .2)}><b>08</b>ХУЛОСА</div>
<div class="card3" style="left:60px;top:110px;width:360px;height:340px" {A('up', x1)}><div class="emo">🔀</div><div class="t">Шарт</div><div class="u">савол + ду роҳ</div>
 <div class="codechip" style="font-size:20px;line-height:1.5"><span class="k">if</span> (<span class="n">…</span>) {{ … }}<br><span class="k">else</span> {{ … }}</div></div>
<div class="card3" style="left:460px;top:110px;width:360px;height:340px" {A('up', x2)}><div class="emo">🔗</div><div class="t">if · else if · else</div><div class="u">агар · вагарна агар · вагарна<br>роҳҳо аз боло ба поён</div>
 <div class="codechip" style="font-size:20px;line-height:1.5"><span class="k">if</span> … <span class="k">else if</span> … <span class="k">else</span> …</div></div>
<div class="card3" style="left:860px;top:110px;width:360px;height:340px" {A('up', x3)}><div class="emo">⚖️</div><div class="t">Муқоиса</div><div class="u">&gt; &lt; &gt;= &lt;= ===<br>баробарӣ — се баробарӣ</div>
 <div class="codechip" style="font-size:20px;line-height:1.7"><span class="t-ok">age === 18</span> ✓<br><span class="e">age = 18</span> ✗</div></div>
<div style="left:60px;top:560px" {A('up', x_pdf)}><span class="pill accent">📘 Шпаргалкаи бепул (PDF) — дар тавсифи видео</span></div>
</section>''')
S('s-sum', S8_END, X_NEXT)

x_sub = T('Обуна шавед')
slides.append(f'''<section class="scene" id="s-next">
<div class="kicker" {A('down', X_NEXT + .1)}><b>ДАРСИ 3</b>НАВБАТӢ</div>
<div class="h1" style="left:60px;top:130px;font-size:140px" {A('stamp', X_NEXT + .3)}>ДАВР</div>
<div class="mono acc" style="left:66px;top:300px;font-size:56px;font-weight:800" {A('up', X_NEXT + .8)}>loop</div>
<div class="sub" style="left:68px;top:380px" {A('up', X_NEXT + 1.2)}>як корро сад маротиба — бе такрор навиштан</div>
<div class="codechip" style="left:68px;top:460px;font-size:28px;line-height:1.5" {A('up', X_NEXT + 2.6)}><span class="k">for</span> (<span class="k">let</span> i = <span class="n">1</span>; i &lt;= <span class="n">100</span>; i++) {{<br>&nbsp;&nbsp;<span class="f">console.log</span>(i);<br>}}</div>
<div style="left:820px;top:170px" {A('pop', x_sub)}><span class="pill accent" style="font-size:34px;padding:20px 40px">🔔 Обуна шавед</span></div>
<div style="left:820px;top:270px" {A('pop', x_sub + .5)}><span class="pill" style="font-size:26px;padding:16px 30px">@shahriyor_yunusov</span></div>
</section>''')
S('s-next', X_NEXT, END + 1)

chapters = [dict(t=0, title='Хук'), dict(t=S1_END, title='Шарт чист?'), dict(t=S2_END, title='Аввалин шарт дар IDE'), dict(t=S3_END, title='Аломатҳои муқоиса'),
            dict(t=S4_END, title='Шарт дар ҳаёт ва else if'), dict(t=S6_END, title='Хатогиҳои маъмул'), dict(t=S7_END, title='Вазифаҳо'), dict(t=S8_END, title='Хулоса')]
ide.sort(key=lambda o: o['t']); ptr.sort(key=lambda o: o['t'])

# ---------- субтитры (.srt для YouTube; в самом видео субтитров НЕТ) ----------
MAP = [(r'ай-ди-и', 'IDE'), (r'консол лог', 'console.log'), (r'элс иф', 'else if'), (r'иф', 'if'), (r'элс', 'else'), (r'эйдж', 'age'), (r'лет', 'let'), (r'луп', 'loop'),
       (r'пасс', 'pass'), (r'тру', 'true'), (r'фолс', 'false'), (r'температура', 'temperature'), (r'бисту панҷ', '25'), (r'ҳаждаҳ', '18'), (r'понздаҳ', '15'), (r'сӣ', '30'),
       (r'як, ду, се, чор', '1234')]
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
with open('../youtube-lesson-2.srt', 'w', encoding='utf8') as f:
    for k, c in enumerate(caps, 1): f.write(f"{k}\n{ts(c['t0'])} --> {ts(c['t1'])}\n{c['text']}\n\n")
with open('chapters.txt', 'w', encoding='utf8') as f:
    for c in chapters: f.write(f"{int(c['t'] // 60)}:{int(c['t'] % 60):02} {c['title']}\n")
print('END', END, 'scenes', len(scenes), 'ide ops', len(ide), 'sfx', len(sfx))
print(open('chapters.txt').read())
