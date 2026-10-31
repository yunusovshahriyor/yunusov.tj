# Сжимает длинные паузы по разметке ElevenLabs, ускоряет на 10% и пересчитывает время слов/предложений.
import json, re, subprocess, wave, numpy as np, sys
sys.path.insert(0, '.')
from sentences_function import S, PRE_N
TEMPO = 1.1; MAXGAP = 0.30; KEEP = 0.20; SR = 44100
# Начало (заголовок + первое предложение) читаем без ускорения, после «Давр?» — пауза
SLOW_SENTENCES = 4; SLOW_TEMPO = 0.95; LEAD = 0.30
# после «Чӣ тавр?» и «Давр?» — паузы подлиннее
SENT_PAUSE = {1: 0.45, 2: 0.45}
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
_ends = {}; _p = 0
for _i, (_tt, _) in enumerate(S):
    _k = text.index(_tt, _p); _p = _k + len(_tt); _ends[_p] = _i
for k, (p, n) in enumerate(zip(words, words[1:])):
    g = n[3] - p[4]
    keep_gap = SENT_PAUSE.get(_ends.get(p[1]), KEEP)
    if g <= keep_gap:
        continue
    if g > max(MAXGAP, keep_gap) or keep_gap != KEEP:
        m = (p[4] + n[3]) / 2; cuts.append((m - (g - keep_gap) / 2, m + (g - keep_gap) / 2))
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
w = wave.open('voice_cut.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(y.astype('<i2').tobytes()); w.close()
def cut(t):
    return t - sum(max(0, min(b, t) - a) for a, b in cuts if a < t)
# граница «медленной» части: середина паузы после SLOW_SENTENCES-го предложения
_k = text.index(S[SLOW_SENTENCES - 1][0]) + len(S[SLOW_SENTENCES - 1][0])
_last = [w for w in words if w[1] <= _k][-1]; _next = [w for w in words if w[0] >= _k][0]
B = cut((_last[4] + _next[3]) / 2)
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', 'voice_cut.wav', '-filter_complex',
                f'[0]asplit[a][b];[a]atrim=0:{B},asetpts=PTS-STARTPTS,atempo={SLOW_TEMPO},adelay={int(LEAD*1000)}:all=1[s];[b]atrim={B},asetpts=PTS-STARTPTS,atempo={TEMPO}[q];'
                f'[s][q]concat=n=2:v=0:a=1,loudnorm=I=-16:TP=-1.5:LRA=11', '-ar', '48000', 'voiceA.wav'], check=True)
def f(t):
    c = cut(t)
    return LEAD + (c / SLOW_TEMPO if c <= B else B / SLOW_TEMPO + (c - B) / TEMPO)
W = [dict(c0=a, c1=b, w=wd, t0=round(f(s), 3), t1=round(f(e), 3)) for a, b, wd, s, e in words]
# предложения: по позициям в тексте
sent = []; pos = 0
for i, (tt, disp) in enumerate(S):
    k = text.index(tt, pos); pos = k + len(tt)
    ws = [x for x in W if x['c0'] >= k and x['c1'] <= pos]
    sent.append(dict(i=i, tts=tt, text=disp or tt, start=ws[0]['t0'], end=ws[-1]['t1'], words=ws))
total = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', 'voiceA.wav'], capture_output=True, text=True).stdout)
pre = sent[:PRE_N]; main = [dict(x, i=j) for j, x in enumerate(sent[PRE_N:])]
json.dump(dict(total=total, pre=pre, sentences=main), open('timelineA.json', 'w'), ensure_ascii=False, indent=0)
for s in sent: print(f"{s['start']:6.2f}-{s['end']:6.2f} {s['text'][:60]}")
print('total', total, 'removed', round(sum(b - a for a, b in cuts), 2))
