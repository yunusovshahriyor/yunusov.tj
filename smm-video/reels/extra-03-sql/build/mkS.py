# Матни овоз ва субтитрро аз narration.md мегирад ва sentences_sql.py месозад (ҷумлаҳо аз рӯи нуқта/савол/ундов).
import re
s = open('../narration.md', encoding='utf-8').read()
a = s.index('## Матн (барои субтитрҳо)'); b = s.index('## Матн барои ElevenLabs'); c = s.index('## Код дар видео')
def blocks(t): return [x.strip().strip('*') for x in t.split('\n\n')[1:] if x.strip()]
sub = blocks(s[a:b]); voi = blocks(s[b:c])
assert len(sub) == len(voi), (len(sub), len(voi))
def split(t):
    parts = re.split(r'(?<=[.!?])\s+(?=[А-ЯЁҶҲҚҒӢӮA-Z«"])', t)
    return [p.strip() for p in parts if p.strip()]
q = lambda z: '"' + z.replace('\\', '\\\\').replace('"', '\\"') + '"'
out = []
for vb, sb in zip(voi, sub):
    vs, ss = split(vb), split(sb)
    if len(vs) != len(ss):
        print('ФАРҚ ДАР ТАҚСИМ:', len(vs), len(ss), '|', vb[:50])
        vs, ss = [vb], [sb]
    for x, y in zip(vs, ss): out.append((x, None if x == y else y))
lines = ['# Ролик «Базаи маълумот чист?»: (текст для ElevenLabs v4, текст субтитров или None если совпадает).', 'S = [']
for x, y in out:
    lines.append('(' + q(x) + ', ' + ('None' if y is None else q(y)) + '),')
lines += [']', 'PRE_N = 1']
open('sentences_sql.py', 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
t = " ".join(x for x, _ in out)
open('tts-text.txt', 'w', encoding='utf-8').write(t + '\n')
print(len(out), 'ҷумла,', len(t), 'аломат')
