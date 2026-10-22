"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { Container } from "./ui/Container";

const navItems = [
  { href: "/#about", label: "Обо мне" },
  { href: "/#projects", label: "Проекты" },
  { href: "/#services", label: "Услуги" },
  { href: "/#technologies", label: "Технологии" },
  { href: "/#blog", label: "Блог" },
  { href: "/#contact", label: "Контакты" },
];

export function Header() {
  const [open, setOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 8);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  useEffect(() => {
    document.body.style.overflow = open ? "hidden" : "";
    return () => {
      document.body.style.overflow = "";
    };
  }, [open]);

  return (
    <header
      className={`sticky top-0 z-50 -mb-[72px] h-[72px] w-full border-b transition-all duration-300 ${
        scrolled
          ? "border-border/70 bg-background/70 shadow-sm shadow-black/[0.03] backdrop-blur-xl"
          : "border-transparent bg-transparent"
      }`}
    >
      <Container className="flex h-full items-center justify-between">
        <Link href="#top" className="text-base font-semibold tracking-tight text-foreground">
          Shahriyor Yunusov
        </Link>

        <nav className="hidden items-center gap-1 rounded-full border border-border bg-background/80 p-1 shadow-sm backdrop-blur md:flex">
          {navItems.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="rounded-full px-4 py-2 text-sm text-muted transition-colors hover:bg-accent-soft hover:text-accent-strong"
            >
              {item.label}
            </Link>
          ))}
        </nav>

        <Link
          href="#contact"
          className="hidden md:inline-flex items-center justify-center rounded-full bg-foreground px-5 py-2.5 text-sm font-medium text-background transition-colors hover:bg-accent-strong"
        >
          Обсудить проект
        </Link>

        <button
          type="button"
          onClick={() => setOpen((v) => !v)}
          aria-expanded={open}
          aria-label={open ? "Закрыть меню" : "Открыть меню"}
          className="md:hidden flex h-10 w-10 items-center justify-center rounded-full border border-border"
        >
          <span className="relative block h-3.5 w-4">
            <span
              className={`absolute left-0 top-0 h-[1.5px] w-full bg-foreground transition-transform duration-300 ${
                open ? "translate-y-[6px] rotate-45" : ""
              }`}
            />
            <span
              className={`absolute left-0 top-[6px] h-[1.5px] w-full bg-foreground transition-opacity duration-300 ${
                open ? "opacity-0" : "opacity-100"
              }`}
            />
            <span
              className={`absolute left-0 top-[12px] h-[1.5px] w-full bg-foreground transition-transform duration-300 ${
                open ? "-translate-y-[6px] -rotate-45" : ""
              }`}
            />
          </span>
        </button>
      </Container>

      <div
        className={`md:hidden overflow-hidden border-b border-border bg-background/95 backdrop-blur-xl transition-[max-height] duration-300 ease-out ${
          open ? "max-h-96" : "max-h-0"
        }`}
      >
        <Container className="flex flex-col gap-1 py-4">
          {navItems.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              onClick={() => setOpen(false)}
              className="rounded-lg px-3 py-3 text-base text-foreground hover:bg-surface"
            >
              {item.label}
            </Link>
          ))}
          <Link
            href="#contact"
            onClick={() => setOpen(false)}
            className="mt-2 inline-flex items-center justify-center rounded-full bg-foreground px-5 py-3 text-sm font-medium text-background"
          >
            Обсудить проект
          </Link>
        </Container>
      </div>
    </header>
  );
}
