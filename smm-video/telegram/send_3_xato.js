// Фиристодани Reels дарси 7 «3 хатои рӯзи аввал» ба Telegram: видео + конспект, муқова ҳамчун файл (тавсифи Instagram — бо `--ig`).
// Калид ва канал танҳо аз муҳит: TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL. `--dry` — бе фиристодан.
const fs = require('fs'), path = require('path');
const R = path.join(__dirname, '..', 'reels', 'extra-01-3-xato');
const TOKEN = process.env.TELEGRAM_BOT_TOKEN, CHAT = process.env.TELEGRAM_CHANNEL, DRY = process.argv.includes('--dry');
const post = fs.readFileSync(path.join(__dirname, 'post-11-3-xato.html'), 'utf8').trim();
const igCaption = fs.readFileSync(path.join(R, 'caption.txt'), 'utf8').trim();
const files = { video: path.join(R, 'reel-3-xato.mp4'), cover: path.join(R, 'cover.jpg') };
for (const f of Object.values(files)) if (!fs.existsSync(f)) { console.error('Файл нест:', f); process.exit(1); }
console.log('конспект:', post.length, 'аломат (ҳадди caption — 1024)'); console.log('тавсифи Instagram:', igCaption.length, 'аломат');
if (post.length > 1024) { console.error('Конспект аз 1024 дароз аст'); process.exit(1); }
if (DRY) { console.log('DRY: ҳеҷ чиз фиристода нашуд.'); process.exit(0); }
if (!TOKEN || !CHAT) { console.error('TELEGRAM_BOT_TOKEN ва TELEGRAM_CHANNEL лозиманд.'); process.exit(1); }
const api = async (method, fd) => { const r = await fetch(`https://api.telegram.org/bot${TOKEN}/${method}`, { method: 'POST', body: fd }); const j = await r.json(); if (!j.ok) throw new Error(method + ': ' + j.description); return j.result; };
const blob = (f, type) => new Blob([fs.readFileSync(f)], { type });
(async () => {
  let fd = new FormData(); fd.set('chat_id', CHAT); fd.set('caption', post); fd.set('parse_mode', 'HTML'); fd.set('supports_streaming', 'true'); fd.set('width', '1080'); fd.set('height', '1920');
  fd.set('video', blob(files.video, 'video/mp4'), 'reel-3-xato.mp4');
  const m1 = await api('sendVideo', fd); console.log('видео + конспект: message_id', m1.message_id);
  fd = new FormData(); fd.set('chat_id', CHAT); fd.set('document', blob(files.cover, 'image/jpeg'), 'cover.jpg');
  const m2 = await api('sendDocument', fd); console.log('муқова: message_id', m2.message_id);
  if (process.argv.includes('--ig')) {
  const esc = t => t.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  fd = new FormData(); fd.set('chat_id', CHAT); fd.set('text', '📲 <b>Тавсиф барои Instagram</b> (барои нусха пахш кунед):\n\n<pre>' + esc(igCaption) + '</pre>'); fd.set('parse_mode', 'HTML');
  const m3 = await api('sendMessage', fd); console.log('тавсифи Instagram: message_id', m3.message_id);
  }
})().catch(e => { console.error(e.message); process.exit(1); });
