from time import time
import numpy as np
import math
import matplotlib.pyplot as plt
from numpy.core.records import recarray
import re

from utils.parser import *
from modules.density import Density
from modules.manipulation import obtainManipCalculation
from modules.LNness import obtainLNnessCalculation
from modules.inverse import obtainInverseCalculation
from modules.release import obtainReleaseCalculation
from modules.strain import obtainStrainCalculation
from modules.hold import Hold

BIN_SIZE = 1000


def sigmoid(x):
    return 1 / (1 + math.exp(9-0.1*x))


def gaussian(x):
    return math.exp(-(x ** 2) / 2)


class HitObject:
    def __init__(self, column, timestamp, lnend=0) -> None:
        self.column = column
        self.timestamp = timestamp
        self.isln = lnend > timestamp
        self.lnend = lnend


class Beatmap:
    def __init__(self, title, artist, creator, version, hitobjects, beatmapid, keys, dt_hitobjects):
        self.name = f"{artist} - {title} ({creator}) [{version}]"
        self.hitobjects = hitobjects
        self.dt_hitobjects = dt_hitobjects
        self.beatmapid = beatmapid
        self.keys = keys

class BeatmapCalculations:
    def __init__(self, beatmap):
        hit_objects = beatmap.hitobjects
        hit_objects_dt = beatmap.dt_hitobjects
        self.nomod = ModuleCalculations(hit_objects)
        self.dt = ModuleCalculations(hit_objects_dt)


class ModuleCalculations:
    def __init__(self,hit_objects):

        t=time()
        #Basic Module calculations
        self.dns = Density(gaussian, BIN_SIZE).calculate_difficulty(hit_objects)
        # print(f"Density: {time()-t}")
        t0=time()
        self.stn = obtainStrainCalculation(hit_objects)
        # print(f"Strain: {time()-t0}")
        t0=time()
       
        self.inv = obtainInverseCalculation(hit_objects)
        # print(f"Inverse: {time()-t0}")
        t0=time()
        self.rel = obtainReleaseCalculation(hit_objects)
        # print(f"Release: {time()-t0}")
        t0=time()
        self.lns = obtainLNnessCalculation(hit_objects)
        # print(f"LNNess: {time()-t0}")
        t0=time()
        self.hld = Hold(sigmoid).calculate(hit_objects)
        # print(f"Hold: {time()-t0}")
        t0=time()
        self.mnp = obtainManipCalculation(hit_objects)
        # print(f"Manip: {time()-t0}")
        t0=time()
        # print(f"Basic Modules: {time()-t}")
        t=time()

        #Rolling averages
        self.dns_roll=roll(self.dns)
        self.mnp_roll=roll(self.mnp)
        self.stn_roll=roll(self.stn)
        self.inv_roll=roll(self.inv)
        self.rel_roll=roll(self.rel)
        self.lns_roll=roll(self.lns)
        self.hld_roll=roll(self.hld)
        # print(f"Rolling avgs: {time()-t}")
        t=time()
        #Rice Total
        self.rice_ttl=self.computeRiceTotal(self.dns,self.mnp,self.stn)
        self.rice_ttl_roll=self.computeRiceTotal(self.dns_roll,self.mnp_roll,self.stn_roll)

        #Ln Total
        self.ln_ttl=self.computeLNTotal(self.inv,self.rel,self.lns,self.hld)
        self.ln_ttl_roll=self.computeLNTotal(self.inv_roll,self.rel_roll,self.lns_roll,self.hld_roll)

        #Global
        self.ttl=self.computeGlobal(self.rice_ttl,self.ln_ttl)
        self.ttl_roll=self.computeGlobal(self.rice_ttl_roll,self.ln_ttl_roll)
        # print(f"Globals: {time()-t}")
        t=time()

    def computeRiceTotal(self,dns,mnp,stn):
        return (dns/mnp)*stn
    
    def computeLNTotal(self,inv,rel,lns,hld):
        return np.power(1+inv+2*rel,lns)*np.power(hld,1)

    def computeGlobal(self,rice,ln):
        return rice * np.power(ln,1)

def obtainHitObjectArrayFromOsu(file):
    file.seek(0)
    hitobjects = []
    dt_hitobjects = []
    l = file.readline()

    while "Title:" not in l[:10]:
        l = file.readline()
    title = l[l.find(":")+1:].strip()

    while "Artist:" not in l[:10]:
        l = file.readline()
    artist = l[l.find(":")+1:-1].strip()

    while "Creator:" not in l[:10]:
        l = file.readline()
    creator = l[l.find(":")+1:-1].strip()

    while "Version:" not in l[:10]:
        l = file.readline()
    version = l[l.find(":")+1:-1].strip()

    while "BeatmapID:" not in l[:10]:
        l = file.readline()
    beatmapid = l[l.find(":")+1:-1].strip()

    while "CircleSize:" not in l[:15]:
        l = file.readline()
    keys = int(l[l.find(":")+1:-1])

    while "[HitObjects]" not in l:
        l = file.readline()

    while True:
        l = file.readline()
        if not l:
            break
        if l == "\n":
            continue
        lineinfo = l.split(',')
        column = max(min(round((int(lineinfo[0])-64)/128), 3), 0)
        timestamp = int(lineinfo[2])
        try:
            lnend = int(lineinfo[5].split(":")[0])
        except ValueError:
            lnend = 0
        hitobjects.append(HitObject(column, timestamp, lnend))
        dt_hitobjects.append(HitObject(column, timestamp//1.5, lnend//1.5))
    b = Beatmap(title, artist, creator, version,
                    hitobjects, beatmapid, keys, dt_hitobjects)
    return b


def generate_subplot(subplot, x, raw, roll, color, map, i, title):

    subplot.set_ylim(min(subplot.get_ylim()[0], np.min(
        roll)), max(subplot.get_ylim()[1], np.max(roll)))
    # subplot.plot(x, raw, c=color, alpha=0.05)
    subplot.plot(x, roll, label=map, c=color, linewidth=1)
    subplot.text(1, i, s=f"{map[:12]+'...'}: {np.average(roll):0.2f}", horizontalalignment='left',
                 verticalalignment='center',
                 transform=subplot.transAxes, size=8)
    subplot.title.set_text(title)
    subplot.autoscale()


def checkMode(file):
    l = file.readline()
    while "Mode" not in l[:4] and l:
        l = file.readline()
    if l:
        m = int(l.split(" ")[1])
    else:
        m = 0
    return m


w = 50


def roll(a):
    # return np.array([np.average(a[max(0, i-w//2):min(len(a), i+w//2)]) for i in range(len(a))])
    a_padded = np.pad(a, (w//2, w-1-w//2), mode='edge')
    return np.convolve(a_padded, np.ones((w,))/w, mode='valid') 

    