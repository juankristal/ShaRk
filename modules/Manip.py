import numpy as np

###############################################################################
# Obtains the manipulabilty of each note based on each surroundings. If the
# amount of notes between each hand's columns and between hands is balanced,
# then the patterning is highly manipulable
###############################################################################
bin_size = 1000

def obtainManipCalculation(ho):

    n_ho=len(ho)
    manip = np.zeros(n_ho)
    col_counts = np.ones(4)
    wl = 0  # Current index of the note that first enters in the window
    for i in range(n_ho):

        t = ho[i].timestamp
        # Find the new first note that is inside the window
        while ho[wl].timestamp < (t-bin_size/2):
            wl += 1

        col_counts[:]=1

        wr=wl
        # Fin the new last note that is inside the window, count notes per column
        
        while ho[wr].timestamp < (t+bin_size/2) and wr < n_ho-1:
            col_counts[ho[wr].column] += 1
            wr += 1

        hand_counts=col_counts[1::2]+col_counts[0::2]
        l_hand=col_counts[:2]
        r_hand=col_counts[2:]

        def var(a,b):
            return ((a-b)**2)/((a+b)/2)
        # For all of the following, 1=Easy to manipulate, 0="Impossible" to manipulate
        m=0
        # How easy is to manipulate the patterning in the left hand
        m+=(1+np.amin(l_hand))/(np.amax(l_hand))/(1+var(l_hand[0],l_hand[1]))
        # How easy is to manipulate the patterning in the right hand
        m+=(1+np.amin(r_hand))/(np.amax(r_hand))/(1+var(r_hand[0],r_hand[1]))
        # How evenly distributed is the patterning between hands
        m+=(1+np.amin(hand_counts))/(np.amax(hand_counts))/(1+var(hand_counts[0],hand_counts[1]))
        manip[i] = m/3

    return manip
