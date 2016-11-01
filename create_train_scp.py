# Author: Alex Gidiotis
#		  gidiotisAlex@outlook.com.gr

# Creates the training script required for htk training.
# Outputs a training script .scp inside the training directory.

import os

path_top = "C:\Users\Alex\Documents\University\Python\Data\MFC_data"
path_out = "C:\Users\Alex\Documents\University\Python\Automatic_Gesture_Recognition\Training_Scripts"

# Go to the data directory and write all .mfc files in the training script.
of = open(path_out+"/Train.scp", 'w')
# List the directory and open each file.
listing = os.listdir(path_top)
for f in listing:
	of.write("%s\\%s\n" %(path_top,f))

print "Training script created."
of.close()