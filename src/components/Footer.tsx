import Link from "next/link";
import { Container } from "./ui/Container";
import { contacts } from "@/data/contacts";
import { TelegramIcon, InstagramIcon, YoutubeIcon, EmailIcon } from "./ui/SocialIcons";

const socials = [
  { key: "telegram" as const, Icon: TelegramIcon },
  { key: "instagram" as const, Icon: InstagramIcon },
  { key: "youtube" as const, Icon: YoutubeIcon },
  { key: "email" as const, Icon: EmailIcon },
];

export function Footer() {
  const year = new Date().getFullYear();

  return (
    <footer className="border-t border-border">
      <Container className="flex flex-col gap-8 py-12 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <p className="text-base font-semibold text-foreground">Shahriyor Yunusov</p>
          <p className="mt-1 text-sm text-muted">Программист и IT-фрилансер</p>
        </div>

        <div className="flex flex-wrap items-center gap-5">
          {socials.map(({ key, Icon }) => (
            <a
              key={key}
              href={contacts[key].href}
              target={key === "email" ? undefined : "_blank"}
              rel="noopener noreferrer"
              className="flex items-center gap-2 text-sm text-muted transition-colors hover:text-accent"
              aria-label={contacts[key].label}
            >
              <Icon className="h-[18px] w-[18px]" />
              <span className="hidden sm:inline">{contacts[key].label}</span>
            </a>
          ))}
        </div>

        <p className="text-sm text-muted">
          © {year} Shahriyor Yunusov.{" "}
          <Link href="#top" className="hover:text-accent">
            Наверх
          </Link>
        </p>
      </Container>
    </footer>
  );
}
