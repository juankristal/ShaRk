import numpy as np
import os
import matplotlib.pyplot as plt
import math
from scipy.interpolate import make_interp_spline, BSpline
import random

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

def obtainDensityCalculation2(ho,bin_size):
    v=np.zeros(len(ho),dtype=int)
    x=np.zeros(len(ho),dtype=int)
    j=0
    k=0
    lastt=-1
    for i in range(len(ho)):
        # if ho[i].timestamp==lastt:
        #     v[i]=-1
        #     x[i]=-1
        #     continue
        # lastt=ho[i].timestamp
        d=0
        while ho[j].timestamp<(ho[i].timestamp-bin_size/2):
            j+=1

        while ho[k].timestamp<(ho[i].timestamp+bin_size/2) and k<len(ho)-1:
            k+=1

        v[i]=k-j
        x[i]=ho[i].timestamp

    return (x,v)


bin_size=3000
for m in os.listdir(maps_folder):
    with open(maps_folder+m,"r",encoding="utf8") as f:
        ho = obtainHitObjectArrayFromOsu(f)
        x,y=obtainDensityCalculation2(ho,bin_size)
        w=1000
        y_roll=np.convolve(y, np.ones(w), 'same') / w
        # xf=x[x!=-1]
        # yf=y[y!=-1]
        # xnew = np.linspace(xf.min(), xf.max(), num=xf.shape[0]*5) 
        # print(xnew)
        # spl = BSpline(xf, yf, k=311,extrapolate="periodic")
        # smooth_y= spl(xnew)
        # plt.plot(xnew[1:],smooth_y[1:],label=m)
        r = random.random()
        b = random.random()
        g = random.random()
  
        color = (r, g, b)
        plt.plot(x,y,c=color,alpha=0.3)
        plt.plot(x,y_roll,label=m,c=color,linewidth=3)
plt.legend()
plt.show()
    
