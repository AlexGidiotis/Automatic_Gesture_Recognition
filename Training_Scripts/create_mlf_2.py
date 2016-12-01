
import os
import re
import pandas as pd

map_lab = {1:'VA_2', 2:'VQ_2', 3:'PF_2', 4:'FU_2', 5:'CP_2', 6:'CV_2', 7:'DC_2', 8:'SP_2', 9:'CN_2', 10:'FN_2', 11:'OK_2', 12:'CF_2',
			13:'BS_2', 14:'PR_2', 15:'NU_2', 16:'FM_2', 17:'TT_2', 18:'BN_2', 19:'MC_2', 20:'ST_2'}

path = 'C:\Users\Alex\Documents\University\Python\Data\MFC_test_data\\labels.csv'

mlf = open("C:\Users\Alex\Documents\University\Python\Automatic_Gesture_Recognition\\Training_Scripts\\testphones0.mlf", "w")
train_scp = open("C:\Users\Alex\Documents\University\Python\Automatic_Gesture_Recognition\\Training_Scripts\\Test.scp")
df = pd.read_csv(path,'r',index_col = 0, delimiter = ',')
# Phonemes label file starts with #!MLF!#
mlf.write("#!MLF!#\n")

for line in train_scp:
	# We want to get the file name only.
	name = re.findall('.*\\\(\w*_\w*\d*).mfc',line)[0]
	file_num = re.findall('\w*_Sequence(\d*)',name)[0]
	idx = int(file_num)
	lab_list = df.loc[idx].tolist()[0].split()
	# Write to master label file.
	mlf.write('"*/%s.lab"\n' % name)
	for lab in lab_list:
		gest = map_lab[int(lab)]
		mlf.write('%s\n'%gest)
	mlf.write(".\n")
mlf.close()

