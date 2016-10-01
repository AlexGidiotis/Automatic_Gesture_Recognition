# loads and test the trained model on a series of test videos.

import numpy as np
import pandas as pd
import os
import theano
import time
import pickle
from theano import tensor as T
from activity_detector_dnn import floatX, init_weights, softmax, RMSprop, dropout, model, rectify

# loads the data from csv files and labels frames as active or inactive
# arg: data_path: the path where the csv files are stored
# returns: df: a dataframe with the loaded data and the 'inactive' column added
def load_data(data_path):
	data_listing = os.listdir(data_path)
	df = pd.DataFrame()
	# go through all files and load all data in a big dataframe
	for dfile in data_listing:
		new_df = pd.read_csv(data_path + '/' + dfile)
		df = df.append(new_df)

	return df

# keep only the features we need for activity detection	
def split_to_sets(df):
	df = df[['lh_v', 'rh_v', 'lh_dist_rp', 'rh_dist_rp','lhX', 'lhY', 'rhX', 'rhY']]
	test_s = df
	return test_s.as_matrix()

############################## main ######################################

data_path = "C:\Users\Alex\Documents\University\Python\Data\CSV_TEST_data"

print "Loading test set..."
df = load_data(data_path)
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

print "Testing..."

# compile to python function
predict = theano.function(inputs=[X], outputs=y_x, allow_input_downcast=True)


# write predictions to a file
of = open("test_predictions.txt", 'w')
predictions = predict(teX)

# average every 3 frames for smoothing
for i in range(0,(len(predictions)-2)):
	batch = np.array([predictions[i], predictions[(i+1)], predictions[(i+2)]])
	predictions[i] = np.median(batch)

for pr in predictions:
	of.write("%s\n" %pr)
of.close()

