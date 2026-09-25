export type TechCategory = {
  title: string;
  items: string[];
};

// Список легко редактируется: добавляйте или убирайте элементы в массиве items.
// Указывайте только те инструменты, которыми реально владеете.
export const techCategories: TechCategory[] = [
  {
    title: "Mobile Development",
    items: ["Android"],
  },
  {
    title: "Web Development",
    items: [],
  },
  {
    title: "No-code / Tilda",
    items: ["Tilda"],
  },
  {
    title: "Backend / Database",
    items: [],
  },
  {
    title: "AI tools",
    items: ["Автоматизация и AI в разработке"],
  },
];
