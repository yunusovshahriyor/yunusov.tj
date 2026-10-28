// Локальная проверка без сети: node test.mjs
import worker, { matchKeyword } from "./worker.js";
import assert from "node:assert/strict";
import crypto from "node:crypto";

const env = { IG_ACCESS_TOKEN: "tok", IG_APP_SECRET: "sec", VERIFY_TOKEN: "vt", TELEGRAM_LINK: "https://t.me/test" };
const kv = new Map();
env.SEEN = { get: async (k) => kv.get(k) ?? null, put: async (k, v) => { kv.set(k, v); } };
const calls = [];
globalThis.fetch = async (url, init) => { calls.push({ url, body: JSON.parse(init.body) }); return new Response("{}", { status: 200 }); };

async function post(body, secret = "sec") {
  const raw = JSON.stringify(body);
  const sig = "sha256=" + crypto.createHmac("sha256", secret).update(raw).digest("hex");
  const waits = [];
  const res = await worker.fetch(new Request("https://x/", { method: "POST", body: raw, headers: { "x-hub-signature-256": sig } }), env, { waitUntil: (p) => waits.push(p) });
  await Promise.all(waits);
  return res;
}
const update = (text, id = "c1", from = "u1") => ({ object: "instagram", entry: [{ id: "me", changes: [{ field: "comments", value: { id, text, from: { id: from, username: "x" }, media: { id: "m1" } } }] }] });

// верификация вебхука
let r = await worker.fetch(new Request("https://x/?hub.mode=subscribe&hub.verify_token=vt&hub.challenge=42"), env, {});
assert.equal(await r.text(), "42");
r = await worker.fetch(new Request("https://x/?hub.mode=subscribe&hub.verify_token=no&hub.challenge=42"), env, {});
assert.equal(r.status, 403);

// подпись
r = await post(update("ДАВР"), "wrong");
assert.equal(r.status, 401); assert.equal(calls.length, 0);

// ключевые слова
assert.ok(matchKeyword("давр!!", env)); assert.ok(matchKeyword("Код лутфан 🙏", env));
assert.equal(matchKeyword("давраш хуб", env), null);
assert.ok(matchKeyword("рӯйхат", env));

// успешный сценарий: DM + публичный ответ
r = await post(update("ДАВР 🔥"));
assert.equal(r.status, 200);
assert.equal(calls.length, 2);
assert.match(calls[0].url, /\/me\/messages$/);
assert.deepEqual(calls[0].body.recipient, { comment_id: "c1" });
assert.match(calls[0].body.message.text, /https:\/\/t\.me\/test/);
assert.match(calls[1].url, /\/c1\/replies$/);

// повтор того же комментария и второй комментарий того же человека под тем же роликом — без DM
await post(update("ДАВР", "c1")); await post(update("код", "c2"));
assert.equal(calls.length, 2);
// другой человек — DM
await post(update("код", "c3", "u2"));
assert.equal(calls.length, 4);
// свой комментарий и комментарий без слова — игнор
await post(update("ДАВР", "c4", "me")); await post(update("зӯр!", "c5", "u3"));
assert.equal(calls.length, 4);
console.log("all tests passed");
