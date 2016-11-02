# Author: Alex Gidiotis
#         gidiotisAlex@outlook.com.gr

# Reads the Train.scp script and creates the phonemes master label file and .lab files
# Outputs phones0.mlf and a directory train_labels with all the .lab files that contain each label.

# NEED TO BE MODILIED TO HANDLE EMBEDDED SEQUENCIES.

import os
import re

# This lists will match each numeric class label into each coding word.
classes = ["SIL", "BS", "BN", "CP", "CV", "CN", "CF", "DC", "FM", "FN", "FU", "MC", "OK", "PF", "PR", "SP", "TT", "ST", "VA", "VQ", "NU"]
classnum=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

# Modify this flag to 'Training' or 'Testing'.
flag = 'Testing'
print flag
if flag == 'Training':
    # Create a directory to put the label files if it doesn't already exist.
    if not os.path.exists("train_labels"):
        os.makedirs("train_labels")

    # Create the output .mlf file
    mlf = open("C:\Users\Alex\Documents\University\Python\Automatic_Gesture_Recognition\Training_Scripts\\phones0.mlf", "w")
    # Phonemes label file starts with #!MLF!#
    mlf.write("#!MLF!#\n")

    train_scp = open("C:\Users\Alex\Documents\University\Python\Automatic_Gesture_Recognition\Training_Scripts\\Train.scp")

    # Names in Train.scp appear in the following format.
    # C:\Users\Alex\Documents\University\Python\Data\MFC_data\Training_Sequence101_0.mfc
    for line in train_scp:
        # We want to get the file name only.
        name = re.findall('.*\\\(\w*_\w*\d*_\d+).mfc',line)[0]
        # We also want to get the label.
        num = int(re.findall('.*_(\d+)',name)[0])

        # Write to master label file.
        mlf.write('"*/%s.lab"\n' % name)
        label = classes[num]
        mlf.write("%s\n"% label)
        mlf.write(".\n")

        # Also create a .lab file and write the class in there too.
        lf = open("C:\Users\Alex\Documents\University\Python\Automatic_Gesture_Recognition\Training_Scripts\\train_labels\\"+name+'.lab','w')
        lf.write(label)
        lf.close()
        
    mlf.close()
elif flag == 'Testing':
    # Create a directory to put the label files if it doesn't already exist.
    if not os.path.exists("test_labels"):
        os.makedirs("test_labels")

    # Create the output .mlf file
    mlf = open("C:\Users\Alex\Documents\University\Python\Automatic_Gesture_Recognition\Training_Scripts\\testphones0.mlf", "w")
    # Phonemes label file starts with #!MLF!#
    mlf.write("#!MLF!#\n")

    train_scp = open("C:\Users\Alex\Documents\University\Python\Automatic_Gesture_Recognition\Training_Scripts\\Test.scp")

    # Names in Train.scp appear in the following format.
    # C:\Users\Alex\Documents\University\Python\Data\MFC_data\Testing_Sequence101_0.mfc
    for line in train_scp:
        # We want to get the file name only.
        name = re.findall('.*\\\(\w*_\w*\d*_\d+).mfc',line)[0]
        # We also want to get the label.
        num = int(re.findall('.*_(\d+)',name)[0])

        # Write to master label file.
        mlf.write('"*/%s.lab"\n' % name)
        label = classes[num]
        mlf.write("%s\n"% label)
        mlf.write(".\n")

        # Also create a .lab file and write the class in there too.
        lf = open("C:\Users\Alex\Documents\University\Python\Automatic_Gesture_Recognition\Training_Scripts\\test_labels\\"+name+'.lab','w')
        lf.write(label)
        lf.close()
        
    mlf.close()