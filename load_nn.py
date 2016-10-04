# loads and test the trained model on a series of test videos.
# outputs a label file(.csv) for all frames in the training or test set"

import numpy as np
import pandas as pd
import os
import re
import theano
import time
import pickle
from theano import tensor as T
from activity_detector_dnn import floatX, init_weights, softmax, RMSprop, dropout, model, rectify

# loads the data from csv files and labels frames as active or inactive
# arg: data_path: the path where the csv files are stored
#	   labels_path: the path where the label files are stored
#	   labeled: True if data are labeled False if not
# returns: df: a dataframe with the loaded data and the 'inactive' column added as well as the labels
def load_data(data_path,labels_path,labeled):
	data_listing = os.listdir(data_path)
	df = pd.DataFrame()
	# if data are labeled load the labels as well
	if labeled == 'True':
		labels_listing = os.listdir(labels_path)		
		# go through all files and load all data and labels in a big dataframe
		for dfile, lfile in zip(data_listing, labels_listing):
			new_df = pd.read_csv(data_path + '/' + dfile)
			# initialize label column to 'None'
			labels = ['None' for i in range(len(new_df.index))]
			lf = open(labels_path + '/' + lfile, 'r')
			# extract labels as well as starting and ending frames
			for line in lf:
				begin_frame = int(re.findall('Begin: (\d+) ',line)[0])
				end_frame = int(re.findall('End: (\d+)',line)[0])
				lab = re.findall('(^\S+) ',line)[0]
				for i in range(begin_frame, end_frame):
					labels[(i)] = lab
			lf.close()
			# append the 'labels' column
			new_df["labels"] = labels

			# append the file dataframe to the big dataframe				
			df = df.append(new_df)
	elif labeled == 'False':
		for dfile in data_listing:
			new_df = pd.read_csv(data_path + '/' + dfile)
			# append the file dataframe to the big dataframe				
			df = df.append(new_df)
	return df

# keep only the features we need for activity detection	
def split_to_sets(df):
	df = df[['lh_v', 'rh_v', 'lh_dist_rp', 'rh_dist_rp','lhX', 'lhY', 'rhX', 'rhY']]
	test_s = df
	return test_s.as_matrix()

############################## main ######################################
# modify this flag for Training or Testing
flag = 'Testing'
labeled = 'False'
training_path = "C:\Users\Alex\Documents\University\Python\Data\CSV_data"
test_path = "C:\Users\Alex\Documents\University\Python\Data\CSV_TEST_data"
training_labels = "C:\Users\Alex\Documents\University\Python\Data\Labels"
test_labels = "C:\Users\Alex\Documents\University\Python\Data\Test_Labels"

if flag == 'Training':
	data_path = training_path
	labels_path = training_labels
elif flag == 'Testing':
	data_path = test_path
	labels_path = test_labels

print "Loading data set..."
df = load_data(data_path,labels_path,labeled)
teX = split_to_sets(df)
print "Test set loaded."
print teX.shape

print "Loading trained model..."
pkl_file = open('saved_activity_detector.pkl', 'rb')
loaded_nn = pickle.load(pkl_file)

# symbolic variables matrices initialization
X = T.fmatrix()
Y = T.fmatrix()

# load between layers weight vectors
w_h = theano.shared(value=loaded_nn[0], name='w_h', borrow=True)
w_h2 = theano.shared(value=loaded_nn[1], name='w_h2', borrow=True)
w_o = theano.shared(value=loaded_nn[2], name='w_o', borrow=True)

# create a prediction model
h, h2, py_x = model(X, w_h, w_h2, w_o, 0., 0.)

# maxima prediction
y_x = T.argmax(py_x, axis=1)

print "Classifying..."

# compile to python function
predict = theano.function(inputs=[X], outputs=y_x, allow_input_downcast=True)

predictions = predict(teX)

# average every 3 frames for smoothing
for i in range(0,(len(predictions)-2)):
	batch = np.array([predictions[i], predictions[(i+1)], predictions[(i+2)]])
	predictions[i] = np.median(batch)
if labeled == 'True':
	labs = df["labels"].as_matrix()
	# if prediction is 0 we  re-label "sil"
	# if prediction is 1 we keep the original label
	for i in range(0,len(labs)):	
		if predictions[i] == 0:
			 labs[i] = "sil"

	print "Writing output..."
	# writing output to csv
	np.savetxt("training_label_file.csv", labs, fmt='%s', delimiter=',')
	# if prediction is 0 we  re-label "sil"
	# if prediction is 1 we label 'action'
elif labeled == 'False':
	labs = ['action' for i in range(len(predictions))]
	for i in range(0,len(labs)):	
		if predictions[i] == 0:
			labs[i] = "sil"
	print "Writing output..."
	# writing output to csv
	np.savetxt("label_file.csv", labs, fmt='%s', delimiter=',')





