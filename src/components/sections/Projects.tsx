import Image from "next/image";
import { Container } from "../ui/Container";
import { SectionHeading } from "../ui/SectionHeading";
import { Reveal } from "../ui/Reveal";
import { projects } from "@/data/projects";
import { assetPath } from "@/lib/basePath";

export function Projects() {
  return (
    <section id="projects" className="py-20 sm:py-28">
      <Container className="flex flex-col gap-12">
        <SectionHeading
          eyebrow="Проекты"
          title="Реальные продукты, которые я разработал"
          description="Мобильные приложения в Google Play и сайты, которые я разработал."
        />

        <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
          {projects.map((project, i) => (
            <Reveal key={project.slug} delay={(i % 3) * 100} className="h-full">
              <article className="flex h-full flex-col overflow-hidden rounded-2xl border border-border bg-background transition-all duration-300 hover:-translate-y-1 hover:shadow-lg hover:shadow-black/5">
                <div className="relative h-40 w-full border-b border-border bg-surface">
                  <Image
                    src={assetPath(project.banner)}
                    alt={`Скриншот приложения ${project.name}`}
                    fill
                    sizes="(min-width: 1024px) 33vw, (min-width: 640px) 50vw, 100vw"
                    className="object-cover"
                  />
                </div>

                <div className="flex flex-1 flex-col gap-4 p-6">
                  <div className="flex items-start gap-3">
                    <div className="relative h-11 w-11 shrink-0 overflow-hidden rounded-xl border border-border">
                      <Image
                        src={assetPath(project.icon)}
                        alt={`Иконка приложения ${project.name}`}
                        fill
                        sizes="44px"
                        className="object-cover"
                      />
                    </div>
                    <div className="flex-1">
                      <h3 className="text-base font-semibold leading-tight text-foreground">
                        {project.name}
                      </h3>
                      <p className="mt-0.5 text-xs text-muted">
                        {project.rating
                          ? `${project.category} · ★ ${project.rating}`
                          : project.category}
                      </p>
                    </div>
                  </div>

                  <p className="text-sm text-muted">{project.summary}</p>

                  <dl className="flex flex-col gap-3 text-sm">
                    <div>
                      <dt className="font-medium text-foreground">Проблема</dt>
                      <dd className="text-muted">{project.problem}</dd>
                    </div>
                    <div>
                      <dt className="font-medium text-foreground">Решение</dt>
                      <dd className="text-muted">{project.solution}</dd>
                    </div>
                    <div>
                      <dt className="font-medium text-foreground">Моя роль</dt>
                      <dd className="text-muted">{project.role}</dd>
                    </div>
                    <div>
                      <dt className="font-medium text-foreground">Технологии</dt>
                      <dd className="text-muted">{project.technologies}</dd>
                    </div>
                  </dl>

                  <div className="mt-auto pt-2">
                    <a
                      href={project.link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-sm font-medium text-accent hover:text-accent-strong"
                    >
                      {project.link.includes("play.google.com")
                        ? "Открыть в Google Play →"
                        : "Открыть сайт →"}
                    </a>
                  </div>
                </div>
              </article>
            </Reveal>
          ))}
        </div>
      </Container>
    </section>
  );
}
