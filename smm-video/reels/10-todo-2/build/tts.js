// tts-text.txt -> ElevenLabs with-timestamps (один раз; ключ подставляет прокси) -> raw.mp3 + raw.alignment.json
const fs = require('fs');
const VOICE = 'VaoFGWxF44cUZfrRbO4x';
(async () => {
  if (fs.existsSync('raw.mp3')) { console.log('raw.mp3 уже есть — повтор запрещён (кредит)'); return; }
  const text = fs.readFileSync('tts-text.txt', 'utf8').trim();
  const r = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${VOICE}/with-timestamps?output_format=mp3_44100_128`, {
    method: 'POST', headers: { 'xi-api-key': process.env.ELEVENLABS_API_KEY || 'dummy', 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, model_id: 'eleven_v4', language_code: 'tg', voice_settings: { stability: 0.5, similarity_boost: 0.9 } }) });
  if (!r.ok) { console.log('HTTP', r.status, (await r.text()).slice(0, 300)); process.exit(1); }
  const j = await r.json();
  fs.writeFileSync('raw.mp3', Buffer.from(j.audio_base64, 'base64'));
  fs.writeFileSync('raw.alignment.json', JSON.stringify({ text, alignment: j.alignment }));
  console.log('ok', text.length);
})();
