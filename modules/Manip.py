import numpy as np

###############################################################################
# Obtains the manipulabilty of each note based on each surroundings. If the
# amount of notes between each hand's columns and between hands is balanced,
# then the patterning is highly manipulable
###############################################################################
bin_size = 1000

def obtainManipCalculation(ho):
    manip = np.zeros(len(ho))

    wl = 0  # Current index of the note that first enters in the window
    wr = 0  # Same but for last
    for i in range(len(ho)):

        # Find the new first note that is inside the window
        while ho[wl].timestamp < (ho[i].timestamp-bin_size/2):
            wl += 1

        # Fin the new last note that is inside the window
        while ho[wr].timestamp < (ho[i].timestamp+bin_size/2) and wr < len(ho)-1:
            wr += 1

        # Count the amount of notes in each column for the window
        col_counts = [1, 1, 1, 1]
        for h in range(wl, wr):
            col_counts[ho[h].column] += 1

        # For all of the following, 1=Easy to manipulate, 0="Impossible" to manipulate

        # How easy is to manipulate the patterning in the left hand
        l_manip = (1+min(col_counts[:2]))/(max(col_counts[:2]))/(1+np.var([col_counts[:2]]))
        # How easy is to manipulate the patterning in the right hand
        r_manip = (1+min(col_counts[2:]))/(max(col_counts[2:]))/(1+np.var([col_counts[2:]]))
        h_manip = (min(sum(col_counts[:2]), sum(col_counts[2:]))/max(sum(col_counts[:2]), sum(col_counts[2:]))/(
            1+np.var([sum(col_counts[:2]), sum(col_counts[2:])])))  # How evenly distributed is the patterning between hands

        manip[i] = np.average([l_manip, r_manip,h_manip])

    return manip
