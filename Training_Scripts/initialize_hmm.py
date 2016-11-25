# Author: Alex Gidiotis
#         gidiotisAlex@outlook.com.gr

# This script initializes the hmms for training.

import sys, subprocess

classes=['SIL', 'BN_2', 'BS_2', 'CF_2', 'CN_2', 'CP_2', 'CV_2', 'DC_2', 'FM_2', 'FN_2', 'FU_2', 'MC_2', 'NU_2', 'OK_2', 'PF_2', 'PR_2', 'SP_2', 'ST_2', 'TT_2', 'VA_2', 'VQ_2', 'OH_U', 'OH_D', 'TH_LU', 'TH_LD', 'TH_U', 'TH_D']


path = "C:\Users\Alex\Documents\University\Python\Automatic_Gesture_Recognition\\Training_Scripts\hmm0"

#path = "C:\Users\Alex\Documents\University\Python\Automatic_Gesture_Recognition\\Devel\\Training_Scripts\hmm0"
#path = "/home/dimitris/GitProjects/Automatic_Gesture_Recognition/Training_Scripts/hmm0"

#=============================== Create the macros file =======================================================================================
pf = open(path+"/prototype",'r')
of = open(path+"/macros",'w')

# Read the first lines of the prototype file.
lin1 = pf.readline()
lin2 = pf.readline()
lin3 = pf.readline()
pf.close()

# Write the first lines of the prototype file to the macros file.
of.write(lin1)
of.write(lin2)
of.write(lin3)

vf = open(path+"/vFloors", 'r')

# Read lines from vFloors and write them to the macros file.
for line in vf:
    of.write(line)

vf.close()
of.close()

#========================================== Create the hmmdefs file ==========================================================================
deff = open(path+"/hmmdefs",'w')

# Write the prototype hmm for each class to the hmmdefs file.
for cl in classes:
    deff.write('~h "%s" \n' % cl)
    pf = open(path+"/prototype",'r')
    pf.readline()
    pf.readline()
    pf.readline()
    pf.readline()
    for line in pf:
        deff.write("    "+line)

    pf.close()
