/* Дарсҳои JavaScript (трек «js»).
   Дарс: { id, tab, tag, theory, tasks: [{ title, text, starter, hint, solution, check(code, R) }] } */
window.IDE_EXAMPLES_JS = [
    ["Мисолҳо ▾", ""],
    ["Салом, ҷаҳон", 'console.log("Салом, ҷаҳон!");\n'],
    ["Тағйирёбанда", 'let age = 25;\nconsole.log(age);\nage = 26;\nconsole.log(age);\n\nconst name = "Шаҳриёр";\nconsole.log("Салом, " + name + "!");\n'],
    ["Шарт (if / else)", 'let age = 15;\n\nif (age >= 18) {\n  console.log("Хуш омадед!");\n} else {\n  console.log("Ҳанӯз барвақт");\n}\n'],
    ["else if (баҳо)", 'let score = 75;\n\nif (score >= 90) {\n  console.log("Аъло");\n} else if (score >= 70) {\n  console.log("Хуб");\n} else {\n  console.log("Боз кӯшиш кунед");\n}\n'],
    ["Давр: 1 то 10", 'for (let i = 1; i <= 10; i++) {\n  console.log("Нишаст-хез " + i);\n}\n'],
    ["Ҷамъи 1 то 100", 'let sum = 0;\nfor (let i = 1; i <= 100; i++) {\n  sum = sum + i;\n}\nconsole.log(sum);\n'],
    ["Ҷадвали зарб", 'for (let i = 1; i <= 10; i++) {\n  console.log("7 × " + i + " = " + 7 * i);\n}\n'],
    ["Ҷуфт ё тоқ", 'for (let i = 1; i <= 6; i++) {\n  if (i % 2 === 0) {\n    console.log(i + " — ҷуфт");\n  } else {\n    console.log(i + " — тоқ");\n  }\n}\n']
  ];
window.IDE_LESSONS = [
    { id: "l1", tab: "1 · Тағйирёбанда", tag: "ДАРСИ 1",
      theory: "Тағйирёбанда — қуттӣ бо <b>ном</b>, ки <b>қимат</b> нигоҳ медорад: <code>let age = 25;</code>. Қиматро иваз кардан мумкин: <code>age = 26;</code>.",
      tasks: [
        { title: "Вазифаи 1: қимати нав", text: "Тағйирёбандаи <code>age</code>-ро бо қимати <b>25</b> созед, баъд ба <b>26</b> иваз кунед ва онро бо <code>console.log</code> нишон диҳед.",
          starter: "// Тағйирёбандаи age-ро созед ва ба 26 иваз кунед\n", hint: "let age = 25; баъд age = 26; ва console.log(age);",
          solution: "let age = 25;\nage = 26;\nconsole.log(age);\n",
          check: function (c, R) { return R.run(c).then(function (r) { return [
            ["Тағйирёбандаи age сохта шуд (let ё const)", /\b(let|var|const)\s+age\b/.test(c)],
            ["Қиматро иваз кардед (age = 26)", /\bage\s*=\s*26\b/.test(c)],
            ["Дар натиҷа ҳамагӣ 26 нишон дода шуд", !r.err && r.out[r.out.length - 1] === "26"]]; }); } },
        { title: "Вазифаи 2: салом бо ном", text: "Тағйирёбандаи <code>name</code>-ро бо номи худ созед ва «<b>Салом, &lt;ном&gt;!</b>» нависед. Масалан: <code>Салом, Нигина!</code>",
          starter: "// Тағйирёбандаи name-ро созед\n", hint: 'let name = "Нигина"; console.log("Салом, " + name + "!");',
          solution: 'let name = "Нигина";\nconsole.log("Салом, " + name + "!");\n',
          check: function (c, R) { return R.run(c).then(function (r) { var o = r.out[r.out.length - 1] || ""; return [
            ["Тағйирёбандаи name сохта шуд", /\b(let|var|const)\s+name\b/.test(c)],
            ["Матн бо «Салом, » оғоз мешавад", /^Салом, /.test(o)],
            ["Матн бо «!» тамом мешавад ва ном дорад", /^Салом, .+!$/.test(o) && o.length > 9]]; }); } }
      ] },
    { id: "l2", tab: "2 · Шарт", tag: "ДАРСИ 2",
      theory: "<code>if</code> — агар, <code>else</code> — вагарна. Шарт = <b>савол + ду роҳ</b>. Муқоиса: <code>&gt;</code> <code>&lt;</code> <code>&gt;=</code> <code>&lt;=</code> <code>===</code>.",
      tasks: [
        { title: "Вазифаи 1: гарм ё хунук", text: "Агар <code>temperature &gt; 30</code> бошад — нависед «<b>Гарм аст</b>», вагарна — «<b>Хунук аст</b>». Тағйирёбандаи <code>temperature</code>-ро нигоҳ доред: санҷиш онро бо қиматҳои гуногун месанҷад.",
          starter: "let temperature = 34;\n\n// if / else нависед\n", hint: 'if (temperature > 30) { console.log("Гарм аст"); } else { console.log("Хунук аст"); }',
          solution: 'let temperature = 34;\n\nif (temperature > 30) {\n  console.log("Гарм аст");\n} else {\n  console.log("Хунук аст");\n}\n',
          check: function (c, R) { return Promise.all([34, 31, 30, 10].map(function (v) { return R.run(R.setVar(c, "temperature", v)); })).then(function (rs) { var o = function (i) { return rs[i].out.join("|"); }; return [
            ["temperature = 34 → «Гарм аст»", o(0) === "Гарм аст"], ["temperature = 31 → «Гарм аст»", o(1) === "Гарм аст"],
            ["temperature = 30 → «Хунук аст»", o(2) === "Хунук аст"], ["temperature = 10 → «Хунук аст»", o(3) === "Хунук аст"]]; }); } },
        { title: "Вазифаи 2: даромадан иҷозат аст?", text: "Агар <code>age</code> аз <b>18</b> зиёд ё баробар бошад — «<b>Хуш омадед!</b>», вагарна — «<b>Ҳанӯз барвақт</b>». Ёдовар: барои «зиёд ё баробар» <code>&gt;=</code> лозим аст.",
          starter: "let age = 15;\n\n// if / else нависед\n", hint: 'if (age >= 18) { console.log("Хуш омадед!"); } else { console.log("Ҳанӯз барвақт"); }',
          solution: 'let age = 15;\n\nif (age >= 18) {\n  console.log("Хуш омадед!");\n} else {\n  console.log("Ҳанӯз барвақт");\n}\n',
          check: function (c, R) { return Promise.all([25, 18, 17, 5].map(function (v) { return R.run(R.setVar(c, "age", v)); })).then(function (rs) { var o = function (i) { return rs[i].out.join("|"); }; return [
            ["age = 25 → «Хуш омадед!»", o(0) === "Хуш омадед!"], ["age = 18 → «Хуш омадед!» (18 ҳам дохил аст)", o(1) === "Хуш омадед!"],
            ["age = 17 → «Ҳанӯз барвақт»", o(2) === "Ҳанӯз барвақт"], ["age = 5 → «Ҳанӯз барвақт»", o(3) === "Ҳанӯз барвақт"]]; }); } }
      ] },
    { id: "l3", tab: "3 · Давр", tag: "ДАРСИ 3",
      theory: "<code>for (let i = 1; i &lt;= 10; i++)</code> — се қисм: <b>оғоз</b> (<code>i = 1</code>), <b>шарт</b> (<code>i &lt;= 10</code>), <b>қадам</b> (<code>i++</code>). Давр = оғоз + шарт + қадам.",
      tasks: [
        { title: "Вазифаи 1: аз 1 то 5", text: "Бо давр рақамҳои <b>1, 2, 3, 4, 5</b>-ро нависед (ҳар як дар сатри алоҳида).",
          starter: "// давр нависед\n", hint: "for (let i = 1; i <= 5; i++) { console.log(i); }",
          solution: "for (let i = 1; i <= 5; i++) {\n  console.log(i);\n}\n",
          check: function (c, R) { return R.run(c).then(function (r) { return [
            ["Давр (for ё while) истифода шуд", /\b(for|while)\b/.test(c)],
            ["Дар натиҷа 1, 2, 3, 4, 5 аст", !r.err && r.out.join(",") === "1,2,3,4,5"]]; }); } },
        { title: "Вазифаи 2: ҷамъи 1 то 100", text: "Бо давр ҷамъи ҳамаи рақамҳои <b>1 то 100</b>-ро ҳисоб кунед ва нависед. Ҷавоб: <b>5050</b>. Ёдовар: тағйирёбандаи <code>sum</code> созед ва дар давр ба он илова кунед.",
          starter: "let sum = 0;\n\n// давр нависед\n\nconsole.log(sum);\n", hint: "for (let i = 1; i <= 100; i++) { sum = sum + i; }",
          solution: "let sum = 0;\nfor (let i = 1; i <= 100; i++) {\n  sum = sum + i;\n}\nconsole.log(sum);\n",
          check: function (c, R) { return R.run(c).then(function (r) { return [
            ["Давр истифода шуд", /\b(for|while)\b/.test(c)],
            ["Ҷавоб 5050 аст", !r.err && r.out[r.out.length - 1] === "5050"]]; }); } },
        { title: "Вазифаи 3: ҳисоби баръакс", text: "Рақамҳоро аз <b>10 то 1</b> баръакс нависед: 10, 9, 8 … 1. Ёдовар: <code>i--</code> ҳар бор як кам мекунад.",
          starter: "// ҳисоби баръакс\n", hint: "for (let i = 10; i >= 1; i--) { console.log(i); }",
          solution: "for (let i = 10; i >= 1; i--) {\n  console.log(i);\n}\n",
          check: function (c, R) { return R.run(c).then(function (r) { return [
            ["Давр истифода шуд", /\b(for|while)\b/.test(c)],
            ["Дар натиҷа 10, 9, … 1 аст", !r.err && r.out.join(",") === "10,9,8,7,6,5,4,3,2,1"]]; }); } }
      ] },
    { id: "l4", tab: "4 · Рӯйхат", tag: "ДАРСИ 4",
      theory: "Рӯйхат (array) — тағйирёбанда бо <b>якчанд қимат</b>: <code>let fruits = [\"себ\", \"нок\", \"ангур\"];</code>. Ҳар қимат шумора дорад, ва шумора аз <b>0</b> оғоз мешавад: <code>fruits[0]</code> — себ. <code>fruits.length</code> — чанд қимат; <code>fruits.push(x)</code> — ба охир илова мекунад.",
      tasks: [
        { title: "Вазифаи 1: рӯйхати хӯрок", text: "Рӯйхати 3 хӯроки дӯстдоштаатонро бо номи <code>foods</code> созед ва қимати <b>дуюм</b>-ро нишон диҳед (бо шумора!).",
          starter: "// let foods = [ ... ];\n", hint: 'let foods = ["палав", "самбуса", "ошташ"]; console.log(foods[1]); — шумораи дуюм 1 аст!',
          solution: 'let foods = ["палав", "самбуса", "ошташ"];\nconsole.log(foods[1]);\n',
          check: function (c, R) { return R.run(c).then(function (r) { var m = /\bfoods\s*=\s*\[([^\]]*)\]/.exec(c), it = m ? m[1].split(",").map(function (x) { return x.trim().replace(/^["'`]|["'`]$/g, ""); }) : [];
            return [["Рӯйхати foods созед (3 қимат)", it.length === 3 && it.every(function (x) { return x; })], ["Қимати дуюм бо foods[1] гирифта шуд", /foods\s*\[\s*1\s*\]/.test(c)], ["Дар натиҷа қимати дуюм аст", !r.err && it.length === 3 && r.out[r.out.length - 1] === it[1]]]; }); } },
        { title: "Вазифаи 2: илова кардан", text: "Бо <code>push</code> «<b>анор</b>»-ро ба рӯйхат илова кунед ва шумораи қиматҳоро (<code>length</code>) нишон диҳед. Бояд <b>4</b> шавад.",
          starter: 'let fruits = ["себ", "нок", "ангур"];\n\n// push ва length\n', hint: 'fruits.push("анор"); console.log(fruits.length);',
          solution: 'let fruits = ["себ", "нок", "ангур"];\nfruits.push("анор");\nconsole.log(fruits.length);\n',
          check: function (c, R) { return R.run(c).then(function (r) { return [["push истифода шуд", /fruits\.push\(/.test(c)], ["Шумораи қиматҳо 4 аст", !r.err && r.out[r.out.length - 1] === "4"]]; }); } },
        { title: "Вазифаи 3: рӯйхат ва давр", text: "Бо давр ҳар як қимати рӯйхатро як-як нависед: себ, нок, ангур. Ёдовар: <code>i &lt; fruits.length</code>.",
          starter: 'let fruits = ["себ", "нок", "ангур"];\n\n// давр нависед\n', hint: "for (let i = 0; i < fruits.length; i++) { console.log(fruits[i]); }",
          solution: 'let fruits = ["себ", "нок", "ангур"];\nfor (let i = 0; i < fruits.length; i++) {\n  console.log(fruits[i]);\n}\n',
          check: function (c, R) { return R.run(c).then(function (r) { return [["Давр истифода шуд", /\b(for|while)\b/.test(c)], ["Дар натиҷа: себ, нок, ангур", !r.err && r.out.join(",") === "себ,нок,ангур"]]; }); } }
      ] },
    { id: "l5", tab: "5 · Функсия", tag: "ДАРСИ 5",
      theory: "Функсия — «рецепти» барнома: як маротиба менависем, бисёр бор истифода мебарем. <code>function double(x) { return x * 2; }</code> — қабул мекунад <code>x</code> ва <code>return</code> ҷавоб бармегардонад. Даъват: <code>double(5)</code> → 10.",
      tasks: [
        { title: "Вазифаи 1: ду баробар", text: "Функсияи <code>double(x)</code> нависед, ки рақамро <b>ду баробар</b> кунад ва баргардонад (<code>return</code>).",
          starter: "function double(x) {\n  // return ...\n}\n", hint: "return x * 2;", solution: "function double(x) {\n  return x * 2;\n}\n",
          check: function (c, R) { return R.run(c + "\nconsole.log(double(4), double(0), double(-3));").then(function (r) { return [["double(4) → 8, double(0) → 0, double(-3) → -6", !r.err && r.out[r.out.length - 1] === "8 0 -6"], ["return истифода шуд", /\breturn\b/.test(c)]]; }); } },
        { title: "Вазифаи 2: калон аст?", text: "Функсияи <code>isAdult(age)</code> нависед: агар <code>age &gt;= 18</code> бошад — <code>true</code>, вагарна — <code>false</code> баргардонад.",
          starter: "function isAdult(age) {\n  // ...\n}\n", hint: "return age >= 18;", solution: "function isAdult(age) {\n  return age >= 18;\n}\n",
          check: function (c, R) { return R.run(c + "\nconsole.log(isAdult(20), isAdult(18), isAdult(17));").then(function (r) { return [["isAdult(20) → true", !r.err && r.out[r.out.length - 1].split(" ")[0] === "true"], ["isAdult(18) → true, isAdult(17) → false", !r.err && r.out[r.out.length - 1] === "true true false"]]; }); } },
        { title: "Вазифаи 3: салом", text: "Функсияи <code>greet(name)</code> нависед: <b>«Салом, &lt;ном&gt;!»</b> баргардонад. Масалан <code>greet(\"Нигина\")</code> → <code>Салом, Нигина!</code>",
          starter: "function greet(name) {\n  // ...\n}\n", hint: 'return "Салом, " + name + "!";', solution: 'function greet(name) {\n  return "Салом, " + name + "!";\n}\n',
          check: function (c, R) { return R.run(c + '\nconsole.log(greet("Нигина")); console.log(greet("Фарҳод"));').then(function (r) { return [["greet(\"Нигина\") → Салом, Нигина!", !r.err && r.out[0] === "Салом, Нигина!"], ["greet(\"Фарҳод\") → Салом, Фарҳод!", !r.err && r.out[1] === "Салом, Фарҳод!"]]; }); } }
      ] },
    { id: "l6", tab: "6 · Объект", tag: "ДАРСИ 6",
      theory: "Объект — «корти» чизе бо якчанд хусусият: <code>let person = { name: \"Нигина\", age: 20 };</code>. Хусусиятро бо нуқта мегиранд: <code>person.name</code>, иваз мекунанд: <code>person.age = 21</code>.",
      tasks: [
        { title: "Вазифаи 1: корт", text: "Объекти <code>person</code> созед: <code>name</code> — «<b>Нигина</b>», <code>age</code> — <b>20</b>.",
          starter: "let person = {\n  \n};\n", hint: 'let person = { name: "Нигина", age: 20 };', solution: 'let person = {\n  name: "Нигина",\n  age: 20\n};\n',
          check: function (c, R) { return R.run(c + "\nconsole.log(typeof person, person.name, person.age);").then(function (r) { return [["person объект аст", !r.err && /^object /.test(r.out[r.out.length - 1] || "")], ["name = Нигина ва age = 20", !r.err && r.out[r.out.length - 1] === "object Нигина 20"]]; }); } },
        { title: "Вазифаи 2: иваз кардан", text: "Бо <code>person.age = ...</code> синну солро <b>1 зиёд</b> кунед (бояд 21 шавад) ва нишон диҳед.",
          starter: 'let person = { name: "Нигина", age: 20 };\n\n// синну солро 1 зиёд кунед ва нишон диҳед\n', hint: "person.age = person.age + 1; console.log(person.age);",
          solution: 'let person = { name: "Нигина", age: 20 };\nperson.age = person.age + 1;\nconsole.log(person.age);\n',
          check: function (c, R) { return R.run(c).then(function (r) { return [["Синну сол иваз шуд (person.age = …)", /person\.age\s*=/.test(c)], ["Дар натиҷа 21 аст", !r.err && r.out[r.out.length - 1] === "21"]]; }); } },
        { title: "Вазифаи 3: хусусияти нав", text: "Ба объект хусусияти <code>city</code>-ро бо қимати «<b>Душанбе</b>» илова кунед ва онро нишон диҳед.",
          starter: 'let person = { name: "Нигина", age: 20 };\n\n// city илова кунед\n', hint: 'person.city = "Душанбе"; console.log(person.city);',
          solution: 'let person = { name: "Нигина", age: 20 };\nperson.city = "Душанбе";\nconsole.log(person.city);\n',
          check: function (c, R) { return R.run(c).then(function (r) { return [["city дар код ҳаст", /\bcity\b/.test(c)], ["Дар натиҷа «Душанбе» аст", !r.err && r.out[r.out.length - 1] === "Душанбе"]]; }); } }
      ] },
    { id: "l7", tab: "7 · Хатогиро ёб", tag: "ДАРСИ 7",
      theory: "Дебаг — ёфтан ва ислоҳи хато. Хатогӣ — муқаррарӣ аст! <b>Қадамҳо:</b> 1) хатои сурхро бихонед, 2) сатри нишондодашударо бубинед, 3) ишораи 💡-ро истифода баред. Дар ин ҷо коди хатодор ҳаст — ислоҳ кунед!",
      tasks: [
        { title: "Хатои 1: қавси гумшуда", text: "Барнома хато медиҳад. Чӣ гум шудааст? Ислоҳ кунед, то «<b>Гарм аст</b>» нишон дода шавад.",
          starter: 'let temperature = 34;\nif (temperature > 30) {\n  console.log("Гарм аст");\n} else {\n  console.log("Хунук аст");\n', hint: "Дар охир қавси } намерасад — онро илова кунед.",
          solution: 'let temperature = 34;\nif (temperature > 30) {\n  console.log("Гарм аст");\n} else {\n  console.log("Хунук аст");\n}\n',
          check: function (c, R) { return R.run(c).then(function (r) { return [["Хато нест", !r.err], ["Натиҷа: «Гарм аст»", !r.err && r.out.join("|") === "Гарм аст"]]; }); } },
        { title: "Хатои 2: давре, ки хотима намеёбад", text: "Давр бояд 1, 2, 3-ро нависад, вале «овезон» мешавад (♾️). Ислоҳ кунед.",
          starter: "for (let i = 1; i <= 3; ) {\n  console.log(i);\n}\n", hint: "Қадам (i++) фаромӯш шудааст.", solution: "for (let i = 1; i <= 3; i++) {\n  console.log(i);\n}\n",
          check: function (c, R) { return R.run(c).then(function (r) { return [["Барнома қатъ мешавад (бе ♾️)", !r.timeout], ["Натиҷа: 1, 2, 3", !r.timeout && !r.err && r.out.join(",") === "1,2,3"]]; }); } },
        { title: "Хатои 3: const-ро иваз кардан", text: "Барнома бояд ҷамъи 1 то 5-ро нависад (<b>15</b>), вале хато медиҳад. Ислоҳ кунед.",
          starter: "const total = 0;\nfor (let i = 1; i <= 5; i++) {\n  total = total + i;\n}\nconsole.log(total);\n", hint: "const-ро иваз кардан мумкин нест. Ба ҷои он let нависед.", solution: "let total = 0;\nfor (let i = 1; i <= 5; i++) {\n  total = total + i;\n}\nconsole.log(total);\n",
          check: function (c, R) { return R.run(c).then(function (r) { return [["Хато нест", !r.err], ["Натиҷа: 15", !r.err && r.out[r.out.length - 1] === "15"]]; }); } },
        { title: "Хатои 4: шумораи нодуруст", text: "Барнома бояд «<b>тухм</b>»-ро нишон диҳад, вале <code>undefined</code> менависад. Шумора аз 0 оғоз мешавад! Ислоҳ кунед.",
          starter: 'let shopping = ["нон", "шир", "тухм"];\nconsole.log(shopping[3]);\n', hint: "«тухм» сеюм аст, шумораи он 2 аст.", solution: 'let shopping = ["нон", "шир", "тухм"];\nconsole.log(shopping[2]);\n',
          check: function (c, R) { return R.run(c).then(function (r) { return [["Хато нест", !r.err], ["Натиҷа: «тухм»", !r.err && r.out.join("|") === "тухм"]]; }); } }
      ] }
  ];
