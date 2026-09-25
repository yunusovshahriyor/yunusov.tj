"use client";

import { FormEvent, useState } from "react";
import { contacts } from "@/data/contacts";

type Status = "idle" | "loading" | "success" | "error";

const projectTypes = [
  "Мобильное приложение",
  "Сайт",
  "Сайт на Tilda",
  "Цифровой продукт",
  "Другое",
];

// В статической сборке для GitHub Pages нет сервера, поэтому форма
// не может обратиться к /api/contact и вместо этого открывает mailto-ссылку.
const isStaticExport = process.env.NEXT_PUBLIC_STATIC_EXPORT === "true";

export function ContactForm() {
  const [status, setStatus] = useState<Status>("idle");
  const [errorMessage, setErrorMessage] = useState("");

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const formData = new FormData(event.currentTarget);
    const payload = Object.fromEntries(formData.entries()) as Record<string, string>;

    if (isStaticExport) {
      const emailAddress = contacts.email.href.replace("mailto:", "");
      const subject = `Заявка с сайта: ${payload.projectType ?? ""}`;
      const body = [
        `Имя: ${payload.name}`,
        `Контакт: ${payload.contact}`,
        `Сообщение: ${payload.message}`,
      ].join("\n");
      window.location.href = `mailto:${emailAddress}?subject=${encodeURIComponent(
        subject
      )}&body=${encodeURIComponent(body)}`;
      setStatus("success");
      return;
    }

    setStatus("loading");
    setErrorMessage("");

    try {
      const response = await fetch("/api/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error("request-failed");
      }

      setStatus("success");
      event.currentTarget.reset();
    } catch {
      setStatus("error");
      setErrorMessage(
        "Не удалось отправить заявку. Попробуйте ещё раз или напишите напрямую в Telegram."
      );
    }
  }

  if (status === "success") {
    return (
      <div className="flex flex-col items-start gap-2 rounded-2xl border border-accent/30 bg-accent-soft p-6">
        <p className="text-base font-semibold text-foreground">
          {isStaticExport ? "Открываем почтовый клиент" : "Заявка отправлена"}
        </p>
        <p className="text-sm text-muted">
          {isStaticExport
            ? "Отправьте письмо в открывшемся приложении почты — и я вам отвечу."
            : "Спасибо! Я свяжусь с вами в ближайшее время."}
        </p>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-5">
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2">
        <Field label="Имя" name="name" placeholder="Как к вам обращаться" required />
        <Field
          label="Контакт"
          name="contact"
          placeholder="Telegram, email или телефон"
          required
        />
      </div>

      <label className="flex flex-col gap-2">
        <span className="text-sm font-medium text-foreground">Что нужно разработать</span>
        <select
          name="projectType"
          defaultValue={projectTypes[0]}
          className="rounded-xl border border-border bg-background px-4 py-3 text-sm text-foreground outline-none transition-colors focus:border-accent"
        >
          {projectTypes.map((type) => (
            <option key={type} value={type}>
              {type}
            </option>
          ))}
        </select>
      </label>

      <label className="flex flex-col gap-2">
        <span className="text-sm font-medium text-foreground">Сообщение</span>
        <textarea
          name="message"
          required
          rows={4}
          placeholder="Расскажите коротко о задаче"
          className="resize-none rounded-xl border border-border bg-background px-4 py-3 text-sm text-foreground outline-none transition-colors focus:border-accent"
        />
      </label>

      {status === "error" && (
        <p className="text-sm text-red-600">{errorMessage}</p>
      )}

      <button
        type="submit"
        disabled={status === "loading"}
        className="inline-flex items-center justify-center rounded-full bg-foreground px-6 py-3 text-sm font-medium text-background transition-colors hover:bg-accent-strong disabled:opacity-60"
      >
        {status === "loading" ? "Отправка..." : "Отправить заявку"}
      </button>
    </form>
  );
}

function Field({
  label,
  name,
  placeholder,
  required,
}: {
  label: string;
  name: string;
  placeholder: string;
  required?: boolean;
}) {
  return (
    <label className="flex flex-col gap-2">
      <span className="text-sm font-medium text-foreground">{label}</span>
      <input
        type="text"
        name={name}
        placeholder={placeholder}
        required={required}
        className="rounded-xl border border-border bg-background px-4 py-3 text-sm text-foreground outline-none transition-colors focus:border-accent"
      />
    </label>
  );
}
