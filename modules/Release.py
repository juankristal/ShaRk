import numpy as np
import math

#Sigmoidal
def s(x):
        return 1 / (1 + math.exp(-x))

#Sigmoidal-based function that peaks at around 120 and descends on both sites
def f(x):
        if x>1000:x=1000
        return s(0.1*(x-60))+s(0.1*(-x+180))-1
        
###############################################################################
#   Obtain the release/timing difficulty of each LN based on how the timings of
#   the ln ends and notes surrounding the release (one for each column)
###############################################################################

onehand_w=2
twohand_w=1


def obtainReleaseCalculation(ho,bin_size):
    
    v=np.zeros(len(ho))       

    for i in range(len(ho)):
        if ho[i].isln:
            c=ho[i].column
            n=i

            #Obtain the index of the note that is at i's ln end or the nearest after it
            while ho[n].timestamp<ho[i].lnend:
                n+=1
                if n>=len(ho):break
            if n>=len(ho):break


            r=0 #Release difficulty counter
            cols=[0,1,2,3]
            cols.remove(c)

            #For all the columsn that aren't the note's one
            for col in cols:

                a=onehand_w if c+col==1 or c+col==5 else twohand_w #Choose weight based on column combination

                #Find the previous closest note in that column...
                j=n
                while ho[j].column!=col:
                    j-=1
                    if j<0: break
                if j<0: break

                #...and add the difficulty to the counter based on timing difference
                if ho[j].isln: 
                    r+=a*f(abs(ho[i].lnend-ho[j].lnend)) #Notice the abs to support both cases
                else: r+=a*f(ho[i].lnend-ho[j].timestamp)
                
                #Find the following closest note in that column...
                j=n+1
                if j>=len(ho):break
                while ho[j].column!=col:
                    j+=1
                    if j>=len(ho):break
                if j>=len(ho):break

                #... and add it to the counter
                r+=a*f(ho[j].timestamp-ho[i].lnend)

            v[i]=r
    return v