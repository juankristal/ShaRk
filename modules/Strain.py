import numpy as np

jack_w=2
onehand_w=1.4
twohand_w=0.9

###############################################################################
# Obtains the strain of hitting each consecutive note pair based on the type of
# motion it requires (same hand but different column, different hand, jack)
###############################################################################


#TO-DO: Consider separately all 4 columns for each note? Currently it's buggy cause if one note isn't a jack then it gets supressed a lot by the distance thing

def obtainStrainCalculation(ho):
    strain=np.zeros(len(ho))       



    supr_threshold=35
    for i in range(len(ho)):

        w=0 #Total strain difficulty of the note

        if ho[i].timestamp!=ho[len(ho)-1].timestamp: #Last note doesn't get assigned any value
            n=0
            #Find the next note after the current one
            while ho[i+1+n].timestamp==ho[i].timestamp:
                n+=1
            
            distance=ho[i+1+n].timestamp-ho[i].timestamp

            #Compute, for all notes in that timestamp (it may be a chord), the added difficulty
            nn=n
            while ho[i+1+nn].timestamp==ho[i+1+n].timestamp:
                ch=ho[i].column
                c=ho[i+1+nn].column
                csum=c+ch
                
                #Jacks don't get supressed for graces obviously
                if c==ch:
                    w+=jack_w
                
                #Otherwise, supress based on how gracey it is
                else:
                    if distance<supr_threshold: distance=2*supr_threshold-distance

                    #Same hand, different colum 
                    if csum==5 or csum==1:
                        w+=onehand_w

                    #Different hand
                    else:
                        w+=twohand_w
                nn+=1
                if (i+1+nn)>=len(ho):break
            

            strain[i]=w*(100/distance)

    return strain