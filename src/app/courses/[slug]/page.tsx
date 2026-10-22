import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { notFound } from "next/navigation";
import { Container } from "@/components/ui/Container";
import { Button } from "@/components/ui/Button";
import { courses, getCourse } from "@/data/courses";
import { assetPath } from "@/lib/basePath";

type Props = { params: Promise<{ slug: string }> };

export const dynamicParams = false;

export function generateStaticParams() {
  return courses.map((c) => ({ slug: c.slug }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const course = getCourse(slug);
  if (!course) return {};
  return { title: course.title, description: course.description };
}

function List({ title, items }: { title: string; items: string[] }) {
  return (
    <div className="flex flex-col gap-3 rounded-2xl border border-border p-6">
      <h3 className="text-base font-semibold text-foreground">{title}</h3>
      <ul className="flex flex-col gap-2 text-sm leading-relaxed text-muted">
        {items.map((item) => (
          <li key={item} className="flex gap-2">
            <span aria-hidden className="mt-2 size-1.5 shrink-0 rounded-full bg-accent" />
            <span>{item}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default async function CoursePage({ params }: Props) {
  const { slug } = await params;
  const course = getCourse(slug);
  if (!course) notFound();

  const index = courses.findIndex((c) => c.slug === slug);
  const first = courses[0];

  return (
    <section className="py-12 sm:py-20">
      <Container className="flex flex-col gap-12">
        <div className="flex flex-col gap-6">
          <Link href="/#courses" className="text-sm text-muted hover:text-accent">
            ← Все курсы
          </Link>
          <div className="grid items-center gap-8 md:grid-cols-2">
            <div className="flex flex-col gap-4">
              <span className="text-xs font-medium uppercase tracking-wide text-muted">
                Курс {String(index + 1).padStart(2, "0")} · {course.level} · Скоро
              </span>
              <h1 className="text-3xl font-semibold leading-tight text-balance text-foreground sm:text-4xl">
                {course.title}
              </h1>
              <p className="leading-relaxed text-muted">{course.description}</p>
              <p className="rounded-xl bg-accent-soft p-4 text-sm leading-relaxed text-accent-strong">
                <strong>Что нужно для старта: </strong>
                {course.prerequisite}
                {index > 0 && (
                  <>
                    {" "}
                    <Link href={`/courses/${first.slug}`} className="underline">
                      Перейти к курсу «{first.title}»
                    </Link>
                  </>
                )}
              </p>
            </div>
            <div className="relative aspect-[16/10] w-full overflow-hidden rounded-2xl border border-border bg-accent-soft">
              <Image
                src={assetPath(course.image)}
                alt={`Иллюстрация к курсу «${course.title}»`}
                fill
                priority
                sizes="(min-width: 768px) 50vw, 100vw"
                className="object-cover"
              />
            </div>
          </div>
        </div>

        {course.goal && (
          <div className="flex flex-col gap-2">
            <h2 className="text-xl font-semibold text-foreground">Цель курса</h2>
            <p className="max-w-3xl leading-relaxed text-muted">{course.goal}</p>
          </div>
        )}

        {course.modules ? (
          <div className="flex flex-col gap-6">
            <h2 className="text-xl font-semibold text-foreground">Программа курса</h2>
            <ol className="grid gap-4 md:grid-cols-2">
              {course.modules.map((m, i) => (
                <li key={m.title} className="flex flex-col gap-3 rounded-2xl border border-border p-6">
                  <span className="text-xs font-medium uppercase tracking-wide text-accent">
                    Модуль {i + 1}
                  </span>
                  <h3 className="font-semibold text-foreground">{m.title}</h3>
                  <ul className="flex flex-col gap-2 text-sm leading-relaxed text-muted">
                    {m.items.map((item) => (
                      <li key={item} className="flex gap-2">
                        <span aria-hidden className="mt-2 size-1.5 shrink-0 rounded-full bg-border" />
                        <span>{item}</span>
                      </li>
                    ))}
                  </ul>
                </li>
              ))}
            </ol>
          </div>
        ) : (
          <p className="rounded-2xl border border-dashed border-border p-6 text-sm text-muted">
            Подробная программа курса ещё готовится.
          </p>
        )}

        {(course.knowledge || course.skills || course.mindset) && (
          <div className="flex flex-col gap-6">
            <h2 className="text-xl font-semibold text-foreground">
              Что вы получите по итогам курса
            </h2>
            <div className="grid gap-4 md:grid-cols-3">
              {course.knowledge && <List title="Знания" items={course.knowledge} />}
              {course.skills && <List title="Навыки" items={course.skills} />}
              {course.mindset && <List title="Мышление" items={course.mindset} />}
            </div>
          </div>
        )}

        <div>
          <Button href="/#contact">Узнать первым о запуске</Button>
        </div>
      </Container>
    </section>
  );
}
