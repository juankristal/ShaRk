import numpy as np
import os
import matplotlib.pyplot as plt
import math

class HitObject:
    def __init__(self,column,timestamp,lnend=0) -> None:
        self.column=column
        self.timestamp=timestamp
        self.isln=lnend>0
        self.lnend=lnend

maps_folder="./mapas/"

def obtainHitObjectArrayFromOsu(file):
    hitobjects=[]
    l=file.readline()
    while "[HitObjects]" not in l:
        l=file.readline()

    while True:
        l=file.readline()
        if not l: break
        lineinfo=l.split(',')
        column=(int(lineinfo[0])-64)//128
        timestamp=int(lineinfo[2])
        hitobjects.append(HitObject(column,timestamp))

    return hitobjects

def obtainDensityCalculation(ho,bin_size):
    v=np.zeros(int(math.ceil(ho[-1].timestamp-ho[0].timestamp)/bin_size))
    x=np.zeros(int(math.ceil(ho[-1].timestamp-ho[0].timestamp)/bin_size))
    d=0
    i=0
    b=0
    while i in range(len(ho)):
        if ho[i].timestamp<=(ho[0].timestamp+(b+1)*bin_size):
            d+=1
            i+=1
        else:
            x[b]=b*bin_size
            v[b]=d*(1000/bin_size)
            b+=1
            d=0
    plt.plot(x,v, color ="blue")
    plt.show()
    return np.average(v)


bin_size=500

for m in os.listdir(maps_folder):
    with open(maps_folder+m,"r",encoding="utf8") as f:
        ho = obtainHitObjectArrayFromOsu(f)
        print(obtainDensityCalculation(ho,bin_size))



