import pandas as pd
import os
import numpy as np

flag = 'Testing'

if flag == 'Training':
	in_file = 'Training_set_skeletal.csv'
	out_file = 'Training_set_skeletal_extended.csv'
elif flag == 'Testing':
	in_file = 'Testing_set_skeletal.csv'
	out_file = 'Testing_set_skeletal_extended.csv'

print flag
print 'Loading data...'
df = pd.read_csv(in_file)
for file in df['file'].unique():
	print 'File',int(file)
	vf = df[df['file']==file]
	for ges in vf['label'].unique():
		if ges == 'sil':continue
		gf = vf[vf['label']==ges]
		labels = gf['label'].as_matrix()
		new_length = len(labels)/3

		sub_1 = np.ones_like(labels[0:new_length])
		sub_2 = np.ones_like(labels[new_length:2*new_length])
		sub_3 = np.ones_like(labels[2*new_length:])

		sub_1 = (ges + '_1') * sub_1
		sub_2 = (ges + '_2') * sub_2
		sub_3 = (ges + '_3') * sub_3

		labels = np.hstack((sub_1,sub_2,sub_3))
		gf['label'] = labels
		vf.ix[vf['label']==ges, 'label'] = labels
	df[df['file']==file] = vf

df.to_csv(out_file)	