# Author: Alex Gidiotis
#		  gidiotisAlex@outlook.com.gr

# This script reads extracted features and writes them to htk mfc format.
# Outputs one .mfc file for every gesture in every file.

# We need to add handles for testing and unlabeled data as well.

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

# Change this path to the saved skeletal .csv file.
out_path = "C:\Users\Alex\Documents\University\Python\Data\MFC_data"

# Load the data and get the different file ids in a list.
print "Loading data..."
df = pd.read_csv("Training_set_skeletal.csv")
files = df['file'].unique()

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
		file_name = 'Training_Sequence' + str(file_id) + '_' + str(label) + '.mfc'
		out_file_name = os.path.join(out_path,file_name)
		print out_file_name

		# Get the frames that correspond to the specific gesture.
		gf = vf[vf['label'] == gest]

		mfc_writer = htkmfc.open(out_file_name,'w',22)
		# Go through all frames in the specific file id and write the extracted features to mfc format.
		for i in gf.index:
			feats = df.iloc[i]
			gest = feats['label']
			feats = feats[['lh_v','rh_v','le_v','re_v','lh_dist_rp','rh_dist_rp','lh_hip_d','rh_hip_d','le_hip_d','re_hip_d','lh_shc_d','rh_shc_d','le_shc_d','re_shc_d',
							'lh_hip_ang','rh_hip_ang','lh_shc_ang','rh_shc_ang','lh_el_ang','rh_el_ang','lh_dir','rh_dir']].as_matrix().astype(float)
			mfc_writer.writevec(feats)

		# Close the mfc file.
		mfc_writer.close()

print "finished"