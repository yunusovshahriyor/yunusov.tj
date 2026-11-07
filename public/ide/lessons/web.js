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
]);
