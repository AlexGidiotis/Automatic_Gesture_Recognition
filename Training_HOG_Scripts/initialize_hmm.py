# Author: Alex Gidiotis
#         gidiotisAlex@outlook.com.gr

# This script initializes the hmms for training.

import sys, subprocess
#path = "C:\Users\Alex\Documents\University\Python\Automatic_Gesture_Recognition\Training_HOG_Scripts\hmm0"
path = '/home/dimitris/GitProjects/Automatic_Gesture_Recognition/Training_HOG_Scripts/hmm0'

classes=['SIL', 'BN', 'BS', 'CF', 'CN', 'CP', 'CV', 'DC', 'FM', 'FN', 'FU', 'MC', 'NU', 'OK', 'PF', 'PR', 'SP', 'ST', 'TT', 'VA', 'VQ']


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
