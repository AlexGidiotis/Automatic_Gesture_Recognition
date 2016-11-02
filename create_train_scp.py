# Author: Alex Gidiotis
#		  gidiotisAlex@outlook.com.gr

# Creates the training script required for htk training.
# Outputs a training script .scp inside the training directory.

import os

path_train = "C:\Users\Alex\Documents\University\Python\Data\MFC_data"
path_test = "C:\Users\Alex\Documents\University\Python\Data\MFC_test_data"
path_out = "C:\Users\Alex\Documents\University\Python\Automatic_Gesture_Recognition\Training_Scripts"

# Modify this flag to 'Training' or 'Testing'.
flag = 'Testing'
# Modify this flag to 'Isolated' or 'Embedded'.
flag_emb = 'Embedded'
print flag, flag_emb

if flag == 'Training':
	path_top = path_train
	# Go to the data directory and write all .mfc files in the training script.
	of = open(path_out+"/Train.scp", 'w')
	# List the directory and open each file.
	listing = os.listdir(path_top)
	for f in listing:
		# Ignore some files.
		if f.startswith('Embedded'):continue
		elif f[-3:] == 'txt':continue
		of.write("%s\\%s\n" %(path_top,f))
	print "Training script created."
	of.close()
elif flag == 'Testing':
	path_top = path_test
	# Go to the data directory and write all .mfc files in the training script.
	of = open(path_out+"/Test.scp", 'w')
	# Handle isolated gestures.
	if flag_emb == 'Isolated':
		# List the directory and open each file.
		listing = os.listdir(path_top)
		for f in listing:
			# Ignore some files.
			if f.startswith('Embedded'):continue
			elif f[-3:] == 'txt':continue
			of.write("%s\\%s\n" %(path_top,f))
		print "Test script created."
	# Handle embedded sequences.
	elif flag_emb == 'Embedded':
		# List the directory and open each file.
		listing = os.listdir(path_top)
		for f in listing:
			# Ignore some files.
			if not f.startswith('Embedded'):continue
			elif f[-3:] == 'txt':continue
			of.write("%s\\%s\n" %(path_top,f))
		print "Test script created."
	of.close()