# Тартиби охир: «Қадами навбатӣ … Обуна шавед…» (884.8–893.9 с) ба охири овоз кӯчонида мешавад (то ҷумлаи тасдиқшудаи «Обуна шавед…» охирин бошад). Бе сабти нав.
import json, subprocess, wave, numpy as np
SR = 48000
J = json.load(open('words_orig.json')); W = J['words']
ia = next(i for i, w in enumerate(W) if w['w'] == 'Қадами' and w['t0'] > 880)
ib = next(i for i, w in enumerate(W) if w['w'] == 'Ва' and w['t0'] > 893 and W[i + 1]['w'] == 'ҳоло')
assert W[ib - 1]['w'] == 'намонед.', W[ib - 1]
ta = (W[ia - 1]['t1'] + W[ia]['t0']) / 2; tb = (W[ib - 1]['t1'] + W[ib]['t0']) / 2
x = np.frombuffer(subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', 'voice_orig.wav', '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout, '<i2').astype(np.float32)
A, X, B = x[:int(ta * SR)], x[int(ta * SR):int(tb * SR)], x[int(tb * SR):]
f = int(.01 * SR)
def fade(s):
    s = s.copy(); s[:f] *= np.linspace(0, 1, f); s[-f:] *= np.linspace(1, 0, f); return s
# хомӯшии охири B (0.8 с) нигоҳ дошта мешавад ба охири X
tail = int(.8 * SR); Bm, Bt = B[:-tail], B[-tail:]
y = np.concatenate([A, Bm, np.zeros(int(.5 * SR), np.float32), X])
y = np.concatenate([y, np.zeros(tail, np.float32)])
sh_b = -(tb - ta); sh_x = (len(Bm) + int(.5 * SR)) / SR - 0  # X ба ҷои B меафтад
W2 = []
for i, w in enumerate(W):
    w = dict(w)
    if ia <= i < ib: w['t0'] = round(w['t0'] - ta + len(A) / SR + (len(Bm) + int(.5 * SR)) / SR, 3); w['t1'] = round(w['t1'] - ta + len(A) / SR + (len(Bm) + int(.5 * SR)) / SR, 3)
    elif i >= ib: w['t0'] = round(w['t0'] - (tb - ta), 3); w['t1'] = round(w['t1'] - (tb - ta), 3)
    W2.append(w)
W2.sort(key=lambda w: w['t0'])
w = wave.open('voice.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(np.clip(y, -32768, 32767).astype('<i2').tobytes()); w.close()
json.dump(dict(total=len(y) / SR, words=W2), open('words.json', 'w'), ensure_ascii=False)
print('ok', round(ta, 2), round(tb, 2), 'total', round(len(y) / SR, 2), 'was', round(J['total'], 2))
