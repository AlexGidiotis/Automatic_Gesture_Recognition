# Author: Alex Gidiotis
#		  gidiotisAlex@outlook.com.gr

# This script processes the extracted hand images and performs depth masking in order to subtract the background of the regions
# of interest before extracting the HOG descriptors.
# Inputs the color and depth images of hands and outputs the masked images minus some empty frames which are ignored.
import os
import shutil
import cv2
import numpy as np
import pandas as pd
import re

#=========================================================== MAIN =============================================================
# Modify this to 'Training' or 'Testing'.
flag = 'Training'
print flag
flag_path = 'Dimitris'
#==================================================== Isolated Training =======================================================
# Choose between Training and Testing.
if flag_path == 'Alex':
	if flag == 'Training':
		path = '/home/alex/Documents/Data/Train_Images'
		in_file = "Training_set_skeletal.csv"
	elif flag == 'Testing':
		path = '/home/alex/Documents/Data/Test_Images'
		in_file = "Testing_set_skeletal.csv"
elif flag_path == 'Dimitris':
	if flag == 'Training':
		path = '/home/dimitris/GitProjects/Automatic_Gesture_Recognition/Data/Train_Images'
		in_file = "Training_set_skeletal.csv"
	elif flag == 'Testing':
		path = '/home/dimitris/GitProjects/Automatic_Gesture_Recognition/Data/Test_Images'
		in_file = "Testing_set_skeletal.csv"
# Load some data.
print "Loading data..."
all_df = pd.read_csv(in_file)
# May need to change some labels.
all_df.ix[all_df['label'] == 'None','label'] = 'sil'
all_df = all_df[['frame','label','file']]

# List the files in the directory and open each file.
file_list = sorted(os.listdir(path))
for file in file_list:
	print file
	# Get the file number.
	# 'sample1'
	fileNum = float(re.findall('\D+(\d+)',file)[0])
	# Get the df for the particular file number.
	df = all_df[all_df['file'] == fileNum]
	df = df.reset_index(drop=True)

	# The input files.
	color_file = os.path.join(path,file,'color')
	depth_file = os.path.join(path,file,'depth')
	# The output file.
	masked_file = os.path.join(path,file,'masked')
	# First remove previous output directories.
	try:	
		shutil.rmtree(masked_file)
	except: pass
	# Create the output directory.
	if not os.path.exists(masked_file):
		os.makedirs(masked_file)
		print 'Created',masked_file

	# List the input directories and open color and depth images in pairs.
	color_list = sorted(os.listdir(color_file))
	depth_list = sorted(os.listdir(depth_file))
	for col,dep in zip(color_list,depth_list):
		# Read the two input images.
		c_img = cv2.imread(color_file + '/' + col,cv2.IMREAD_COLOR)
		d_img = cv2.imread(depth_file + '/' + dep,cv2.IMREAD_COLOR)

		# Sometimes throws an exception.
		try:
			# Decide the range of depths we want to filter.
			dmax,dmin = np.max(d_img[d_img<205]), np.min(d_img[d_img>40])
			upper = dmin + 30
			lower = 0

			# Create and preprocess the depth mask we are going to use.
			mask = cv2.inRange(d_img, (lower, lower, lower), (upper, upper, upper))
			kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
			mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel,1)
			mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
			mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel) 

			# Use the depth mask over the color image.
			masked = cv2.bitwise_and(c_img,mask)

			# If the output image is almost empty ignore it.
			if np.sum(masked) < 100000: continue
			
			# Write the output images.
			# Get the frame number.
			# sample1_color_6_right.png
			frame = int(re.findall('color_(\d+)_',col)[0])
			# Get the label and append it to the name.
			frame_series = df[df['frame'] == frame]
			label = frame_series['label'].values[0] 
			outName = col[:-4] + '_' + label + col[-4:]
			cv2.imwrite(masked_file + '/' + outName, masked)
			
		except: continue