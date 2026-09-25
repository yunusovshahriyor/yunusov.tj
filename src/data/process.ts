export type ProcessStep = {
  number: string;
  title: string;
  description: string;
};

export const processSteps: ProcessStep[] = [
  {
    number: "01",
    title: "Обсуждаем задачу",
    description: "Разбираемся, что нужно бизнесу и какой результат важен.",
  },
  {
    number: "02",
    title: "Определяем решение",
    description: "Подбираем формат продукта и подход, которые решат задачу.",
  },
  {
    number: "03",
    title: "Разрабатываю продукт",
    description: "Пишу код и собираю продукт по согласованному плану.",
  },
  {
    number: "04",
    title: "Тестируем",
    description: "Проверяю продукт на ошибки и удобство использования.",
  },
  {
    number: "05",
    title: "Запускаем",
    description: "Публикуем продукт и передаю его в работу заказчику.",
  },
];
