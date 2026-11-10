import re
s = open('narration.md', encoding='utf-8').read()
a = s.index('## Матн (барои субтитрҳо)'); b = s.index('## Матн барои ElevenLabs'); c = s.index('## Код дар видео')
sub = [x.strip().strip('*') for x in s[a:b].split('\n\n')[1:] if x.strip()]
voi = [x.strip().strip('*') for x in s[b:c].split('\n\n')[1:] if x.strip()]
print(len(sub), len(voi))
for i, (x, y) in enumerate(zip(sub, voi)):
    print(i, '|S|', x[:95]); print(i, '|V|', y[:95])
print('--- ферма:', [x[:60] for x in sub[len(voi):]], [y[:60] for y in voi[len(sub):]])
