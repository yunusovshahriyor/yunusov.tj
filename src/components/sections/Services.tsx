import { Container } from "../ui/Container";
import { SectionHeading } from "../ui/SectionHeading";
import { Reveal } from "../ui/Reveal";
import { services } from "@/data/services";

export function Services() {
  return (
    <section id="services" className="py-20 sm:py-28">
      <Container className="flex flex-col gap-12">
        <SectionHeading
          eyebrow="Услуги"
          title="Чем я могу помочь вашему бизнесу"
          description="Основные направления, в которых я работаю с клиентами."
        />

        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
          {services.map((service, i) => (
            <Reveal key={service.title} delay={i * 80}>
              <div className="flex h-full flex-col gap-4 rounded-2xl border border-border p-7 transition-colors duration-300 hover:border-accent">
                <h3 className="text-xl font-semibold text-foreground">
                  {service.title}
                </h3>
                <p className="text-sm leading-relaxed text-muted">
                  {service.description}
                </p>
                <p className="text-sm leading-relaxed text-muted/90">
                  <span className="font-medium text-foreground">Решает: </span>
                  {service.problem}
                </p>
                <a
                  href="#contact"
                  className="mt-auto inline-flex w-fit items-center gap-1.5 pt-2 text-sm font-medium text-accent hover:text-accent-strong"
                >
                  Обсудить проект →
                </a>
              </div>
            </Reveal>
          ))}
        </div>
      </Container>
    </section>
  );
}
