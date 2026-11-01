# Голос с паузами-вставками + фон + эффекты -> mix.wav
import json, subprocess, wave, numpy as np
SR = 48000; G = json.load(open('gaps.json'))
x = np.frombuffer(subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', 'voice.wav', '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout, '<i2').astype(np.float32)
parts, q = [], 0
for t, d in sorted(G['gaps']):
    i = int(t * SR); parts += [x[q:i], np.zeros(int(d * SR), np.float32)]; q = i
parts.append(x[q:]); y = np.concatenate(parts)
y = np.concatenate([y, np.zeros(max(0, int(G['end'] * SR) - len(y)), np.float32)])[:int(G['end'] * SR)]
w = wave.open('voice_g.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(y.astype('<i2').tobytes()); w.close()
