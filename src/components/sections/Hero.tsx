import { Container } from "../ui/Container";
import { Button } from "../ui/Button";
import { Reveal } from "../ui/Reveal";
import { projects } from "@/data/projects";

const playApps = projects.filter((p) => p.link.includes("play.google.com")).length;

const facts = [
  `${playApps} приложений в Google Play`,
  "Android · сайты · AI",
  "Работаю онлайн с клиентами",
];

export function Hero() {
  return (
    <section id="top" className="relative isolate overflow-hidden pt-[calc(72px+3rem)] pb-24 sm:pt-[calc(72px+5rem)] sm:pb-32 lg:pt-[calc(72px+6rem)] lg:pb-40">
      <div aria-hidden="true" className="pointer-events-none absolute inset-0 -z-10">
        <div className="absolute inset-0 bg-gradient-to-b from-accent-soft/70 via-background to-background" />
        <div
          className="absolute inset-0 opacity-60 [background-image:radial-gradient(circle,#c9d4ec_1.2px,transparent_1.2px)] [background-size:28px_28px] [mask-image:radial-gradient(ellipse_70%_60%_at_50%_30%,black,transparent)]"
        />
        <div className="absolute -top-32 left-1/2 h-[28rem] w-[28rem] -translate-x-[85%] rounded-full bg-accent/15 blur-3xl" />
        <div className="absolute -top-20 left-1/2 h-[24rem] w-[24rem] translate-x-[15%] rounded-full bg-accent/10 blur-3xl" />
      </div>

      <Container className="flex flex-col items-center gap-8 text-center">
        <Reveal>
          <span className="inline-flex items-center gap-2 rounded-full border border-border bg-background/80 px-4 py-1.5 text-sm text-muted shadow-sm backdrop-blur">
            <span className="h-1.5 w-1.5 rounded-full bg-accent" />
            Shahriyor Yunusov
            <span className="hidden sm:inline"> · программист и IT-фрилансер</span>
          </span>
        </Reveal>

        <Reveal delay={80}>
          <h1 className="max-w-4xl text-4xl font-semibold tracking-tight text-balance sm:text-5xl lg:text-6xl">
            Создаю мобильные приложения и сайты, которые помогают бизнесу{" "}
            <span className="text-accent">развиваться</span>
          </h1>
        </Reveal>

        <Reveal delay={160}>
          <p className="max-w-2xl text-lg leading-relaxed text-muted">
            Разрабатываю Android-приложения, сайты и цифровые продукты для
            предпринимателей и бизнеса.
          </p>
        </Reveal>

        <Reveal delay={240}>
          <div className="flex flex-wrap items-center justify-center gap-4">
            <Button href="#contact">Обсудить проект</Button>
            <Button href="#projects" variant="secondary">
              Посмотреть проекты
            </Button>
          </div>
        </Reveal>

        <Reveal delay={320}>
          <ul className="mt-4 flex flex-wrap items-center justify-center gap-3">
            {facts.map((fact) => (
              <li
                key={fact}
                className="rounded-full border border-border bg-background/80 px-4 py-2 text-sm text-muted backdrop-blur"
              >
                {fact}
              </li>
            ))}
          </ul>
        </Reveal>
      </Container>
    </section>
  );
}
