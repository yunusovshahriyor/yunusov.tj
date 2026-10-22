export type Course = {
  slug: string;
  title: string;
  description: string;
  image: string;
};

// Курсы ещё не запущены — это темы, которые планируются.
// Иллюстрации лежат в public/courses.
export const courses: Course[] = [
  {
    slug: "ai-development",
    title: "Разработка с AI-инструментами",
    description:
      "Как использовать AI-инструменты в работе программиста: от идеи и планирования до готового кода.",
    image: "/courses/ai-development.svg",
  },
  {
    slug: "websites-with-ai",
    title: "Создание сайтов с помощью AI",
    description:
      "Как создавать современные сайты с помощью AI — от структуры и дизайна до публикации в интернете.",
    image: "/courses/websites-with-ai.svg",
  },
  {
    slug: "mobile-apps-with-ai",
    title: "Создание мобильных приложений с помощью AI",
    description:
      "Как разрабатывать мобильные приложения с помощью AI — от идеи до публикации в Google Play.",
    image: "/courses/mobile-apps-with-ai.svg",
  },
];
