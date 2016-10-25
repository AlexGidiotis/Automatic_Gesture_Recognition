import re
import os
import numpy as np
import pandas as pd

train_labels_file = "C:\Users\Alex\Documents\University\Python\Automatic_Gesture_Recognition\\training_label_file.csv"
test_labels_file = "C:\Users\Alex\Documents\University\Python\Automatic_Gesture_Recognition\\testing_label_file.csv"
unlabelled_lab_file = "C:\Users\Alex\Documents\University\Python\Automatic_Gesture_Recognition\\label_file.csv"
flag = 'Train'
labeled = 'True'

# ========================================= Loads the skeletal data and labels =================================================================
# Returns a dataframe with the whole training set frame by frame. (num frames x 27)
def load_data(sk_data_path, labeled):
	if flag == 'Train':
		labels_file = train_labels_file
	elif flag == 'Test':
		labels_file = test_labels_file

	sk_list = os.listdir(sk_data_path)
	df = pd.DataFrame()
	for dfile in sk_list:
		new_df = pd.read_csv(sk_data_path + '/' + dfile)
		df = df.append(new_df, ignore_index=True)
	df = df.drop(df.columns[[0]], axis=1)
	if labeled == 'True':
		labs = pd.read_csv(labels_file)
		df['label'] = labs
		return df
	elif labeled == 'False':
		labs = pd.read_csv(unlabelled_lab_file)
		df['label'] = labs
		return df

#============================================================= Main function ====================================================================

sk_training_path = "C:\Users\Alex\Documents\University\Python\Data\CSV_data"
sk_test_path = "C:\Users\Alex\Documents\University\Python\Data\CSV_TEST_data"
out_training_path = "C:\Users\Alex\Documents\University\Python\Data\SK_CSV_feats"
out_test_path = "C:\Users\Alex\Documents\University\Python\Data\SK_CSV_TEST_feats"

#============================================= change this flag to Train or Test to extract ====================================================
if flag == 'Train':
	sk_data_path = sk_training_path
	out_path = out_training_path
elif flag == 'Test':
	sk_data_path = sk_test_path
	out_path = out_test_path

print "Loading data..."
df = load_data(sk_data_path, labeled)
print df 





