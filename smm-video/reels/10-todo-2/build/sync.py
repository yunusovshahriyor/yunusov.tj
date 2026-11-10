s = open('narration.md', encoding='utf-8').read()
def R(a, b):
    global s
    if a not in s: print('MISS', a[:60])
    s = s.replace(a, b)
R("силка дар описанияии профил!", "силка дар описанияи профил!")
R("Видеои пурраи дарсро дар YouTube тамошо кунед — пайванд дар Био-и профил!", "Видеои пурраи дарсро дар YouTube тамошо кунед — силка дар описанияи профил!")
R("▶️ Видеои пурраи дарс дар YouTube — пайванд дар Био-и профил (@shahriyor_yunusov).", "▶️ Видеои пурраи дарс дар YouTube — силка дар описанияи профил (@shahriyor_yunusov).")
open('narration.md', 'w', encoding='utf-8').write(s)
t = open('build/sentences_todo2.py', encoding='utf-8').read()
t = t.replace('("Видеои пурраи дарсро дар Ютюб тамошо кунед — пайванд дар Био-и профил!", "Видеои пурраи дарсро дар YouTube тамошо кунед — пайванд дар Био-и профил!")', '("Видеои пурраи дарсро дар Ютюб тамошо кунед — силка дар описанияи профил!", "Видеои пурраи дарсро дар YouTube тамошо кунед — силка дар описанияи профил!")')
open('build/sentences_todo2.py', 'w', encoding='utf-8').write(t)
