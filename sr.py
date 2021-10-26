import numpy as np
import os
import matplotlib.pyplot as plt
from numpy.lib.function_base import average
import random
import csv

from utils.parser import *
from modules.Density import obtainDensityCalculation
from modules.Manip import obtainManipCalculation
from modules.LNness import obtainLNnessCalculation
from modules.Inverse import obtainInverseCalculation
from modules.Release import obtainReleaseCalculation
from modules.Strain import obtainStrainCalculation
from modules.Hold import obtainHoldCalculation



plots=False
wcsv=True

maps_folder = "./mapas/"

#Can write whatever specific search here. Use [] to parse all maps
text = ["zero!!", "bleed the fifth", "fake promise", "dark samba master", "eiyuu", "obligatory",
        "wanderflux", "b l a c k - r a y", "dusanco", "fortunate", "algebra", "lubeder", "vis::cracked", "purple palace","blastix riotz (Fresh Chicken) [GRAVITY]"
        ,"aural annihilation"]

fig, ((dens, inverse), (manip, release), (strain, lnness), (rice_total,
      hold), (total,  ln_total)) = plt.subplots(nrows=5, ncols=2, sharex=True)

wcsv=True
if wcsv: 
    header=["Beatmap ID","Name","Density","Manipulability","Strain","RICE TOTAL","Inverse","Release","Hold","LNNess","LN TOTAL","GLOBAL","DT GLOBAL"]
    csv_file=open("calc.csv","w",encoding='UTF8',newline='')
    writer=csv.writer(csv_file)
    writer.writerow(header)

counter=0
i = .9

for m in os.listdir(maps_folder):

    with open(maps_folder+m, "r", encoding="utf8",errors='ignore') as f: 
        
        #Parse .osu file
        beatmap = obtainHitObjectArrayFromOsu(f)

        #Filter only 4k (and the searched files if applicable)
        if text!=[] and not any([t.lower() in beatmap.name.lower() for t in text]): continue
        if beatmap.keys!=4: continue

        print(counter, " | ", beatmap.name)
        
        #Obtain module calculations (Nomod)
        dns = obtainDensityCalculation(beatmap.hitobjects)
        mnp = obtainManipCalculation(beatmap.hitobjects)
        str = obtainStrainCalculation(beatmap.hitobjects)
        inv = obtainInverseCalculation(beatmap.hitobjects)
        rel = obtainReleaseCalculation(beatmap.hitobjects)
        lns = obtainLNnessCalculation(beatmap.hitobjects)
        hld = obtainHoldCalculation(beatmap.hitobjects)

        #Obtain module calculations (DT)
        dt_dns = obtainDensityCalculation(beatmap.dt_hitobjects)
        dt_mnp = obtainManipCalculation(beatmap.dt_hitobjects)
        dt_str = obtainStrainCalculation(beatmap.dt_hitobjects)
        dt_inv = obtainInverseCalculation(beatmap.dt_hitobjects)
        dt_rel = obtainReleaseCalculation(beatmap.dt_hitobjects)
        dt_lns = obtainLNnessCalculation(beatmap.dt_hitobjects)
        dt_hld = obtainHoldCalculation(beatmap.dt_hitobjects)


        #Obtain moving averages
        [dns_roll,mnp_roll,str_roll,inv_roll,rel_roll,lns_roll,hld_roll] = [roll(a) for a in [dns,mnp,str,inv,rel,lns,hld]]
        [dt_dns_roll,dt_mnp_roll,dt_str_roll,dt_inv_roll,dt_rel_roll,dt_lns_roll,dt_hld_roll] = [roll(a) for a in [dt_dns,dt_mnp,dt_str,dt_inv,dt_rel,dt_lns,dt_hld]]

        #Obtain LN difficulty multiplier calculations
        dt_lnttl_raw = np.power((1+dt_inv+dt_rel), dt_lns)*np.power(dt_hld, 2)
        dt_lnttl = np.power((1+dt_inv_roll+dt_rel_roll), dt_lns_roll)*np.power(dt_hld_roll, 2)
        dt_lnttl_roll = roll(dt_lnttl)

        lnttl_raw = np.power((1+inv+rel), lns)*np.power(hld, 2)
        lnttl = np.power((1+inv_roll+rel_roll), lns_roll)*np.power(hld_roll, 2)
        lnttl_roll = roll(lnttl)

        #Obtain RICE difficulty multiplier calculations
        dt_ricettl_raw = (dt_dns/dt_mnp)*dt_str
        dt_ricettl = (dt_dns_roll/dt_mnp_roll)*(dt_str_roll)
        dt_ricettl_roll = roll(dt_ricettl)

        ricettl_raw = (dns/mnp)*str
        ricettl = (dns_roll/mnp_roll)*(str_roll)
        ricettl_roll = roll(ricettl)


        #Obtain GLOBAL difficulty calculations
        dt_ttl_raw = total_diff(dt_dns,dt_mnp,dt_str,dt_inv,dt_rel,dt_lns,dt_hld)
        dt_ttl = total_diff(dt_dns_roll,dt_mnp_roll,dt_str_roll,dt_inv_roll,dt_rel_roll,dt_lns_roll,dt_hld_roll)
        dt_ttl_roll = roll(dt_ttl)

        ttl_raw = total_diff(dns,mnp,str,inv,rel,lns,hld)
        ttl = total_diff(dns_roll,mnp_roll,str_roll,inv_roll,rel_roll,lns_roll,hld_roll)
        ttl_roll = roll(ttl)

        #Plots
        if plots:
            color = (random.random(),random.random(),random.random())
            x = np.array([h.timestamp for h in beatmap.hitobjects])

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

        #Write to CSV
        if wcsv: 
            writer.writerow(
            [beatmap.beatmapid,
            beatmap.name,
            np.average(dns_roll),
            np.average(mnp_roll),
            np.average(str_roll),
            np.average(ricettl_roll),
            np.average(inv_roll),
            np.average(rel_roll),
            np.average(hld_roll),
            np.average(lns_roll),
            np.average(lnttl_roll),
            np.average(ttl_roll),
            np.average(dt_ttl_roll)
            ]
            )

            counter+=1

if plots:
    inverse.legend()
    plt.subplots_adjust(wspace=.5)
    plt.show()


