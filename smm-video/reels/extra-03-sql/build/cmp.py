import re, sys
s = open('narration.md', encoding='utf-8').read()
a = s.index('## Матн (барои субтитрҳо)'); b = s.index('## Матн барои ElevenLabs'); c = s.index('## Код дар видео')
sub = [x.strip().strip('*') for x in s[a:b].split('\n\n')[1:] if x.strip()]
voi = [x.strip().strip('*') for x in s[b:c].split('\n\n')[1:] if x.strip()]
print(len(sub), len(voi))
for i in range(max(len(sub), len(voi))):
    print(i, '|S|', sub[i] if i < len(sub) else '—'); print(i, '|V|', voi[i] if i < len(voi) else '—'); print()
