import { Container } from "../ui/Container";
import { SectionHeading } from "../ui/SectionHeading";
import { Reveal } from "../ui/Reveal";
import { techCategories } from "@/data/technologies";

export function Technologies() {
  return (
    <section id="technologies" className="py-20 sm:py-28">
      <Container className="flex flex-col gap-12">
        <SectionHeading
          eyebrow="Технологии"
          title="Инструменты, которыми я пользуюсь"
        />

        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-5">
          {techCategories.map((category, i) => (
            <Reveal key={category.title} delay={i * 60}>
              <div className="flex h-full flex-col gap-4 rounded-2xl bg-surface p-6">
                <h3 className="text-sm font-semibold text-foreground">
                  {category.title}
                </h3>
                <div className="flex flex-wrap gap-2">
                  {category.items.length > 0 ? (
                    category.items.map((item) => (
                      <span
                        key={item}
                        className="rounded-full border border-border bg-background px-3 py-1.5 text-xs text-muted"
                      >
                        {item}
                      </span>
                    ))
                  ) : (
                    <span className="rounded-full border border-dashed border-border px-3 py-1.5 text-xs text-muted/70">
                      Список пополняется
                    </span>
                  )}
                </div>
              </div>
            </Reveal>
          ))}
        </div>
      </Container>
    </section>
  );
}
