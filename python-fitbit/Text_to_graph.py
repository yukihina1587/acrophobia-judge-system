import matplotlib
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
part = []

for line in f:
    s = line.split("|")
    if(len(s) >= 2 and s[1] != "   TIME   "):
        xx = s[1]
        xxtime = dt.strptime(xx, ' %H:%M:%S ')
        yy = s[2]
        pulse.append(int(s[2]))

        if(xxtime.hour >= 3 and xxtime.minute >= 0 and xxtime.second >= 0):
            if (xxtime.hour == 3 and xxtime.minute == 11):
                break
            xlist.append(xx)
            ylist.append(yy)
            part.append(int(yy))
            sum += int(yy)
            count += 1
f.close()

rate = 0
i = 1
for p in part:
    x = (p-(sum/count)) ** 2
    i += 1

S_D_ = 0
S_E_ = 0

print(x/count)
S_D_ = (x / count) ** 0.5
S_E_ = S_D_ / (count ** 0.5)

print("標準偏差:", S_D_)
print("標準誤差:", S_E_)

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