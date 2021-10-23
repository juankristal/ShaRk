import math
import numpy as np

# Sigmoidal centered at 90ms


def s(x):
    return 1 / (1 + math.exp(9-0.1*x))

###############################################################################
#   Defines how much of an LN a long note really is based on its length
#   anything lower than 120ms becomes way easier to press because of the average
#   press time and how OD works
##########################################


def obtainLNnessCalculation(ho):
    lnness = np.zeros(len(ho))

    for i in range(len(ho)):
        if ho[i].isln:
            lnness[i] = s(ho[i].lnend-ho[i].timestamp)

    return lnness
