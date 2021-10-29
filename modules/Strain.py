import numpy as np
import math

jack_w = 2.5
onehand_w = 1.4
twohand_w = 0.7

def s(x):
    return 1 / (1 + math.exp(6-0.1*x))

###############################################################################
# Obtains the strain of hitting each consecutive note pair based on the type of
# motion it requires (same hand but different column, different hand, jack)
###############################################################################


# TO-DO: Consider separately all 4 columns for each note? Currently it's buggy cause if one note isn't a jack then it gets supressed a lot by the distance thing

def obtainStrainCalculation(ho):
    strain = np.zeros(len(ho))

    supr_threshold = 60
    for i in range(len(ho)):

        w = 0  # Total strain difficulty of the note

        # Last note doesn't get assigned any value
        if ho[i].timestamp != ho[len(ho)-1].timestamp:
            n = 0
            # Find the next note after the current one

            cols=[0,1,2,3]

            for c in cols:
                n=i
                while ho[n].timestamp==ho[i].timestamp or c!=ho[n].column:
                    n += 1
                    if n>=len(ho):break
                if n>=len(ho): continue

                distance = ho[n].timestamp-ho[i].timestamp

                csum = ho[n].column + ho[i].column

                # Jacks don't get supressed for graces obviously
                if c == ho[i].column:
                    w += jack_w*(100/distance)

                # Otherwise, supress based on how gracey it is
                else:
                    nn=n
                    while ho[n].timestamp==ho[nn].timestamp or c!=ho[nn].column:
                        nn -= 1
                        if nn<0: break
                    if nn<0: 

                            # Same hand, different colum
                        if csum == 5 or csum == 1:
                                w += onehand_w*(100/distance)*s(ho[n].timestamp-ho[i].timestamp)

                            # Different hand
                        else:
                                w += twohand_w*(100/distance)*s(ho[n].timestamp-ho[i].timestamp)
                    else: 
                        if csum == 5 or csum == 1:
                                w += onehand_w*(100/distance)*s(ho[i].timestamp-ho[nn].timestamp)*s(ho[n].timestamp-ho[i].timestamp)

                                # Different hand
                        else:
                                w += twohand_w*(100/distance)*s(ho[i].timestamp-ho[nn].timestamp)*s(ho[n].timestamp-ho[i].timestamp)

            strain[i] = w

    return strain
