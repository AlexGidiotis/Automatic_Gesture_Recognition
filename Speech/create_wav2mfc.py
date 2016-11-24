# Author: Alex Gidiotis
#         gidiotisAlex@outlook.com.gr

# This script creates the wav2mfc.scp file that HCopy requires to extract the mfc features from the .wav files.
# The script looks like this:

#C:\Users\Alex\Documents\University\Python\Data\Test_audio\Sample00410_audio.wav C:\Users\Alex\Documents\University\Python\Data\MFC_test_audio\TestingSample410.mfc
#C:\Users\Alex\Documents\University\Python\Data\Test_audio\Sample00411_audio.wav C:\Users\Alex\Documents\University\Python\Data\MFC_test_audio\TestingSample411.mfc
# 									... 																			...
import os
import re


# Modify this flag to 'Training' or 'Testing'.
flag = 'Testing'
print flag

# Choose between the two modes.
if flag == 'Training':
	path = 'C:\Users\Alex\Documents\University\Python\Data\Train_audio'
	out_path = 'C:\Users\Alex\Documents\University\Python\Data\MFC_audio'
	out_name = 'TrainingSample'
elif flag == 'Testing':
	path = 'C:\Users\Alex\Documents\University\Python\Data\Test_audio'
	out_path = 'C:\Users\Alex\Documents\University\Python\Data\MFC_test_audio'
	out_name = 'TestingSample'

# List the directory with the input .wav data.
f_list = os.listdir(path)
# Create the .scp file.
of = open('wav2mfc.scp','w')
# Write all input files and output files.
for file in f_list:
	# Create the output file name.
	fileNum = re.findall('Sample0+(\d+)_',file)[0]
	out_file = out_name + fileNum + '.mfc'
	of.write('%s\%s %s\%s\n' % (path,file,out_path,out_file))
of.close()


