import numpy as np
import matplotlib.pyplot as plt
from numpy.core.records import recarray


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


def obtainHitObjectArrayFromOsu(file):
    hitobjects = []
    dt_hitobjects = []
    l = file.readline()

    while "Title:" not in l[:10]:
        l = file.readline()
    title = l[l.find(":")+1:-1]

    while "Artist:" not in l[:10]:
        l = file.readline()
    artist = l[l.find(":")+1:-1]

    while "Creator:" not in l[:10]:
        l = file.readline()
    creator = l[l.find(":")+1:-1]

    while "Version:" not in l[:10]:
        l = file.readline()
    version = l[l.find(":")+1:-1]

    while "BeatmapID:" not in l[:10]:
        l = file.readline()
    beatmapid = l[l.find(":")+1:-1]

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

def total_diff(dns, mnp, str, inv, rel, lns, hld):
    return (
        (dns/mnp)*str*np.power((1+inv+rel), lns)*hld
    )
