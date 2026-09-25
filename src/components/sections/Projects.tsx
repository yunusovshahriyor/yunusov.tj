import { Container } from "../ui/Container";
import { SectionHeading } from "../ui/SectionHeading";
import { Reveal } from "../ui/Reveal";
import { ProjectImagePlaceholder } from "../ui/ImagePlaceholder";
import { projects } from "@/data/projects";

export function Projects() {
  return (
    <section id="projects" className="py-20 sm:py-28">
      <Container className="flex flex-col gap-12">
        <SectionHeading
          eyebrow="Проекты"
          title="Реальные продукты, которые я разработал"
          description="Мобильные приложения и цифровые платформы, над которыми я работал."
        />

        <div className="grid grid-cols-1 gap-8 lg:grid-cols-3">
          {projects.map((project, i) => (
            <Reveal key={project.slug} delay={i * 100} className="h-full">
              <article className="flex h-full flex-col overflow-hidden rounded-2xl border border-border bg-background transition-all duration-300 hover:-translate-y-1 hover:shadow-lg hover:shadow-black/5">
                <ProjectImagePlaceholder name={project.name} className="h-48 w-full" />

                <div className="flex flex-1 flex-col gap-4 p-6">
                  <div>
                    <h3 className="text-lg font-semibold text-foreground">
                      {project.name}
                    </h3>
                    <p className="mt-1 text-sm text-muted">{project.summary}</p>
                  </div>

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
                    {project.link ? (
                      <a
                        href={project.link}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-sm font-medium text-accent hover:text-accent-strong"
                      >
                        Смотреть проект →
                      </a>
                    ) : (
                      <span className="text-sm text-muted">[Добавить ссылку]</span>
                    )}
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
