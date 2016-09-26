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


###################### Main function #############################################################

sk_data_path = "C:\Users\Alex\Documents\University\Python\Data\SKData_txt"

sk_data_list = os.listdir(sk_data_path)

file_count = 0
print "Loading data..."
for data_file in sk_data_list:
	file_count += 1
	print data_file
	df = import_data(sk_data_path, data_file)
	print "Finished loading data."
	print "Calculating hand velocities..."
	df = calculate_hand_velocities(df)
	print "Estimating rest position..."
	df, rest_position = estimate_rest_position(df)	
	print rest_position


	############################ to be continued #############################


	print "Calculating hand distances from rp"
	df = calc_distance_from_rp(df)
	break


		




