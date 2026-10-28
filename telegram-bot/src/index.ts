// SMM-бот: калимаи рамзӣ дар шарҳҳои канал → ссилка ба директ.
//
// Ҷараён:
// 1. Обуначӣ дар шарҳи пост калимаи рамзиро менависад.
// 2. Бот ба шарҳ бо тугмаи t.me/<bot>?start=<id> ҷавоб медиҳад
//    (Telegram ба бот иҷозат намедиҳад, ки худаш аввал ба директ нависад).
// 3. Обуначӣ Start-ро пахш мекунад → бот обунаро месанҷад ва ссилкаро мефиристад.

import rawKeywords from "../keywords.json";
import { type Keyword, KeywordMatcher, parseKeywords } from "./matching";
import {
  type CallbackQuery,
  type InlineKeyboard,
  type Message,
  Telegram,
  TelegramError,
  type Update,
  type User,
  webhookSecret,
} from "./telegram";

export interface Env {
  DB: D1Database;
  TELEGRAM_BOT_TOKEN: string;
  TELEGRAM_CHANNEL: string;
  BOT_USERNAME: string;
  DISCUSSION_CHAT_ID?: string;
  REQUIRE_SUBSCRIPTION?: string;
  DIRECT_LINK?: string;
  ADMIN_IDS?: string;
  COMMENT_COOLDOWN?: string;
  COMMENT_REPLY?: string;
  COMMENT_BUTTON?: string;
  WELCOME_TEXT?: string;
  NOT_SUBSCRIBED_TEXT?: string;
}

const keywords = parseKeywords(rawKeywords);
const matcher = new KeywordMatcher(keywords);

const SUBSCRIBED = new Set(["creator", "administrator", "member"]);

let discussionChatId: number | null = null;

function text(env: Env) {
  return {
    commentReply: env.COMMENT_REPLY || "Ташаккур! Барои гирифтани мавод тугмаро пахш кунед 👇",
    commentButton: env.COMMENT_BUTTON || "📩 Гирифтан",
    welcome:
      env.WELCOME_TEXT ||
      "Салом! Дар шарҳҳои канал калимаи рамзиро нависед — ман маводро ба шумо мефиристам.",
    notSubscribed:
      env.NOT_SUBSCRIBED_TEXT ||
      "Мавод танҳо барои обуначиёни канал аст. Обуна шавед ва «✅ Санҷидан»-ро пахш кунед.",
  };
}

function keywordById(id: string): Keyword | undefined {
  return keywords.find((k) => k.id === id);
}

function channelUrl(channel: string): string {
  return `https://t.me/${channel.replace(/^@/, "")}`;
}

async function getDiscussionChatId(env: Env, tg: Telegram): Promise<number> {
  if (env.DISCUSSION_CHAT_ID) return Number(env.DISCUSSION_CHAT_ID);
  if (discussionChatId === null) {
    const chat = await tg.call<{ linked_chat_id?: number }>("getChat", {
      chat_id: env.TELEGRAM_CHANNEL,
    });
    if (!chat.linked_chat_id) throw new Error("Канал гурӯҳи шарҳҳо надорад");
    discussionChatId = chat.linked_chat_id;
  }
  return discussionChatId;
}

async function isSubscribed(env: Env, tg: Telegram, userId: number): Promise<boolean> {
  if (env.REQUIRE_SUBSCRIPTION === "false") return true;
  try {
    const member = await tg.call<{ status: string; is_member?: boolean }>("getChatMember", {
      chat_id: env.TELEGRAM_CHANNEL,
      user_id: userId,
    });
    // Корбари маҳдудшуда (restricted) метавонад узв бошад.
    return SUBSCRIBED.has(member.status) || member.is_member === true;
  } catch (e) {
    if (e instanceof TelegramError) return false;
    throw e;
  }
}

// Як корбар бо як калима дар шарҳҳо на зудтар аз як бор дар COMMENT_COOLDOWN сония ҷавоб мегирад.
async function cooldownAllows(env: Env, userId: number, keywordId: string): Promise<boolean> {
  const now = Math.floor(Date.now() / 1000);
  const cooldown = Number(env.COMMENT_COOLDOWN || "600");
  const result = await env.DB.prepare(
    `INSERT INTO comment_replies (user_id, keyword_id, replied_at) VALUES (?1, ?2, ?3)
     ON CONFLICT (user_id, keyword_id) DO UPDATE SET replied_at = excluded.replied_at
     WHERE comment_replies.replied_at <= excluded.replied_at - ?4`,
  )
    .bind(userId, keywordId, now, cooldown)
    .run();
  return result.meta.changes > 0;
}

async function deliver(env: Env, tg: Telegram, user: User, keyword: Keyword): Promise<void> {
  const markup: InlineKeyboard = { inline_keyboard: [[{ text: keyword.button, url: keyword.url }]] };
  await tg.sendMessage(user.id, keyword.message.replaceAll("{url}", keyword.url), {
    reply_markup: markup,
  });
  await env.DB.prepare(
    `INSERT INTO deliveries (user_id, keyword_id, username, first_name) VALUES (?1, ?2, ?3, ?4)
     ON CONFLICT (user_id, keyword_id) DO UPDATE SET
       username = excluded.username, first_name = excluded.first_name`,
  )
    .bind(user.id, keyword.id, user.username ?? null, user.first_name ?? null)
    .run();
  console.log(`Delivered ${keyword.id} to ${user.id}`);
}

function subscribeMarkup(env: Env, keyword: Keyword): InlineKeyboard {
  return {
    inline_keyboard: [
      [{ text: "📢 Обуна шудан", url: channelUrl(env.TELEGRAM_CHANNEL) }],
      [{ text: "✅ Санҷидан", callback_data: `check:${keyword.id}` }],
    ],
  };
}

async function onComment(env: Env, tg: Telegram, message: Message): Promise<void> {
  // Постҳои канал, ки худкор ба гурӯҳ меоянд, ва шарҳҳо «аз номи канал» сарфи назар мешаванд.
  if (message.is_automatic_forward || message.sender_chat || !message.from || message.from.is_bot) {
    return;
  }
  const keyword = matcher.match(message.text ?? message.caption);
  if (!keyword) return;
  if (!(await cooldownAllows(env, message.from.id, keyword.id))) return;

  const t = text(env);
  // DIRECT_LINK=true: тугма худи ссилкаро мекушояд (бе бот ва санҷиши обуна).
  const buttonUrl =
    env.DIRECT_LINK === "true"
      ? keyword.url
      : `https://t.me/${env.BOT_USERNAME}?start=${keyword.id}`;
  await tg.sendMessage(message.chat.id, t.commentReply, {
    reply_parameters: { message_id: message.message_id, allow_sending_without_reply: true },
    reply_markup: { inline_keyboard: [[{ text: t.commentButton, url: buttonUrl }]] },
  });
  console.log(`Keyword ${keyword.id} from ${message.from.id} in comments`);
}

async function onPrivate(env: Env, tg: Telegram, message: Message): Promise<void> {
  const user = message.from;
  const body = message.text?.trim() ?? "";
  if (!user) return;

  const [command, ...args] = body.split(/\s+/);
  const name = command.split("@")[0];

  if (name === "/stats") {
    const admins = (env.ADMIN_IDS ?? "").split(",").map((s) => s.trim());
    if (!admins.includes(String(user.id))) return;
    const total = await env.DB.prepare(
      "SELECT COUNT(DISTINCT user_id) AS n FROM deliveries",
    ).first<{ n: number }>();
    const perKeyword = await env.DB.prepare(
      "SELECT keyword_id, COUNT(*) AS n FROM deliveries GROUP BY keyword_id ORDER BY n DESC",
    ).all<{ keyword_id: string; n: number }>();
    const replies = await env.DB.prepare(
      "SELECT COUNT(*) AS n FROM comment_replies",
    ).first<{ n: number }>();
    const lines = [`Ҷавобҳо дар шарҳҳо: ${replies?.n ?? 0}`, `Дар директ гирифтанд: ${total?.n ?? 0}`];
    for (const row of perKeyword.results) lines.push(`• ${row.keyword_id}: ${row.n}`);
    await tg.sendMessage(user.id, lines.join("\n"));
    return;
  }

  const keyword = name === "/start" && args[0] ? keywordById(args[0]) : undefined;
  if (!keyword) {
    await tg.sendMessage(user.id, text(env).welcome);
    return;
  }
  if (!(await isSubscribed(env, tg, user.id))) {
    await tg.sendMessage(user.id, text(env).notSubscribed, {
      reply_markup: subscribeMarkup(env, keyword),
    });
    return;
  }
  await deliver(env, tg, user, keyword);
}

async function onCallback(env: Env, tg: Telegram, callback: CallbackQuery): Promise<void> {
  const data = callback.data ?? "";
  const keyword = data.startsWith("check:") ? keywordById(data.slice(6)) : undefined;
  if (!keyword) {
    await tg.call("answerCallbackQuery", { callback_query_id: callback.id });
    return;
  }
  if (!(await isSubscribed(env, tg, callback.from.id))) {
    await tg.call("answerCallbackQuery", {
      callback_query_id: callback.id,
      text: "Шумо ҳанӯз обуна нашудаед 🙂",
      show_alert: true,
    });
    return;
  }
  await tg.call("answerCallbackQuery", {
    callback_query_id: callback.id,
    text: "Ташаккур барои обуна!",
  });
  if (callback.message) {
    await tg
      .call("deleteMessage", {
        chat_id: callback.message.chat.id,
        message_id: callback.message.message_id,
      })
      .catch(() => {});
  }
  await deliver(env, tg, callback.from, keyword);
}

async function handleUpdate(env: Env, update: Update): Promise<void> {
  const tg = new Telegram(env.TELEGRAM_BOT_TOKEN);
  if (update.callback_query) {
    await onCallback(env, tg, update.callback_query);
    return;
  }
  const message = update.message;
  if (!message) return;
  if (message.chat.type === "private") {
    await onPrivate(env, tg, message);
  } else if (
    message.chat.type === "supergroup" &&
    message.chat.id === (await getDiscussionChatId(env, tg))
  ) {
    await onComment(env, tg, message);
  }
}

export default {
  async fetch(req: Request, env: Env): Promise<Response> {
    const url = new URL(req.url);
    if (req.method === "GET" && url.pathname === "/") {
      return new Response("SMM bot is running");
    }
    if (req.method !== "POST" || url.pathname !== "/webhook") {
      return new Response("not found", { status: 404 });
    }
    const secret = req.headers.get("x-telegram-bot-api-secret-token");
    if (secret !== (await webhookSecret(env.TELEGRAM_BOT_TOKEN))) {
      return new Response("forbidden", { status: 403 });
    }

    const update = (await req.json()) as Update;
    try {
      await handleUpdate(env, update);
    } catch (e) {
      // Ҳамеша 200 бармегардонем, то Telegram ҳамон навсозиро бепоён такрор накунад.
      console.error(`Update ${update.update_id} failed:`, e);
    }
    return new Response("ok");
  },
};
