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
flag = 'Testing'
print flag

# Choose between the two modes.
if flag == 'Training':
	if not os.path.exists("train_labels"):
		os.makedirs("train_labels")

	# Create the output .mlf file
	mlf = open("words.mlf", "w")

	in_file = 'Train_labels.csv'
	out_words = 'words.mlf'
	out_name = 'TrainingSample'
	out_phones = 'phones0.mlf'
	lab_path = 'C:\Users\Alex\Documents\University\Python\Automatic_Gesture_Recognition\Speech\\train_labels'

elif flag == 'Testing':
	if not os.path.exists("test_labels"):
		os.makedirs("test_labels")

	# Create the output .mlf file
	mlf = open("test_words.mlf", "w")

	in_file = 'Test_labels.csv'
	out_words = 'test_words.mlf'
	out_name = 'TestingSample'
	out_phones = 'test_phones0.mlf'
	lab_path = 'C:\Users\Alex\Documents\University\Python\Automatic_Gesture_Recognition\Speech\\test_labels'

# Words label file starts with #!MLF!#
mlf.write("#!MLF!#\n")

lf = pd.read_csv(in_file)
# Read files one by one.
for file in lf['file'].unique():
	# Get the file id.
	file_num = int(file)
	# Put labels in a list.
	label_list = []
	# Go through all labels except 'sil'. Vectorized for faster computation.
	file_labs = lf.ix[lf['file'] == file, 'label'].as_matrix()
	for lab in file_labs:
		# Sil will be added later in the process.
		if lab == 'sil': continue
		# Append the first label in the list as well as some noise.
		if len(label_list) == 0:
			label_list.append('noise')
			label_list.append(words[lab])
		# Append all other labels and noise.
		elif label_list[-1] != words[lab]:
			label_list.append('noise')
			label_list.append(words[lab])
	# Write the file line in the mlf.
	mlf.write('"*/%s%d.lab"\n' % (out_name,file_num))
	# Write the sequence of labels in the mlf.
	for word in label_list:
		# Write to master label file.
		for item in word.split():
			mlf.write("%s\n"% item)
	# Write the end of file line.
	mlf.write(".\n")

mlf.close()
print out_words,'created'

# This is not required.

#phones_mlf = open(out_phones)
#fline = phones_mlf.readline()
#print fline
#for line in phones_mlf:
#	line = line.rstrip()
#	if line.startswith('"*'):
#		f_name = re.findall('"*/(\D+\d+).lab',line)[0]
#		lab_f = open(os.path.join(lab_path,f_name + '.lab'),'w')
#	elif line.startswith('.'):
#		lab_f.close()
#	else:
#		lab_f.write('%s\n' % line)


