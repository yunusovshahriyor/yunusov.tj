// Як қисми хурди Telegram Bot API, ки бот истифода мебарад.

export type User = {
  id: number;
  is_bot: boolean;
  first_name: string;
  username?: string;
};

export type Chat = { id: number; type: string };

export type Message = {
  message_id: number;
  chat: Chat;
  from?: User;
  sender_chat?: Chat;
  is_automatic_forward?: boolean;
  text?: string;
  caption?: string;
};

export type CallbackQuery = {
  id: string;
  from: User;
  message?: Message;
  data?: string;
};

export type Update = {
  update_id: number;
  message?: Message;
  callback_query?: CallbackQuery;
};

export type InlineKeyboard = {
  inline_keyboard: Array<Array<{ text: string; url?: string; callback_data?: string }>>;
};

export class TelegramError extends Error {
  constructor(
    readonly method: string,
    readonly description: string,
  ) {
    super(`${method}: ${description}`);
  }
}

export class Telegram {
  constructor(private readonly token: string) {}

  async call<T = unknown>(method: string, body: Record<string, unknown>): Promise<T> {
    const res = await fetch(`https://api.telegram.org/bot${this.token}/${method}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const data = (await res.json()) as { ok: boolean; result: T; description?: string };
    if (!data.ok) throw new TelegramError(method, data.description ?? String(res.status));
    return data.result;
  }

  sendMessage(chatId: number | string, text: string, extra: Record<string, unknown> = {}) {
    return this.call("sendMessage", { chat_id: chatId, text, ...extra });
  }
}

// Сирри webhook аз токен ҳосил мешавад, то сирри алоҳида нигоҳ доштан лозим набошад.
// Ҳамин ҳисоб дар workflow-и деплой ҳам ҳаст: sha256("webhook:" + token).
export async function webhookSecret(token: string): Promise<string> {
  const digest = await crypto.subtle.digest(
    "SHA-256",
    new TextEncoder().encode(`webhook:${token}`),
  );
  return [...new Uint8Array(digest)].map((b) => b.toString(16).padStart(2, "0")).join("");
}
