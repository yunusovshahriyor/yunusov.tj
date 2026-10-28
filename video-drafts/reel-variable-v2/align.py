# Выравнивает предложения текста по паузам в записи (без распознавания речи):
# ожидаемые границы считаются по числу слогов, затем притягиваются к ближайшим паузам (DP).
import json,re,sys
gaps=[tuple(map(float,l.split())) for l in open(sys.argv[1])]
TOTAL=float(sys.argv[2])
S=[ # (субтитр, произносимая форма для подсчёта слогов)
("Тағйирёбанда.",None),
("Калимаи душвор менамояд, лекин аслан хеле оддӣ аст.",None),
("Ҳозир дар як дақиқа мефаҳмем.",None),
("Тасаввур кунед, ки як қуттӣ доред.",None),
("Қуттии оддии картонӣ.",None),
("Болои он ном менависем, масалан: «age», яъне синну сол.","Болои он ном менависем масалан эйдж яъне синну сол"),
("Ва дар дохили он рақам мегузорем: бисту панҷ.",None),
("Дар барномасозӣ ин чунин навишта мешавад: let age = 25.","Дар барномасозӣ ин чунин навишта мешавад лет эйдж баробари бисту панҷ"),
("Яъне қуттии «age» қимати бисту панҷ дорад.","Яъне қуттии эйдж қимати бисту панҷ дорад"),
("Як сол мегузарад.",None),
("Рақами кӯҳнаро нест мекунем ва ба ҷои он бисту шашро мегузорем.",None),
("Қуттӣ ҳамон, ном ҳамон.",None),
("Танҳо қимат иваз шуд.",None),
("Барои ҳамин онро «тағйирёбанда» мегӯянд: чизе, ки тағйир меёбад.",None),
("Ин дар ҳаёт ҳам ҳаст, масалан:",None),
("холи бозӣ, бақияи ҳисоби бонк, шумораи пайравонатон дар Instagram.","холи бозӣ бақияи ҳисоби бонк шумораи пайравонатон дар инстаграм"),
("Ҳамааш тағйирёбанда аст.",None),
("Ном — болои қуттӣ.",None),
("Қимат — дар дохили қуттӣ.",None),
("Ва қимат тағйир меёбад.",None),
("Ва акнун савол: агар қуттии худатонро медоштед, номаш чӣ мешуд ва дар дохилаш чӣ мегузоштед?",None),
("Дар шарҳ нависед.",None),
("Дарси оянда — шарт, «if/else».","Дарси оянда шарт иф элс"),
("Обуна шавед!",None),
]
V=set("аеёиоуэюяӣӯ")
syl=[max(1,sum(ch in V for ch in (sp or t).lower())) for t,sp in S]
# speech segments
segs=[];prev=0.0
for a,b in gaps:
    if a>prev: segs.append((prev,a))
    prev=b
if prev<TOTAL: segs.append((prev,TOTAL))
Ts=sum(b-a for a,b in segs)
def wall(x):  # speech-time -> wall-time
    for a,b in segs:
        if x<=b-a: return a+x
        x-=b-a
    return TOTAL
N=sum(syl)
# DP по паузам: каждое предложение должно иметь правдоподобный темп речи (слогов/с),
# длинные паузы предпочтительнее как границы предложений.
import math
r0=N/Ts; NG=len(gaps); K=len(syl)
def sent_cost(i,s0,e0):
    d=e0-s0
    if d<=0.2: return INF
    sp=sum(b-a for a,b in segs if a>=s0-1e-6 and b<=e0+1e-6) or d
    return math.log((syl[i]/sp)/r0)**2
INF=1e18
# state: sentence i starts at time st (index of gap whose end it starts at, -1 = time 0)
best={(-1):(0.0,[])}
for i in range(K):
    nb={}
    for g0,(c0,path) in best.items():
        s0=0.0 if g0==-1 else gaps[g0][1]
        if i==K-1:
            c=c0+sent_cost(i,s0,TOTAL)
            if c<nb.get('end',(INF,))[0]: nb['end']=(c,path)
            continue
        for j in range(g0+1,NG):
            e0=gaps[j][0]
            if e0-s0>12: break
            c=c0+sent_cost(i,s0,e0)-0.8*min(gaps[j][1]-gaps[j][0],0.35)
            if c<nb.get(j,(INF,))[0]: nb[j]=(c,path+[j])
    best=nb
cost,assign=best['end']
starts=[0.0];ends=[]
for j in assign: ends.append(gaps[j][0]); starts.append(gaps[j][1])
ends.append(TOTAL)
assign=[0]+assign
out=[{"i":i,"text":S[i][0],"start":round(starts[i],2),"end":round(ends[i],2),"snap":True} for i in range(len(S))]
json.dump(out,open('timeline.json','w'),ensure_ascii=False,indent=1)
for o in out:
    print(f'{o["start"]:6.2f}-{o["end"]:6.2f} {"" if o["snap"] else "~"} {o["text"][:60]}')
