import { NextResponse } from "next/server";

type ContactPayload = {
  name?: string;
  contact?: string;
  projectType?: string;
  message?: string;
};

export async function POST(request: Request) {
  const body = (await request.json()) as ContactPayload;
  const { name, contact, projectType, message } = body;

  if (!name?.trim() || !contact?.trim() || !message?.trim()) {
    return NextResponse.json({ error: "missing-fields" }, { status: 400 });
  }

  const text = [
    "Новая заявка с сайта",
    `Имя: ${name}`,
    `Контакт: ${contact}`,
    `Тип проекта: ${projectType ?? "—"}`,
    `Сообщение: ${message}`,
  ].join("\n");

  // Чтобы получать заявки в Telegram, задайте переменные окружения
  // TELEGRAM_BOT_TOKEN и TELEGRAM_CHAT_ID (см. README).
  const botToken = process.env.TELEGRAM_BOT_TOKEN;
  const chatId = process.env.TELEGRAM_CHAT_ID;

  if (botToken && chatId) {
    const response = await fetch(
      `https://api.telegram.org/bot${botToken}/sendMessage`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ chat_id: chatId, text }),
      }
    );

    if (!response.ok) {
      return NextResponse.json({ error: "delivery-failed" }, { status: 502 });
    }
  } else {
    console.log(text);
  }

  return NextResponse.json({ ok: true });
}
