// Instagram «comment → DM» бот для Cloudflare Workers.
// Когда под Reels пишут кодовое слово (ДАВР, КОД, …), бот отправляет автору комментария
// приватный ответ в Direct (Private Replies API) со ссылкой и коротко отвечает на сам комментарий.
//
// Переменные окружения (Settings → Variables and Secrets):
//   IG_ACCESS_TOKEN  (secret) — токен Instagram API with Instagram Login
//   IG_APP_SECRET    (secret) — Instagram app secret, для проверки подписи вебхука
//   VERIFY_TOKEN     (secret) — любая строка, та же, что в настройке вебхука в Meta
//   TELEGRAM_LINK    — ссылка, которую получает пользователь
//   KEYWORDS         — необязательно: JSON {"ДАВР": "текст…", "КОД": "текст…"}; иначе DEFAULT_KEYWORDS
//   GRAPH_VERSION    — необязательно, по умолчанию v21.0
// KV binding: SEEN — чтобы не отвечать дважды на один комментарий / одному человеку под одним роликом.

const DEFAULT_KEYWORDS = ["КОД", "ДАВР", "ШАРТ", "РӮЙХАТ", "ТАҒЙИРЁБАНДА"];
const DEFAULT_DM = "Салом! 👋 Шпаргалка ва ҳамаи дарсҳо дар канали Telegram-и ман 👉 {link}\nПости аввал мустаҳкам аст 📌";
const DEFAULT_PUBLIC_REPLY = "📩 Ба Direct фиристодам!";
const DEDUP_TTL = 60 * 60 * 24 * 30;

const worker = {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    if (request.method === "GET") return verifyWebhook(url, env);
    if (request.method !== "POST") return new Response("ok");

    const raw = await request.text();
    if (!(await validSignature(raw, request.headers.get("x-hub-signature-256"), env.IG_APP_SECRET))) {
      return new Response("bad signature", { status: 401 });
    }
    let body;
    try { body = JSON.parse(raw); } catch { return new Response("bad json", { status: 400 }); }

    // Meta ждёт быстрый 200, обработка — в фоне.
    ctx.waitUntil(handleUpdate(body, env).catch((e) => console.log("handle error", e && e.stack || e)));
    return new Response("EVENT_RECEIVED");
  },
};
export default worker;

function verifyWebhook(url, env) {
  const p = url.searchParams;
  if (p.get("hub.mode") === "subscribe" && p.get("hub.verify_token") === env.VERIFY_TOKEN) {
    return new Response(p.get("hub.challenge") || "");
  }
  return new Response("forbidden", { status: 403 });
}

async function validSignature(raw, header, secret) {
  if (!header || !secret || !header.startsWith("sha256=")) return false;
  const key = await crypto.subtle.importKey("raw", new TextEncoder().encode(secret), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const mac = new Uint8Array(await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(raw)));
  const hex = [...mac].map((b) => b.toString(16).padStart(2, "0")).join("");
  const given = header.slice(7);
  if (given.length !== hex.length) return false;
  let diff = 0;
  for (let i = 0; i < hex.length; i++) diff |= hex.charCodeAt(i) ^ given.charCodeAt(i);
  return diff === 0;
}

export function normalize(text) {
  return (text || "").toUpperCase().replace(/[^\p{L}\p{N}]+/gu, " ").trim();
}

export function matchKeyword(text, env) {
  let map = null;
  if (env.KEYWORDS) { try { map = JSON.parse(env.KEYWORDS); } catch { map = null; } }
  const words = new Set(normalize(text).split(" "));
  const keys = map ? Object.keys(map) : DEFAULT_KEYWORDS;
  for (const k of keys) {
    if (words.has(normalize(k))) return { keyword: k, dm: map ? map[k] : null };
  }
  return null;
}

async function handleUpdate(body, env) {
  if (body.object !== "instagram") return;
  for (const entry of body.entry || []) {
    for (const change of entry.changes || []) {
      if (change.field !== "comments") continue;
      const c = change.value || {};
      if (!c.id || !c.text) continue;
      if (c.from && c.from.id === entry.id) continue;   // свои комментарии
      if (c.parent_id) continue;                         // ответы в ветке не трогаем
      const hit = matchKeyword(c.text, env);
      if (!hit) continue;

      const userKey = `u:${c.media && c.media.id}:${c.from && c.from.id}`;
      const commentKey = `c:${c.id}`;
      if (env.SEEN && ((await env.SEEN.get(commentKey)) || (await env.SEEN.get(userKey)))) continue;

      const link = env.TELEGRAM_LINK || "";
      const text = (hit.dm || DEFAULT_DM).replaceAll("{link}", link);
      const dm = await graph(env, `/${entry.id}/messages`, { recipient: { comment_id: c.id }, message: { text } });
      console.log("dm", c.id, hit.keyword, dm.status);
      if (!dm.ok) continue;
      if (env.SEEN) {
        await env.SEEN.put(commentKey, "1", { expirationTtl: DEDUP_TTL });
        await env.SEEN.put(userKey, "1", { expirationTtl: DEDUP_TTL });
      }
      const pub = await graph(env, `/${c.id}/replies`, { message: env.PUBLIC_REPLY || DEFAULT_PUBLIC_REPLY });
      console.log("public reply", c.id, pub.status);
    }
  }
}

async function graph(env, path, payload) {
  const v = env.GRAPH_VERSION || "v21.0";
  const res = await fetch(`https://graph.instagram.com/${v}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${env.IG_ACCESS_TOKEN}` },
    body: JSON.stringify(payload),
  });
  if (!res.ok) console.log("graph error", path, res.status, await res.text());
  return res;
}
