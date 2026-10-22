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
    items: ["HTML", "CSS", "JavaScript", "React", "Next.js", "Tailwind CSS"],
  },
  {
    title: "Backend / Database",
    items: ["Next.js API Routes"],
  },
  {
    title: "AI tools",
    items: ["Разработка с помощью AI-инструментов"],
  },
];
