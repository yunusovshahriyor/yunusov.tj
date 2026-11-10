// narration.md -> chunks.json -> ElevenLabs with-timestamps (один раз на кусок; ключ из ELEVENLABS_API_KEY).
const fs = require('fs');
const VOICE = 'VaoFGWxF44cUZfrRbO4x';
const src = fs.readFileSync('../narration.md', 'utf8');
const chunks = src.split(/\n## /).slice(1).map(sec => {
  const body = sec.split('\n').slice(1).join('\n').split('\n---')[0];
  return body.split('\n').map(l => l.trim()).filter(l => l && !l.startsWith('`[')).join('\n\n');
});
fs.writeFileSync('chunks.json', JSON.stringify(chunks, null, 1));
fs.writeFileSync('tts-text.txt', chunks.join('\n\n'));
console.log(chunks.map(c => c.length), chunks.reduce((a, c) => a + c.length, 0));
if (!process.argv.includes('--go')) process.exit();
(async () => {
  for (let i = 0; i < chunks.length; i++) {
    if (fs.existsSync(`chunk${i}.mp3`)) continue;
    const body = { text: chunks[i], model_id: 'eleven_v4', language_code: 'tg', voice_settings: { stability: 0.5, similarity_boost: 0.9 } };
    if (i > 0) body.previous_text = chunks[i - 1].slice(-300);
    if (i + 1 < chunks.length) body.next_text = chunks[i + 1].slice(0, 300);
    const r = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${VOICE}/with-timestamps?output_format=mp3_44100_128`, {
      method: 'POST', headers: { 'xi-api-key': process.env.ELEVENLABS_API_KEY, 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
    if (!r.ok) { console.log('chunk', i, 'FAILED', r.status, (await r.text()).slice(0, 300)); process.exit(1); }
    const j = await r.json();
    fs.writeFileSync(`chunk${i}.mp3`, Buffer.from(j.audio_base64, 'base64'));
    fs.writeFileSync(`chunk${i}.alignment.json`, JSON.stringify({ alignment: j.alignment }));
    console.log('chunk', i, 'ok');
  }
})();
