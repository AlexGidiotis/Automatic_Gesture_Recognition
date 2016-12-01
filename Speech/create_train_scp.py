# Author: Alex Gidiotis
#         gidiotisAlex@outlook.com.gr

# This script creates the Train.scp and Test.scp used for training and testing the model.
import re
import os

# Modify this flag to 'Training' or 'Testing'.
flag = 'Testing'
print flag

# Choose between the two modes.
if flag == 'Training':
	path = 'C:\Users\Alex\Documents\University\Python\Data\MFC_audio'
	out_name = 'Train.scp'
elif flag == 'Testing':
	path = 'C:\Users\Alex\Documents\University\Python\Data\MFC_test_audio'
	out_name = 'Test.scp'

# List the directory with the input .mfc data.
f_list = sorted(os.listdir(path))
# Create the .scp file.
of = open(out_name,'w')
# Write all input files.
for file in f_list:
	of.write('%s\%s\n' % (path,file))
of.close()