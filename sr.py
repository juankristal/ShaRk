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
        lnend=int(lineinfo[5].split(":")[0])
        hitobjects.append(HitObject(column,timestamp,lnend))

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
        v[i]=np.average([l_manip,r_manip,h_manip]) #[0,1] Closer to 1 -> easier to mash
        # v[i]=(
        #     np.var(d[:2]) * (min(d[:2])/max(d[:2]))
        #    +np.var(d[2:]) * (min(d[2:])/max(d[2:]))
        #    +np.var([sum(d[:2]),sum(d[2:])]) * (min(sum(d[:2]),sum(d[2:]))/max(sum(d[:2]),sum(d[2:])))
        # )
    return v

def obtainMotionCalculation(ho,bin_size):
    v=np.zeros(len(ho))       
    x=np.zeros(len(ho))
    j=0
    k=0

    supr_threshold=35
    for i in range(len(ho)):
        # while ho[j].timestamp<(ho[i].timestamp-bin_size/2):
        #     j+=1

        # while ho[k].timestamp<(ho[i].timestamp+bin_size/2) and k<len(ho)-1:
        #     k+=1

        # m=0
        # before,after=False,False
        # if ho[i].timestamp!=ho[0].timestamp:
        #     print(ho[i].timestamp)
        #     print(ho[0].timestamp)
        #     n=0
        #     while ho[i-1-n].timestamp==ho[i].timestamp:
        #         n+=1
        #         print(i-1-n)
        #         print(ho[i-1-n].column,"",ho[i-1-n].timestamp)
        #     ch=ho[i].column
        #     c=ho[i-1-n].column
        #     csum=c+ch
        #     if c==ch:
        #         m+=1.5
        #     elif csum==5 or csum==1:
        #         m+=1
        #     else:
        #         m+=0.5
        #     before=True
        w=0
        if ho[i].timestamp!=ho[len(ho)-1].timestamp:
            n=0
            while ho[i+1+n].timestamp==ho[i].timestamp:
                n+=1
            distance=ho[i+1+n].timestamp-ho[i].timestamp
            nn=n
            while ho[i+1+nn].timestamp==ho[i+1+n].timestamp:
                ch=ho[i].column
                c=ho[i+1+nn].column
                csum=c+ch
                
                if c==ch:
                    w+=2
                else:
                    if distance<supr_threshold: distance=2*supr_threshold-distance
                    if csum==5 or csum==1:
                        w+=1.4
                    else:
                        w+=0.9
                nn+=1
                if (i+1+nn)>=len(ho):break
            
            v[i]=w*(100/distance)
        else: 
            v[i]=0

    return v

def obtainInverseCalculation(ho,bin_size):
    v=np.zeros(len(ho))       
    x=np.zeros(len(ho))
    j=0
    k=0

    for i in range(len(ho)):
        if ho[i].isln:
            print("ln")
            n=0
            while ho[i+n].column!=ho[i].column:
                n+=1
            v[i]=100/(ho[i+n].timestamp-ho[i].lnend)
    return v

raw_alpha=0
text=["delrio","snows","starfall","shinbatsu"]
dns_bin_size=1000
mnp_bin_size=1000
mtn_bin_size=1000
w=100
fig, (dens, manip, motion, inverse, total)=plt.subplots(5,1,sharex=True)

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
       
        dens.plot(x,dns,c=color,alpha=raw_alpha)
        dens.plot(x,dns_roll,label=m,c=color,linewidth=3)
        dens.text(0.8,i,s=f"{m[:12]+'...'}Avg. diff= {np.average(dns_roll):0.2f}",horizontalalignment='left',
                    verticalalignment='center',
                    transform = dens.transAxes)
        dens.title.set_text("DNS - Density Component")
        mnp=obtainManipCalculation(ho,mnp_bin_size)
        mnp_roll=np.array([np.average(mnp[max(0,i-w//2):min(len(ho),i+w//2)]) for i in range(len(ho))])
        manip.plot(x,mnp,c=color,alpha=raw_alpha)
        manip.text(0.8,i,s=f"{m[:12]+'...'}Avg. diff= {np.average(mnp_roll):0.2f}",horizontalalignment='left',
                    verticalalignment='center',
                    transform = manip.transAxes)
        manip.title.set_text("MSH - Mashability Component")
        manip.plot(x,mnp_roll,label=m,c=color,linewidth=3)
        manip.set_ylim(0.35,0.85)
        mtn=obtainMotionCalculation(ho,mtn_bin_size)
        mtn_roll=np.array([np.average(mtn[max(0,i-w//2):min(len(ho),i+w//2)]) for i in range(len(ho))])
        motion.plot(x,mtn,c=color,alpha=raw_alpha)
        motion.text(0.8,i,s=f"{m[:12]+'...'}Avg. diff= {np.average(mtn):0.2f}",horizontalalignment='left',
                    verticalalignment='center',
                    transform = motion.transAxes)
        motion.plot(x,mtn_roll,label=m,c=color,linewidth=3)
        motion.set_ylim(0,3.5)
        motion.title.set_text("STR - Strain Component")

        inv=obtainInverseCalculation(ho,mtn_bin_size)
        inv_roll=np.array([np.average(inv[max(0,i-w//2):min(len(ho),i+w//2)]) for i in range(len(ho))])
        inverse.plot(x,inv,c=color,alpha=raw_alpha)
        inverse.text(0.8,i,s=f"{m[:12]+'...'}Avg. diff= {np.average(inv):0.2f}",horizontalalignment='left',
                    verticalalignment='center',
                    transform = motion.transAxes)
        inverse.plot(x,inv_roll,label=m,c=color,linewidth=3)
        inverse.title.set_text("LN-INV - LN Inverse Component")

        ttl_raw=(dns/mnp)*mtn
        ttl=(dns_roll/mnp_roll)*(mtn_roll)
        ttl_roll=np.array([np.average(ttl[max(0,i-w//2):min(len(ho),i+w//2)]) for i in range(len(ho))])
        total.plot(x,ttl_raw,c=color,alpha=raw_alpha)
        total.text(0.8,i,s=f"{m[:12]+'...'}Avg. diff= {np.average(ttl):0.2f}",horizontalalignment='left',
                    verticalalignment='center',
                    transform = total.transAxes)
        total.plot(x,ttl_roll,label=m,c=color,linewidth=3)
        total.set_ylim(0,100)
        total.title.set_text("Total (DNS/MSH)*STR")



        i-=0.1

dens.legend()
plt.show()

