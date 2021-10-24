import numpy as np
import math

f = lambda x: 10/(math.e**(0.05*x))

# TO-DO: make the scaling non-linear in relation to the gap

def obtainInverseCalculation(ho):
    v = np.zeros(len(ho))

    for i in range(len(ho)):
        
        if ho[i].isln and ho[i].timestamp != ho[-1].timestamp:
            # Find the next note in the same column
            n = i
            while ho[n].column != ho[i].column or i==n:
                n += 1
                if n >= len(ho):
                    break
            if n >= len(ho):
                break

            # print(ho[i].lnend-ho[i].lnend)
            # Difficulty of the inversed press is inversely proportional to the size of the gap
            v[i] += f(ho[n].timestamp-ho[i].lnend)
    return v
