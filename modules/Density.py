import numpy as np

###############################################################################
# Obtains the density calculation for each note in the map by counting the
# amount of notes around the note in a timing window of size bin_size
###############################################################################


def obtainDensityCalculation(ho, bin_size):
    density = np.zeros(len(ho), dtype=int)
    wl = 0  # Current index of the note that first enters in the window
    wr = 0  # Same but for last

    for i in range(len(ho)):

        # Find the new first note that is inside the window
        while ho[wl].timestamp < (ho[i].timestamp-bin_size/2):
            wl += 1

        # Fin the new last note that is inside the window
        while ho[wr].timestamp < (ho[i].timestamp+bin_size/2) and wr < len(ho)-1:
            wr += 1

        # The note count is simply the index difference
        density[i] = wr-wl

    return density
