import numpy as np


# TO-DO: make the scaling non-linear in relation to the gap

def obtainInverseCalculation(ho):
    v = np.zeros(len(ho))

    for i in range(len(ho)):
        if ho[i].isln and ho[i].timestamp != ho[-1].timestamp:

            # Find the next note in the same column
            n = 1
            while ho[i+n].column != ho[i].column:
                n += 1
                if i+n >= len(ho):
                    break
            if i+n >= len(ho):
                break

            # Difficulty of the inversed press is inversely proportional to the size of the gap
            v[i] += 100/(ho[i+n].timestamp-ho[i].lnend)
    return v
