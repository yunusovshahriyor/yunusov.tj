import { Container } from "../ui/Container";
import { SectionHeading } from "../ui/SectionHeading";
import { Reveal } from "../ui/Reveal";

const points = [
  {
    title: "Чем занимаюсь",
    text: "Разрабатываю Android-приложения, мобильные приложения, сайты и сайты на Tilda, а также помогаю превращать идеи в цифровые продукты.",
  },
  {
    title: "Как работаю",
    text: "Работаю онлайн с клиентами и создаю IT-решения для предпринимателей, малого и среднего бизнеса.",
  },
  {
    title: "Что использую",
    text: "В работе применяю автоматизацию и AI-инструменты, чтобы разрабатывать продукты быстрее и качественнее.",
  },
];

export function About() {
  return (
    <section id="about" className="py-20 sm:py-28">
      <Container className="flex flex-col gap-12">
        <SectionHeading
          eyebrow="Обо мне"
          title="Разработчик цифровых продуктов для бизнеса"
          description="Меня зовут Shahriyor Yunusov. Я программист и IT-фрилансер, помогаю предпринимателям и компаниям создавать мобильные приложения, сайты и цифровые продукты."
        />

        <div className="grid grid-cols-1 gap-6 sm:grid-cols-3">
          {points.map((point, i) => (
            <Reveal key={point.title} delay={i * 100}>
              <div className="flex h-full flex-col gap-3 rounded-2xl border border-border bg-surface p-6">
                <h3 className="text-base font-semibold text-foreground">
                  {point.title}
                </h3>
                <p className="text-sm leading-relaxed text-muted">{point.text}</p>
              </div>
            </Reveal>
          ))}
        </div>
      </Container>
    </section>
  );
}
