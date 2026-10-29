# Шпаргалка «Барномасозӣ аз сифр · Дарсҳои 1–4» → cheatsheet.html (печать в PDF через Playwright).
import html, re

KW = {"let", "const", "if", "else", "for", "while", "true", "false", "typeof"}
def hl(code):
    out = []
    for m in re.finditer(r'(//[^\n]*)|("(?:[^"\\]|\\.)*")|(\b\d+\b)|([A-Za-z_]\w*)|(\s+|.)', code):
        cm, st, num, ident, other = m.groups()
        if cm: out.append(f'<span class="cm">{html.escape(cm)}</span>')
        elif st: out.append(f'<span class="st">{html.escape(st)}</span>')
        elif num: out.append(f'<span class="nu">{num}</span>')
        elif ident:
            cls = "kw" if ident in KW else ("fn" if ident in ("console", "log") else "id")
            out.append(f'<span class="{cls}">{ident}</span>')
        else: out.append(html.escape(other))
    return "".join(out)
def code(src, out=None, title=None):
    o = f'<div class="out"><b>▶ Натиҷа</b><pre>{html.escape(out)}</pre></div>' if out else ""
    t = f'<span>{title}</span>' if title else ""
    return f'<div class="term"><div class="bar"><i></i><i></i><i></i>{t}</div><pre>{hl(src.strip())}</pre>{o}</div>'

pages = []
def page(n, body, cls=""):
    pages.append(f'<section class="page {cls}"><div class="hdr"><span>ШАҲРИЁР ЮНУСОВ</span><span>БАРНОМАСОЗӢ АЗ СИФР</span></div>{body}'
                 f'<div class="foot"><span>@shahriyor_yunusov</span><span>{n} / 9</span></div></section>')

BOX = '<div class="box"><div class="flap l"></div><div class="flap r"></div><div class="back"></div><div class="num">25</div><div class="front"><div class="tag">age</div></div></div>'

# 1. Обложка
page(1, f'''
<div class="cover">
  <span class="chip">ШПАРГАЛКА · ДАРСҲОИ 1–4</span>
  <h1>Барномасозӣ<br>аз сифр</h1>
  <h2>4 ғишти ҳар барнома</h2>
  {BOX}
  <div class="toc">
    <div><b>01</b> Тағйирёбанда <code>let</code></div>
    <div><b>02</b> Шарт <code>if / else</code></div>
    <div><b>03</b> Давр <code>for</code></div>
    <div><b>04</b> Рӯйхат <code>array [ ]</code></div>
    <div><b>+</b> Лоиҳаи хурд, вазифаҳо ва ҷавобҳо</div>
  </div>
  <p class="muted">Сабт кунед ва ҳар вақт ба он баргардед 📌</p>
</div>''', "cover-page")

# 2. Как запустить код
page(2, f'''
<span class="chip">ҚАДАМИ 0</span>
<h1 class="h">Кодро ҳозир санҷед</h1>
<p>Барои оғоз ҳеҷ барнома насб кардан лозим нест. Браузер кифоя аст.</p>
<div class="steps">
  <div><b>1</b><span><b>Компютер:</b> дар Chrome тугмаи <kbd>F12</kbd> (ё <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>J</kbd>) → ҷадвали <b>Console</b>.</span></div>
  <div><b>2</b><span>Кодро нусха кунед, гузоред ва <kbd>Enter</kbd>-ро пахш кунед.</span></div>
  <div><b>3</b><span><b>Телефон:</b> сайти <b>playcode.io</b> ё <b>jsfiddle.net</b>-ро кушоед — код дар браузер кор мекунад.</span></div>
</div>
{code('console.log("Салом, ҷаҳон!");', "Салом, ҷаҳон!", "аввалин код")}
<div class="tip"><b>💡 Ёдовар:</b> <code>console.log(...)</code> — «ба экран нишон деҳ». Бо он натиҷаи ҳар кодро мебинед.</div>
<div class="bricks">
  <div><span class="emo">📦</span><b>Тағйирёбанда</b><small>маълумотро нигоҳ медорад</small></div>
  <div><span class="emo">🔀</span><b>Шарт</b><small>қарор қабул мекунад</small></div>
  <div><span class="emo">🔁</span><b>Давр</b><small>такрор мекунад</small></div>
  <div><span class="emo">📋</span><b>Рӯйхат</b><small>якчанд қимат</small></div>
</div>
<p class="muted center">Ҳар барнома — аз Instagram то бозӣ — аз ҳамин ғиштҳо сохта шудааст.</p>''')

# 3. Тағйирёбанда
page(3, f'''
<span class="chip">ДАРСИ 1</span>
<h1 class="h">📦 Тағйирёбанда</h1>
<div class="def"><b>Тағйирёбанда</b> — қуттӣ бо <b>ном</b>, ки дар дохилаш <b>қимат</b> нигоҳ медорад. Қиматро иваз кардан мумкин аст.</div>
{code("""let age = 25;   // қуттии нав
age = 26;       // қимати нав
console.log(age);""", "26")}
<h3>Се навъи асосии маълумот</h3>
{code("""let age = 26;              // рақам   (number)
const name = "Шаҳриёр";    // матн    (string)
let isStudent = true;      // ҳа / не (boolean)""")}
<div class="two">
  <div class="card"><b class="kw2">let</b> — қимат иваз мешавад</div>
  <div class="card"><b class="kw2">const</b> — қимат доимист</div>
</div>
<h3>Қоидаҳои ном</h3>
<table>
<tr><td class="ok">✓ <code>age</code>, <code>userName</code>, <code>score2</code></td><td class="no">✗ <code>2score</code>, <code>user name</code>, <code>let</code></td></tr>
</table>
<p class="muted">Номро бо ҳарф оғоз кунед, бе фосила. Калимаҳои дуюмро бо ҳарфи калон: <code>userName</code>.</p>''')

# 4. Шарт
page(4, f'''
<span class="chip">ДАРСИ 2</span>
<h1 class="h">🔀 Шарт: if / else</h1>
<div class="def"><b>if</b> — агар, <b>else</b> — вагарна. Шарт = <b>савол</b> + <b>ду роҳ</b>.</div>
{code("""let age = 15;
if (age >= 18) {
  console.log("Хуш омадед!");
} else {
  console.log("Ҳанӯз барвақт");
}""")}
<h3>Аломатҳои муқоиса</h3>
<table class="ops">
<tr><td><code>&gt;</code> калон</td><td><code>&lt;</code> хурд</td><td><code>===</code> баробар</td></tr>
<tr><td><code>&gt;=</code> калон ё баробар</td><td><code>&lt;=</code> хурд ё баробар</td><td><code>!==</code> баробар нест</td></tr>
</table>
<h3>Зиёда аз ду роҳ: else if</h3>
{code("""let score = 75;
if (score >= 90) {
  console.log("Аъло");
} else if (score >= 70) {
  console.log("Хуб");
} else {
  console.log("Боз кӯшиш кунед");
}""", "Хуб")}
<div class="tip warn"><b>⚠️ Хатои маъмул:</b> <code>=</code> қимат мегузорад, <code>===</code> муқоиса мекунад. Дар шарт ҳамеша <code>===</code>.</div>''')

# 5. Давр
page(5, f'''
<span class="chip">ДАРСИ 3</span>
<h1 class="h">🔁 Давр: for</h1>
<div class="def">Давр — такрори як амал чанд маротиба. <b>Давр = оғоз + шарт + қадам.</b></div>
<div class="anat"><span class="a1">let i = 1</span>; <span class="a2">i &lt;= 10</span>; <span class="a3">i++</span></div>
<div class="legend"><span class="a1">1 · оғоз</span><span class="a2">2 · шарт</span><span class="a3">3 · қадам</span></div>
{code("""let sum = 0;
for (let i = 1; i <= 100; i++) {
  sum = sum + i;
}
console.log(sum);""", "5050", "ҷамъи 1 то 100")}
{code("""for (let i = 1; i <= 3; i++) {
  console.log("7 × " + i + " = " + 7 * i);
}""", "7 × 1 = 7\n7 × 2 = 14\n7 × 3 = 21", "ҷадвали зарб")}
<div class="tip warn"><b>⚠️ Давре, ки хотима намеёбад:</b> агар қадамро (<code>i++</code>) фаромӯш кунед, шарт ҳамеша дуруст мемонад ва барнома «овезон» мешавад.</div>''')

# 6. Рӯйхат
page(6, f'''
<span class="chip">ДАРСИ 4</span>
<h1 class="h">📋 Рӯйхат (array)</h1>
<div class="def">Рӯйхат — <b>тағйирёбанда</b>, ки <b>якчанд қимат</b> нигоҳ медорад. Ҳар қимат <b>шумора</b> дорад, ва шумора аз <b>0</b> оғоз мешавад!</div>
<div class="arr"><div><i>0</i>нон</div><div><i>1</i>шир</div><div><i>2</i>тухм</div><div><i>3</i>себ</div><div><i>4</i>нок</div></div>
{code('''let shopping = ["нон", "шир", "тухм", "себ", "нок"];
console.log(shopping[2]);      // тухм
console.log(shopping.length);  // 5
shopping.push("анор");         // ба охир илова''', None, "royhat.js")}
<h3>Амалҳои асосӣ</h3>
<table class="ops">
<tr><td><code>list[0]</code> қимати аввал</td><td><code>list.length</code> чанд қимат</td></tr>
<tr><td><code>list.push(x)</code> илова</td><td><code>list[list.length - 1]</code> охирин</td></tr>
</table>
<h3>Рӯйхат + давр</h3>
{code('''for (let i = 0; i < shopping.length; i++) {
  console.log(i + ". " + shopping[i]);
}''', "0. нон\n1. шир\n…\n5. анор")}
<div class="tip warn"><b>⚠️ Хатои маъмул:</b> шумора аз <code>0</code> оғоз мешавад. Дар рӯйхати 3-қиматӣ охирин шумора <code>2</code> аст, ва <code>list[3]</code> → <code>undefined</code>.</div>''')

# 7. Мини-проект
page(7, f'''
<span class="chip">ЛОИҲАИ ХУРД</span>
<h1 class="h">Ҳар се ғишт якҷоя</h1>
<p>Барнома рақамҳои 1 то 6-ро месанҷад: ҷуфт ё тоқ?</p>
{code("""for (let i = 1; i <= 6; i++) {       // 🔁 давр
  if (i % 2 === 0) {                   // 🔀 шарт
    console.log(i + " — ҷуфт");
  } else {
    console.log(i + " — тоқ");
  }
}""", "1 — тоқ\n2 — ҷуфт\n3 — тоқ\n4 — ҷуфт\n5 — тоқ\n6 — ҷуфт", "juft-toq.js")}
<div class="tip"><b>💡</b> <code>i % 2</code> — бақияи тақсим ба 2. Агар бақия <code>0</code> бошад, рақам ҷуфт аст. Ва <code>i</code> — ҳамон 📦 тағйирёбанда.</div>
<h3>🧠 Вазифаҳо (ҷавобҳо дар саҳифаи 8)</h3>
<ol class="tasks">
<li>Тағйирёбандаи <code>myName</code> созед ва «Салом, …!» нишон диҳед.</li>
<li>Агар <code>temperature &gt; 30</code> — «Гарм аст», вагарна — «Хунук аст».</li>
<li>Бо давр аз 10 то 1 баръакс ҳисоб кунед.</li>
<li>Рӯйхати 3 хӯроки дӯстдоштаатонро созед ва қимати <b>дуюм</b>-ро нишон диҳед.</li>
<li>Бо <code>push</code> хӯроки чорум илова кунед ва бо давр ҳамаро нишон диҳед.</li>
</ol>''')

# 7. Ответы
page(8, f'''
<span class="chip">ҶАВОБҲО</span>
<h1 class="h">Худро санҷед ✅</h1>
<div class="quiz"><b>Санҷиши дарси 1:</b> <code>let age = 25; age = 26;</code> → <b class="good">26</b>. Қимати нав кӯҳнаро иваз мекунад.</div>
<div class="quiz"><b>Санҷиши дарси 2:</b> <code>age = 15</code> → <b class="good">«Ҳанӯз барвақт»</b>: 15 &lt; 18, шарт нодуруст → <code>else</code>.</div>
<div class="quiz"><b>Санҷиши дарси 3:</b> <code>for (let i = 0; i &lt; 3; i++)</code> → <b class="good">3 бор</b>: i = 0, 1, 2.</div>
<div class="quiz"><b>Санҷиши дарси 4:</b> нон — 0, шир — 1, <b class="good">тухм — 2</b>. Шумора аз <code>0</code> оғоз мешавад.</div>
<h3>Ҳалли вазифаҳо</h3>
{code("""// 1
let myName = "Нигина";
console.log("Салом, " + myName + "!");
// 2
let temperature = 34;
if (temperature > 30) { console.log("Гарм аст"); }
else { console.log("Хунук аст"); }
// 3
for (let i = 10; i >= 1; i--) { console.log(i); }
// 4
let fav = ["палав", "самбуса", "ошташ"];
console.log(fav[1]);   // самбуса
// 5
fav.push("қурутоб");
for (let i = 0; i < fav.length; i++) {
  console.log(fav[i]);
}""")}''')

# 8. Дальше
page(9, f'''
<span class="chip">ҚАДАМИ НАВБАТӢ</span>
<h1 class="h">Роҳи шумо 🚀</h1>
<div class="road">
  <div class="done"><b>01</b>Тағйирёбанда ✓</div>
  <div class="done"><b>02</b>Шарт ✓</div>
  <div class="done"><b>03</b>Давр ✓</div>
  <div class="done"><b>04</b>Рӯйхат ✓</div>
  <div><b>05</b>Функсия</div>
  <div><b>06</b>Объект</div>
  <div><b>07</b>Хатогӣ ва дебаг</div>
  <div><b>08–09</b>Лоиҳаи хурд</div>
  <div><b>10–12</b>Сайт, HTML/CSS/JS, AI</div>
</div>
<div class="tip"><b>💡 Маслиҳат:</b> ҳар рӯз 20 дақиқа. Кодро на танҳо хонед — <b>худатон нависед</b> ва иваз кунед: «агар 10-ро ба 100 иваз кунам, чӣ мешавад?»</div>
<div class="cta">
  <div>📲 Дарсҳои нав дар Instagram<br><b>@shahriyor_yunusov</b></div>
  <div>💬 Савол доред? Дар шарҳ ё Direct нависед — ҷавоб медиҳам.</div>
  <div>🤝 Ин файлро ба дӯсте фиристед, ки барномасозиро мехоҳад.</div>
</div>''')

css = open('style.css').read()
open('cheatsheet.html', 'w').write(f'<!doctype html><html lang="tg"><head><meta charset="utf-8"><title>Барномасозӣ аз сифр — Шпаргалка</title><style>{css}</style></head><body>{"".join(pages)}</body></html>')
print(len(pages), "pages")
