# Author: Alex Gidiotis
#         gidiotisAlex@outlook.com.gr

#This script creates the word master label file for speech training and testing. This file will then be turned into a phones mlf using HLEd.
# In this script we add noise between gestures for better generalization.
import pandas as pd
import os
import re
import subprocess

# We match the class labels with sentences and words for speech recognition.
words = {'vieniqui':'Vieni qui','prendere':'Le vuoi prendere','sonostufo':'sono stufo','chevuoi':'Che vuoi',
		'daccordo':'Vanno d\'accordo','perfetto':'Perfetto','vattene':'Vattene','basta':'Basta','buonissimo':'Buonissimo',
		'cheduepalle':'Che due palle','cosatifarei':'Cosa ti farei','fame':'Ho fame','noncenepiu':'Non ce n\'e piu',
		'furbo':'E\' un furbo','combinato':'Cos\'hai combinato','freganiente':'Non me ne frega niente','seipazzo':'Sei Pazzo',
		'tantotempo':'Tanto tempo fa','messidaccordo':'Si sono messi d\'accordo','ok':'ok'}

# Modify this flag to 'Training' or 'Testing'.
flag = 'Training'
print flag

# Choose between the two modes.
if flag == 'Training':
	# Create the output .mlf file
	mlf = open("words_filler.mlf", "w")


# Words label file starts with #!MLF!#
mlf.write("#!MLF!#\n")

# Read files one by one.
file_list = sorted(os.listdir("/home/alex/Documents/Data/MFC_audio"))
for file in file_list:

	file_name = file[:-4]
	# Write the file line in the mlf.
	mlf.write('"*/%s.lab"\n' % (file_name))

	# Write the sequence of labels in the mlf.
	for i in range(20):
		mlf.write("%s\n"% 'noise')
		mlf.write("%s\n"% 'oov')
		mlf.write("%s\n"% 'noise')
	# Write the end of file line.
	mlf.write(".\n")

mlf.close()
print 'words_filler.mlf created'
