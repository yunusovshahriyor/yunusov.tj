// Фиристодани quiz-и Telegram: node send_quiz.js <файли.json>. Калид ва канал аз муҳит: TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL. `--dry` — бе фиристодан.
const fs = require('fs'), path = require('path');
const TOKEN = process.env.TELEGRAM_BOT_TOKEN, CHAT = process.env.TELEGRAM_CHANNEL, DRY = process.argv.includes('--dry');
const file = process.argv.find((a, i) => i > 1 && a.endsWith('.json'));
const q = JSON.parse(fs.readFileSync(path.resolve(file), 'utf8'));
const len = s => [...s].length;
const errs = [];
if (len(q.question) > 300) errs.push('question > 300');
q.options.forEach(o => { if (len(o) > 100) errs.push('option > 100: ' + o); });
if (len(q.explanation || '') > 200) errs.push('explanation > 200');
if (q.options.length < 2 || q.options.length > 10) errs.push('options count');
console.log('question', len(q.question), '| explanation', len(q.explanation || ''), '| options', q.options.map(len).join(','));
if (errs.length) { console.error(errs.join('\n')); process.exit(1); }
if (DRY) { console.log('DRY: ҳеҷ чиз фиристода нашуд.'); process.exit(0); }
if (!TOKEN || !CHAT) { console.error('TELEGRAM_BOT_TOKEN ва TELEGRAM_CHANNEL лозиманд.'); process.exit(1); }
(async () => {
  const body = { chat_id: CHAT, question: q.question, options: q.options, type: 'quiz', correct_option_id: q.correct_option_id, explanation: q.explanation, is_anonymous: q.is_anonymous !== false };
  const r = await fetch(`https://api.telegram.org/bot${TOKEN}/sendPoll`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
  const j = await r.json(); if (!j.ok) { console.error(j.description); process.exit(1); }
  console.log('quiz: message_id', j.result.message_id);
})();
