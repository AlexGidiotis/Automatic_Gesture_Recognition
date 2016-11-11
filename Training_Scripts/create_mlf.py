# Author: Alex Gidiotis
#         gidiotisAlex@outlook.com.gr

# Reads the Train.scp script and creates the phonemes master label file and .lab files. For embedded sequences reads the label_file.txt as well.
# For isolated sequences the labels are appended in the file name.
# Outputs phones0.mlf and a directory train_labels with all the .lab files that contain each label.

import os
import re

# This dictionary will match each numeric class label into each coding word.
classes = {'0':"SIL", '1':"BS", '2':"BN", '3':"CP", '4':"CV", '5':"CN", '6':"CF", '7':"DC", 
        '8':"FM",  '9':"FN", '10':"FU", '11':"MC", '12':"OK", '13':"PF", '14':"PR",
         '15':"SP", '16':"TT", '17':"ST",  '18':"VA",  '19':"VQ", '20':"NU"}

# Modify this flag to 'Training' or 'Testing'.
flag = 'Testing'
# Modify this to 'Isolated' or 'Embedded'.
embed_flag = 'Embedded'
print flag, embed_flag

#=========================================================== Training ==========================================================================
if flag == 'Training':
    # Create a directory to put the label files if it doesn't already exist.
    if not os.path.exists("train_labels"):
        os.makedirs("train_labels")

    # Create the output .mlf file
    mlf = open("C:\Users\Alex\Documents\University\Python\Automatic_Gesture_Recognition\Training_Scripts\\phones0.mlf", "w")
    # Phonemes label file starts with #!MLF!#
    mlf.write("#!MLF!#\n")

    train_scp = open("C:\Users\Alex\Documents\University\Python\Automatic_Gesture_Recognition\Training_Scripts\\Train.scp")

#=================================================== Isolated Training =========================================================
    # Names in Train.scp appear in the following format.
    # C:\Users\Alex\Documents\University\Python\Data\MFC_data\Training_Sequence101_0.mfc
    # Label is appended in the filename.
    if embed_flag == 'Isolated':
        for line in train_scp:
            # We want to get the file name only.
            name = re.findall('.*\\\(\w*_\w*\d*_\d+).mfc',line)[0]
            # We also want to get the label.
            num = re.findall('.*_(\d+)',name)[0]

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
#=================================================== Embedded Training ==========================================================
    elif embed_flag == 'Embedded':
        # Labels are found in the label file.
        # Names in Train.scp appear in the following format.
        # C:\Users\Alex\Documents\University\Python\Data\MFC_data\Testing_Sequence101.mfc
        # Read the class sequences from the lab file.
        lab_file = open('C:\Users\Alex\Documents\University\Python\Data\MFC_data\\label_file.txt')
        for line, lab_line in zip(train_scp,lab_file):
            # We want to get the file name only.
            name = re.findall('.*\\\(\w*_\w*\d*).mfc',line)[0]
            # Extract labels sequence.
            seq = lab_line.split('[')[1]
            seq = seq.split(']')[0].split(', ')
            # Write to master label file.
            mlf.write('"*/%s.lab"\n' % name)
            for lab in seq:
                label = classes[lab]
                mlf.write("%s\n"% label)
            mlf.write(".\n")

            # Also create a .lab file and write the class in there too.
            lf = open("C:\Users\Alex\Documents\University\Python\Automatic_Gesture_Recognition\Training_Scripts\\train_labels\\"+name+'.lab','w')
            for lab in seq:
                label = classes[lab]
                lf.write("%s\n"% label)
            lf.close()
        mlf.close()

#============================================================== Testing ========================================================================
elif flag == 'Testing':
    # Create a directory to put the label files if it doesn't already exist.
    if not os.path.exists("test_labels"):
        os.makedirs("test_labels")

    # Create the output .mlf file
    mlf = open("C:\Users\Alex\Documents\University\Python\Automatic_Gesture_Recognition\Training_Scripts\\testphones0.mlf", "w")
    # Phonemes label file starts with #!MLF!#
    mlf.write("#!MLF!#\n")

    train_scp = open("C:\Users\Alex\Documents\University\Python\Automatic_Gesture_Recognition\Training_Scripts\\Test.scp")
 
#=================================================== Isolated Testing ==========================================================   
    if embed_flag == 'Isolated':
        # Label is appended in the filename.
        # Names in Train.scp appear in the following format.
        # C:\Users\Alex\Documents\University\Python\Data\MFC_data\Testing_Sequence101_0.mfc
        for line in train_scp:
            # We want to get the file name only.
            name = re.findall('.*\\\(\w*_\w*\d*_\d+).mfc',line)[0]
            # We also want to get the label.
            num = re.findall('.*_(\d+)',name)[0]

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
#=================================================== Embedded Testing ==========================================================
    elif embed_flag == 'Embedded':
        # Labels are found in the label file.
        # Names in Train.scp appear in the following format.
        # C:\Users\Alex\Documents\University\Python\Data\MFC_data\Testing_Sequence101.mfc
        # Read the class sequences from the lab file.
        lab_file = open('C:\Users\Alex\Documents\University\Python\Data\MFC_test_data\\label_file.txt')
        for line, lab_line in zip(train_scp,lab_file):
            # We want to get the file name only.
            name = re.findall('.*\\\(\w*_\w*\d*).mfc',line)[0]
            # Extract labels sequence.
            seq = lab_line.split('[')[1]
            seq = seq.split(']')[0].split(', ')
            # Write to master label file.
            mlf.write('"*/%s.lab"\n' % name)
            for lab in seq:
                label = classes[lab]
                mlf.write("%s\n"% label)
            mlf.write(".\n")

            # Also create a .lab file and write the class in there too.
            lf = open("C:\Users\Alex\Documents\University\Python\Automatic_Gesture_Recognition\Training_Scripts\\test_labels\\"+name+'.lab','w')
            for lab in seq:
                label = classes[lab]
                lf.write("%s\n"% label)
            lf.close()
        mlf.close()