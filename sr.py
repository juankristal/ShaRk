import numpy as np
import os
import matplotlib.pyplot as plt
import math
from numpy.lib.function_base import average
from scipy.interpolate import make_interp_spline, BSpline
import random

from utils.parser import *
from modules.Density import obtainDensityCalculation
from modules.Manip import obtainManipCalculation
from modules.LNness import obtainLNnessCalculation
from modules.Inverse import obtainInverseCalculation
from modules.Release import obtainReleaseCalculation
from modules.Strain import obtainStrainCalculation

maps_folder="./mapas/"

raw_alpha=0.05
text=["nanahoshi","inai inai","fortunate","nostalgia","levitation","penguin"]
dns_bin_size=1000
mnp_bin_size=1000
mtn_bin_size=1000
w=100

fig, ((dens,inverse), (manip,release), (motion,lnness), (rice_total,ln_total), (total,filler))=plt.subplots(nrows=5,ncols=2,sharex=True)

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

        dns=obtainDensityCalculation(ho,dns_bin_size)
        mnp=obtainManipCalculation(ho,dns_bin_size)
        str=obtainStrainCalculation(ho,dns_bin_size)
        inv=obtainInverseCalculation(ho,dns_bin_size)
        rel=obtainReleaseCalculation(ho,dns_bin_size)
        lns=obtainLNnessCalculation(ho,dns_bin_size)
        
        dns_roll=np.array([np.average(dns[max(0,i-w//2):min(len(ho),i+w//2)]) for i in range(len(ho))])
        mnp_roll=np.array([np.average(mnp[max(0,i-w//2):min(len(ho),i+w//2)]) for i in range(len(ho))])
        inv_roll=np.array([np.average(inv[max(0,i-w//2):min(len(ho),i+w//2)]) for i in range(len(ho))])
        rel_roll=np.array([np.average(rel[max(0,i-w//2):min(len(ho),i+w//2)]) for i in range(len(ho))])
        lns_roll=np.array([np.average(lns[max(0,i-w//2):min(len(ho),i+w//2)]) for i in range(len(ho))])
        str_roll=np.array([np.average(str[max(0,i-w//2):min(len(ho),i+w//2)]) for i in range(len(ho))])

        generate_subplot(x,dns,dns_roll,color,m,i,"DNS - Density Component")
        generate_subplot(x,mnp,mnp_roll,color,m,i,"MNP - Manipulability Component")
        generate_subplot(x,dns,dns_roll,color,m,i,"STR - Strain Component")
        generate_subplot(x,dns,dns_roll,color,m,i,"LN-INV - LN Inverse Component")
        generate_subplot(x,dns,dns_roll,color,m,i,"LN-REL - LN Release Component")
        generate_subplot(x,dns,dns_roll,color,m,i,"LN-LNS - LN LNness Component")
        

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
                    transform = inverse.transAxes)
        inverse.plot(x,inv_roll,label=m,c=color,linewidth=3)
        inverse.title.set_text("LN-INV - LN Inverse Component")

        rel=obtainReleaseCalculation(ho,mtn_bin_size)
        rel_roll=np.array([np.average(rel[max(0,i-w//2):min(len(ho),i+w//2)]) for i in range(len(ho))])
        release.plot(x,rel,c=color,alpha=raw_alpha)
        release.text(0.8,i,s=f"{m[:12]+'...'}Avg. diff= {np.average(rel):0.2f}",horizontalalignment='left',
                    verticalalignment='center',
                    transform = release.transAxes)
        release.plot(x,rel_roll,label=m,c=color,linewidth=3)
        release.title.set_text("LN-REL - LN Release Component")

        lns=obtainLNnessCalculation(ho,mtn_bin_size)
        lns_roll=np.array([np.average(lns[max(0,i-w//2):min(len(ho),i+w//2)]) for i in range(len(ho))])
        lnness.plot(x,lns,c=color,alpha=raw_alpha)
        lnness.text(0.8,i,s=f"{m[:12]+'...'}Avg. diff= {np.average(lns):0.2f}",horizontalalignment='left',
                    verticalalignment='center',
                    transform = lnness.transAxes)
        lnness.plot(x,lns_roll,label=m,c=color,linewidth=3)
        lnness.title.set_text("LN-LNS - LN \"LNness\" Component")

        lnness.set_ylim(.25,1)

        lnttl_raw=np.power((inv*rel),lns)
        lnttl=np.power((inv_roll*rel_roll),lns_roll)
        lnttl_roll=np.array([np.average(lnttl[max(0,i-w//2):min(len(ho),i+w//2)]) for i in range(len(ho))])
        ln_total.plot(x,lnttl_raw,c=color,alpha=raw_alpha)
        ln_total.text(0.8,i,s=f"{m[:12]+'...'}Avg. diff= {np.average(lnttl):0.2f}",horizontalalignment='left',
                    verticalalignment='center',
                    transform = ln_total.transAxes)
        ln_total.plot(x,lnttl_roll,label=m,c=color,linewidth=3)
        ln_total.set_ylim(0,8)
        ln_total.title.set_text("LN Total (INV*REL)^LNS")

        ricettl_raw=(dns/mnp)*mtn
        ricettl=(dns_roll/mnp_roll)*(mtn_roll)
        ricettl_roll=np.array([np.average(ricettl[max(0,i-w//2):min(len(ho),i+w//2)]) for i in range(len(ho))])
        rice_total.plot(x,ricettl_raw,c=color,alpha=raw_alpha)
        rice_total.text(0.8,i,s=f"{m[:12]+'...'}Avg. diff= {np.average(ricettl):0.2f}",horizontalalignment='left',
                    verticalalignment='center',
                    transform = rice_total.transAxes)
        rice_total.plot(x,ricettl_roll,label=m,c=color,linewidth=3)
        rice_total.set_ylim(0,100)
        rice_total.title.set_text("RICE Total (DNS/MSH)*STR")

        ttl_raw=(dns/mnp)*mtn*np.power((inv*rel),lns)
        ttl=(dns_roll/mnp_roll)*(mtn_roll)*np.power((inv_roll*rel_roll),lns_roll)
        ttl_roll=np.array([np.average(ttl[max(0,i-w//2):min(len(ho),i+w//2)]) for i in range(len(ho))])
        total.plot(x,ttl_raw,c=color,alpha=raw_alpha)
        total.text(0.8,i,s=f"{m[:12]+'...'}Avg. diff= {np.average(ttl):0.2f}",horizontalalignment='left',
                    verticalalignment='center',
                    transform = total.transAxes)
        total.plot(x,ttl_roll,label=m,c=color,linewidth=3)
        total.set_ylim(0,300)
        total.title.set_text("Total (DNS/MSH)*STR*(INV*REL)^LNS")



        i-=0.1

dens.legend()
plt.show()

