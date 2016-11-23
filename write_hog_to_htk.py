# Author: Alex Gidiotis
#		  gidiotisAlex@outlook.com.gr

# This script reads extracted features and writes them to htk mfc format.
# Outputs one .mfc file for every gesture in every file.
# Also supports embedded sequencies. In this case it creates a .mfc file for each sequence and a labels file that keeps track of all labels.

# We need to add handles for unlabeled data as well.

import os
import htkmfc
import pandas as pd
import re

# Map each gesture code into an integer id.
def map_gesture(gest):
	if gest == 'sil': return 0
	if gest == 'basta': return 1
	if gest == 'buonissimo' : return 2
	if gest == 'cheduepalle' : return 3
	if gest == 'chevuoi' : return 4
	if gest == 'combinato' : return 5
	if gest == 'cosatifarei' : return 6
	if gest == 'daccordo' : return 7
	if gest == 'fame' : return 8
	if gest == 'freganiente' : return 9
	if gest == 'furbo' : return 10
	if gest == 'messidaccordo' : return 11
	if gest == 'ok' : return 12
	if gest == 'perfetto': return 13
	if gest == 'prendere': return 14
	if gest == 'seipazzo': return 15
	if gest == 'tantotempo': return 16
	if gest == 'sonostufo': return 17
	if gest == 'vattene': return 18
	if gest == 'vieniqui': return 19
	if gest == 'noncenepiu': return 20

#================================================================= MAIN =======================================================================

# Change this path to the saved skeletal .csv file.
#out_path_train = "C:\Users\Alex\Documents\University\Python\Data\MFC_HOG_data"
#out_path_test = "C:\Users\Alex\Documents\University\Python\Data\MFC_HOG_test_data"
# Modify this flag to 'Training' or 'Testing'.
flag = 'Training'
# Modify this flag to 'Isolated' or 'Embedded'.
flag_embed = 'Embedded'
flag_path = 'Dimitris'


#================================================================ Switch between Training and Testing =========================================
#Define paths
if flag_path == 'Alex':
	if flag == 'Training':
		out_path = "C:\Users\Alex\Documents\University\Python\Data\MFC_HOG_data"
		in_path = "C:\Users\Alex\Documents\University\Python\Data\Train_hog_feats"
		out_file = 'Training_Sequence'
	elif flag == 'Testing':
		out_path = "C:\Users\Alex\Documents\University\Python\Data\MFC_HOG_test_data"
		in_path = "C:\Users\Alex\Documents\University\Python\Data\Test_hog_feats"
		out_file = 'Testing_Sequence'
elif flag_path == 'Dimitris':
	if flag == 'Training':
		out_path = "/home/dimitris/GitProjects/Automatic_Gesture_Recognition/Data/MFC_HOG_data"
		in_path = "/home/dimitris/GitProjects/Automatic_Gesture_Recognition/Data/Train_hog_feats"
		out_file = 'Training_Sequence'
	elif flag == 'Testing':
		out_path = "/home/dimitris/GitProjects/Automatic_Gesture_Recognition/Data/MFC_HOG_test_data"
		in_path = "/home/dimitris/GitProjects/Automatic_Gesture_Recognition/Data/Test_hog_feats"
		out_file = 'Testing_Sequence'
		
#============================================== Load data and get rid of some weird labels ====================================================
# Load the data and get the different file ids in a list.
print flag, flag_embed
file_list = sorted(os.listdir(in_path))

print 'Loading data...'
# Make a list of all file ids.
files = []
for file in file_list:
	if file.startswith('Reduced'):continue
	file_id = re.findall('sample(\d+)_',file)[0]
	if file_id not in files: 
		files.append(file_id)


#========================================================== Isolated ==========================================================================
# Handled isolated gestures.
if flag_embed == 'Isolated':
	for file in file_list:
		df = pd.read_csv(in_path + '/' + file)
		df = df.drop(['label', 'file', 'frame', 'hand'], axis=1)
		# Alternative isolated gestures.
		# Go through all the data by file id.
		# sample1_hog_basta.csv
		gest = re.findall('sample\d+_hog_(\D+).csv',file)[0]
		file_id = re.findall('sample(\d+)_',file)[0]
		# Open a .mfc file for each gesture to write the feature vectors.
		label = map_gesture(gest)
		file_name = out_file + str(file_id) + '_hog_' + str(label) + '.mfc'
		out_file_name = os.path.join(out_path,file_name)
		print out_file_name
		
		mfc_writer = htkmfc.open(out_file_name,'w',576)
		# Go through all frames in the specific file id and write the extracted features to mfc format.
		for i in df.index:
			feats = df.iloc[i].as_matrix().astype(float)
			
			mfc_writer.writevec(feats)

		# Close the mfc file.
		mfc_writer.close()


#===================================================================== Embedded================================================================
# If we choose embedded testing we will write a sequence of gestures in each file.
elif flag_embed == 'Embedded':
	# Alternative embeded gestures.
	# Create a label file for embedded class sequencies.
	lab_file_name = 'label_file.txt'
	lab_file_name = os.path.join(out_path,lab_file_name)
	lab_file = open(lab_file_name,'w')
	# Go through all the data by file id.
	for f_id in files:
		# Gather all parts of a file in one dataframe.
		all_df = pd.DataFrame()
		for file in file_list:
			file_id = re.findall('sample(\d+)_',file)[0]
			if file_id != f_id: continue
			df = pd.read_csv(in_path + '/' + file)
			all_df = all_df.append(df,ignore_index=True)

		# Sort by frame.
		all_df = all_df.sort_values('frame').reset_index(drop=True)
		# Drop useless columns.
		all_df = all_df.drop(['file', 'frame', 'hand'], axis=1)

		# Write .mfc output vectors.
		file_name = 'Embedded' + out_file + str(f_id) + '.mfc'
		out_file_name = os.path.join(out_path,file_name)
		print out_file_name

		label_sequence = []
		mfc_writer = htkmfc.open(out_file_name,'w',576)
		# Go through all frames in the specific file id and write the extracted features to mfc format.
		for i in all_df.index:	
			# Get the feature vector.
			feats = all_df.iloc[i]
			# Get the label.
			gest = feats['label']
			label = map_gesture(gest)
			# Drop the label column.
			feats = feats.drop('label').as_matrix().astype(float)
			# Write feat vector.
			mfc_writer.writevec(feats)
			# Make a list of label sequence.
			if len(label_sequence) > 0:
				if label_sequence[-1] == label:
					pass
				else:
					label_sequence.append(label)
			else:
				label_sequence.append(label)
		mfc_writer.close()
		# Write label file.
		lab_file.write('%s:%s\n' %(file_name,label_sequence))
	lab_file.close()


print "finished"