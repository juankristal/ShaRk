import numpy as np
import math

jack_w = 2.75
onehand_w = 1.1
twohand_w = 0.5

def s(x):
    x=max(-1000,min(x,1000))
    return 1 / (1 + math.exp(6-0.12*x))

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
            for c in [0,1,2,3]:
                j=i

                # j: The next note **after** i in column c
                while ho[j].timestamp==ho[i].timestamp or c!=ho[j].column:
                    j += 1
                    if j>=len(ho):break
                if j>=len(ho): continue

                distance = ho[j].timestamp-ho[i].timestamp

                csum = ho[j].column + ho[i].column

                # Jacks don't get supressed for graces obviously
                if c == ho[i].column:
                    c1= (ho[i].column+1) % 2 if ho[i].column in [0,1] else (ho[i].column-1) % 2+2 #Different column in the same hand

                    k=i #List index pointer for iteration
                    n2=-1; n1=-1   #Notes that could make the jack [i n2] and [j n1] (j is the next note in c after i)
                    
                    while not k<0 and n1==-1:   #While we don't obtain both notes or run out of notes to check, go backward through the HitObjects list
                        if ho[k].column==c1:    #If we find a note in the desired column, "roll" the elements of the "queue" adding the new found note
                            n1=n2
                            n2=k
                        k-=1
                    
                    if k<0 and n1==-1: #If we ran out of notes before i and couldn't find two 
                        k=i+1  #Start looking for the missing notes after i this time

                        while k<len(ho) and (n1==-1 or n2==-1):     #While we don't obtain both this time or run out of notes to check, go forward through the HitObjects list
                            if ho[k].column==c1:    #If we find a note in the desired column, update n2 and n1
                                if n2==-1: n2=n1 #If we had already found one note in the previous while, lock n2
                                n1=k
                            k+=1

                    if n2==-1 or n1==-1: supress=1 #If we didn't have enough notes, just don't supress for jacks
                    else:
                        k=n1+1
                        while k<len(ho): #Else, start iterating forward (find next noteS after n1 in c1)
                            if ho[k].column==c1:
                                d1=abs(ho[i].timestamp-ho[n2].timestamp)+abs(ho[j].timestamp-ho[n1].timestamp)   #Old pair distance
                                d2=abs(ho[i].timestamp-ho[n1].timestamp)+abs(ho[j].timestamp-ho[k].timestamp)   #New pair distance
                                
                                if d2>d1: break     #If it increased, curent pair is better
                                else:       #Otherwise move the currrent pair to the new found one
                                    n2=n1
                                    n1=k
                            k+=1
                        supress=0.5**((1-s(abs(ho[i].timestamp-ho[n2].timestamp)))*(1-s(abs(ho[j].timestamp-ho[n1].timestamp))))
        
                    if ho[i].timestamp==4197: 
                            print(f"Column (i): {ho[i].column}")
                            print(f"Column (j): {ho[j].column}")
                            print(f"Base_strain: {jack_w*(100/distance)}")
                            print(f"Double_supr: {supress}")
                            print(f"Total: {jack_w*(100/distance)*supress}")

                    w += jack_w*(100/distance)*supress

                # Otherwise, supress based on how gracey it is
                else:

                    # Next note in i's column
                    k_i=i
                    while ho[i].column!=ho[k_i].column or k_i==i:
                        k_i+=1
                        if k_i>=len(ho):
                            break

                    #Measure how much after j happens the next note in i's column. If it's relatively before j, then one handed difficulty for i it gets suppressed
                    oh_supr=1 if k_i>=len(ho) else 1-s(ho[j].timestamp-ho[k_i].timestamp)

                    # Previous note in i's column
                    k_c=j
                    while ho[j].timestamp==ho[k_c].timestamp or c!=ho[k_c].column:
                        k_c -= 1
                        if k_c<0: break
                    if k_c<0: 
                        jack_supr=1
                    else:
                        jack_supr=s(ho[i].timestamp-ho[k_c].timestamp)
                            
                    # Same hand, different colum
                    if csum == 5 or csum == 1:

                            
                            #Grace Suppression
                            grace_supr=s(ho[j].timestamp-ho[i].timestamp)

                            if ho[i].timestamp==4197: 
                                print(f"Column (i): {ho[i].column}")
                                print(f"Column (j): {ho[j].column}")
                                print(ho[k_i].timestamp)
                                print(ho[j].timestamp)
                                print(f"Base_strain: {onehand_w*(100/distance)}")
                                print(f"Double_supr: {s(ho[i].timestamp-ho[k_c].timestamp)}")
                                print(f"Jack_supr: {oh_supr}")
                                print(f"Total: {onehand_w*(100/distance)*s(ho[i].timestamp-ho[k_c].timestamp)*s(ho[j].timestamp-ho[i].timestamp)*oh_supr}")

                            w += onehand_w*(100/distance)*jack_supr*grace_supr*oh_supr

                    else:
                        #Other column in the other hand
                        c1= (c+1) % 2 if c in [0,1] else (c-1) % 2+2

                        #Other column in the same hand
                        c2= (ho[i].column+1) % 2 if ho[i].column in [0,1] else (ho[i].column-1) % 2+2


                        #Find the previous note to j in c1
                        k_th_otherc=j
                        while c1!=ho[k_th_otherc].column:
                            k_th_otherc-=1
                            if k_th_otherc<0:
                                break
                        if k_th_otherc<0: by_oh_supr=1
                        else: by_oh_supr=s(ho[i].timestamp-ho[k_th_otherc].timestamp)

                      
                        #Find the previous note to j in c2
                        k_oh_otherc=j
                        while c2!=ho[k_oh_otherc].column:
                            k_oh_otherc-=1
                            if k_oh_otherc<0:
                                break
                        if k_oh_otherc<0: double_supr=1
                        else: double_supr=s(ho[i].timestamp-ho[k_oh_otherc].timestamp+50)

                        total=twohand_w*(100/distance)*jack_supr*s(ho[j].timestamp-ho[i].timestamp)*by_oh_supr*double_supr*oh_supr

                        if ho[i].timestamp==4197: 
                            print(f"Column (i): {ho[i].column}")
                            print(f"Column (j): {ho[j].column}")
                            print(f"Base_strain: {twohand_w*(100/distance)}")
                            print(f"Double_supr: {double_supr}")
                            print(f"Th_supr: {by_oh_supr}")
                            print(f"Jack_supr: {jack_supr}")
                            print(f"Total: {total}")
                        w +=total

            strain[i] = w

    return strain
