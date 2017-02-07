# Author: Alex Gidiotis
#         gidiotisAlex@outlook.com.gr

# Reads the Train.scp script and creates the phonemes master label file and .lab files. For embedded sequences reads the label_file.txt as well.
# For isolated sequences the labels are appended in the file name.
# Outputs phones0.mlf and a directory train_labels with all the .lab files that contain each label.

import os
import re
import sys

# This dictionary will match each numeric class label into each coding word.
classes = {'0_0':"SIL", '1_1':"TH_LU", '1_2':"BS_2", '1_3':"TH_LD", '2_1':"OH_U", '2_2':"BN_2", '2_3':"OH_D", '3_1':"TH_LU", '3_2':"CP_2", '3_3':"TH_LD", '4_1':"TH_U", '4_2':"CV_2", '4_3':"TH_D", '5_1':"TH_U", '5_2':"CN_2", '5_3':"TH_D", '6_1':"OH_U", '6_2':"CF_2", '6_3':"OH_D", '7_1':"TH_U", '7_2':"DC_2", '7_3':"TH_D", 
        '8_1':"OH_U", '8_2':"FM_2", '8_3':"OH_D", '9_1':"OH_U", '9_2':"FN_2", '9_3':"OH_D", '10_1':"OH_U", '10_2':"FU_2", '10_3':"OH_D", '11_1':"OH_U", '11_2':"MC_2", '11_3':"OH_D", '12_1':"OH_U", '12_2':"OK_2", '12_3':"OH_D", '13_1':"OH_U", '13_2':"PF_2", '13_3':"OH_D", '14_1':"OH_U", '14_2':"PR_2", '14_3':"OH_U",
         '15_1':"OH_U", '15_2':"SP_2", '15_3':"OH_D", '16_1':"OH_U", '16_2':"TT_2", '16_3':"OH_D", '17_1':"OH_U", '17_2':"ST_2", '17_3':"OH_D",  '18_1':"OH_U", '18_2':"VA_2", '18_3':"OH_D",  '19_1':"OH_U", '19_2':"VQ_2", '19_3':"OH_D", '20_1':"OH_U", '20_2':"NU_2", '20_3':"OH_D"}

# Modify this flag to 'Training' or 'Testing'.
flag = 'Training'
# Modify this to 'Isolated' or 'Embedded'.
embed_flag = 'Isolated'
print flag, embed_flag

flag_path = 'Alex'

if flag_path == 'Alex':
    #Alex's Paths
    path_train = "/home/alex/Documents/git_projects/Automatic_Gesture_Recognition"
elif flag_path == 'Dimitris':
    #Dimitri's Paths
    path_train = "/home/dimitris/GitProjects/Automatic_Gesture_Recognition/"


#=========================================================== Training ==========================================================================
if flag == 'Training':
    # Create the output .mlf file
    mlf = open(path_train + "/Training_Scripts/filler_model/phones0_filler.mlf", "w")
    # Phonemes label file starts with #!MLF!#
    mlf.write("#!MLF!#\n")

    train_scp = open(path_train + "/Training_Scripts/filler_model/Train.scp")

#=================================================== Isolated Training =========================================================
    # Names in Train.scp appear in the following format.
    # C:\Users\Alex\Documents\University\Python\Data\MFC_data\Training_Sequence101_0.mfc
    # Label is appended in the filename.
    if embed_flag == 'Isolated':
        for line in train_scp:
            # We want to get the file name only.
            if flag_path == 'Alex':
                name = re.findall('.*\\\(\w*_\w*\d*_\d+).mfc',line)[0]
                #num = re.findall('.*_(\d+_\d+)',name)[0]
            elif flag_path == 'Dimitris':
                name = re.findall('.*\\/(\w*_\w*\d*_\d+).mfc',line)[0]
                # We also want to get the label.
            num = re.findall('.*_(\d+_\d+)',name)[0]
            # Write to master label file.
            mlf.write('"*/%s.lab"\n' % name)
            mlf.write("%s\n"% 'oov')
            mlf.write(".\n")
        mlf.close()