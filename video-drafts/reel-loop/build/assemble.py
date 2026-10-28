# Собирает голос v2: [хук] + старая запись (S0..S20) + [CTA «ДАВР»] + старая запись (S22..S23).
# Новые фразы озвучены отдельно (clip-hook, clip-cta), старая запись — без повторной генерации.
import json, re, subprocess, wave, numpy as np
SR = 48000
def load(path, tempo=1.0):
    af = f"atempo={tempo}" if tempo != 1.0 else "anull"
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', path, '-af', af, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, '<i2').astype(np.float32)
def clip_words(name, tempo):
    A = json.load(open(f'clip-{name}.alignment.json')); al = A['alignment']; text = A['text']
    cs, ce = al['character_start_times_seconds'], al['character_end_times_seconds']
    ws = []
    for m in re.finditer(r'\S+', text):
        idx = [k for k in range(m.start(), m.end()) if re.match(r'\w', text[k])] or list(range(m.start(), m.end()))
        ws.append(dict(w=m.group(), t0=cs[idx[0]] / tempo, t1=ce[idx[-1]] / tempo, c0=m.start(), c1=m.end()))
    x = load(f'clip-{name}.mp3', tempo)
    a, b = max(0.0, ws[0]['t0'] - 0.04), ws[-1]['t1'] + 0.08
    seg = x[int(a * SR):int(b * SR)]
    for w in ws: w['t0'] -= a; w['t1'] -= a
    return text, ws, seg
TL = json.load(open('timeline.json')); SN = TL['sentences']
old = load('voice.wav')
LEAD, GAP_HOOK, GAP_CTA = 0.30, 0.45, 0.22
htext, hw, hseg = clip_words('hook', 1.0)
ctext, cw, cseg = clip_words('cta', 1.1)
parts = []; pos = 0.0
def add(seg):
    global pos
    parts.append(seg); pos += len(seg) / SR
def silence(t): add(np.zeros(int(t * SR), np.float32))
silence(LEAD)
h0 = pos; add(hseg); silence(GAP_HOOK)
a1, b1 = SN[0]['start'] - 0.05, SN[20]['end'] + 0.12
o1 = pos - a1; add(old[int(a1 * SR):int(b1 * SR)]); silence(GAP_CTA)
c0 = pos; add(cseg); silence(0.25)
a2 = SN[22]['start'] - 0.05
o2 = pos - a2; add(old[int(a2 * SR):])
y = np.concatenate(parts)
w = wave.open('/tmp/voice2_raw.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(np.clip(y, -32768, 32767).astype('<i2').tobytes()); w.close()
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', '/tmp/voice2_raw.wav', '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11', '-ar', '48000', 'voice2.wav'], check=True)
def shift(ws, o): return [dict(w, t0=round(w['t0'] + o, 3), t1=round(w['t1'] + o, 3)) for w in ws]
# хук: два предложения
k = htext.index('Чӣ')
hA = [w for w in shift(hw, h0) if w['c0'] < k]; hB = [w for w in shift(hw, h0) if w['c0'] >= k]
pre = [dict(i='p0', tts=htext[:k].strip(), text=htext[:k].strip(), start=hA[0]['t0'], end=hA[-1]['t1'], words=hA),
       dict(i='p1', tts=htext[k:].strip(), text=htext[k:].strip(), start=hB[0]['t0'], end=hB[-1]['t1'], words=hB)]
new = []
for s in SN:
    i = s['i']
    if i <= 20: o = o1
    elif i == 21:
        ws = shift(cw, c0)
        new.append(dict(i=21, tts=ctext, text="Ҷавоб ва калимаи «ДАВР»-ро дар шарҳ нависед — шпаргалкаи бепулро ба Direct мефиристам!", start=ws[0]['t0'], end=ws[-1]['t1'], words=ws)); continue
    else: o = o2
    new.append(dict(s, start=round(s['start'] + o, 3), end=round(s['end'] + o, 3), words=shift(s['words'], o)))
total = len(y) / SR
json.dump(dict(total=total, pre=pre, sentences=new), open('timeline2.json', 'w'), ensure_ascii=False, indent=0)
for s in pre + new[:2] + new[19:]: print(f"{s['start']:6.2f}-{s['end']:6.2f} {s['text'][:60]}")
print('total', round(total, 2))
