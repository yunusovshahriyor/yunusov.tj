import { Container } from "../ui/Container";
import { Reveal } from "../ui/Reveal";
import { Button } from "../ui/Button";

export function Courses() {
  return (
    <section id="courses" className="py-20 sm:py-28">
      <Container>
        <Reveal>
          <div className="flex flex-col items-start gap-6 rounded-3xl bg-surface p-8 sm:p-12">
            <span className="rounded-full border border-border bg-background px-4 py-1.5 text-sm text-muted">
              Курсы
            </span>
            <h2 className="max-w-2xl text-3xl font-semibold tracking-tight text-balance sm:text-4xl">
              Обучаю программированию и делюсь практическим опытом разработки
            </h2>
            <p className="max-w-xl text-base leading-relaxed text-muted">
              Образовательное направление находится в разработке. Здесь появятся
              курсы и материалы по программированию, основанные на реальном
              опыте создания мобильных приложений и сайтов.
            </p>
            <Button href="#contact" variant="secondary">
              Узнать первым о запуске
            </Button>
          </div>
        </Reveal>
      </Container>
    </section>
  );
}
