import re
s = open('scenes_todo.py', encoding='utf-8').read()
# 1. бе сатри холӣ байни .ln дар pre
s = s.replace("html = f'''<!doctype html>", "H = [re.sub(r'</div>\s*\n<div class=\"ln\"', '</div><div class=\"ln\"', h) for h in H]\nhtml = f'''<!doctype html>")
# 2. санҷиш: кортҳо амудӣ
s = s.replace('''{task(330, "нон харидан", T[16] + 0.4, left=30, right=300, idx=0, extra="padding:8px 10px")}
{task(330, "дарс хондан", T[16] + 0.5, left=180, right=150, idx=1, extra="padding:8px 10px")}
{task(330, "занг задан", T[16] + 0.6, left=330, right=20, idx=2, extra="padding:8px 10px")}
<div class="h1 acc pop" style="--a:{t_c:.2f}s;top:420px;font-size:110px">?</div>
<div class="pill pop" style="--a:{T[18]:.2f}s;top:590px;''', '''{task(305, "нон харидан", T[16] + 0.4, idx=0, extra="padding:7px 16px")}
{task(353, "дарс хондан", T[16] + 0.5, idx=1, extra="padding:7px 16px")}
{task(401, "занг задан", T[16] + 0.6, idx=2, extra="padding:7px 16px")}
<div class="h1 acc pop" style="--a:{t_c:.2f}s;top:455px;font-size:100px">?</div>
<div class="pill pop" style="--a:{T[18]:.2f}s;top:590px;''')
open('scenes_todo.py', 'w', encoding='utf-8').write(s)
