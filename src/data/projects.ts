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
    slug: "business-network",
    name: "Бизнес дар шабакаҳои иҷтимоӣ",
    category: "Книги и справочники",
    rating: "4,0",
    summary:
      "Образовательное приложение о заработке и продвижении бизнеса в социальных сетях.",
    problem:
      "Многие пользователи проводят время в социальных сетях, не используя их как инструмент для заработка.",
    solution:
      "Приложение учит зарабатывать и продвигать бизнес через социальные сети.",
    role: "Разработчик",
    technologies: "Android",
    link: "https://play.google.com/store/apps/details?id=com.programs.businessNetwork",
    icon: "/projects/business-network-icon.webp",
    banner: "/projects/business-network-banner.webp",
  },
  {
    slug: "manizha-deutsch",
    name: "Manizha Deutsch",
    category: "Образование",
    rating: "3,9",
    summary:
      "Приложение для изучения немецкого языка с нуля на таджикском языке.",
    problem:
      "Таджикоязычным пользователям сложно найти понятный курс немецкого языка на родном языке.",
    solution:
      "Manizha Deutsch предлагает интерактивные уроки немецкого языка для всех уровней — от начинающего до продвинутого.",
    role: "Разработчик",
    technologies: "Android",
    link: "https://play.google.com/store/apps/details?id=tj.manizha.deutsch",
    icon: "/projects/manizha-deutsch-icon.webp",
    banner: "/projects/manizha-deutsch-banner.webp",
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
    slug: "muvaffaq-bosh",
    name: "Muvaffaq Bosh Academy",
    category: "Книги и справочники",
    rating: "4,7",
    summary:
      "Аудиокниги, статьи и курсы по финансам и личностному развитию на таджикском языке.",
    problem:
      "Таджикоязычной аудитории не хватает качественного контента по финансовой грамотности и личностному росту в одном месте.",
    solution:
      "Muvaffaq Bosh Academy собирает статьи, подкасты, аудиокниги и курсы по бизнесу, финансам и личностному развитию на таджикском языке.",
    role: "Разработчик",
    technologies: "Android",
    link: "https://play.google.com/store/apps/details?id=tjk.programs.audiobookmuvaffaqbosh",
    icon: "/projects/muvaffaq-bosh-icon.webp",
    banner: "/projects/muvaffaq-bosh-banner.webp",
  },
  {
    slug: "deutschbook",
    name: "Deutsch — бо забони тоҷикӣ",
    category: "Книги и справочники",
    rating: "4,0",
    summary:
      "Интерактивный самоучитель немецкого языка с нуля на таджикском языке.",
    problem:
      "Изучающим немецкий с нуля нужен понятный самоучитель с объяснениями на родном языке.",
    solution:
      "Приложение проводит от базовой фонетики до более сложных грамматических конструкций, с упражнениями в каждой главе.",
    role: "Разработчик",
    technologies: "Android",
    link: "https://play.google.com/store/apps/details?id=tjk.programs.deutschbook",
    icon: "/projects/deutschbook-icon.webp",
    banner: "/projects/deutschbook-banner.webp",
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
