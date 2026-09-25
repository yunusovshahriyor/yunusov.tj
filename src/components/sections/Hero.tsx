import { Container } from "../ui/Container";
import { Button } from "../ui/Button";
import { PhotoPlaceholder } from "../ui/ImagePlaceholder";

export function Hero() {
  return (
    <section id="top" className="pt-16 pb-20 sm:pt-24 sm:pb-28">
      <Container className="grid grid-cols-1 items-center gap-12 lg:grid-cols-[1.1fr_0.9fr] lg:gap-16">
        <div className="flex flex-col items-start gap-6">
          <span className="rounded-full border border-border bg-surface px-4 py-1.5 text-sm text-muted">
            Shahriyor Yunusov
          </span>

          <h1 className="text-4xl font-semibold tracking-tight text-balance sm:text-5xl lg:text-6xl">
            Создаю мобильные приложения и сайты, которые помогают бизнесу
            развиваться
          </h1>

          <p className="max-w-xl text-lg leading-relaxed text-muted">
            Я программист и IT-фрилансер. Разрабатываю Android-приложения,
            сайты, в том числе на Tilda, и цифровые продукты для
            предпринимателей и бизнеса.
          </p>

          <div className="flex flex-wrap items-center gap-4 pt-2">
            <Button href="#contact">Обсудить проект</Button>
            <Button href="#projects" variant="secondary">
              Посмотреть проекты
            </Button>
          </div>
        </div>

        <PhotoPlaceholder className="aspect-[4/5] w-full rounded-3xl" />
      </Container>
    </section>
  );
}
