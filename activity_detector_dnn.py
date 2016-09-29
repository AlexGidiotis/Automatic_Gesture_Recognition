# here we implement the parameters of our neural network

import theano
from theano import tensor as T
from theano.sandbox.rng_mrg import MRG_RandomStreams as RandomStreams
import numpy as np

srng = RandomStreams()

# convert to correct data type
def floatX(X):
    return np.asarray(X, dtype=theano.config.floatX)

# initialize model parameters
def init_weights(shape):
    return theano.shared(floatX(np.random.randn(*shape) * 0.01))

# numerically stable softmax
def softmax(X):
	e_x = T.exp(X - X.max(axis=1).dimshuffle(0, 'x'))
	return	e_x/ e_x.sum(axis=1).dimshuffle(0, 'x')

# RMSprop implementation
def RMSprop(cost, params, lr=0.001, rho=0.9, epsilon=1e-6):
	grads = T.grad(cost=cost, wrt=params)
	updates = []
	for p, g in zip(params, grads):
		# a running average of the magnitude of the gradient
		acc = theano.shared(p.get_value() * 0.)
		acc_new = rho * acc + (1 - rho) * g ** 2
		# scale the gradient based on the running average
		gradient_scaling = T.sqrt(acc_new + epsilon)
		g = g / gradient_scaling
		# simultaneously update parameters
		updates.append((acc, acc_new))
		updates.append((p, p - lr * g))
	return updates

# use dropout in order to add noise to the data for regularization
# randomly drops value and scales the rest
def dropout(X, p=0.):
	if p>0:
		retain_prob = 1 - p
		X *= srng.binomial(X.shape, p=retain_prob, dtype=theano.config.floatX)
		X /= retain_prob
	return X

# our neural net model is a single layer neural net with sigmoid activation for hidden units and softmax output
def model(X, w_h, w_o, p_drop_input, p_drop_hidden):
	# inject noise to every layer
	X = dropout(X, p_drop_input)
	# use sigmoid activation for hidden layer activation
	h = T.nnet.sigmoid(T.dot(X, w_h))
	# inject noise again 
	h = dropout(h, p_drop_hidden)	
	py_x = softmax(T.dot(h, w_o))
	return h, py_x

