import numpy as np
import os
import matplotlib.pyplot as plt
from numpy.lib.function_base import average
import random

from utils.parser import *
from modules.Density import obtainDensityCalculation
from modules.Manip import obtainManipCalculation
from modules.LNness import obtainLNnessCalculation
from modules.Inverse import obtainInverseCalculation
from modules.Release import obtainReleaseCalculation
from modules.Strain import obtainStrainCalculation
from modules.Hold import obtainHoldCalculation

import csv 

plots=False

maps_folder = "./mapas/"

text = ["zero!!", "bleed the fifth", "fake promise", "dark samba master", "eiyuu", "obligatory",
        "wanderflux", "b l a c k - r a y", "dusanco", "fortunate", "algebra", "lubeder", "viscracked", "purple","blastix","psystyle"]
text = ["shinbatsu","snows","azure","fake promise","ayumu's","starfall","elekton","gendarme","siinamota","endorphin","bass"]
# text = ["kamah","azure","regret","aqua","tidek"]
# text = ["blue zenith","viscracked","lubeder","inai inai","juankristal","howtoplayln"]
text=["zalex","inai inai","move that body (juankristal)","first (juankristal)","pi (jinjin) [4k hard]"]
text=[]
dns_bin_size = 1000
w = 100

fig, ((dens, inverse), (manip, release), (strain, lnness), (rice_total,
      hold), (total,  ln_total)) = plt.subplots(nrows=5, ncols=2, sharex=True)

i = .9

header=["Beatmap ID","Name","Density","Manipulability","Strain","RICE TOTAL","Inverse","Release","Hold","LNNess","LN TOTAL","GLOBAL","DT GLOBAL"]
wcsv=True
if wcsv: 
    csv_file=open("calc.csv","w",encoding='UTF8',newline='')
    writer=csv.writer(csv_file)
    writer.writerow(header)
counter=0

for m in os.listdir(maps_folder):

    with open(maps_folder+m, "r", encoding="utf8",errors='ignore') as f: 
        
        print(m)
        beatmap = obtainHitObjectArrayFromOsu(f)

        if text!=[] and not any([t.lower() in beatmap.name.lower() for t in text]):
            continue
        if beatmap.keys!=4: continue

        print(counter, " | ", beatmap.name)
        counter+=1
        x = np.array([h.timestamp for h in beatmap.hitobjects])

        r = random.random()
        b = random.random()
        g = random.random()
        color = (r, g, b)

        dns = obtainDensityCalculation(beatmap.hitobjects, dns_bin_size)
        mnp = obtainManipCalculation(beatmap.hitobjects, dns_bin_size)
        str = obtainStrainCalculation(beatmap.hitobjects)
        inv = obtainInverseCalculation(beatmap.hitobjects)
        rel = obtainReleaseCalculation(beatmap.hitobjects)
        lns = obtainLNnessCalculation(beatmap.hitobjects)
        hld = obtainHoldCalculation(beatmap.hitobjects)

        dt_dns = obtainDensityCalculation(beatmap.dt_hitobjects, dns_bin_size)
        dt_mnp = obtainManipCalculation(beatmap.dt_hitobjects, dns_bin_size)
        dt_str = obtainStrainCalculation(beatmap.dt_hitobjects)
        dt_inv = obtainInverseCalculation(beatmap.dt_hitobjects)
        dt_rel = obtainReleaseCalculation(beatmap.dt_hitobjects)
        dt_lns = obtainLNnessCalculation(beatmap.dt_hitobjects)
        dt_hld = obtainHoldCalculation(beatmap.dt_hitobjects)

        dns_roll = np.array(
            [np.average(dns[max(0, i-w//2):min(len(beatmap.hitobjects), i+w//2)]) for i in range(len(beatmap.hitobjects))])
        mnp_roll = np.array(
            [np.average(mnp[max(0, i-w//2):min(len(beatmap.hitobjects), i+w//2)]) for i in range(len(beatmap.hitobjects))])
        inv_roll = np.array(
            [np.average(inv[max(0, i-w//2):min(len(beatmap.hitobjects), i+w//2)]) for i in range(len(beatmap.hitobjects))])
        rel_roll = np.array(
            [np.average(rel[max(0, i-w//2):min(len(beatmap.hitobjects), i+w//2)]) for i in range(len(beatmap.hitobjects))])
        lns_roll = np.array(
            [np.average(lns[max(0, i-w//2):min(len(beatmap.hitobjects), i+w//2)]) for i in range(len(beatmap.hitobjects))])
        str_roll = np.array(
            [np.average(str[max(0, i-w//2):min(len(beatmap.hitobjects), i+w//2)]) for i in range(len(beatmap.hitobjects))])
        hld_roll = np.array(
            [np.average(hld[max(0, i-w//2):min(len(beatmap.hitobjects), i+w//2)]) for i in range(len(beatmap.hitobjects))])


        dt_dns_roll = np.array(
            [np.average(dt_dns[max(0, i-w//2):min(len(beatmap.hitobjects), i+w//2)]) for i in range(len(beatmap.hitobjects))])
        dt_mnp_roll = np.array(
            [np.average(dt_mnp[max(0, i-w//2):min(len(beatmap.hitobjects), i+w//2)]) for i in range(len(beatmap.hitobjects))])
        dt_inv_roll = np.array(
            [np.average(dt_inv[max(0, i-w//2):min(len(beatmap.hitobjects), i+w//2)]) for i in range(len(beatmap.hitobjects))])
        dt_rel_roll = np.array(
            [np.average(dt_rel[max(0, i-w//2):min(len(beatmap.hitobjects), i+w//2)]) for i in range(len(beatmap.hitobjects))])
        dt_lns_roll = np.array(
            [np.average(dt_lns[max(0, i-w//2):min(len(beatmap.hitobjects), i+w//2)]) for i in range(len(beatmap.hitobjects))])
        dt_str_roll = np.array(
            [np.average(dt_str[max(0, i-w//2):min(len(beatmap.hitobjects), i+w//2)]) for i in range(len(beatmap.hitobjects))])
        dt_hld_roll = np.array(
            [np.average(dt_hld[max(0, i-w//2):min(len(beatmap.hitobjects), i+w//2)]) for i in range(len(beatmap.hitobjects))])

        dt_lnttl_raw = np.power((1+dt_inv+dt_rel), dt_lns)*np.power(dt_hld, 2)
        dt_lnttl = np.power((1+dt_inv_roll+dt_rel_roll), dt_lns_roll)*np.power(dt_hld_roll, 2)
        dt_lnttl_roll = np.array(
            [np.average(dt_lnttl[max(0, i-w//2):min(len(beatmap.hitobjects), i+w//2)]) for i in range(len(beatmap.hitobjects))])

        lnttl_raw = np.power((1+inv+rel), lns)*np.power(hld, 2)
        lnttl = np.power((1+inv_roll+rel_roll), lns_roll)*np.power(hld_roll, 2)
        lnttl_roll = np.array(
            [np.average(lnttl[max(0, i-w//2):min(len(beatmap.hitobjects), i+w//2)]) for i in range(len(beatmap.hitobjects))])

        dt_ricettl_raw = (dt_dns/dt_mnp)*dt_str
        dt_ricettl = (dt_dns_roll/dt_mnp_roll)*(dt_str_roll)
        dt_ricettl_roll = np.array(
            [np.average(dt_ricettl[max(0, i-w//2):min(len(beatmap.hitobjects), i+w//2)]) for i in range(len(beatmap.hitobjects))])

        ricettl_raw = (dns/mnp)*str
        ricettl = (dns_roll/mnp_roll)*(str_roll)
        ricettl_roll = np.array(
            [np.average(ricettl[max(0, i-w//2):min(len(beatmap.hitobjects), i+w//2)]) for i in range(len(beatmap.hitobjects))])

        dt_ttl_raw = (dt_dns/dt_mnp)*dt_str*np.power((1+dt_inv+dt_rel), dt_lns)*np.power(dt_hld, 2)
        dt_ttl = (dt_dns_roll/(dt_mnp_roll)*(dt_str_roll)) * \
            np.power((1+dt_inv_roll+dt_rel_roll), dt_lns_roll)*np.power(dt_hld_roll, 2)
        dt_ttl_roll = np.array(
            [np.average(dt_ttl[max(0, i-w//2):min(len(beatmap.hitobjects), i+w//2)]) for i in range(len(beatmap.hitobjects))])

        ttl_raw = (dns/mnp)*str*np.power((1+inv+rel), lns)*np.power(hld, 2)
        ttl = (dns_roll/(mnp_roll)*(str_roll)) * \
            np.power((1+inv_roll+rel_roll), lns_roll)*np.power(hld_roll, 2)
        ttl_roll = np.array(
            [np.average(ttl[max(0, i-w//2):min(len(beatmap.hitobjects), i+w//2)]) for i in range(len(beatmap.hitobjects))])

        
        if plots:
            generate_subplot(dens, x, dns, dns_roll, color,
                            beatmap.name, i, "DNS - Density Component")
            generate_subplot(manip, x, mnp, mnp_roll, color, beatmap.name,
                            i, "MNP - Manipulability Component")
            generate_subplot(strain, x, str, str_roll, color,
                            beatmap.name, i, "STR - Strain Component")
            generate_subplot(inverse, x, inv, inv_roll, color, beatmap.name,
                            i, "LN-INV - LN Inverse Component")
            generate_subplot(release, x, rel, rel_roll, color, beatmap.name,
                            i, "LN-REL - LN Release Component")
            generate_subplot(lnness, x, lns, lns_roll, color, beatmap.name,
                            i, "LN-LNS - LN LNness Component")
            generate_subplot(hold, x, hld, hld_roll, color, beatmap.name,
                            i, "LN-HLD - LN Hold Strain Difficulty")
            generate_subplot(ln_total, x, lnttl_raw, lnttl_roll,
                            color, beatmap.name, i, "LN Total - (INV+REL)^LNS * HLD")
            generate_subplot(rice_total, x, ricettl_raw, ricettl_roll,
                            color, beatmap.name, i, "RICE Total - (DNS*STR)/MNP")
            generate_subplot(total, x, ttl_raw, ttl_roll, color, beatmap.name,
                            i, "Total - ((DNS*STR)/MNP * (INV+REL)^LNS) * HLD")

            i -= 0.07

        if wcsv: writer.writerow([beatmap.beatmapid,beatmap.name,np.average(dns_roll),np.average(mnp_roll),np.average(str_roll),np.average(ricettl_roll),np.average(inv_roll),np.average(rel_roll),np.average(hld_roll),np.average(lns_roll),np.average(lnttl_roll),np.average(ttl_roll),np.average(dt_ttl_roll)])


if plots:
    inverse.legend()
    plt.subplots_adjust(
        wspace=.5)
    plt.show()


