# Author: Alex Gidiotis
# 		  gidiotisAlex@outlook.com.gr

# This scripts reads the depth and color video files as well as the previously extracted skeletal features. Then it finds and
# segments the images of both hands for both streams.
# Outputs directories with the segmented hand images. 

import pandas as pd
import os
import cv2
import numpy as np
import re

#============================================ Calculate the rectangle edge points. ============================================
# Calculates the edge points we are going to use to draw a rectangle around each hand.
# Args: a dataframe with the skeletal data of hands and a constant with the half the side size of the rectangle we will draw.
# Returns the original df with the points columns added.
def calculate_rect_points(all_df,const):
	# Initialize the arrays to store the results.
	lpt1x = np.zeros((all_df.shape[0]), dtype=int)
	lpt1y = np.zeros((all_df.shape[0]), dtype=int)
	lpt2x = np.zeros((all_df.shape[0]), dtype=int)
	lpt2y = np.zeros((all_df.shape[0]), dtype=int)
	rpt1x = np.zeros((all_df.shape[0]), dtype=int)
	rpt1y = np.zeros((all_df.shape[0]), dtype=int)
	rpt2x = np.zeros((all_df.shape[0]), dtype=int)
	rpt2y = np.zeros((all_df.shape[0]), dtype=int)
	# Initialize some temporary arrays.
	lpt1x_temp = np.zeros((all_df.shape[0]), dtype=int)
	lpt1y_temp = np.zeros((all_df.shape[0]), dtype=int)
	lpt2x_temp = np.zeros((all_df.shape[0]), dtype=int)
	lpt2y_temp = np.zeros((all_df.shape[0]), dtype=int)
	rpt1x_temp = np.zeros((all_df.shape[0]), dtype=int)
	rpt1y_temp = np.zeros((all_df.shape[0]), dtype=int)
	rpt2x_temp = np.zeros((all_df.shape[0]), dtype=int)
	rpt2y_temp = np.zeros((all_df.shape[0]), dtype=int)

	# Convert to matrix for faster computation.
	hands = all_df[['lhX','lhY','rhX','rhY',]].as_matrix()

	# Find the left hand points.
	lpt1x_temp,lpt1y_temp = (hands[:,0] - const),(hands[:,1] - const)
	lpt2x_temp,lpt2y_temp = (hands[:,0] + const),(hands[:,1] + const)
	# Find the right hand points.
	rpt1x_temp,rpt1y_temp = (hands[:,2] - const),(hands[:,3] - const)
	rpt2x_temp,rpt2y_temp = (hands[:,2] + const),(hands[:,3] + const)

	# Save the points back to the dataframe.
	lpt1x[3:],lpt1y[3:] = lpt1x_temp[3:],lpt1y_temp[3:] 
	lpt2x[3:],lpt2y[3:] = lpt2x_temp[3:],lpt2y_temp[3:] 
	rpt1x[3:],rpt1y[3:] = rpt1x_temp[3:],rpt1y_temp[3:] 
	rpt2x[3:],rpt2y[3:] = rpt2x_temp[3:],rpt2y_temp[3:] 

	all_df['lpt1X'], all_df['lpt1Y'], all_df['lpt2X'], all_df['lpt2Y'], all_df['rpt1X'], all_df['rpt1Y'], all_df['rpt2X'], all_df['rpt2Y'] = lpt1x, lpt1y, lpt2x, lpt2y, rpt1x, rpt1y, rpt2x, rpt2y
	return all_df


#=========================================================== MAIN =============================================================
# Modify this to 'Training' or 'Testing'.
flag = 'Training'
print flag
# This constant will be half the side of the bounding rectangle we will draw around each hand.
const = 20

flag_path = 'Dimitris'
#==================================================== Isolated Training =======================================================
# Choose between Training and Testing.
if flag_path == 'Alex':
	if flag == 'Training':
		color_path = '/home/alex/Documents/Data/Color_vid'
		depth_path = '/home/alex/Documents/Data/Depth_vid'
		out_path = '/home/alex/Documents/Data/Train_Images'
		in_file = "Training_set_skeletal.csv"
	elif flag == 'Testing':
		color_path = '/home/alex/Documents/Data/Test_Color_vid'
		depth_path = '/home/alex/Documents/Data/Test_Depth_vid'
		out_path = '/home/alex/Documents/Data/Test_Images'
		in_file = "Testing_set_skeletal.csv"
elif flag_path == 'Dimitris':
	if flag == 'Training':
		color_path = '/home/dimitris/GitProjects/Automatic_Gesture_Recognition/Data/Color_vid'
		depth_path = '/home/dimitris/GitProjects/Automatic_Gesture_Recognition/Data/Depth_vid'
		out_path = '/home/dimitris/GitProjects/Automatic_Gesture_Recognition/Data/Train_Images'
		in_file = "Training_set_skeletal.csv"
	elif flag == 'Testing':
		color_path = '/home/dimitris/GitProjects/Automatic_Gesture_Recognition/Data/Test_Color_vid'
		depth_path = '/home/dimitris/GitProjects/Automatic_Gesture_Recognition/Data/Test_Depth_vid'
		out_path = '/home/dimitris/GitProjects/Automatic_Gesture_Recognition/Data/Test_Images'
		in_file = "Testing_set_skeletal.csv"

print "Loading data..."
all_df = pd.read_csv(in_file)
# May need to change some labels.
all_df.ix[all_df['label'] == 'None','label'] = 'sil'
all_df = all_df[['frame','lwX','lwY','lhX','lhY','rwX','rwY','rhX','rhY','label','file']]
all_df = calculate_rect_points(all_df,const)

# List the directories with the input videos.
listing_color = sorted(os.listdir(color_path))
listing_depth = sorted(os.listdir(depth_path))

# Go through all color and depth videos.
for vid,dep in zip(listing_color,listing_depth):
	file = float(re.findall('\D+(\d+)_color',vid)[0])
	df = all_df[all_df['file'] == file]
	df = df.reset_index(drop=True)

	# Create the directories to put images in.
	fileName_color = 'sample' + str(int(file)) + '/color'
	fileName_depth = 'sample' + str(int(file)) + '/depth'
	fileName = 'sample' + str(int(file))
	if not os.path.exists(out_path + '/' + fileName_color): 
		os.makedirs(out_path + '/' + fileName_color)
		print "Created folder " + fileName_color
	if not os.path.exists(out_path + '/' + fileName_depth): 
		os.makedirs(out_path + '/' + fileName_depth)
		print "Created folder " + fileName_depth

#======================================================== Color Images ==========================================================
	cap = cv2.VideoCapture(color_path + '/' + vid)

	frame = 0
	while cap.isOpened():
		ret, img = cap.read()
		if not ret: break
		frame += 1 
		# Skip the empty frames.
		if frame < 4: continue

		# Create image masks.
		roi_maskl = np.zeros(img.shape,np.uint8)
		roi_maskr = np.zeros(img.shape,np.uint8)      
		
		# Get the points to draw a rectangle around each hand.
		points_col = df[['lpt1X','lpt1Y','lpt2X','lpt2Y','rpt1X','rpt1Y','rpt2X','rpt2Y']].as_matrix()

		lpt1x, lpt1y = points_col[frame-1,0], points_col[frame-1,1]
		lpt1 = lpt1x, lpt1y
		lpt2x, lpt2y = points_col[frame-1,2], points_col[frame-1,3]
		lpt2 = lpt2x, lpt2y
		rpt1x, rpt1y = points_col[frame-1,4], points_col[frame-1,5]
		rpt1 = rpt1x, rpt1y 
		rpt2x, rpt2y = points_col[frame-1,6], points_col[frame-1,7]
		rpt2 = rpt2x, rpt2y

		# Find the two points to draw the rectangle around the left hand.
		cv2.rectangle(roi_maskl,lpt1,lpt2,(255,255,255),-1)

		# Find the two points to draw the rectangle around the right hand.
		cv2.rectangle(roi_maskr,rpt1,rpt2,(255,255,255),-1)

		# Mask the frame to get the images.
		maskedl = cv2.bitwise_and(img,roi_maskl)
		image_l = maskedl[lpt1y:lpt2y,lpt1x:lpt2x]
		maskedr = cv2.bitwise_and(img,roi_maskr)
		image_r = maskedr[rpt1y:rpt2y,rpt1x:rpt2x]
		
		# Save the masked images.
		try:
			outNameLeft = "%s_color_%d_left.png" %(fileName,frame)
			outNameRight = "%s_color_%d_right.png" %(fileName,frame)
			cv2.imwrite(out_path +'/'+ fileName_color + '/' + outNameLeft, image_l) 
			cv2.imwrite(out_path +'/'+ fileName_color + '/' + outNameRight, image_r)
		except: pass

		k = cv2.waitKey(10)
		if k == 27:
			break

#======================================================= Depth Images ========================================================		
	depcap = cv2.VideoCapture(depth_path + '/' + dep)

	frame = 0
	while depcap.isOpened():
		ret, img = depcap.read()
		if not ret: break
		frame += 1
		# Skip the empty frames.
		if frame < 4: continue  

		# Create image masks.
		roi_maskl = np.zeros(img.shape,np.uint8)
		roi_maskr = np.zeros(img.shape,np.uint8) 

		# Get the points to draw a rectangle around each hand.
		points_dep = df[['lpt1X','lpt1Y','lpt2X','lpt2Y','rpt1X','rpt1Y','rpt2X','rpt2Y']].as_matrix()

		lpt1x, lpt1y = points_dep[frame-1,0], points_dep[frame-1,1]
		lpt1 = lpt1x, lpt1y
		lpt2x, lpt2y = points_dep[frame-1,2], points_dep[frame-1,3]
		lpt2 = lpt2x, lpt2y
		rpt1x, rpt1y = points_dep[frame-1,4], points_dep[frame-1,5]
		rpt1 = rpt1x, rpt1y 
		rpt2x, rpt2y = points_dep[frame-1,6], points_dep[frame-1,7]
		rpt2 = rpt2x, rpt2y     
		
		# Find the two points to draw the rectangle around the left hand.
		cv2.rectangle(roi_maskl,lpt1,lpt2,(255,255,255),-1)

		# Find the two points to draw the rectangle around the right hand.
		cv2.rectangle(roi_maskr,rpt1,rpt2,(255,255,255),-1)

		# Mask the frame to get the images.
		maskedl = cv2.bitwise_and(img,roi_maskl)
		image_l = maskedl[lpt1y:lpt2y,lpt1x:lpt2x]
		maskedr = cv2.bitwise_and(img,roi_maskr)
		image_r = maskedr[rpt1y:rpt2y,rpt1x:rpt2x]
		
		# Save the masked images.
		try:
			outNameLeft = "%s_depth_%d_left.png" %(fileName,frame)
			outNameRight = "%s_depth_%d_right.png" %(fileName,frame)
			cv2.imwrite(out_path +'/'+ fileName_depth + '/' + outNameLeft, image_l)
			cv2.imwrite(out_path +'/'+ fileName_depth + '/' + outNameRight, image_r)
		except: pass

		k = cv2.waitKey(10)
		if k == 27:
			break


