import re
s = open('sentences_html.py', encoding='utf-8').read()
t = " ".join(re.findall(r'^\("([^"]*)",', s, re.M))
open('tts-text.txt', 'w', encoding='utf-8').write(t + "\n")
print(len(t), "аломат")
