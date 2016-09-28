import numpy as np
import pandas as pd
import os
import theano
from theano import tensor as T
from activity_detector_dnn import floatX, init_weights, rectify, softmax, RMSprop, dropout, model

# loads the data from csv files and labels frames as active or inactive
# arg: data_path: the path where the csv files are stored
# returns: df: a dataframe with the loaded data and the 'inactive' column added
def load_data(data_path):
	data_listing = os.listdir(data_path)
	df = pd.DataFrame()
	#count = 0
	# go through all files and load all data in a big dataframe
	for dfile in data_listing:
		#count += 1
		#if count > 50: break
		new_df = pd.read_csv(data_path + '/' + dfile)
		df = df.append(new_df)

	df = label_inactive(df)
	return df

# labels frames as active or inactive based on velocity and distance of hands from the rest position
# inactive are labelled the frames the have low hand velocity and both hands are close to the rest position.
# arg/returned: a data frame with the loaded data that is returned with the 'inactive' column appended to it
def label_inactive(df):
	# distance from the rest position threshold.
	dist_thres = 25
	# True if inactive or False if active
	inactive = (df['low_velocity']==True)&((df['lh_dist_rp']<dist_thres)&(df['rh_dist_rp']<dist_thres))
	df['inactive'] = inactive
	return df

# split the data into training and test set (60% training, 40% testing)
def split_to_sets(df):
	# keep only the features we need for activity detection	
	df = df[['lh_v', 'rh_v', 'lh_dist_rp', 'rh_dist_rp', 'inactive']]
	# split into the two sets
	tr_s = df.iloc[0:int(0.6*len(df))]
	test_s = df.iloc[int(0.6*len(df)):]
	# extract labels from the 'inactive' column and convert to int
	labs_tr = tr_s['inactive'].as_matrix()
	labs_test = test_s['inactive'].as_matrix()
	labs_tr = map(lambda x: 1 if x else 0, labs_tr)
	labs_test = map(lambda x: 1 if x else 0, labs_test)
	new_labs_tr = np.zeros((len(labs_tr),2), dtype=np.int)
	new_labs_tr[:,0] = labs_tr
	new_labs_test = np.zeros((len(labs_test),2), dtype=np.int)
	new_labs_test[:,0] = labs_test
	for lab in new_labs_tr:		
		if lab[0] == 1: pass
		else:
			lab[1] = 1
	for lab in new_labs_test:
		if lab[0] == 1: pass
		else:
			lab[1] = 1

	# drop the 'inactive' column
	tr_s = tr_s.drop(['inactive'],1)
	test_s = test_s.drop(['inactive'],1)

	return tr_s.as_matrix(), test_s.as_matrix(), new_labs_tr, new_labs_test
############## main ##################

data_path = "C:\Users\Alex\Documents\University\Python\Data\CSV_data"

# load training and testing data and labels
print "Loading data set..."
df = load_data(data_path)
trX, teX, trY, teY = split_to_sets(df)
print trX.shape, teX.shape, trY.shape, teY.shape

# symbolic variables matrices initialization
X = T.fmatrix()
Y = T.fmatrix()

# initialize weights
# input to hidden layer: 4 input units, 4 hidden units
w_h = init_weights((4, 4))
# second hidden to output layer: 4 hidden units, 1 output unit
w_o = init_weights((4, 2))

# probability output
# use noise during training
noise_h, noise_py_x = model(X, w_h, w_o, 0.2, 0.5)
# we do not want noise for prdiction
h, py_x = model(X, w_h, w_o, 0., 0.)

# maxima prediction
y_x = T.argmax(py_x, axis=1)

# mean crossentropy cost function
cost = T.mean(T.nnet.categorical_crossentropy(noise_py_x, Y))

# parameters
params = [w_h, w_o]
# update gradients
updates = RMSprop(cost, params, lr=0.001)

# compile to python functions
train = theano.function(inputs=[X, Y], outputs=cost, updates=updates, allow_input_downcast=True)
predict = theano.function(inputs=[X], outputs=y_x, allow_input_downcast=True)

print "Starting training for 100 epochs..."
for i in range(3):
	#file = open("predictions.txt", 'w')
	# training on mini batches of 128 examples (very slow convergence)
	# training on mini batches of 128 examples (very slow convergence)
	#count = 0 
	for start, end in zip(range(0, len(trX), 128), range(128, len(trX), 128)):
		#count += 1
		cost = train(trX[start:end], trY[start:end])
		# the cost may increase in some iterations
	print i, np.mean(np.argmax(teY, axis=1) == predict(teX))

	#for i in predict(teX):
		#file.write("%s\n"%i)
	#file.close()

