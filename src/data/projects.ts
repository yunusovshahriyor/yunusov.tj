export type Project = {
  slug: string;
  name: string;
  summary: string;
  problem: string;
  solution: string;
  role: string;
  technologies: string;
  link: string | null;
  audience: string;
};

export const projects: Project[] = [
  {
    slug: "zabondon",
    name: "ZabonDon",
    summary:
      "Мобильное приложение для изучения русского и английского языков с переводом слов на таджикский и узбекский.",
    problem:
      "Носителям таджикского и узбекского языков сложно изучать русский и английский без перевода на понятный родной язык.",
    solution:
      "ZabonDon даёт перевод слов на таджикский и узбекский прямо в процессе изучения русского и английского, делая обучение понятным и доступным.",
    role: "[Добавить роль в проекте]",
    technologies: "[Добавить технологии]",
    link: null,
    audience: "Носители таджикского и узбекского языков",
  },
  {
    slug: "markazi-khirad",
    name: "Markazi Khirad",
    summary:
      "Цифровая платформа для электронных книг: поиск, покупка и чтение в одном приложении.",
    problem:
      "Читателям нужен удобный способ находить, покупать и читать электронные книги, не переключаясь между разными сервисами.",
    solution:
      "Markazi Khirad объединяет поиск, покупку и чтение книг в единой платформе.",
    role: "[Добавить роль в проекте]",
    technologies: "[Добавить технологии]",
    link: null,
    audience: "Читатели электронных книг",
  },
  {
    slug: "kitobkhonai-millioner",
    name: "Kitobkhonai Millioner",
    summary: "Онлайн-библиотека с книгами разных направлений.",
    problem:
      "Читателям нужен доступ к большой библиотеке книг разных направлений в одном месте.",
    solution:
      "Kitobkhonai Millioner — онлайн-библиотека, где собраны книги разных жанров и направлений.",
    role: "[Добавить роль в проекте]",
    technologies: "[Добавить технологии]",
    link: null,
    audience: "Читатели онлайн-библиотек",
  },
];
