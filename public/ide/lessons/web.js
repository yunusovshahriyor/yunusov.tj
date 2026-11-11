/* Дарсҳои HTML ва CSS (трек «web»).
   Вазифа: { title, text, files: { html, css, js }, hint, solution: { html, css, js }, checks: [...] }.
   Санҷиш (checks) дар саҳифаи пешнамоиш аз рӯи DOM иҷро мешавад. Ҳар санҷиш:
     { label, sel,            // CSS-селектор
       count | min | none,    // чанд унсур (бе инҳо: ҳадди аққал 1)
       text,                  // матни унсури аввал (RegExp ё сатр)
       attr: { name: RegExp|сатр },
       css: { "property": "қимат" } }   // услуби ҳисобшуда (computed) */
window.IDE_LESSONS = (window.IDE_LESSONS || []).concat([
  { id: "l10", track: "web", tab: "10 · HTML ва CSS", tag: "ПЕШНАМУНА",
    theory: "Саҳифаи веб аз <b>теғҳо</b> иборат аст: <code>&lt;h1&gt;</code> — сарлавҳа, <code>&lt;p&gt;</code> — абзац. Ҳар теғ кушода ва баста мешавад: <code>&lt;p&gt;Матн&lt;/p&gt;</code>. Дар таби <b>CSS</b> намуди онҳоро тағйир медиҳем: <code>h1 { color: red; }</code>. Натиҷа дар тарафи рост зуд пайдо мешавад.",
    tasks: [
      { title: "Вазифаи 1: сарлавҳа ва абзац", text: "Бо <code>&lt;h1&gt;</code> сарлавҳа ва бо <code>&lt;p&gt;</code> абзац нависед. Дар ҳарду матн бошад.",
        files: { html: "<!-- сарлавҳа ва абзац нависед -->\n", css: "" },
        hint: "<h1>Салом</h1> ва дар зери он <p>Ман барномасоз мешавам.</p>",
        solution: { html: "<h1>Салом</h1>\n<p>Ман барномасоз мешавам.</p>\n", css: "" },
        checks: [
          { label: "Сарлавҳаи <h1> бо матн", sel: "h1", text: /\S/ },
          { label: "Абзаци <p> бо матн", sel: "p", text: /\S/ },
          { label: "Абзац дар зери сарлавҳа аст", sel: "h1 + p" }
        ] },
      { title: "Вазифаи 2: ранг ва андоза", text: "Дар таби <b>CSS</b> сарлавҳаро <b>сурх</b> (<code>red</code>) ва андозаи матни абзацро <b>20px</b> кунед.",
        files: { html: "<h1>Салом</h1>\n<p>Ман барномасоз мешавам.</p>\n", css: "/* h1 { ... } */\n" },
        hint: "h1 { color: red; } p { font-size: 20px; }",
        solution: { html: "<h1>Салом</h1>\n<p>Ман барномасоз мешавам.</p>\n", css: "h1 {\n  color: red;\n}\n\np {\n  font-size: 20px;\n}\n" },
        checks: [
          { label: "Сарлавҳа сурх аст", sel: "h1", css: { color: "red" } },
          { label: "Андозаи абзац 20px аст", sel: "p", css: { "font-size": "20px" } }
        ] }
    ] }
  ,
  { id: "l11", track: "web", tab: "11 · HTML, CSS, JS", tag: "ДАРСИ 11",
    theory: "Саҳифаи веб аз се забон иборат аст: <b>HTML</b> — сохтор (деворҳо), <b>CSS</b> — намуд (ранг), <b>JavaScript</b> — ҳаракат (барқ). Ҳар се дар як саҳифа якҷоя кор мекунанд. Барои гирифтани элемент: <code>document.querySelector(\"h1\")</code>, барои иваз кардани матн: <code>.textContent = \"...\"</code>, барои пахши тугма: <code>onclick</code>.",
    tasks: [
      { title: "Вазифаи 1: HTML", text: "Бо <code>&lt;h1&gt;</code> сарлавҳа бо номи худатон ва бо <code>&lt;p&gt;</code> як сархат дар бораи худатон нависед.",
        files: { html: "<!-- сарлавҳа ва сархат -->\n", css: "", js: "" },
        hint: "<h1>Нигина</h1> ва дар зери он <p>Ман барномасоз мешавам.</p>",
        solution: { html: "<h1>Нигина</h1>\n<p>Ман барномасоз мешавам.</p>\n", css: "", js: "" },
        checks: [
          { label: "Сарлавҳаи <h1> бо матн", sel: "h1", text: /\S/ },
          { label: "Сархати <p> бо матн", sel: "p", text: /\S/ }
        ] },
      { title: "Вазифаи 2: CSS", text: "Дар таби <b>CSS</b> ранги сарлавҳаро <b>сурх</b> (<code>red</code>) кунед ва ба тугма замина — <b>бунафш</b> (<code>#BD93F9</code>) диҳед.",
        files: { html: "<h1>Нигина</h1>\n<p>Ман барномасоз мешавам.</p>\n<button>Пахш кун</button>\n", css: "/* h1 { ... } button { ... } */\n", js: "" },
        hint: "h1 { color: red; } button { background: #BD93F9; }",
        solution: { html: "<h1>Нигина</h1>\n<p>Ман барномасоз мешавам.</p>\n<button>Пахш кун</button>\n", css: "h1 {\n  color: red;\n}\n\nbutton {\n  background: #BD93F9;\n}\n", js: "" },
        checks: [
          { label: "Сарлавҳа сурх аст", sel: "h1", css: { color: "red" } },
          { label: "Заминаи тугма бунафш аст", sel: "button", css: { "background-color": "#BD93F9" } }
        ] },
      { title: "Вазифаи 3: JavaScript", text: "Дар таби <b>JS</b> функсияи <code>greet</code> нависед, ки матни сарлавҳаро ба «<b>Салом, Нигина!</b>» иваз кунад. Тугма аллакай ба он пайваст аст (<code>onclick</code>): пахш кунед ва санҷед.",
        files: { html: "<h1>Нигина</h1>\n<button onclick=\"greet()\">Пахш кун</button>\n", css: "", js: "function greet() {\n  // матни h1-ро иваз кунед\n}\n" },
        hint: 'document.querySelector("h1").textContent = "Салом, Нигина!";',
        solution: { html: "<h1>Нигина</h1>\n<button onclick=\"greet()\">Пахш кун</button>\n", css: "", js: 'function greet() {\n  document.querySelector("h1").textContent = "Салом, Нигина!";\n}\n' },
        checks: [
          { label: "Пас аз пахши тугма сарлавҳа «Салом, Нигина!» мешавад", sel: "h1", click: "button", text: "Салом, Нигина!" }
        ] }
    ] }
]);
