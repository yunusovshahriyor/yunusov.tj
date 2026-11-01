# Склеивает куски озвучки, ограничивает слишком длинные паузы, нормализует громкость; сохраняет тайминги слов.
import json, re, subprocess, wave, numpy as np
SR = 48000; MAXGAP = 0.9; KEEPGAP = 0.7; CHUNK_GAP = 0.6; LEAD = 0.4
chunks = json.load(open('chunks.json')); out = []; words = []; pos = 0.0
def dec(p): return np.frombuffer(subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', p, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout, '<i2').astype(np.float32)
out.append(np.zeros(int(LEAD * SR), np.float32)); pos = LEAD
for ci, t in enumerate(chunks):
    A = json.load(open(f'chunk{ci}.alignment.json'))['alignment']
    cs, ce = A['character_start_times_seconds'], A['character_end_times_seconds']
    x = dec(f'chunk{ci}.mp3'); dur = len(x) / SR
    toks = [(m.start(), m.end(), m.group()) for m in re.finditer(r'\S+', t)]
    ws = []
    for a, b, w in toks:
        idx = [k for k in range(a, b) if re.match(r'\w', t[k])] or list(range(a, b))
        ws.append([w, cs[idx[0]], ce[idx[-1]], a, b])
    cuts = [(0.0, max(0.0, ws[0][1] - 0.03))]
    for p, n in zip(ws, ws[1:]):
        g = n[1] - p[2]
        if g > MAXGAP:
            m = (p[2] + n[1]) / 2; cuts.append((m - (g - KEEPGAP) / 2, m + (g - KEEPGAP) / 2))
    cuts.append((min(dur, ws[-1][2] + 0.15), dur))
    keep = []; q = 0.0
    for a, b in cuts:
        if a > q: keep.append((q, a))
        q = max(q, b)
    if q < dur: keep.append((q, dur))
    def mp(t0):  # исходное время -> время после вырезок
        return t0 - sum(max(0, min(b, t0) - a) for a, b in cuts if a < t0)
    fade = int(0.008 * SR)
    for a, b in keep:
        seg = x[int(a * SR):int(b * SR)].copy()
        if len(seg) > 2 * fade: seg[:fade] *= np.linspace(0, 1, fade); seg[-fade:] *= np.linspace(1, 0, fade)
        out.append(seg)
    cl = sum(len(s) for s in out[-len(keep):]) / SR
    for w, s0, s1, a, b in ws: words.append(dict(w=w, t0=round(pos + mp(s0), 3), t1=round(pos + mp(s1), 3), chunk=ci))
    pos += cl
    if ci + 1 < len(chunks): out.append(np.zeros(int(CHUNK_GAP * SR), np.float32)); pos += CHUNK_GAP
out.append(np.zeros(int(0.8 * SR), np.float32))
y = np.concatenate(out)
w = wave.open('/tmp/yt_raw.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(np.clip(y, -32768, 32767).astype('<i2').tobytes()); w.close()
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', '/tmp/yt_raw.wav', '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11', '-ar', '48000', 'voice.wav'], check=True)
json.dump(dict(total=len(y) / SR, words=words), open('words.json', 'w'), ensure_ascii=False)
print('total', round(len(y) / SR, 1), 's;', len(words), 'words')
