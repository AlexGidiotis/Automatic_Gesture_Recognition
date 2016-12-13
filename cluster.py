# NEEDS TO BE REMOVED


import numpy as np
import pandas as pd
import os
from sklearn.cluster import KMeans

def load_data(in_file):
	df = pd.read_csv(in_file)
	return df

#========================================= MAIN FUNCTION =======================================================
flag = 'Testing'

if flag == 'Training':
	in_file = 'Training_set_skeletal.csv'
	out_file = 'Training_set_skeletal.csv'
elif flag == 'Testing':
	in_file = 'Testing_set_skeletal.csv'
	out_file = 'Testing_set_skeletal.csv'

classes = {'basta':1, 'buonissimo':2, 'cheduepalle':3, 'chevuoi':4, 'combinato':5, 'cosatifarei':6, 'daccordo':7,
			'fame':8, 'freganiente': 9, 'furbo':10, 'messidaccordo': 11, 'ok':12, 'perfetto':13, 'prendere': 14,
			'seipazzo':15, 'tantotempo':16, 'sonostufo':17, 'vattene': 18, 'vieniqui':19, 'noncenepiu':20, 'sil':21}
print flag
print "Loading data..."
df = load_data(in_file)
print "Loaded data."

print 'Clustering...'
X = df[['lh_dist_rp','rh_dist_rp']].as_matrix()
kmeans =KMeans(n_clusters=2, random_state=0)
kmeans.fit(X)
subcl = kmeans.labels_
labs = df['label'].as_matrix()
for i in range(0,(len(subcl)-7)):
	batch = np.array([subcl[i], subcl[(i+1)], subcl[(i+2)], subcl[(i+3)], subcl[(i+4)],subcl[i+5],subcl[i+6],subcl[i+7]])
	sample = np.median(batch)
	subcl[i] = sample

print 'Relabeling...'
labels = []
for l,s in zip(labs,subcl):
	new_class = str(l) + '_' + str(s)
	labels.append(new_class)


df['label'] = labels
df.to_csv(out_file,index=False)
