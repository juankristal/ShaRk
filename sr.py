import numpy as np
import os
import matplotlib.pyplot as plt
import math
from numpy.lib.function_base import average
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

    return v

def obtainManipCalculation(ho,bin_size):
    v=np.zeros(len(ho))       
    x=np.zeros(len(ho))
    j=0
    k=0
    for i in range(len(ho)):
        while ho[j].timestamp<(ho[i].timestamp-bin_size/2):
            j+=1

        while ho[k].timestamp<(ho[i].timestamp+bin_size/2) and k<len(ho)-1:
            k+=1

        d=[1,1,1,1]
        for h in range(j,k):
            d[ho[h].column]=d[ho[h].column]+1
        
        l_manip=min(d[:2])/max(d[:2])/(1+np.var(d[:2])) #[0,1]Closer to 1-> more masheable
        r_manip=min(d[2:])/max(d[2:])/(1+np.var(d[2:]))
        h_manip=min(sum(d[:2]),sum(d[2:]))/max(sum(d[:2]),sum(d[2:]))/(1+np.var([sum(d[:2]),sum(d[2:])]))
        v[i]=np.average([l_manip,r_manip,h_manip]) #[0,1] Clpser to 1 -> easier to mash
        # v[i]=(
        #     np.var(d[:2]) * (min(d[:2])/max(d[:2]))
        #    +np.var(d[2:]) * (min(d[2:])/max(d[2:]))
        #    +np.var([sum(d[:2]),sum(d[2:])]) * (min(sum(d[:2]),sum(d[2:]))/max(sum(d[:2]),sum(d[2:])))
        # )
    return v


text=["suiren","bass drop","lolit","starfall","nhelv"]
dns_bin_size=1000
mnp_bin_size=1000
w=100
fig, (dens, manip, total)=plt.subplots(3,1,sharex=True)

i=.9
for m in os.listdir(maps_folder):
    if text!=[] and not any([t in m.lower() for t in text]): continue
    with open(maps_folder+m,"r",encoding="utf8") as f:
        ho = obtainHitObjectArrayFromOsu(f)
        x=np.array([h.timestamp for h in ho])

        r = random.random()
        b = random.random()
        g = random.random()
        color = (r, g, b)

        dns=obtainDensityCalculation2(ho,dns_bin_size)
        dns_roll=np.array([np.average(dns[max(0,i-w//2):min(len(ho),i+w//2)]) for i in range(len(ho))])
       
        dens.plot(x,dns,c=color,alpha=0.1)
        dens.plot(x,dns_roll,label=m,c=color,linewidth=3)
        dens.text(0,i,s=f"{m[:12]+'...'}Avg. diff= {np.average(dns_roll)}",horizontalalignment='left',
     verticalalignment='center',
     transform = dens.transAxes)

        mnp=obtainManipCalculation(ho,mnp_bin_size)
        mnp_roll=np.array([np.average(mnp[max(0,i-w//2):min(len(ho),i+w//2)]) for i in range(len(ho))])
        manip.plot(x,mnp,c=color,alpha=0.1)
        manip.text(0,i,s=f"{m[:12]+'...'}Avg. diff= {np.average(mnp_roll)}",horizontalalignment='left',
     verticalalignment='center',
     transform = manip.transAxes)

        manip.plot(x,mnp_roll,label=m,c=color,linewidth=3)
        ttl_raw=dns/mnp
        ttl=dns_roll/mnp_roll
        ttl_roll=np.array([np.average(ttl[max(0,i-w//2):min(len(ho),i+w//2)]) for i in range(len(ho))])
        total.plot(x,ttl_raw,c=color,alpha=0.1)
        total.text(0,i,s=f"{m[:12]+'...'}Avg. diff= {np.average(ttl)}",horizontalalignment='left',
     verticalalignment='center',
     transform = total.transAxes)
        total.plot(x,ttl_roll,label=m,c=color,linewidth=3)
        total.set_ylim(0,100)

        i-=0.1

dens.legend()
plt.show()

