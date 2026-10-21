export type Project = {
  slug: string;
  name: string;
  category: string;
  rating: string;
  summary: string;
  problem: string;
  solution: string;
  role: string;
  technologies: string;
  link: string;
  icon: string;
  banner: string;
};

// Данные взяты со страницы разработчика в Google Play:
// https://play.google.com/store/apps/dev?id=8979338274923782952
// Иконки и обложки лежат в public/projects.
export const projects: Project[] = [
  {
    slug: "zabondon",
    name: "ZabonDon",
    category: "Образование",
    rating: "4,4",
    summary:
      "Мобильное приложение для изучения русского и английского языков с переводом слов на таджикский и узбекский.",
    problem:
      "Носителям таджикского и узбекского языков сложно изучать русский и английский без перевода на понятный родной язык.",
    solution:
      "ZabonDon даёт перевод слов на таджикский и узбекский прямо в процессе изучения русского и английского через интерактивные уроки и карточки слов.",
    role: "Разработчик",
    technologies: "Android",
    link: "https://play.google.com/store/apps/details?id=com.zabondon.app",
    icon: "/projects/zabondon-icon.webp",
    banner: "/projects/zabondon-banner.webp",
  },
  {
    slug: "khirad",
    name: "Хирад",
    category: "Книги и справочники",
    rating: "4,5",
    summary:
      "Цифровая библиотека с тысячами электронных и аудиокниг на таджикском языке.",
    problem:
      "Таджикоязычным читателям сложно найти классическую и современную литературу на родном языке в одном месте.",
    solution:
      "Хирад собирает тысячи электронных и аудиокниг — от классиков персо-таджикской литературы до мировых бестселлеров по саморазвитию и финансам — переведённых на таджикский язык, с возможностью читать и слушать.",
    role: "Разработчик",
    technologies: "Android",
    link: "https://play.google.com/store/apps/details?id=com.khirad.ebooks",
    icon: "/projects/khirad-icon.webp",
    banner: "/projects/khirad-banner.webp",
  },
  {
    slug: "millionaires-book",
    name: "Китобхонаи Миллионер",
    category: "Книги и справочники",
    rating: "4,6",
    summary:
      "Онлайн-библиотека книг по бизнесу, личностному развитию и финансовой грамотности на таджикском языке.",
    problem:
      "Читателям, стремящимся к финансовой грамотности и личностному росту, сложно найти качественную бизнес-литературу на таджикском языке.",
    solution:
      "Китобхонаи Миллионер собирает книги ведущих мировых авторов по бизнесу, личностному развитию и финансам, переведённые на таджикский язык.",
    role: "Разработчик",
    technologies: "Android",
    link: "https://play.google.com/store/apps/details?id=tjk.programs.millionairesBook",
    icon: "/projects/millionaires-book-icon.webp",
    banner: "/projects/millionaires-book-banner.webp",
  },
  {
    slug: "quiz-patent",
    name: "Тесты ПАТЕНТ, РВП, ВНЖ",
    category: "Образование",
    rating: "4,5",
    summary:
      "Тренажёр для подготовки к экзаменам на патент, РВП и ВНЖ по русскому языку.",
    problem:
      "Мигрантам нужно самостоятельно и системно готовиться к экзамену по русскому языку для получения патента, РВП или ВНЖ.",
    solution:
      "Приложение даёт тренировочные варианты по каждому направлению, задания в разных форматах и повторение ошибок для закрепления материала.",
    role: "Разработчик",
    technologies: "Android",
    link: "https://play.google.com/store/apps/details?id=com.e2.quizapp",
    icon: "/projects/quiz-patent-icon.webp",
    banner: "/projects/quiz-patent-banner.webp",
  },
  {
    slug: "smartcode-translator",
    name: "Переводчик Школа-LE",
    category: "Образование",
    rating: "4,7",
    summary:
      "Переводчик текста, фото и речи между таджикским, русским, английским и другими языками.",
    problem:
      "Ученикам и изучающим языки нужен быстрый перевод текста, фотографий документов и устной речи в одном приложении.",
    solution:
      "Переводчик «Школа-LE» переводит текст в реальном времени, распознаёт текст с фото и переводит речь с озвучиванием результата.",
    role: "Разработчик",
    technologies: "Android",
    link: "https://play.google.com/store/apps/details?id=tj.smartcode.translator",
    icon: "/projects/smartcode-translator-icon.webp",
    banner: "/projects/smartcode-translator-banner.webp",
  },
  {
    slug: "rustjk-dict",
    name: "Русско-таджикский словарь",
    category: "Книги и справочники",
    rating: "4,6",
    summary:
      "Русско-таджикский словарь с быстрым доступом к тысячам слов и выражений.",
    problem:
      "Пользователям нужен удобный словарь для перевода повседневной и специализированной лексики между русским и таджикским языками.",
    solution:
      "Словарь даёт быстрый доступ к тысячам слов и фраз для перевода и изучения языка.",
    role: "Разработчик",
    technologies: "Android",
    link: "https://play.google.com/store/apps/details?id=tjk.programs.rustjk",
    icon: "/projects/rustjk-dict-icon.webp",
    banner: "/projects/rustjk-dict-banner.webp",
  },
];
