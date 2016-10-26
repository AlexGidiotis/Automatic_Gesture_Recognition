import re
import os
import numpy as np
import pandas as pd
import numpy.linalg as la

train_labels_file = "C:\Users\Alex\Documents\University\Python\Automatic_Gesture_Recognition\\training_label_file.csv"
test_labels_file = "C:\Users\Alex\Documents\University\Python\Automatic_Gesture_Recognition\\testing_label_file.csv"
unlabelled_lab_file = "C:\Users\Alex\Documents\University\Python\Automatic_Gesture_Recognition\\label_file.csv"
flag = 'Train'
labeled = 'True'

# ========================================= Loads the skeletal data and labels =================================================================
# Returns: a dataframe with the whole training set frame by frame. (num frames x 27)
def load_data(sk_data_path, labeled):
	# Choose between training and testing mode.
	if flag == 'Train':
		labels_file = train_labels_file
	elif flag == 'Test':
		labels_file = test_labels_file

	# Go find all the saved data.
	sk_list = os.listdir(sk_data_path)
	df = pd.DataFrame()
	# Put all the data in a new dataframe.
	for dfile in sk_list:
		new_df = pd.read_csv(sk_data_path + '/' + dfile)
		df = df.append(new_df, ignore_index=True)
	df = df.drop(df.columns[[0]], axis=1)
	# Choose between labeled and unlabeled mode.
	if labeled == 'True':
		labs = pd.read_csv(labels_file)
		df['label'] = labs
		return df
	elif labeled == 'False':
		labs = pd.read_csv(unlabelled_lab_file)
		df['label'] = labs
		return df

# ================================= Get the previous position of both hands and elbows. ========================================================
# We are going to use this positions to calculate movements and velocities.
# Returns: the original df with the hands and elbows previous positions added.
def get_previous_pos(df):
	# Put the indices into matrices for faster manipulation.
	lh_x,lh_y,rh_x,rh_y = df['lhX'].as_matrix(),df['lhY'].as_matrix(),df['rhX'].as_matrix(),df['rhY'].as_matrix()
	le_x,le_y,re_x,re_y = df['leX'].as_matrix(),df['leY'].as_matrix(),df['reX'].as_matrix(),df['reY'].as_matrix()

	# Create zero-like matrices.
	pr_lh_x,pr_lh_y,pr_rh_x,pr_rh_y = np.zeros_like(lh_x),np.zeros_like(lh_y),np.zeros_like(rh_x),np.zeros_like(rh_y)
	pr_le_x,pr_le_y,pr_re_x,pr_re_y = np.zeros_like(le_x),np.zeros_like(le_y),np.zeros_like(re_x),np.zeros_like(re_y)

	# Get the previous positions.
	pr_lh_x[1:],pr_lh_y[1:],pr_rh_x[1:],pr_rh_y[1:] = lh_x[:-1],lh_y[:-1],rh_x[:-1],rh_y[:-1]
	pr_le_x[1:],pr_le_y[1:],pr_re_x[1:],pr_re_y[1:] = le_x[:-1],le_y[:-1],re_x[:-1],re_y[:-1]

	# Put them in the dataframes.
	df['pre_lhX'],df['pre_lhY'],df['pre_rhX'],df['pre_rhY'] = pr_lh_x,pr_lh_y,pr_rh_x,pr_rh_y
	df['pre_leX'],df['pre_leY'],df['pre_reX'],df['pre_reY'] = pr_le_x,pr_le_y,pr_re_x,pr_re_y

	return df

# ======================================== Calculate and return hand and elbow velocities. =====================================================
def calculate_velocities(df):
	lh_x,lh_y,rh_x,rh_y = df['lhX'].as_matrix(),df['lhY'].as_matrix(),df['rhX'].as_matrix(),df['rhY'].as_matrix()
	le_x,le_y,re_x,re_y = df['leX'].as_matrix(),df['leY'].as_matrix(),df['reX'].as_matrix(),df['reY'].as_matrix()
	
	pr_lh_x,pr_lh_y,pr_rh_x,pr_rh_y = df['pre_lhX'].as_matrix(),df['pre_lhY'].as_matrix(),df['pre_rhX'].as_matrix(),df['pre_rhY'].as_matrix()
	pr_le_x,pr_le_y,pr_re_x,pr_re_y = df['pre_leX'].as_matrix(),df['pre_leY'].as_matrix(),df['pre_reX'].as_matrix(),df['pre_reY'].as_matrix()

	lh_vel,rh_vel = np.zeros_like(lh_x), np.zeros_like(rh_x)
	le_vel,re_vel = np.zeros_like(le_x), np.zeros_like(re_x)

	lh, pre_lh, rh, pre_rh = np.array((lh_x,lh_y)), np.array((pr_lh_x,pr_lh_y)), np.array((rh_x,rh_y)), np.array((pr_rh_x,pr_rh_y))
	le, pre_le, re, pre_re = np.array((le_x,le_y)), np.array((pr_le_x,pr_le_y)), np.array((re_x,re_y)), np.array((pr_re_x,pr_re_y))

	dist_lh, dist_rh = (lh - pre_lh)**2, (rh - pre_rh)**2
	dist_le, dist_re = (le - pre_le)**2, (re - pre_re)**2

	dist_lh, dist_rh = dist_lh.sum(axis=0), dist_rh.sum(axis=0) 
	dist_le, dist_re = dist_le.sum(axis=0), dist_re.sum(axis=0)

	dist_lh, dist_rh = np.sqrt(dist_lh), np.sqrt(dist_rh) 
	dist_le, dist_re = np.sqrt(dist_le), np.sqrt(dist_re)

	lh_vel[5:],rh_vel[5:] = dist_lh[5:], dist_rh[5:]
	le_vel[5:],re_vel[5:] = dist_le[5:], dist_re[5:]

	df['lh_v'], df['rh_v'] = lh_vel, rh_vel	
	df['le_v'], df['re_v'] = le_vel, re_vel
	return df

#============================================================= Main function ====================================================================

sk_training_path = "C:\Users\Alex\Documents\University\Python\Data\CSV_data"
sk_test_path = "C:\Users\Alex\Documents\University\Python\Data\CSV_TEST_data"
out_training_path = "C:\Users\Alex\Documents\University\Python\Data\SK_CSV_feats"
out_test_path = "C:\Users\Alex\Documents\University\Python\Data\SK_CSV_TEST_feats"

#============================================= change this flag to Train or Test to extract ====================================================
# Chose between training and testing mode.
if flag == 'Train':
	sk_data_path = sk_training_path
	out_path = out_training_path
elif flag == 'Test':
	sk_data_path = sk_test_path
	out_path = out_test_path

print "Loading data..."
df = load_data(sk_data_path, labeled) 
print "Finished loading."
df = get_previous_pos(df)
print "Calculating velocities..."
df = calculate_velocities(df)
print df






