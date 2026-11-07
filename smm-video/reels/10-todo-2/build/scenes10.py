
def appcard(top, tasks, a, header="To-Do", cnt="", cls="pop"):
    rows = ""
    for t, done in tasks:
        ck = '<span class="ckb on">✓</span>' if done else '<span class="ckb"></span>'
        tx = f'<s style="color:#8B949E">{t}</s>' if done else t
        rows += f'<div class="rw">{ck}{tx}</div>'
    return (f'<div class="app {cls}" style="--a:{a:.2f}s;top:{top}px"><div class="tp"><b>{header}</b><span>{cnt}</span></div>{rows}</div>')

APP_CSS = '''<style>
.app{position:absolute;left:62px;right:62px;border-radius:26px;background:linear-gradient(160deg,#2a2a31,#202026);border:1.5px solid rgba(189,147,249,.55);box-shadow:0 0 60px rgba(189,147,249,.3),0 26px 50px rgba(0,0,0,.55);overflow:hidden}
.app .tp{padding:12px 18px;background:linear-gradient(90deg,#BD93F9,#FF79C6);color:#1E1E1E;display:flex;justify-content:space-between;align-items:center}
.app .tp b{font:900 20px 'Segoe UI Black','Segoe UI'}.app .tp span{font:800 13px 'Segoe UI'}
.app .rw{display:flex;align-items:center;gap:12px;padding:11px 18px;border-bottom:1px solid #3a3a42;font:700 19px 'Segoe UI';color:#fff}
.app .rw:last-child{border:0}
.ckb{width:24px;height:24px;border-radius:7px;border:2.5px solid #BD93F9;display:flex;align-items:center;justify-content:center;font-size:15px}
.ckb.on{background:#4EC9B0;border-color:#4EC9B0;color:#1E1E1E;font-weight:900}
.fnb{position:absolute;width:150px;padding:14px 8px;border-radius:18px;background:var(--panel);border:1px solid var(--line);text-align:center;box-shadow:0 12px 30px rgba(0,0,0,.45)}
.fnb .ic{font-size:34px}.fnb .nm{font:800 13px var(--mono);color:var(--par);margin-top:6px}
</style>'''
H.append(APP_CSS)

# ===== ХУК (0..T0) =====
p0 = PRE[0]
t_il = WT(0, "илова", 0, p0); t_ij = WT(0, "иҷро", 0, p0); t_fn = WT(0, "функсия", 0, p0); t_ch = WT(0, "чӣ", 0, p0)
scene(0, T[0] - 0.1, f'''
<div class="kicker" style="top:100px">ДАРСИ 10 · ЛОИҲА, ҚИСМИ 2</div>
{appcard(145, [("нон харидан", False), ("дарс хондан", False)], 0.2, cnt="0 / 2")}
<div class="fnb pop" style="--a:{t_il:.2f}s;left:28px;top:345px"><div class="ic">➕</div><div class="nm">addTask</div></div>
<div class="fnb pop" style="--a:{t_ij:.2f}s;left:195px;top:345px"><div class="ic">✅</div><div class="nm">completeTask</div></div>
<div class="fnb pop" style="--a:{t_fn:.2f}s;left:362px;top:345px"><div class="ic">📋</div><div class="nm">showTasks</div></div>
<div class="pill acc2 pop" style="--a:{t_ch:.2f}s;top:500px;font-size:22px;padding:11px 26px">Чӣ тавр? 🤔</div>''', whoosh=False)
sfx("hit", 0.0, 0.8); sfx("pop", 0.2, 0.6)
for t_ in (t_il, t_ij, t_fn): sfx("pop", t_, 0.8)
sfx("pop", t_ch, 0.8)

# ===== ЛОИҲА, ҚИСМИ 2 (T0..T1) =====
scene(T[0] - 0.1, T[1] - 0.1, f'''
<div class="slam acc" style="--a:{T[0]:.2f}s;top:210px;font-size:64px">ЛОИҲА</div>
<div class="slam" style="--a:{T[0] + 0.15:.2f}s;top:290px;font-size:46px;color:#fff">қисми дуюм</div>
<div class="emo pop" style="--a:{T[0] + 0.4:.2f}s;position:absolute;left:0;right:0;top:400px;text-align:center;font-size:84px">⚙️</div>''')
sfx("hit", T[0], 0.9); sfx("chime", T[0] + 0.4, 0.5)

# ===== ПУЛТ (T1..T3) =====
t_bl = WT(2, "баланд"); t_kh = WT(2, "хомӯш"); t_kn = WT(2, "каналро")
scene(T[1] - 0.1, T[3] - 0.1, f'''
<div class="kicker" style="top:120px">ПУЛТИ ТЕЛЕВИЗОР 📺</div>
<div class="abs pop" style="--a:{T[1]:.2f}s;left:175px;top:165px;width:190px;height:430px;border-radius:40px;background:linear-gradient(160deg,#34343A,#26262b);border:2px solid #4a4a52;box-shadow:0 26px 60px rgba(0,0,0,.6)"></div>
<div class="abs" style="left:240px;top:185px;width:60px;height:10px;border-radius:99px;background:#444"></div>
<div class="abs pop" style="--a:{t_bl:.2f}s;left:215px;top:225px;width:110px;height:76px;border-radius:38px;background:var(--accent);color:#1E1E1E;display:flex;align-items:center;justify-content:center;font:900 30px 'Segoe UI'">🔊 +</div>
<div class="abs pop" style="--a:{t_kh:.2f}s;left:215px;top:330px;width:110px;height:76px;border-radius:38px;background:#3a3a42;border:2px solid var(--purple);display:flex;align-items:center;justify-content:center;font-size:32px">🔇</div>
<div class="abs pop" style="--a:{t_kn:.2f}s;left:215px;top:435px;width:110px;height:76px;border-radius:38px;background:#3a3a42;border:2px solid var(--pink);display:flex;align-items:center;justify-content:center;font:900 26px 'Segoe UI'">📺 ↻</div>
<div class="pill pop" style="--a:{t_bl + 0.2:.2f}s;left:12px;translate:0 0;top:250px;font-size:15px;border-color:var(--purple);color:var(--purple)">баланд кардан</div>
<div class="pill pop" style="--a:{t_kh + 0.2:.2f}s;left:12px;translate:0 0;top:355px;font-size:15px;border-color:var(--purple);color:var(--purple)">хомӯш кардан</div>
<div class="pill pop" style="--a:{t_kn + 0.2:.2f}s;left:12px;translate:0 0;top:460px;font-size:15px;border-color:var(--pink);color:var(--pink)">иваз кардани канал</div>
<div class="pill acc2 pop" style="--a:{WT(1, 'пульти') + 0.5:.2f}s;top:620px;font-size:19px;padding:10px 24px">ҳар тугма — як амал</div>''')
sfx("pop", T[1], 0.6)
for t_ in (t_bl, t_kh, t_kn): sfx("pop", t_, 0.8); sfx("tick2", t_ + 0.05, 0.4)

# ===== ТУГМА = ФУНКСИЯ (T3..T6) =====
scene(T[3] - 0.1, T[6] - 0.1, f'''
<div class="kicker" style="top:110px">ДАР БАРНОМАИ МО ҲАМ ҲАМИН ТАВР</div>
<div class="h1 pop" style="--a:{T[4]:.2f}s;top:165px;font-size:40px">тугма = <span class="acc">функсия</span></div>
<div class="fnb pop" style="--a:{T[4] + 0.2:.2f}s;left:28px;top:290px"><div class="ic">➕</div><div class="nm">addTask()</div></div>
<div class="fnb pop" style="--a:{T[4] + 0.4:.2f}s;left:195px;top:290px"><div class="ic">✅</div><div class="nm">completeTask()</div></div>
<div class="fnb pop" style="--a:{T[4] + 0.6:.2f}s;left:362px;top:290px"><div class="ic">📋</div><div class="nm">showTasks()</div></div>
<div class="card pop" style="--a:{T[5]:.2f}s;left:50px;right:50px;top:450px;padding:12px 18px;font:700 16px var(--mono)"><span class="k">function</span> <span class="f">greet</span>(<span class="p">name</span>) {{ … }} <span class="cm">// дарси 5</span></div>
<div class="pill ok pop" style="--a:{T[5] + 0.3:.2f}s;top:535px;font-size:18px">ин ҳамон функсия аст ✓</div>''')
sfx("pop", T[4], 0.7)
for k in range(3): sfx("pop", T[4] + 0.2 + k * 0.2, 0.7)
sfx("pop", T[5], 0.6); sfx("ding", T[5] + 0.3, 0.5)

# ===== addTask (T6..T8) =====
a1 = K("function") + " " + F("addTask") + "(" + P("text") + ") {"
a2 = "  " + P("tasks") + "." + F("push") + "({ " + P("text") + ": " + P("text") + ", " + P("done") + ": " + K("false") + " });"
t_ry = WT(7, "рӯйхат")
scene(T[6] - 0.1, T[8] - 0.1, f'''
<div class="kicker" style="top:100px">1 · addTask ➕</div>
<div class="ide" style="top:135px"><div class="bar"><i></i><i></i><i></i><span>todo.js</span></div><div class="code" style="font-size:14px;padding-top:10px">
<div class="ln">{TYP(T[6] + 0.15, 1.0, a1, 'function addTask(text) {')}</div>
<div class="ln">{TYP(T[7] + 0.1, 2.4, a2, '  tasks.push({ text: text, done: false });')}</div>
<div class="ln">{TYP(T[7] + 2.55, 0.2, "}", "}")}</div></div></div>
<div class="pill pop" style="--a:{T[7] + 0.2:.2f}s;top:290px;font-size:17px;border-color:var(--kw);color:var(--kw)">push — аз дарси 4</div>
{appcard(350, [("нон харидан", False)], t_ry, cnt="1")}
<div class="pill ok pop" style="--a:{t_ry + 0.4:.2f}s;top:470px;font-size:18px">вазифаи нав илова шуд ✓</div>''')
sfx("pop", T[6] + 0.1, 0.5); sfx("pop", t_ry, 0.8); sfx("ding", t_ry + 0.4, 0.5)

# ===== completeTask (T8..T10) =====
c1 = K("function") + " " + F("completeTask") + "(" + P("i") + ") {"
c2 = "  " + P("tasks") + "[" + P("i") + "]." + P("done") + " = " + K("true") + ";"
t_tr = WT(9, "тру")
scene(T[8] - 0.1, T[10] - 0.1, f'''
<div class="kicker" style="top:100px">2 · completeTask ✅</div>
<div class="ide" style="top:135px"><div class="bar"><i></i><i></i><i></i><span>todo.js</span></div><div class="code" style="font-size:14px;padding-top:10px">
<div class="ln">{TYP(T[8] + 0.15, 1.1, c1, 'function completeTask(i) {')}</div>
<div class="ln">{TYP(T[9] + 0.1, 2.4, c2, '  tasks[i].done = true;')}</div>
<div class="ln">{TYP(T[9] + 2.6, 0.2, "}", "}")}</div></div></div>
{appcard(300, [("нон харидан", False)], T[9], cnt="0 / 1")}
{appcard(300, [("нон харидан", True)], t_tr + 0.1, cnt="1 / 1")}
<div class="pill pop" style="--a:{t_tr + 0.2:.2f}s;top:430px;font-size:17px;border-color:var(--ok);color:var(--ok)">done: false → true</div>''')
sfx("pop", T[9], 0.5); sfx("ding", t_tr + 0.1, 0.8); sfx("chime", t_tr + 0.2, 0.6)

# ===== showTasks (T10..T12) =====
s1 = K("function") + " " + F("showTasks") + "() {"
s2 = "  " + CT("for") + " (" + K("let") + " " + P("i") + " = " + N("0") + "; " + P("i") + " &lt; " + P("tasks") + ".length; " + P("i") + "++) {"
s3 = "    " + K("let") + " " + P("mark") + " = " + S_('"☐"') + ";"
s4 = "    " + CT("if") + " (" + P("tasks") + "[" + P("i") + "]." + P("done") + ") { " + P("mark") + " = " + S_('"☑"') + "; }"
s5 = "    " + F("console") + "." + F("log") + "(" + P("mark") + " + " + S_('" "') + " + " + P("tasks") + "[" + P("i") + "]." + P("text") + ");"
w_dv = WT(11, "давр"); w_ag = WT(11, "агар"); w_pr = WT(11, "пур"); w_kh = WT(11, "холӣ")
scene(T[10] - 0.1, T[12] - 0.1, f'''
<div class="kicker" style="top:100px">3 · showTasks 📋</div>
<div class="ide" style="top:130px"><div class="bar"><i></i><i></i><i></i><span>todo.js</span></div><div class="code" style="font-size:12.5px;padding-top:8px">
<div class="ln" style="height:22px">{TYP(T[10] + 0.1, 1.2, s1, 'function showTasks() {')}</div>
<div class="ln" style="height:22px">{TYP(T[11] + 0.1, 1.2, s2, '  for (let i = 0; i < tasks.length; i++) {')}</div>
<div class="ln" style="height:22px">{TYP(w_dv + 0.6, 0.8, s3, '    let mark = "☐";')}</div>
<div class="ln" style="height:22px">{TYP(w_ag, 1.6, s4, '    if (tasks[i].done) { mark = "☑"; }')}</div>
<div class="ln" style="height:22px">{TYP(w_ag + 1.8, 1.8, s5, '    console.log(mark + " " + tasks[i].text);')}</div>
<div class="ln" style="height:22px">  }}</div><div class="ln" style="height:22px">}}</div></div></div>
<div class="pill pop" style="--a:{w_dv:.2f}s;top:350px;font-size:16px;border-color:var(--ctrl);color:var(--ctrl)">for — давр (дарси 3)</div>
<div class="pill pop" style="--a:{w_ag:.2f}s;top:402px;font-size:16px;border-color:var(--ctrl);color:var(--ctrl)">if — шарт (дарси 2)</div>
<div class="pill ok pop" style="--a:{w_pr:.2f}s;top:470px;font-size:20px">☑ иҷро шуд</div>
<div class="pill err pop" style="--a:{w_kh:.2f}s;top:525px;font-size:20px">☐ ҳанӯз не</div>''')
sfx("pop", w_dv, 0.6); sfx("pop", w_ag, 0.6); sfx("ding", w_pr, 0.6); sfx("pop", w_kh, 0.5)

# ===== ИСТИФОДА (T12..T14) =====
u_t = [WT(12, "эд", 0), WT(12, "эд", 1), WT(12, "комплит"), WT(12, "шоу")]
u_h = [F("addTask") + "(" + S_('"нон харидан"') + ");", F("addTask") + "(" + S_('"дарс хондан"') + ");", F("completeTask") + "(" + N("0") + ");", F("showTasks") + "();"]
u_r = ['addTask("нон харидан");', 'addTask("дарс хондан");', 'completeTask(0);', 'showTasks();']
w_n1 = WT(13, "нон"); w_n2 = WT(13, "дарс")
lines = "".join(f'<div class="ln">{TYP(u_t[k], 1.0, u_h[k], u_r[k])}</div>' for k in range(4))
scene(T[12] - 0.1, T[14] - 0.1, f'''
<div class="kicker" style="top:100px">ИСТИФОДА</div>
<div class="ide" style="top:135px"><div class="bar"><i></i><i></i><i></i><span>todo.js</span></div><div class="code" style="font-size:15px;padding-top:10px">{lines}</div></div>
<div class="term abs fade" style="left:20px;right:20px;top:310px;border-radius:12px;border:1px solid var(--line);--a:{u_t[3] + 0.8:.2f}s;padding:12px 16px">
<div class="ln fade" style="--a:{w_n1:.2f}s"><span class="pr">&gt; </span><span style="color:var(--ok)">☑ нон харидан</span></div>
<div class="ln fade" style="--a:{w_n2:.2f}s"><span class="pr">&gt; </span>☐ дарс хондан</div></div>''')
for t_ in u_t: sfx("pop", t_, 0.4)
sfx("ding", w_n1, 0.6); sfx("ding", w_n2, 0.6)

# ===== ЛОИҲА ТАЙЁР АСТ! (T14..T15) =====
scene(T[14] - 0.1, T[15] - 0.1, f'''
<div class="slam acc" style="--a:{T[14]:.2f}s;top:120px;font-size:50px">ЛОИҲА ТАЙЁР!</div>
{appcard(220, [("нон харидан", True), ("дарс хондан", False)], T[14] + 0.2, cnt="1 / 2")}
<div class="pill ok pop" style="--a:{T[14] + 0.5:.2f}s;top:410px;font-size:20px">аввалин барномаи ман ✅</div>
<div class="emo pop" style="--a:{T[14] + 0.3:.2f}s;position:absolute;left:0;right:0;top:480px;text-align:center;font-size:76px">🎉</div>''')
sfx("hit", T[14], 0.9); sfx("chime", T[14] + 0.2, 0.7); sfx("ding", T[14] + 0.5, 0.6)

# ===== ХУЛОСА (T15..T16) =====
scene(T[15] - 0.1, T[16] - 0.1, f'''
<div class="kicker" style="top:150px">ХУЛОСА</div>
<div class="h1 pop" style="--a:{T[15] + 0.05:.2f}s;top:195px;font-size:56px">TO-DO</div>
<div class="h1 acc pop" style="--a:{WT(15, 'рӯйхати'):.2f}s;top:270px;font-size:34px">= рӯйхати объектҳо</div>
<div class="h1 acc pop" style="--a:{WT(15, 'се'):.2f}s;top:325px;font-size:34px">+ се функсия</div>
<div class="fnb pop" style="--a:{WT(15, 'се') + 0.1:.2f}s;left:28px;top:410px"><div class="ic">➕</div><div class="nm">addTask</div></div>
<div class="fnb pop" style="--a:{WT(15, 'се') + 0.25:.2f}s;left:195px;top:410px"><div class="ic">✅</div><div class="nm">completeTask</div></div>
<div class="fnb pop" style="--a:{WT(15, 'се') + 0.4:.2f}s;left:362px;top:410px"><div class="ic">📋</div><div class="nm">showTasks</div></div>''')
sfx("hit", T[15] + 0.05, 0.7); sfx("pop", WT(15, 'рӯйхати'), 0.7); sfx("pop", WT(15, 'се'), 0.7)

# ===== САНҶИШ (T16..T20) =====
q_t = [WT(16, "эд", 0), WT(16, "эд", 1), WT(16, "комплит"), WT(16, "шоу")]
q_h = [F("addTask") + "(" + S_('"А"') + ");", F("addTask") + "(" + S_('"Б"') + ");", F("completeTask") + "(" + N("1") + ");", F("showTasks") + "();"]
q_r = ['addTask("А");', 'addTask("Б");', 'completeTask(1);', 'showTasks();']
qlines = "".join(f'<div class="ln">{TYP(q_t[k], 0.9, q_h[k], q_r[k])}</div>' for k in range(4))
t_q = WT(17, "иҷро")
scene(T[16] - 0.1, T[20] - 0.1, f'''
<div class="kicker" style="top:120px">САНҶИШ</div>
<div class="h1 pop" style="--a:{T[16] + 0.05:.2f}s;top:150px;font-size:38px">кадом вазифа ☑ мешавад?</div>
<div class="ide" style="top:215px;left:12px;right:12px"><div class="bar"><i></i><i></i><i></i><span>test.js</span></div><div class="code" style="font-size:15px;padding-top:10px">{qlines}</div></div>
<div class="h1 acc pop" style="--a:{t_q:.2f}s;top:445px;font-size:100px">?</div>
<div class="pill pop" style="--a:{T[18]:.2f}s;top:580px;font-size:17px;border-color:var(--kw);color:var(--kw)">шумора аз 0 оғоз мешавад</div>
<div class="pill ok pop" style="--a:{T[19]:.2f}s;top:630px">💬 ҷавобро дар шарҳ нависед</div>''')
for t_ in q_t: sfx("pop", t_, 0.4)
sfx("pop", t_q, 0.8); sfx("tick2", t_q, 0.5); sfx("pop", T[18], 0.6); sfx("pop", T[19], 0.6)

# ===== ПАЙВАНД ДАР ОПИСАНИЯ (T20..T21) =====
w_vd = WT(20, "видеои"); w_sl = WT(20, "силка"); w_op = WT(20, "описанияи")
scene(T[20] - 0.1, T[21] - 0.1, f'''
<div class="kicker" style="top:105px">ВИДЕОИ ПУРРА ДАР YOUTUBE</div>
<div class="card pop" style="--a:{w_vd:.2f}s;left:50px;right:50px;top:135px;padding:0;overflow:hidden">
 <div style="height:120px;background:linear-gradient(135deg,#2a1f45,#1E1E1E);display:flex;align-items:center;justify-content:center"><div style="width:58px;height:42px;border-radius:11px;background:#F4443C;color:#fff;font-size:20px;line-height:42px;text-align:center">▶</div></div>
 <div style="padding:9px 16px"><div style="font:800 16px 'Segoe UI';color:var(--white)">Дарси 10: Лоиҳа — функсияҳо</div><div style="font:600 12px 'Segoe UI';color:var(--muted);margin-top:2px">YouTube · видеои пурраи дарс</div></div></div>
<div class="h1 pop bob" style="--a:{w_sl - 0.2:.2f}s;top:290px;font-size:40px;color:var(--purple)">↓</div>
<div class="abs pop" style="--a:{w_sl:.2f}s;left:70px;top:345px;width:400px;height:335px;border-radius:18px;overflow:hidden;border:1px solid var(--line);box-shadow:0 20px 50px rgba(0,0,0,.6)"><img src="profile.png" style="width:400px;height:335px;display:block"/>
 <div class="hlt" style="--a:{w_op:.2f}s;--b:{END + 5:.2f}s;position:absolute;left:8px;top:260px;width:290px;height:30px;border-radius:10px;border:2.5px solid var(--pink)"></div></div>''')
sfx("pop", w_vd, 0.7); sfx("pop", w_sl, 0.7); sfx("chime", w_op + 0.1, 0.7)

# ===== ДАРСИ ОЯНДА (T21..T22) =====
t_nm = WT(21, "намуди"); t_h = WT(21, "эйч"); t_c = WT(21, "си")
scene(T[21] - 0.1, T[22] - 0.1, f'''
<div class="kicker" style="top:120px">ДАРСИ ОЯНДА</div>
<div class="h1 pop" style="--a:{T[21] + 0.05:.2f}s;top:158px;font-size:38px">11 · <span class="acc">Намуди барнома</span></div>
<div class="term abs pop" style="--a:{t_nm:.2f}s;left:30px;width:170px;top:260px;border-radius:12px;border:1px solid var(--line);padding:12px 12px;font-size:13px"><div style="color:var(--muted);font:700 10px var(--mono);margin-bottom:6px">ҲОЗИР · консол</div><div style="color:var(--ok)">☑ нон харидан</div><div>☐ дарс хондан</div><div>☐ занг задан</div></div>
<div class="abs pop" style="--a:{t_nm + 0.3:.2f}s;left:208px;top:318px;font-size:34px;color:var(--purple)">➜</div>
<div class="abs pop" style="--a:{t_nm + 0.5:.2f}s;left:262px;width:248px;top:250px">{appcard(0, [("нон харидан", True), ("дарс хондан", False), ("занг задан", False)], t_nm + 0.5, cnt="1 / 3", cls="fade").replace("top:0px", "top:0px;left:0;right:0")}</div>
<div class="pill acc2 pop" style="--a:{t_h:.2f}s;left:35%;top:480px;font-size:22px;padding:10px 24px">HTML</div>
<div class="pill pop" style="--a:{t_c:.2f}s;left:68%;top:480px;font-size:22px;padding:10px 24px;border-color:var(--pink);color:var(--pink)">CSS</div>
<div class="pill ok pop" style="--a:{t_c + 0.3:.2f}s;top:545px;font-size:17px">сохтор + ранг ва шакл</div>''')
sfx("hit", T[21] + 0.05, 0.7); sfx("pop", t_nm, 0.7); sfx("pop", t_nm + 0.5, 0.7); sfx("pop", t_h, 0.7); sfx("pop", t_c, 0.7)

# ===== ОБУНА (T22..END) =====
t_sub = SN[22]['start'] + 0.2
scene(T[22] - 0.1, END + 5, f'''
<div class="kicker" style="top:150px">БАРНОМАСОЗӢ АЗ СИФР</div>
<div class="h1 pop" style="--a:{T[22] + 0.05:.2f}s;top:200px;font-size:50px"><span class="acc">Лоиҳаи</span> шумо</div>
<div class="pill acc2 pop" style="--a:{t_sub:.2f}s;top:330px;font-size:22px;padding:13px 32px">🔔 Обуна шавед</div>''')
sfx("hit", T[22] + 0.05, 0.7); sfx("pop", t_sub, 0.8); sfx("ding", t_sub + 0.1, 0.6)

H = [re.sub(r'</div>\s+<div class="ln"', '</div><div class="ln"', h) for h in H]
html = f'''<!doctype html><html lang="tg"><head><meta charset="utf-8"><link rel="stylesheet" href="style.css"></head><body>
{"".join(H)}
{"".join(cap_html)}
</body></html>'''
open('reel.html', 'w', encoding='utf-8').write(html)
json.dump(dict(end=END, sfx=SFX), open('sfx.json', 'w'))
print('END', END, 'sfx', len(SFX), 'captions', len(cap_html))
