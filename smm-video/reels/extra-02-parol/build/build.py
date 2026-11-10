# words.json + cues.txt -> reel.html (сахнаҳо, субтитр, хати пешрафт) ва sfx.json.
import json, re, html
D = json.load(open('words.json')); W = D['words']; END = round(D['total'] + 0.4, 2)
norm = lambda s: re.sub(r'[^\w-]', '', s.replace('́', '')).lower()
toks = [norm(w['w']) for w in W]
def I(ph, after=0):
    q = [norm(x) for x in ph.split()]
    for i in range(after, len(W) - len(q) + 1):
        if toks[i:i + len(q)] == q: return i
    raise SystemExit('not found: ' + ph)
def T(ph, after=0, off=0.0): return round(W[I(ph, after)]['t0'] + off, 2)

# субтитрҳо
caps = []; i = 0
for ln in open('cues.txt', encoding='utf8'):
    ln = ln.strip()
    if not ln: continue
    ph, _, disp = ln.partition(' || '); disp = disp or ph; n = len(ph.split())
    assert [norm(x) for x in ph.split()] == toks[i:i + n], (ph, toks[i:i + n])
    caps.append(dict(t0=W[i]['t0'], t1=W[i + n - 1]['t1'], ws=[[W[k]['t0'], W[k]['t1']] for k in range(i, i + n)], text=disp)); i += n
assert i == len(W)
for a, b in zip(caps, caps[1:]): a['t1'] = min(a['t1'] + .3, b['t0'])

sfx = []
def A(kind, t, o=None, ok='fade'):
    if kind in ('pop', 'stamp', 'drop'): sfx.append(dict(name={'pop': 'pop', 'stamp': 'thud', 'drop': 'thud'}[kind], t=round(t + (.3 if kind == 'drop' else 0), 2), gain=.35))
    return f'data-a="{kind};{t}"' + (f' data-o="{o}" data-ok="{ok}"' if o is not None else '')
def TW(t, dur, text, cls=''):  # чопи ҳарф ба ҳарф
    n = max(1, len(text)); sfx.extend(dict(name='key', t=round(t + dur * k / n, 3), gain=.35) for k in range(0, n, 2))
    return f'<span class="{cls}" data-tw="{t};{dur}" data-text="{html.escape(text)}"></span>'

GRINDER = '''<svg class="grind" viewBox="0 0 220 170"><g fill="none" stroke="currentColor" stroke-width="4" stroke-linejoin="round" stroke-linecap="round">
<path d="M70 12 H150 L128 56 H92 Z"/><rect x="48" y="56" width="124" height="52" rx="14"/><path d="M172 66 h26 v32 h-26"/>
<path d="M198 70 v24" stroke-dasharray="3 5"/><path d="M48 82 H22"/><circle cx="16" cy="82" r="7"/><path d="M16 82 v-26"/>
<path d="M82 108 v40 h56 v-40"/><path d="M70 148 h80"/></g></svg>'''

sc = []; stages = []
def S(id, t0, t1, body, stage=None):
    sc.append(f'<section class="scene" id="{id}" data-t0="{t0}" data-t1="{t1}">{body}</section>')
    sfx.append(dict(name='whoosh', t=round(t0 - .12, 2), gain=.3))
    if stage: stages.append(dict(t=t0, label=stage))

# --- 0. Хук ---
t1 = T('Шумо дар сайт')
S('s0', 0, t1, f'''
<div class="form" style="left:70px;top:150px;width:400px" {A('pop', .2)}><div class="ft">🔐 Воридшавӣ</div>
<div class="fl">Логин</div><div class="fi">shahriyor</div><div class="fl">Пароль</div><div class="fi">••••</div><div class="fb">Ворид шудан</div></div>
<div class="tagn" style="left:200px;top:96px" {A('drop', .5)}>1234</div>
<div class="h1 c" style="top:470px" {A('up', .3)}>Пароли шумо<br><span class="acc">дар куҷо</span> нигоҳ дошта мешавад?</div>
<div class="q" style="left:390px;top:110px" {A('stamp', 1.4)}>?</div>''', 'ПАРОЛ')

# --- 1. ПАРОЛ ---
t_reg = T('Шумо дар сайт'); t_pw = T('ва пароли як,'); t_no = T('ҳеҷ ҷо'); t_dev = T('Ҳатто барномасози'); t2 = T('Ба ҷои пароль')
S('s1', t1, t2, f'''
<div class="form" style="left:70px;top:110px;width:400px" {A('up', t_reg, t_no - .3)}><div class="ft">📝 Сабти ном</div>
<div class="fl">Логин</div><div class="fi">shahriyor</div><div class="fl">Пароль</div><div class="fi">{TW(t_pw + .3, 1.3, '1234')}</div><div class="fb">Сабт шудан</div></div>
<div class="db" style="left:50px;top:150px;width:440px" {A('up', t_no - .2)}><div class="dt">🗄 DATABASE</div>
<div class="dr dh"><span>username</span><span>password</span></div><div class="dr"><span>shahriyor</span><span class="empty"></span></div></div>
<div class="stamp" style="left:300px;top:250px" {A('stamp', t_no + .2)}>НЕСТ</div>
<div class="pill" style="left:110px;top:420px" {A('pop', t_dev)}>👨‍💻 барномасоз ҳам намедонад</div>''')

# --- 2. ХЕШ ---
t_h = T('хеши онро нигоҳ'); t_g = T('Хеш — мисли'); t_meat = T('гӯштро қийма'); t_back = T('вале қиймаро'); t_sha = T('Ша-дусаду'); t_long = T('ва аз пароль ин'); t_add = T('Як рақам илова'); t_5 = T('як, ду, се, чор, панҷ'); t_diff = T('ва хеш тамоман'); t3 = T('Вақте шумо ворид')
S('s2', t2, t_sha - .2, f'''
<div class="gwrap" style="left:120px;top:150px" {A('pop', t2 + .2)}>{GRINDER}</div>
<div class="tagn" style="left:225px;top:96px" {A('drop', t_h, t_g + .4, 'down')}>1234</div>
<div class="hash" style="left:340px;top:305px" {A('right', t_g + .3)}>03ac6742…</div>
<div class="lbl" style="left:0;right:0;top:120px;text-align:center" {A('up', t_g)}>ХЕШ = <span class="acc">гӯштқимакунак</span></div>
<div class="row3" style="top:390px" {A('up', t_meat)}><span class="emo">🥩</span><span class="arr">→</span><span class="emo">⚙️</span><span class="arr">→</span><span class="mince">қийма</span></div>
<div class="row3" style="top:470px" {A('up', t_back)}><span class="mince">қийма</span><span class="arr">→</span><span class="emo">🥩</span><span class="x" {A('stamp', t_back + 1.0)}>✕</span></div>''', 'ХЕШ')
S('s2b', t_sha - .2, t3, f'''
<div class="term" style="left:30px;top:130px;width:480px" {A('pop', t_sha - .1)}><div class="tb"><i></i><i></i><i></i><span>node</span></div>
<pre>&gt; {TW(t_sha, 1.6, 'sha256("1234")', 'k')}
<span class="hashtxt" {A('fade', t_long)}>03ac674216f3e15c761ee1a5
e255f067953623c8b388b445
9e13f978d7c846f4</span>
&gt; {TW(t_add + .2, 1.6, 'sha256("12345")', 'k')}
<span class="hashtxt b" {A('fade', t_5 + .9)}>5994471abb01112afcc18159
f6cc74b4f511b99806da59b3
caf5a9c173cacfc5</span></pre></div>
<div class="cmp" style="top:520px" {A('pop', t_diff)}><span class="hash">03ac6742…</span><span class="neq">≠</span><span class="hash b">5994471a…</span></div>''')

# --- 3. ВОРИДШАВӢ ---
t_hash3 = T('сайт пароли навиштаатонро'); t_cmp = T('муқоиса мекунад.'); t_ok = T('Якхела —'); t4 = T('Аммо як мушкил')
S('s3', t3, t4, f'''
<div class="form sm" style="left:30px;top:110px;width:230px" {A('left', t3)}><div class="ft">🔐 Воридшавӣ</div><div class="fl">Пароль</div><div class="fi">{TW(t3 + .4, 1.0, '1234')}</div></div>
<div class="gwrap sm" style="left:300px;top:110px" {A('pop', t_hash3)}>{GRINDER}</div>
<div class="hash" style="left:60px;top:300px" {A('up', t_hash3 + 1.0)}>03ac6742…</div>
<div class="db" style="left:30px;top:370px;width:480px" {A('up', T('ва бо хеши дар'))}><div class="dt">🗄 DATABASE</div>
<div class="dr dh"><span>username</span><span>password_hash</span></div><div class="dr"><span>shahriyor</span><span class="hashc">03ac6742…</span></div></div>
<div class="eq" style="left:310px;top:300px" {A('stamp', t_cmp)}>= ✓</div>
<div class="ok" style="left:0;right:0;top:560px" {A('pop', t_ok)}>✅ Хуш омадед!</div>''', 'ВОРИДШАВӢ')

# --- 4. ХАКЕР ---
t_same = T('пароли якхела ҳамеша'); t_hk = T('Хакер хеши'); t_pre = T('пешакӣ ҳисоб'); t_srch = T('ва дар ба́заи'); t5 = T('Барои ҳамин ба')
S('s4', t4, t5, f'''
<div class="db" style="left:30px;top:100px;width:480px" {A('up', t4)}><div class="dt">🗄 DATABASE</div>
<div class="dr dh"><span>username</span><span>password_hash</span></div>
<div class="dr"><span>shahriyor</span><span class="hashc r" data-hl="{t_same}">03ac6742…</span></div>
<div class="dr"><span>nigina</span><span class="hashc">65e84be3…</span></div>
<div class="dr"><span>rustam</span><span class="hashc r" data-hl="{t_same}">03ac6742…</span></div>
<div class="dr"><span>madina</span><span class="hashc r" data-hl="{t_same}">03ac6742…</span></div></div>
<div class="hacker" style="left:390px;top:60px" {A('pop', t_hk)}>🕵️</div>
<div class="db red" style="left:30px;top:380px;width:480px" {A('up', t_pre)}><div class="dt">💀 ҶАДВАЛИ ТАЙЁРИ ХАКЕР</div>
<div class="dr" {A('left', T('як, ду, се, чор, кверти'))}><span>1234</span><span class="hashc">03ac6742…</span></div>
<div class="dr" {A('left', T('кверти,'))}><span>qwerty</span><span class="hashc">65e84be3…</span></div>
<div class="dr" {A('left', T('пасворд'))}><span>password</span><span class="hashc">5e884898…</span></div></div>
<div class="stamp red" style="left:195px;top:322px" {A('stamp', t_srch + .6)}>ЁФТ!</div>''', 'ХАКЕР')

# --- 5. SALT ---
t_s1 = T('солт илова мекунанд.'); t_rnd = T('Солт — ин'); t_same2 = T('Пароль якхела, солт'); t_alg = T('Ва алгоритмҳои'); t_yrs = T('кори хакерҳоро'); t6 = T('Сайти хуб')
S('s5', t5, t_alg - .1, f'''
<div class="shaker" style="left:200px;top:100px" {A('drop', t5 + .2)}>🧂<b>salt</b></div>
<div class="srow" style="top:270px" {A('left', t_rnd)}><span class="salt">8f3a</span><span>+</span><span class="tagn s">1234</span><span>→</span><span class="hash">03b60f85…</span><small>shahriyor</small></div>
<div class="srow" style="top:370px" {A('left', t_rnd + 1.2)}><span class="salt">c7d1</span><span>+</span><span class="tagn s">1234</span><span>→</span><span class="hash b">9e3f1b6b…</span><small>rustam</small></div>
<div class="lbl" style="left:0;right:0;top:480px;text-align:center" {A('pop', t_same2)}>пароль <span class="ok2">якхела</span> · хеш <span class="acc">гуногун</span></div>''', 'SALT')
S('s5b', t_alg - .1, t6, f'''
<div class="lbl" style="left:0;right:0;top:120px;text-align:center" {A('up', t_alg)}>Алгоритмҳои махсус</div>
<div class="algo" style="left:70px;top:200px" {A('pop', T('би-крипт'))}>bcrypt</div>
<div class="algo" style="left:290px;top:200px" {A('pop', T('аргон ду'))}>Argon2</div>
<div class="hourg" style="left:0;right:0;top:330px" {A('pop', t_yrs)}>⏳</div>
<div class="lbl" style="left:0;right:0;top:470px;text-align:center" {A('up', t_yrs + .5)}>хакер: <span class="acc">солҳо</span> кор</div>''')

# --- 6. Хулоса ---
t7 = T('Калимаи «ПАРОЛ»-ро')
S('s6', t6, t7, f'''
<div class="db" style="left:30px;top:130px;width:480px" {A('up', t6)}><div class="dt">🗄 DATABASE</div>
<div class="dr dh three"><span>username</span><span>salt</span><span>hash</span></div>
<div class="dr three"><span>shahriyor</span><span class="salt sm">8f3a</span><span class="hashc">03b60f85…</span></div>
<div class="dr three"><span>rustam</span><span class="salt sm">c7d1</span><span class="hashc">9e3f1b6b…</span></div></div>
<div class="nopw" style="left:150px;top:330px" {A('stamp', T('паролро намедонад'))}>password ✕</div>
<div class="h1 c" style="top:430px" {A('up', T('танҳо хеши онро'))}>Сайти хуб паролро <span class="acc">намедонад</span></div>''')

# --- 7. CTA ---
t_pdf = T('пе-де-эфи'); t_dm = T('ба Директ'); t_sub = T('Обуна шавед,')
S('s7', t7, END + 1, f'''
<div class="bubble" style="left:40px;top:110px" {A('pop', t7)}><span class="av">👤</span><div><small>шарҳ</small>{TW(T('«ПАРОЛ»-ро'), .7, 'ПАРОЛ', 'kw')}</div></div>
<img class="pdf" src="pdf-cover.png" style="left:150px;top:220px" {A('pop', t_pdf)}>
<div class="dm" style="left:0;right:0;top:600px" {A('up', t_dm)}>→ ба Direct 📩</div>
<div class="subbtn" style="left:0;right:0;top:680px" {A('pop', t_sub)}><span>🔔 Обуна шавед</span></div>''')

TL = dict(end=END, caps=caps, stages=stages)
page = open('reel.tpl.html', encoding='utf8').read().replace('<!--SCENES-->', ''.join(sc)).replace('/*TL*/', 'window.TL=' + json.dumps(TL, ensure_ascii=False) + ';')
open('reel.html', 'w', encoding='utf8').write(page)
sfx += [dict(name='ding', t=t_ok, gain=.5), dict(name='buzz', t=round(t_srch + .6, 2), gain=.3), dict(name='chime', t=t_same2, gain=.45), dict(name='chime', t=t7, gain=.45)]
json.dump(dict(end=END, sfx=sorted([s for s in sfx if 0 <= s['t'] < END], key=lambda s: s['t'])), open('sfx.json', 'w'))
print('END', END, 'scenes', len(sc), 'caps', len(caps), 'sfx', len(sfx))
