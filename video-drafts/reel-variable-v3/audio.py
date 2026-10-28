# Синтез звуковых эффектов и фоновой музыки (numpy), события из sfx.json.
import json, wave, numpy as np
SR = 48000
cfg = json.load(open('sfx.json')); END = cfg['end']
rng = np.random.default_rng(7)
def env(n, a=0.002, d=0.1):
    t = np.arange(n) / SR
    return np.minimum(1, t / a) * np.exp(-t / d)
def lp(x, k):  # простой однополюсный ФНЧ
    y = np.empty_like(x); acc = 0.0
    for i, v in enumerate(x): acc += k * (v - acc); y[i] = acc
    return y
def sweep(f0, f1, dur):
    n = int(SR * dur); f = np.geomspace(f0, f1, n)
    return np.sin(2 * np.pi * np.cumsum(f) / SR)
def make(name):
    if name == 'pop':
        n = int(SR * .09); return 0.45 * sweep(420, 980, .09) * env(n, .002, .03)
    if name == 'click':
        n = int(SR * .03); x = rng.standard_normal(n) * env(n, .0005, .004) * .5
        return x + 0.4 * np.sin(2 * np.pi * 3200 * np.arange(n) / SR) * env(n, .0005, .006)
    if name == 'key':
        n = int(SR * .035); x = rng.standard_normal(n); x = x - lp(x, .25)
        return 0.22 * x * env(n, .0005, .008) * rng.uniform(.7, 1.1)
    if name == 'tick':
        n = int(SR * .02); return 0.18 * np.sin(2 * np.pi * 2400 * np.arange(n) / SR) * env(n, .0003, .004)
    if name == 'tick2':
        n = int(SR * .25); tt = np.arange(n) / SR
        return 0.3 * (np.sin(2 * np.pi * 880 * tt) + .5 * np.sin(2 * np.pi * 1320 * tt)) * env(n, .002, .06)
    if name == 'ding':
        n = int(SR * .7); tt = np.arange(n) / SR
        return 0.22 * (np.sin(2 * np.pi * 1318.5 * tt) + .6 * np.sin(2 * np.pi * 1975.5 * tt) + .3 * np.sin(2 * np.pi * 2637 * tt)) * env(n, .002, .22)
    if name == 'thump':
        n = int(SR * .3); x = sweep(140, 45, .3) * env(n, .002, .09)
        nz = rng.standard_normal(n) * env(n, .001, .02); nz = lp(nz, .15)
        return 0.9 * x + 0.6 * nz
    if name == 'thud':
        n = int(SR * .2); return 0.55 * sweep(110, 55, .2) * env(n, .002, .05)
    if name == 'whoosh':
        n = int(SR * .4); x = rng.standard_normal(n); tt = np.linspace(0, 1, n)
        k = .02 + .25 * np.sin(np.pi * tt) ** 2
        y = np.empty(n); acc = 0.0
        for i in range(n): acc += k[i] * (x[i] - acc); y[i] = acc
        return 0.5 * y * np.sin(np.pi * tt) ** 1.5
    raise ValueError(name)
N = int(SR * END) + SR
fx = np.zeros(N)
cache = {}
for ev in cfg['sfx']:
    s = make(ev['name']) if ev['name'] == 'key' else cache.setdefault(ev['name'], make(ev['name']))
    i = int(ev['t'] * SR); g = ev.get('gain', 1.0)
    if i < 0: continue
    j = min(N, i + len(s)); fx[i:j] += g * s[:j - i]

# фон: мягкий лоу-фай (аккорды + пиццикато-арпеджио), 92 BPM
bpm = 92; beat = 60 / bpm
chords = [[57, 60, 64, 67], [53, 57, 60, 64], [48, 52, 55, 59], [55, 59, 62, 65]]  # Am7 Fmaj7 Cmaj7 G7
mus = np.zeros(N); tt_all = np.arange(N) / SR
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
bar = 4 * beat; nb = int(END / bar) + 2
for b in range(nb):
    ch = chords[b % 4]; s0 = int(b * bar * SR); n = int(bar * SR)
    if s0 >= N: break
    n = min(n, N - s0); tt = np.arange(n) / SR
    pad = sum(np.sin(2 * np.pi * hz(m) * tt) + .25 * np.sin(2 * np.pi * 2 * hz(m) * tt) for m in ch)
    a = np.minimum(1, tt / .4) * np.minimum(1, (n / SR - tt) / .4)
    mus[s0:s0 + n] += .05 * pad * a
    for k in range(8):  # восьмые
        m = ch[[0, 2, 1, 3, 2, 1, 3, 2][k]] + 12
        i0 = s0 + int(k * beat / 2 * SR); L = int(.35 * SR)
        if i0 + L > N: continue
        t2 = np.arange(L) / SR
        mus[i0:i0 + L] += .07 * (np.sin(2 * np.pi * hz(m) * t2) + .3 * np.sin(4 * np.pi * hz(m) * t2)) * env(L, .003, .12)
    for k in range(4):  # мягкий бас-удар на долях 1 и 3, шейкер на каждой доле
        i0 = s0 + int(k * beat * SR); L = int(.25 * SR)
        if i0 + L > N: continue
        if k % 2 == 0: mus[i0:i0 + L] += .25 * sweep(90, 45, .25) * env(L, .002, .06)
        sh = rng.standard_normal(int(.05 * SR)); sh = sh - lp(sh, .3)
        mus[i0 + int(beat / 2 * SR):i0 + int(beat / 2 * SR) + len(sh)] += .03 * sh * env(len(sh), .002, .012)
mus = lp(mus, .35)
fade = np.ones(N); fl = int(1.5 * SR); end_i = int(END * SR)
fade[end_i - fl:end_i] = np.linspace(1, 0, fl); fade[end_i:] = 0
mus *= fade * np.minimum(1, tt_all / 0.8)
def write(path, x):
    x = np.clip(x, -1, 1); w = wave.open(path, 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((x * 32767).astype('<i2').tobytes()); w.close()
write('fx.wav', fx / max(1, np.abs(fx).max()) * .9)
write('music.wav', mus / np.abs(mus).max() * .9)
print('ok', len(cfg['sfx']))
