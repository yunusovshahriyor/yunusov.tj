import { Container } from "../ui/Container";
import { SectionHeading } from "../ui/SectionHeading";
import { Reveal } from "../ui/Reveal";
import { blogTopics } from "@/data/blogTopics";

export function Blog() {
  return (
    <section id="blog" className="py-20 sm:py-28">
      <Container className="flex flex-col gap-8">
        <SectionHeading
          eyebrow="Блог"
          title="Скоро здесь появятся статьи о разработке и IT"
          description="Буду делиться опытом программирования, разработки приложений, создания сайтов, работы с AI и фриланса."
        />

        <Reveal>
          <div className="flex flex-wrap gap-3">
            {blogTopics.map((topic) => (
              <span
                key={topic}
                className="rounded-full border border-border bg-surface px-4 py-2 text-sm text-muted"
              >
                {topic}
              </span>
            ))}
          </div>
        </Reveal>
      </Container>
    </section>
  );
}
