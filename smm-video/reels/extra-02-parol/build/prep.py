# Склеивает куски, сжимает паузы (>0.30 с -> 0.20 с, между абзацами 0.35 с), темп ×1.1; пишет voice.wav и words.json.
import json, re, subprocess, wave, numpy as np
SR = 44100; TEMPO = 1.1; MAXGAP = 0.30; KEEP = 0.20; PARA = 0.35; LEAD = 0.30
chunks = json.load(open('chunks.json')); parts = []; words = []; pos = 0.0
def dec(p): return np.frombuffer(subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', p, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout, '<i2').astype(np.float32)
for ci, t in enumerate(chunks):
    al = json.load(open(f'chunk{ci}.alignment.json'))['alignment']; cs, ce = al['character_start_times_seconds'], al['character_end_times_seconds']
    x = dec(f'chunk{ci}.mp3'); dur = len(x) / SR
    ws = []
    for m in re.finditer(r'\S+', t):
        idx = [k for k in range(m.start(), m.end()) if re.match(r'\w', t[k])] or list(range(m.start(), m.end()))
        ws.append([m.group(), cs[idx[0]], ce[idx[-1]], '\n\n' in t[m.end():m.end() + 3]])
    cuts = [(0, max(0, ws[0][1] - 0.05))]
    for p, n in zip(ws, ws[1:]):
        keep = PARA if p[3] else KEEP; g = n[1] - p[2]
        if g > max(MAXGAP, keep): m = (p[2] + n[1]) / 2; cuts.append((m - (g - keep) / 2, m + (g - keep) / 2))
    cuts.append((min(dur, ws[-1][2] + 0.12), dur))
    keepi = []; q = 0.0
    for a, b in cuts:
        if a > q: keepi.append((q, a))
        q = max(q, b)
    if q < dur: keepi.append((q, dur))
    fd = int(0.008 * SR)
    for a, b in keepi:
        s = x[int(a * SR):int(b * SR)].copy()
        if len(s) > 2 * fd: s[:fd] *= np.linspace(0, 1, fd); s[-fd:] *= np.linspace(1, 0, fd)
        parts.append(s)
    mp = lambda t0: t0 - sum(max(0, min(b, t0) - a) for a, b in cuts if a < t0)
    for w, a, b, _ in ws: words.append(dict(w=w, t0=pos + mp(a), t1=pos + mp(b)))
    pos += sum(b - a for a, b in keepi)
    if ci + 1 < len(chunks): parts.append(np.zeros(int(PARA * SR), np.float32)); pos += PARA
y = np.concatenate(parts)
w = wave.open('/tmp/claude-0/-home-user-yunusov-tj/0e923016-86d6-520f-a0b3-a6fd06299a3e/scratchpad/vcut.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(y.astype('<i2').tobytes()); w.close()
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', '/tmp/claude-0/-home-user-yunusov-tj/0e923016-86d6-520f-a0b3-a6fd06299a3e/scratchpad/vcut.wav', '-af',
                f'atempo={TEMPO},adelay={int(LEAD * 1000)}:all=1,apad=pad_dur=0.6,loudnorm=I=-16:TP=-1.5:LRA=11', '-ar', '48000', 'voice.wav'], check=True)
for d in words: d['t0'] = round(LEAD + d['t0'] / TEMPO, 3); d['t1'] = round(LEAD + d['t1'] / TEMPO, 3)
total = LEAD + len(y) / SR / TEMPO + 0.6
json.dump(dict(total=round(total, 2), words=words), open('words.json', 'w'), ensure_ascii=False)
print('total', round(total, 1), 'words', len(words))
