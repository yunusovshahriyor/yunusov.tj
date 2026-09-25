import { Container } from "../ui/Container";
import { SectionHeading } from "../ui/SectionHeading";
import { Reveal } from "../ui/Reveal";
import { processSteps } from "@/data/process";

export function Process() {
  return (
    <section id="process" className="py-20 sm:py-28">
      <Container className="flex flex-col gap-12">
        <SectionHeading eyebrow="Как я работаю" title="Простой и понятный процесс" />

        <div className="grid grid-cols-1 gap-px overflow-hidden rounded-2xl border border-border bg-border sm:grid-cols-5">
          {processSteps.map((step, i) => (
            <Reveal key={step.number} delay={i * 80} className="h-full">
              <div className="flex h-full flex-col gap-3 bg-background p-6">
                <span className="text-sm font-semibold text-accent">
                  {step.number}
                </span>
                <h3 className="text-base font-semibold text-foreground">
                  {step.title}
                </h3>
                <p className="text-sm leading-relaxed text-muted">
                  {step.description}
                </p>
              </div>
            </Reveal>
          ))}
        </div>
      </Container>
    </section>
  );
}
