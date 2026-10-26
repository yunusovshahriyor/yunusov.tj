# Сжимает длинные паузы по разметке ElevenLabs, ускоряет на 10% и пересчитывает время слов/предложений.
import json, re, subprocess, wave, numpy as np, sys
sys.path.insert(0, '.')
from sentences import S
TEMPO = 1.1; MAXGAP = 0.30; KEEP = 0.20; SR = 44100
A = json.load(open('raw.alignment.json')); al = A['alignment']; text = A['text']
cs, ce = al['character_start_times_seconds'], al['character_end_times_seconds']
toks = [(m.start(), m.end(), m.group()) for m in re.finditer(r'\S+', text)]
def span(a, b):
    idx = [k for k in range(a, b) if re.match(r'\w', text[k])] or list(range(a, b))
    return cs[idx[0]], ce[idx[-1]]
words = [(a, b, w, *span(a, b)) for a, b, w in toks]
# вырезаемые интервалы
cuts = []
first = words[0][3]
if first > 0.05: cuts.append((0, first - 0.05))
for p, n in zip(words, words[1:]):
    g = n[3] - p[4]
    if g > MAXGAP:
        m = (p[4] + n[3]) / 2; cuts.append((m - (g - KEEP) / 2, m + (g - KEEP) / 2))
raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', 'raw.mp3', '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
x = np.frombuffer(raw, '<i2').astype(np.float32)
dur = len(x) / SR
last = words[-1][4]; cuts.append((min(dur, last + 0.35), dur))
keep = []; pos = 0.0
for a, b in cuts:
    if a > pos: keep.append((pos, a))
    pos = max(pos, b)
if pos < dur: keep.append((pos, dur))
fade = int(0.008 * SR)
parts = []
for a, b in keep:
    seg = x[int(a * SR):int(b * SR)].copy()
    if len(seg) > 2 * fade:
        seg[:fade] *= np.linspace(0, 1, fade); seg[-fade:] *= np.linspace(1, 0, fade)
    parts.append(seg)
y = np.concatenate(parts)
w = wave.open('/tmp/voice_cut.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(y.astype('<i2').tobytes()); w.close()
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', '/tmp/voice_cut.wav', '-af', f'atempo={TEMPO},loudnorm=I=-16:TP=-1.5:LRA=11', '-ar', '48000', 'voice.wav'], check=True)
def f(t):
    removed = sum(max(0, min(b, t) - a) for a, b in cuts if a < t)
    return (t - removed) / TEMPO
W = [dict(c0=a, c1=b, w=wd, t0=round(f(s), 3), t1=round(f(e), 3)) for a, b, wd, s, e in words]
# предложения: по позициям в тексте
sent = []; pos = 0
for i, (tt, disp) in enumerate(S):
    k = text.index(tt, pos); pos = k + len(tt)
    ws = [x for x in W if x['c0'] >= k and x['c1'] <= pos]
    sent.append(dict(i=i, tts=tt, text=disp or tt, start=ws[0]['t0'], end=ws[-1]['t1'], words=ws))
total = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', 'voice.wav'], capture_output=True, text=True).stdout)
json.dump(dict(total=total, sentences=sent), open('timeline.json', 'w'), ensure_ascii=False, indent=0)
for s in sent: print(f"{s['start']:6.2f}-{s['end']:6.2f} {s['text'][:60]}")
print('total', total, 'removed', round(sum(b - a for a, b in cuts), 2))
