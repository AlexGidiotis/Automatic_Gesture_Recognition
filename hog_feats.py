# Author: Gidiotis Alex
#		  gidiotisAlex@outlook.com.gr

# This script extracts the HOG descriptors from the masked hand images.
# We extract a 576-dim HOG descriptor from the dominant hand of each frame.
# The output is saved in gesture files (.csv)

# NEEDS TO BE MODIFIED FOR EMBEDDED SEQUENCES.

import cv2
import os
import re
import numpy as np
import pandas as pd

#========================================== Find the dominant hand in each gesture ============================================
# Uses the average velocity of each hand to decide which is the dominant hand that performs each gesture.
def get_dominant_hand(gest_df):
	vel_left = gest_df['lh_v'].as_matrix()
	vel_right = gest_df['rh_v'].as_matrix()
	# Return the hand with the bigest average velocity.
	if vel_left.mean() > vel_right.mean():
		return 'left'
	else:
		return 'right'

#============================================== Extract HOG descriptor ========================================================
# Arg: a 40 x 40 image of the dominant hand.
# Returns: a flattened vector with the HOG descriptor extracted.
def HOG(img):
	# This parameters are pretty standard for that kind of vision problem.
    cell_size = (8, 8)  # h x w in pixels
    block_size = (4, 4)  # h x w in cells
    nbins = 9

    # create the descriptor.
    hog = cv2.HOGDescriptor(_winSize=(img.shape[1] // cell_size[1] * cell_size[1],
                                  img.shape[0] // cell_size[0] * cell_size[0]),
                        _blockSize=(block_size[1] * cell_size[1],
                                    block_size[0] * cell_size[0]),
                        _blockStride=(cell_size[1], cell_size[0]),
                        _cellSize=(cell_size[1], cell_size[0]),
                        _nbins=nbins)
    
    # Parameterize.
    n_cells = (img.shape[0] // cell_size[0], img.shape[1] // cell_size[1])
    
    # Extract the HOG features.
    hog_feats = hog.compute(img)\
               .reshape(n_cells[1] - block_size[1] + 1,
                        n_cells[0] - block_size[0] + 1,
                        block_size[0], block_size[1], nbins) \
               .transpose((1, 0, 2, 3, 4)) 

    return hog_feats.flatten()

#=========================================================== MAIN =============================================================
# Modify this to 'Training' or 'Testing'.
flag = 'Training'
flag_path = 'Dimitris'
print flag

#==================================================== Isolated Training =======================================================
if flag_path == 'Alex':	
	# Choose between Training and Testing.
	if flag == 'Training':
		path = '/home/alex/Documents/Data/Train_Images'
		in_file = "Training_set_skeletal.csv"
		out_path = '/home/alex/Documents/Data/Train_hog_feats'
	elif flag == 'Testing':
		path = '/home/alex/Documents/Data/Test_Images'
		in_file = "Testing_set_skeletal.csv"
		out_path = '/home/alex/Documents/Data/Test_hog_feats'
elif flag_path == 'Dimitris':
	# Choose between Training and Testing.
	if flag == 'Training':
		path = '/home/dimitris/GitProjects/Automatic_Gesture_Recognition/Data/Train_Images'
		in_file = "Training_set_skeletal.csv"
		out_path = '/home/dimitris/GitProjects/Automatic_Gesture_Recognition/Data/Train_hog_feats'
	elif flag == 'Testing':
		path = '/home/dimitris/GitProjects/Automatic_Gesture_Recognition/Data/Test_Images'
		in_file = "Testing_set_skeletal.csv"
		out_path = '/home/dimitris/GitProjects/Automatic_Gesture_Recognition/Data/Test_hog_feats'

print "Loading data..."
all_df = pd.read_csv(in_file)

# May need to change some labels.
all_df.ix[all_df['label'] == 'None','label'] = 'sil'
all_df = all_df[['frame','lh_v','rh_v','label','file']]

#=============================================== Iterate through files ===========================================================
file_list = sorted(os.listdir(path))
for file in file_list:
	# Get the file number.
	# 'sample1'
	fileNum = float(re.findall('\D+(\d+)',file)[0])

	# Get the df for the particular file number.
	df = all_df[all_df['file'] == fileNum]
	df = df.reset_index(drop=True)

	# Find and list the input directory.
	masked_file = os.path.join(path,file,'masked')
	im_list = sorted(os.listdir(masked_file))

	# Find all gesture that occur in the file.
	gestures = df['label'].unique()

#=============================================== Read frames in a file ===================================================================
	
	# Iterate through all gestures in the file.
	for gest in gestures:
		gest_df = df[df['label'] == gest]
		# Find the dominant hand in each gesture.
		dominant_hand = get_dominant_hand(gest_df)
		# A list to store all descriptors for a gesture.
		hogs = np.zeros((1,576))
		frames = []
		labels = []
		files = []
		hands = []

		# Go through images in directory.
		for image in im_list:
			# Get the frame number.
			# sample1_color_6_right
			frame = int(re.findall('color_(\d+)_',image)[0])
			# Get 'left' or 'right'.
			hand = re.findall('color_\d+_(\D+)_\D+.png$',image)[0]
			# Get label.
			label = re.findall('color_\d+_\D+_(\D+).png$',image)[0]
			if label == gest:
				# Use only the dominant hand for features.
				if hand == dominant_hand:
					img = cv2.imread(masked_file + '/' + image ,cv2.IMREAD_COLOR)
					# Flip leaft hands for invariance.
					if hand == 'left':
						img=cv2.flip(img,1)
#================================================== Extract descriptor ========================================================
					# Convert to grayscale.
					img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
					# Extract HOG descriptor.
					hog = HOG(img)
					# Stack the HOG descriptors.
					hog = hog.reshape((1,len(hog)))
					hogs = np.vstack((hogs,hog))
					# Save some metadata.
					frames.append(frame)
					labels.append(label)
					files.append(fileNum)
					hands.append(hand)

#===================================================== Output =================================================================
		# Create a dataframe with the hog descriptors for each gesture.
		hog_df = pd.DataFrame(hogs[1:,:])
		# Add some useful metadata.
		hog_df['frame'] = frames
		hog_df['label'] = labels
		hog_df['file'] = files
		hog_df['hand'] = hands
		# Sort by frame.
		hog_df = hog_df.sort_values('frame').reset_index(drop=True)
		# Write output to .csv
		out_name = 'sample' + str(int(fileNum)) + '_hog_' + gest + '.csv'
		out_file = os.path.join(out_path,out_name)
		hog_df.to_csv(out_file,index=False)
	print 'Finished',file
