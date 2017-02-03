#This scripts Builds neural network for 
#late fusion usage


from keras.models import Sequential
from keras.layers import Dense
import numpy as np

# load gesture dataset
#dataset = numpy.loadtxt(, delimiter=",")

#input = feature vector extracted 

# create model
model = Sequential()
model.add(Dense(18, input_dim=6, init='uniform', activation='relu'))
model.add(Dense(18, init='uniform', activation='relu'))
model.add(Dense(12, init='uniform', activation='relu'))
model.add(Dense(2, init='uniform', activation='relu'))

# Compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# Fit the model
model.fit(X, Y, nb_epoch=150, batch_size=10,  verbose=2)

# evaluate the model
scores = model.evaluate(X, Y)
print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

# calculate predictions
predictions = model.predict(X)
# round predictions
rounded = [round(x) for x in predictions]