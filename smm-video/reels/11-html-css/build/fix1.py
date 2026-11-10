s = open('scenes11.py', encoding='utf-8').read()
def R(a, b, n=1):
    global s
    assert s.count(a) == n, (a, s.count(a))
    s = s.replace(a, b)
R('top:306px;left:auto;right:36px;font-size:20px', 'top:316px;left:auto;right:30px;font-size:20px')
# HTML code scene
R('left:40px;right:auto;top:262px;font-size:16px;border-color:var(--ok)', 'left:40px;right:auto;top:298px;font-size:16px;border-color:var(--ok)')
R('left:auto;right:40px;top:262px;font-size:16px;border-color:var(--pink)', 'left:auto;right:40px;top:298px;font-size:16px;border-color:var(--pink)')
R('s;top:330px;left:60px;right:60px"><div class="ub"><i></i><i></i><i></i><span>🔒 index.html</span></div><div class="pg" style="height:150px">', 's;top:350px;left:60px;right:60px"><div class="ub"><i></i><i></i><i></i><span>🔒 index.html</span></div><div class="pg" style="height:130px">')
R('top:535px;font-size:16px', 'top:548px;font-size:16px'); R('top:585px;font-size:16px', 'top:596px;font-size:16px'); R('top:640px;font-size:17px', 'top:648px;font-size:17px')
# CSS code scene
R('left:24px;right:auto;top:328px;font-size:15px', 'left:16px;right:auto;top:366px;font-size:13px;padding:6px 12px')
R('top:328px;font-size:15px;border-color:var(--purple)', 'top:366px;left:128px;right:auto;font-size:13px;padding:6px 12px;border-color:var(--purple)')
R('left:auto;right:24px;top:328px;font-size:15px', 'left:auto;right:16px;top:366px;font-size:13px;padding:6px 12px')
R('s;top:385px;left:70px;right:70px"', 's;top:412px;left:70px;right:70px"')
R('<div class="pg" style="height:150px;display:flex', '<div class="pg" style="height:130px;display:flex')
R('top:592px;font-size:16px', 'top:606px;font-size:16px', 2)
R('top:645px;font-size:19px">дарҳол', 'top:654px;font-size:18px">дарҳол')
# quiz
R('top:140px;font-size:34px">ранги кадом чиз <span', 'top:138px;font-size:34px">ранги кадом чиз<br><span')
R('<div class="ide" style="top:235px;left:40px;right:40px">', '<div class="ide" style="top:238px;left:40px;right:40px">')
R("brw(345, T[21] + 0.3, '<div style=\"height:118px\">'", "brw(372, T[21] + 0.3, '<div style=\"height:100px\">'")
R('top:525px;font-size:86px">?', 'top:538px;font-size:64px">?')
R('s;top:645px">💬', 's;top:650px">💬')
open('scenes11.py', 'w', encoding='utf-8').write(s)
