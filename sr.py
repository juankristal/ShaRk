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
from modules.Hold import obtainHoldCalculation

maps_folder = "./mapas/"

text = ["zero!!", "bleed the fifth", "fake promise", "dark samba master", "eiyuu", "obligatory",
        "wanderflux", "b l a c k - r a y", "dusanco", "fortunate", "algebra", "lubeder", "viscracked", "purple","blastix","psystyle"]
# text = ["shinbatsu","snows","azure","fake promise","ayumu's","starfall","elekton","gendarme","blastix","psystyle","nhelv"]

dns_bin_size = 1000
w = 100

fig, ((dens, inverse), (manip, release), (strain, lnness), (rice_total,
      hold), (total,  ln_total)) = plt.subplots(nrows=5, ncols=2, sharex=True)

i = .9
for m in os.listdir(maps_folder):
    if text != [] and not any([t.lower() in m.lower() for t in text]):
        continue
    print(m)
    with open(maps_folder+m, "r", encoding="utf8") as f:
        ho = obtainHitObjectArrayFromOsu(f)
        x = np.array([h.timestamp for h in ho])

        r = random.random()
        b = random.random()
        g = random.random()
        color = (r, g, b)

        dns = obtainDensityCalculation(ho, dns_bin_size)
        mnp = obtainManipCalculation(ho, dns_bin_size)
        str = obtainStrainCalculation(ho)
        inv = obtainInverseCalculation(ho)
        rel = obtainReleaseCalculation(ho)
        lns = obtainLNnessCalculation(ho)
        hld = obtainHoldCalculation(ho)

        dns_roll = np.array(
            [np.average(dns[max(0, i-w//2):min(len(ho), i+w//2)]) for i in range(len(ho))])
        mnp_roll = np.array(
            [np.average(mnp[max(0, i-w//2):min(len(ho), i+w//2)]) for i in range(len(ho))])
        inv_roll = np.array(
            [np.average(inv[max(0, i-w//2):min(len(ho), i+w//2)]) for i in range(len(ho))])
        rel_roll = np.array(
            [np.average(rel[max(0, i-w//2):min(len(ho), i+w//2)]) for i in range(len(ho))])
        lns_roll = np.array(
            [np.average(lns[max(0, i-w//2):min(len(ho), i+w//2)]) for i in range(len(ho))])
        str_roll = np.array(
            [np.average(str[max(0, i-w//2):min(len(ho), i+w//2)]) for i in range(len(ho))])
        hld_roll = np.array(
            [np.average(hld[max(0, i-w//2):min(len(ho), i+w//2)]) for i in range(len(ho))])

        lnttl_raw = np.power((1+inv+rel), lns)*np.power(hld, 2)
        lnttl = np.power((1+inv_roll+rel_roll), lns_roll)*np.power(hld_roll, 2)
        lnttl_roll = np.array(
            [np.average(lnttl[max(0, i-w//2):min(len(ho), i+w//2)]) for i in range(len(ho))])

        ricettl_raw = (dns/mnp)*str
        ricettl = (dns_roll/mnp_roll)*(str_roll)
        ricettl_roll = np.array(
            [np.average(ricettl[max(0, i-w//2):min(len(ho), i+w//2)]) for i in range(len(ho))])

        ttl_raw = (dns/mnp)*str*np.power((1+inv+rel), lns)*np.power(hld, 2)
        ttl = (dns_roll/(mnp_roll)*(str_roll)) * \
            np.power((1+inv_roll+rel_roll), lns_roll)*np.power(hld_roll, 2)
        ttl_roll = np.array(
            [np.average(ttl[max(0, i-w//2):min(len(ho), i+w//2)]) for i in range(len(ho))])

        generate_subplot(dens, x, dns, dns_roll, color,
                         m, i, "DNS - Density Component")
        generate_subplot(manip, x, mnp, mnp_roll, color, m,
                         i, "MNP - Manipulability Component")
        generate_subplot(strain, x, str, str_roll, color,
                         m, i, "STR - Strain Component")
        generate_subplot(inverse, x, inv, inv_roll, color, m,
                         i, "LN-INV - LN Inverse Component")
        generate_subplot(release, x, rel, rel_roll, color, m,
                         i, "LN-REL - LN Release Component")
        generate_subplot(lnness, x, lns, lns_roll, color, m,
                         i, "LN-LNS - LN LNness Component")
        generate_subplot(hold, x, hld, hld_roll, color, m,
                         i, "LN-HLD - LN Hold Strain Difficulty")
        generate_subplot(ln_total, x, lnttl_raw, lnttl_roll,
                         color, m, i, "LN Total - (INV+REL)^LNS * HLD")
        generate_subplot(rice_total, x, ricettl_raw, ricettl_roll,
                         color, m, i, "RICE Total - (DNS*STR)/MNP")
        generate_subplot(total, x, ttl_raw, ttl_roll, color, m,
                         i, "Total - ((DNS*STR)/MNP * (INV+REL)^LNS) * HLD")

        i -= 0.07

dens.legend()
plt.subplots_adjust(
    wspace=.5)
plt.show()
