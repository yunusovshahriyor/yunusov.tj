s = open('scenes_sql.py', encoding='utf-8').read()
def R(a, b):
    global s
    if a not in s: print('MISS', a[:70])
    s = s.replace(a, b)
R('МISЛИ ҶУМЛАИ ОДДӢ', 'МИСЛИ ҶУМЛАИ ОДДӢ')
R('<div class="c blk" style="--a:{T[4]:.2f}s"></div>\n', '')
R('{TYP(w_har, 0.5, "Алӣ", "Алӣ")}', '<span class="reveal" style="--a:{w_har:.2f}s;--d:0.5s">Алӣ</span>')
R(".glass.ph{border-radius:36px}", ".glass.ph{border-radius:36px}\n.hide{position:absolute;inset:0;pointer-events:none;animation:hide .3s ease-in var(--g) forwards}\n@keyframes hide{to{opacity:0}}")
# 5 -> 5 000
R('''<div class="c num blurin" style="--a:{T[6] + 0.2:.2f}s;top:200px;font-size:150px">5</div>
<div class="c rise" style="--a:{T[6] + 0.4:.2f}s;top:360px;font:600 24px 'Segoe UI Semibold';opacity:.8">харидор — ҳама чиз равшан ✓</div>
<div class="c num blurin" style="--a:{w_hz:.2f}s;top:200px;font-size:100px;background:#04060D;padding:20px 0">5 000</div>''',
'''<div class="hide" style="--g:{w_hz:.2f}s"><div class="c num blurin" style="--a:{T[6] + 0.2:.2f}s;top:200px;font-size:150px">5</div>
<div class="c rise" style="--a:{T[6] + 0.4:.2f}s;top:360px;font:600 24px 'Segoe UI Semibold';opacity:.8">харидор — ҳама чиз равшан ✓</div></div>
<div class="c num blurin" style="--a:{w_hz:.2f}s;top:215px;font-size:110px">5 000</div>''')
# хати декоративӣ
import re
s = re.sub(r'\n<svg class="abs" style="left:0;top:380px"[^\n]*', "''')", s)
open('scenes_sql.py', 'w', encoding='utf-8').write(s)
