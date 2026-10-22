import Image from "next/image";
import Link from "next/link";
import { Container } from "../ui/Container";
import { SectionHeading } from "../ui/SectionHeading";
import { Reveal } from "../ui/Reveal";
import { courses } from "@/data/courses";
import { assetPath } from "@/lib/basePath";

export function Courses() {
  return (
    <section id="courses" className="py-20 sm:py-28">
      <Container className="flex flex-col gap-12">
        <SectionHeading
          eyebrow="Курсы"
          title="Обучаю программированию и делюсь практическим опытом разработки"
          description="Курсы находятся в разработке. Сначала — «Основы программирования», чтобы появилось понимание, как всё устроено, а затем курсы по разработке с AI, сайтам и мобильным приложениям, основанные на моём реальном опыте."
        />

        <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-4">
          {courses.map((course, i) => (
            <Reveal key={course.slug} delay={i * 100} className="h-full">
              <Link
                href={`/courses/${course.slug}`}
                className="block h-full focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent rounded-2xl"
              >
              <article className="group flex h-full flex-col overflow-hidden rounded-2xl border border-border bg-background transition-all duration-300 hover:-translate-y-1 hover:border-accent/40 hover:shadow-lg hover:shadow-black/5">
                <div className="relative aspect-[16/10] w-full overflow-hidden border-b border-border bg-accent-soft">
                  <Image
                    src={assetPath(course.image)}
                    alt={`Иллюстрация к курсу «${course.title}»`}
                    fill
                    sizes="(min-width: 1024px) 25vw, (min-width: 768px) 50vw, 100vw"
                    className="object-cover transition-transform duration-500 group-hover:scale-[1.03]"
                  />
                  <span className="absolute left-4 top-4 rounded-full bg-background/90 px-3 py-1 text-xs font-medium text-accent-strong shadow-sm">
                    Скоро
                  </span>
                </div>

                <div className="flex flex-1 flex-col gap-3 p-6">
                  <span className="text-xs font-medium uppercase tracking-wide text-muted">
                    Курс {String(i + 1).padStart(2, "0")}
                  </span>
                  <h3 className="text-lg font-semibold leading-snug text-balance text-foreground">
                    {course.title}
                  </h3>
                  <p className="text-sm leading-relaxed text-muted">
                    {course.description}
                  </p>
                </div>
              </article>
              </Link>
            </Reveal>
          ))}
        </div>

        <Reveal>
          <div className="flex flex-col items-start gap-6 rounded-3xl bg-foreground p-8 text-background sm:flex-row sm:items-center sm:justify-between sm:p-10">
            <div className="flex flex-col gap-2">
              <h3 className="text-xl font-semibold sm:text-2xl">
                Хотите узнать о запуске первыми?
              </h3>
              <p className="max-w-lg text-sm leading-relaxed text-background/70">
                Оставьте контакт — сообщу, когда откроется запись на курсы.
              </p>
            </div>
            <Link
              href="#contact"
              className="inline-flex shrink-0 items-center justify-center rounded-full bg-background px-6 py-3 text-sm font-medium text-foreground transition-all duration-300 hover:-translate-y-0.5 hover:bg-accent-soft focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent"
            >
              Узнать первым о запуске
            </Link>
          </div>
        </Reveal>
      </Container>
    </section>
  );
}
