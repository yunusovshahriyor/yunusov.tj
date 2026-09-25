import { Container } from "../ui/Container";
import { Reveal } from "../ui/Reveal";
import { ContactForm } from "../ContactForm";
import { contacts } from "@/data/contacts";
import { TelegramIcon, InstagramIcon, YoutubeIcon, EmailIcon } from "../ui/SocialIcons";

const socials = [
  { key: "telegram" as const, Icon: TelegramIcon },
  { key: "instagram" as const, Icon: InstagramIcon },
  { key: "youtube" as const, Icon: YoutubeIcon },
  { key: "email" as const, Icon: EmailIcon },
];

export function Contact() {
  return (
    <section id="contact" className="py-20 sm:py-28">
      <Container className="grid grid-cols-1 gap-12 lg:grid-cols-2 lg:gap-16">
        <Reveal className="flex flex-col gap-8">
          <div className="flex flex-col gap-4">
            <span className="text-sm font-medium uppercase tracking-wide text-accent">
              Контакты
            </span>
            <h2 className="text-3xl font-semibold tracking-tight text-balance sm:text-4xl">
              Есть идея проекта? Давайте обсудим её.
            </h2>
            <p className="max-w-md text-base leading-relaxed text-muted">
              Заполните форму или напишите напрямую — отвечаю лично.
            </p>
          </div>

          <div className="flex flex-col gap-3">
            {socials.map(({ key, Icon }) => (
              <a
                key={key}
                href={contacts[key].href}
                target={key === "email" ? undefined : "_blank"}
                rel="noopener noreferrer"
                className="group flex w-fit items-center gap-3 text-sm text-foreground transition-colors hover:text-accent"
              >
                <span className="flex h-10 w-10 items-center justify-center rounded-full border border-border transition-colors group-hover:border-accent">
                  <Icon className="h-[18px] w-[18px]" />
                </span>
                {contacts[key].label}
              </a>
            ))}
          </div>
        </Reveal>

        <Reveal delay={100}>
          <div className="rounded-3xl border border-border p-6 sm:p-8">
            <ContactForm />
          </div>
        </Reveal>
      </Container>
    </section>
  );
}
