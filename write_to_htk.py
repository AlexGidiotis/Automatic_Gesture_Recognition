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
	if gest == 'sil': return '0_0'
	if gest == 'basta_1': return '1_1'
	if gest == 'basta_2': return '1_2'
	if gest == 'basta_3': return '1_3'		
	if gest == 'buonissimo_1' : return '2_1'
	if gest == 'buonissimo_2' : return '2_2'
	if gest == 'buonissimo_3' : return '2_3'		
	if gest == 'cheduepalle_1' : return '3_1'
	if gest == 'cheduepalle_2' : return '3_2'
	if gest == 'cheduepalle_3' : return '3_3'		
	if gest == 'chevuoi_1' : return '4_1'
	if gest == 'chevuoi_2' : return '4_2'
	if gest == 'chevuoi_3' : return '4_3'		
	if gest == 'combinato_1' : return '5_1'
	if gest == 'combinato_2' : return '5_2'
	if gest == 'combinato_3' : return '5_3'		
	if gest == 'cosatifarei_1' : return '6_1'
	if gest == 'cosatifarei_2' : return '6_2'
	if gest == 'cosatifarei_3' : return '6_3'		
	if gest == 'daccordo_1' : return '7_1'
	if gest == 'daccordo_2' : return '7_2'
	if gest == 'daccordo_3' : return '7_3'		
	if gest == 'fame_1' : return '8_1'
	if gest == 'fame_2' : return '8_2'
	if gest == 'fame_3' : return '8_3'		
	if gest == 'freganiente_1' : return '9_1'
	if gest == 'freganiente_2' : return '9_2'
	if gest == 'freganiente_3' : return '9_3'		
	if gest == 'furbo_1' : return '10_1'
	if gest == 'furbo_2' : return '10_2'
	if gest == 'furbo_3' : return '10_3'		
	if gest == 'messidaccordo_1' : return '11_1'
	if gest == 'messidaccordo_2' : return '11_2'
	if gest == 'messidaccordo_3' : return '11_3'		
	if gest == 'ok_1' : return '12_1'
	if gest == 'ok_2' : return '12_2'
	if gest == 'ok_3' : return '12_3'		
	if gest == 'perfetto_1': return '13_1'
	if gest == 'perfetto_2': return '13_2'
	if gest == 'perfetto_3': return '13_3'		
	if gest == 'prendere_1': return '14_1'
	if gest == 'prendere_2': return '14_2'
	if gest == 'prendere_3': return '14_3'		
	if gest == 'seipazzo_1': return '15_1'
	if gest == 'seipazzo_2': return '15_2'
	if gest == 'seipazzo_3': return '15_3'		
	if gest == 'tantotempo_1': return '16_1'
	if gest == 'tantotempo_2': return '16_2'
	if gest == 'tantotempo_3': return '16_3'		
	if gest == 'sonostufo_1': return '17_1'
	if gest == 'sonostufo_2': return '17_2'
	if gest == 'sonostufo_3': return '17_3'		
	if gest == 'vattene_1': return '18_1'
	if gest == 'vattene_2': return '18_2'
	if gest == 'vattene_3': return '18_3'		
	if gest == 'vieniqui_1': return '19_1'
	if gest == 'vieniqui_2': return '19_2'
	if gest == 'vieniqui_3': return '19_3'		
	if gest == 'noncenepiu_1': return '20_1'
	if gest == 'noncenepiu_2': return '20_2'
	if gest == 'noncenepiu_3': return '20_3'		

#================================================================= MAIN =======================================================================

# Change this path to the saved skeletal .csv file.
flag_path = 'Alex'

if flag_path == 'Alex':
	#Alex's Paths
	out_path_train = "/home/alex/Documents/Data/MFC_data"
	out_path_test = "/home/alex/Documents/Data/MFC_test_data"
elif flag_path == "Dimitris":
	#Dimitri's Paths
	out_path_train = "/home/dimitris/GitProjects/Automatic_Gesture_Recognition/Data/MFC_data"
	out_path_test = "/home/dimitris/GitProjects/Automatic_Gesture_Recognition/Data/MFC_test_data"

# Modify this flag to 'Training' or 'Testing'.
flag = 'Testing'
# Modify this flag to 'Isolated' or 'Embedded'.
flag_embed = 'Embedded'

lab_flag = 'Unlabelled'
#================================================================ Switch between Training and Testing =========================================
if flag == 'Training':
	out_path = out_path_train
	if flag_path == 'Alex':
		in_file = "/home/alex/Documents/git_projects/Automatic_Gesture_Recognition/Training_set_skeletal_extended.csv"
	elif flag_path == 'Dimitris':
		in_file = '/home/dimitris/GitProjects/Automatic_Gesture_Recognition/Training_set_skeletal_extended.csv'
	out_file = 'Training_Sequence'
elif flag == 'Testing':
	out_path = out_path_test
	if flag_path == 'Alex':
		in_file = "/home/alex/Documents/git_projects/Automatic_Gesture_Recognition/Testing_set_skeletal_extended.csv"
	elif flag_path == 'Dimitris':
		in_file = '/home/dimitris/GitProjects/Automatic_Gesture_Recognition/Testing_set_skeletal_extended.csv'
	out_file = 'Testing_Sequence'
#============================================== Load data and get rid of some weird labels ====================================================
# Load the data and get the different file ids in a list.
print flag, flag_embed, lab_flag
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
		mfc_writer = htkmfc.open(out_file_name,'w',22)			
		# Go through all frames in the specific file id and write the extracted features to mfc format.
		for i in vf.index:
			feats = df.iloc[i]
			gest = feats['label']
			
			feats = feats[['lh_v','rh_v','le_v','re_v','lh_dist_rp','rh_dist_rp','lh_hip_d','rh_hip_d','le_hip_d','re_hip_d','lh_shc_d','rh_shc_d','le_shc_d','re_shc_d',
							'lh_hip_ang','rh_hip_ang','lh_shc_ang','rh_shc_ang','lh_el_ang','rh_el_ang','lh_dir','rh_dir']].as_matrix().astype(float)
			mfc_writer.writevec(feats)
			if lab_flag == 'Labelled':
				label = map_gesture(gest)
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