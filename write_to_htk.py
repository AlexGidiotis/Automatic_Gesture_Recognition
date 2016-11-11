# Author: Alex Gidiotis
#		  gidiotisAlex@outlook.com.gr

# This script reads extracted features and writes them to htk mfc format.
# Outputs one .mfc file for every gesture in every file.
# Also supports embedded sequencies. In this case it creates a .mfc file for each sequence and a labels file that keeps track of all labels.

# We need to add handles for unlabeled data as well.

import os
import htkmfc
import pandas as pd

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
out_path_train = "C:\Users\Alex\Documents\University\Python\Data\MFC_data"
out_path_test = "C:\Users\Alex\Documents\University\Python\Data\MFC_test_data"
# Modify this flag to 'Training' or 'Testing'.
flag = 'Testing'
# Modify this flag to 'Isolated' or 'Embedded'.
flag_embed = 'Embedded'
#================================================================ Switch between Training and Testing =========================================
if flag == 'Training':
	out_path = out_path_train
	in_file = "Training_set_skeletal.csv"
	out_file = 'Training_Sequence'
elif flag == 'Testing':
	out_path = out_path_test
	in_file = "Testing_set_skeletal.csv"
	out_file = 'Testing_Sequence'

#============================================== Load data and get rid of some weird labels ====================================================
# Load the data and get the different file ids in a list.
print flag, flag_embed
print "Loading data..."
df = pd.read_csv(in_file)
# May need to change some labels.
df.ix[df['label'] == 'None','label'] = 'sil'
files = df['file'].unique()
#========================================================== Isolated ==========================================================================
# Handled isolated gestures.
if flag_embed == 'Isolated':
	# Alternative isolated gestures.
	# Go through all the data by file id.
	for file_id in files:
		vf = df[df['file'] == file_id]
		# Get all the different gestures in the video file.
		gestures = vf['label'].unique()
		for gest in gestures:
			# Open a .mfc file for each gesture to write the feature vectors.
			file_id = int(file_id)
			label = map_gesture(gest)
			file_name = out_file + str(file_id) + '_' + str(label) + '.mfc'
			out_file_name = os.path.join(out_path,file_name)
			print out_file_name

			# Get the frames that correspond to the specific gesture.
			gf = vf[vf['label'] == gest]

			mfc_writer = htkmfc.open(out_file_name,'w',23)
			# Go through all frames in the specific file id and write the extracted features to mfc format.
			for i in gf.index:
				feats = df.iloc[i]
				gest = feats['label']
				feats = feats[['lh_v','rh_v','le_v','re_v','lh_dist_rp','rh_dist_rp','lh_hip_d','rh_hip_d','le_hip_d','re_hip_d','lh_shc_d','rh_shc_d','le_shc_d','re_shc_d',
								'lh_hip_ang','rh_hip_ang','lh_shc_ang','rh_shc_ang','lh_el_ang','rh_el_ang','lh_dir','rh_dir','hands_d']].as_matrix().astype(float)
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
	for file_id in files:
		vf = df[df['file'] == file_id]
		file_id = int(file_id)
		file_name = 'Embedded' + out_file + str(file_id) + '.mfc'
		out_file_name = os.path.join(out_path,file_name)
		print out_file_name
		# We also need to keep a list of the label sequence.
		label_sequence = []
		mfc_writer = htkmfc.open(out_file_name,'w',23)			
		# Go through all frames in the specific file id and write the extracted features to mfc format.
		for i in vf.index:
			feats = df.iloc[i]
			gest = feats['label']
			label = map_gesture(gest)
			feats = feats[['lh_v','rh_v','le_v','re_v','lh_dist_rp','rh_dist_rp','lh_hip_d','rh_hip_d','le_hip_d','re_hip_d','lh_shc_d','rh_shc_d','le_shc_d','re_shc_d',
							'lh_hip_ang','rh_hip_ang','lh_shc_ang','rh_shc_ang','lh_el_ang','rh_el_ang','lh_dir','rh_dir','hands_d']].as_matrix().astype(float)
			mfc_writer.writevec(feats)
			# Append labels into the sequence list of the file.
			if len(label_sequence) > 0:
				if label_sequence[-1] == label:
					pass
				else:
					label_sequence.append(label)
			else:
				label_sequence.append(label)

		# Close the mfc file.
		mfc_writer.close()
		# Write the label sequence for each file to the label file.
		lab_file.write('%s:%s\n' %(file_name,label_sequence))
	lab_file.close()


print "finished"