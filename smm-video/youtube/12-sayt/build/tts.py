# narration.md -> chunks.json -> ElevenLabs with-timestamps (один раз на кусок; ключ подставляет прокси).
import json, re, base64, sys, os, urllib.request
VOICE = 'VaoFGWxF44cUZfrRbO4x'
src = open('../narration.md', encoding='utf-8').read()
chunks = []
for sec in re.split(r'\n## ', src)[1:]:
    body = sec.split('\n', 1)[1].split('\n---')[0]
    lines = [l.strip() for l in body.split('\n') if l.strip() and not l.strip().startswith('`[')]
    chunks.append('\n\n'.join(lines))
json.dump(chunks, open('chunks.json', 'w'), ensure_ascii=False, indent=1)
open('tts-text.txt', 'w', encoding='utf-8').write('\n\n'.join(chunks))
print([len(c) for c in chunks], sum(len(c) for c in chunks))
if '--go' not in sys.argv: sys.exit()
for i, t in enumerate(chunks):
    if os.path.exists(f'chunk{i}.mp3'): continue
    body = dict(text=t, model_id='eleven_v4', language_code='tg',
                voice_settings=dict(stability=0.5, similarity_boost=0.9))
    if i > 0: body['previous_text'] = chunks[i - 1][-300:]
    if i + 1 < len(chunks): body['next_text'] = chunks[i + 1][:300]
    req = urllib.request.Request(
        f'https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps?output_format=mp3_44100_128',
        data=json.dumps(body).encode(), headers={'xi-api-key': 'dummy', 'Content-Type': 'application/json'})
    r = json.load(urllib.request.urlopen(req, timeout=300))
    open(f'chunk{i}.mp3', 'wb').write(base64.b64decode(r['audio_base64']))
    json.dump(dict(alignment=r['alignment']), open(f'chunk{i}.alignment.json', 'w'))
    print('chunk', i, 'ok', flush=True)
