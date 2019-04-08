import matplotlib
# AGG(Anti-Grain Geometry engine)  pngで出力できる
matplotlib.use('TkAgg')
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime as dt

f = open("2018-11-07.txt","r")
xlist = list()
ylist = list()
pulse = []
sum = 0
count = 0

for line in f:
    s = line.split("|")
    if(len(s) >= 2 and s[1] != "   TIME   "):
        # print(s[1])
        xx = s[1]
        xxtime = dt.strptime(xx, ' %H:%M:%S ')
        yy = s[2]
        pulse.append(int(s[2]))

        if(xxtime.hour >= 3 and xxtime.minute >= 0 and xxtime.second >= 0):
            if (xxtime.hour == 4 and xxtime.minute == 0):
                break
            xlist.append(xx)
            ylist.append(yy)
            sum = sum + int(yy)
            count+= 1
f.close()

rate = 0
n = []
i = 1
for p in pulse:
    #print(pulse[p] , end="")
    x = (p-(sum/count)) ** 2
    i+=1
    #n.append(pulse[p+1] - pulse[p])
    #if n[p] >= 2:
    #    rate += 1

print(x)
SD = (x / count) ** 0.5
SE = SD / (count ** 0.5)

#pNN50 = rate / 50
#print("pNN50:", pNN50)

print("標準偏差:", SE)

fig, ax = plt.subplots(figsize=(20, 20))
ax.plot(xlist , ylist)
labels = ax.get_xticklabels()
plt.setp(labels, rotation=90, fontsize=8)

plt.title('pulse data')
plt.xlabel("time")
plt.ylabel("pulse")

plt.tight_layout()
plt.show()

# def fear_judge():