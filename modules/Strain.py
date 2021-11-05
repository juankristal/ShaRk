import numpy as np
import math

jack_w = 2.2
onehand_w = 1.1
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
                    c1= (ho[i].column+1) % 2 if ho[i].column in [0,1] else (ho[i].column-1) % 2+2 #Different column in the same hand

                    j=i #List index pointer for iteration
                    n2=-1; n1=-1   #Notes that could make the jack [i n2] and [n n1] (n is the next note in c after i)
                    
                    while not j<0 and n1==-1:   #While we don't obtain both notes or run out of notes to check, go backward through the HitObjects list
                        if ho[j].column==c1:    #If we find a note in the desired column, "roll" the elements of the "queue" adding the new found note
                            n1=n2
                            n2=j
                        j-=1

                    if j<0 and n1!=1: #If we ran out of notes before i and couldn't find two 
                        j=i+1  #Start looking for the missing notes after i this time

                        while j<len(ho) and (n1==-1 or n2==-1):     #While we don't obtain both this time or run out of notes to check, go forward through the HitObjects list
                            if ho[j].column==c1:    #If we find a note in the desired column, update n2 and n1
                                if n2==-1: n2=n1 #If we had already found one note in the previous while, lock n2
                                n1=j
                            j+=1

                    if n2==-1 or n1==-1: supress=1 #If we didn't have enough notes, just don't supress for jacks
                    else:
                        j=n1+1
                        while j<len(ho): #Else, start iterating forward (find next noteS after n1 in c1)
                            if ho[j].column==c1:
                                d1=abs(ho[i].timestamp-ho[n2].timestamp)+abs(ho[n].timestamp-ho[n1].timestamp)   #Old pair distance
                                d2=abs(ho[i].timestamp-ho[n1].timestamp)+abs(ho[n].timestamp-ho[j].timestamp)   #New pair distance
                                
                                if d2>d1: break     #If it increased, curent pair is better
                                else:       #Otherwise move the currrent pair to the new found one
                                    n2=n1
                                    n1=j
                            j+=1
                        supress=0.5**((1-s(abs(ho[i].timestamp-ho[n2].timestamp)))*(1-s(abs(ho[n].timestamp-ho[n1].timestamp))))
                    w += jack_w*(100/distance)*supress

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
