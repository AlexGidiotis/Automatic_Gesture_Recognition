# -> Get embedded sequencies of gestures and extract features to perform activity/inactivity detection
# Features are hand velocities and distance from rest position
# The inactive segments are going to be classified "sil" using the activity/inactivity detector(neural)
# -> Get class labels
# -> Output files with embedded sequencies relabelled with 21 classes now (including "sil")

import pandas as pd
import numpy as np
import os
import re

from velocity import calculate_hand_velocities
from load_skeleton import import_data
from r_position import estimate_rest_position, calc_distance_from_rp

#Define which path 
flag_path = 'Dimitris'

###################### Main function #############################################################
if flag_path == 'Alex':
	sk_training_path = "C:\Users\Alex\Documents\University\Python\Data\SKData_txt"
	sk_test_path = "C:\Users\Alex\Documents\University\Python\Data\Test_SKData_txt"
	out_training_path = "C:\Users\Alex\Documents\University\Python\Data\CSV_data"
	out_test_path = "C:\Users\Alex\Documents\University\Python\Data\CSV_TEST_data"
elif flag_path == 'Dimitris':
	sk_training_path = "/media/dimitris/TOSHIBA EXT/Chalearn_GestureReco/SKData_txt"
	sk_test_path = "/media/dimitris/TOSHIBA EXT/Chalearn_GestureReco/Test_SKData_txt"
	out_training_path = "/media/dimitris/TOSHIBA EXT/Chalearn_GestureReco/CSV_data"
	out_test_path = "/media/dimitris/TOSHIBA EXT/Chalearn_GestureReco/CSV_TEST_data"

############################ change this flag to Train or Test to extract ########################
flag = 'Train'
if flag == 'Train':
	sk_data_path = sk_training_path
	out_path = out_training_path
elif flag == 'Test':
	sk_data_path = sk_test_path
	out_path = out_test_path

sk_data_list = sorted(os.listdir(sk_data_path))

file_count = 0
print "Loading data..."
for data_file in sk_data_list:
	file_count += 1
	#load a batch of 100 files
	#if file_count > 100 : break
	print data_file
	# sometimes an error is caused here so we want to discard the example
	try:
		df = import_data(sk_data_path, data_file)
	except:
		continue
	print "Finished loading data."
	print "Calculating hand velocities..."
	df = calculate_hand_velocities(df)
	print "Estimating rest position..."
	# another error here
	try:
		df, rest_position = estimate_rest_position(df)	
	except:
		continue
	print rest_position
	print "Calculating hand distances from rp..."
	df = calc_distance_from_rp(df,rest_position)
	if not os.path.exists(out_path):
		os.makedirs(out_path)
	print "Writing output to csv..."
	df.to_csv(out_path + '/' + data_file[:-4] + '.csv')



		




