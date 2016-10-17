# Need to find some good metrics for clustering.


import numpy as np
import pandas as pd
import os
from sklearn.cluster import KMeans

def load_data(data_path,labels):
	data_listing = os.listdir(data_path)
	df = pd.DataFrame()	
	# go through all files and load all data and labels in a big dataframe
	# there must be exactly the same data and label files
	for dfile in data_listing:
		new_df = pd.read_csv(data_path + '/' + dfile)
		# append the file dataframe to the big dataframe				
		df = df.append(new_df,ignore_index=True)

	df["Labels"] = labels
	return df

#========================================= MAIN FUNCTION =======================================================

labels = pd.read_csv("training_label_file.csv")
path = "C:\Users\Alex\Documents\University\Python\Data\CSV_data"
classes = {'basta':1, 'buonissimo':2, 'cheduepalle':3, 'chevuoi':4, 'combinato':5, 'cosatifarei':6, 'daccordo':7,
			'fame':8, 'freganiente': 9, 'furbo':10, 'messidaccordo': 11, 'ok':12, 'perfetto':13, 'prendere': 14,
			'seipazzo':15, 'tantotempo':16, 'sonostufo':17, 'vattene': 18, 'vieniqui':19, 'noncenepiu':20, 'sil':21}

print "Loading data..."
df = load_data(path,labels)
print "Loaded data."

basta = df[df['Labels']=='basta']
X = basta[['lh_v','rh_v','lhX','lhY','rhX','rhY']].as_matrix()
kmeans =KMeans(n_clusters=3, random_state=0)
kmeans.fit(X)
basta['subclass'] = kmeans.labels_
basta.to_csv('basta.csv',index=False)