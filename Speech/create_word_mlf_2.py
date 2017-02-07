# Author: Alex Gidiotis
# gidiotisAlex@outlook.com.gr

# This script is used only for the Test cases when the test labels come in a separate csv file.
import os
import re
import pandas as pd

map_lab = {1:'Vattene', 2:'Vieni qui', 3:'Perfetto', 4:'E\' un furbo', 5:'Che due palle', 6:'Che vuoi', 7:'Vanno d\'accordo', 
			8:'Sei Pazzo', 9:'Cos\'hai combinato', 10:'Non me ne frega niente', 11:'ok', 12:'Cosa ti farei',
			13:'Basta', 14:'Le vuoi prendere', 15:'Non ce n\'e piu', 16:'Ho fame', 17:'Tanto tempo fa', 18:'Buonissimo', 
			19:'Si sono messi d\'accordo', 20:'sono stufo'}

# The path where the labels are. This is the same for both skeletal and speech models.
path = '/home/alex/Documents/Data/MFC_test_data/labels.csv'

# Open the output files.
mlf = open("/home/alex/Documents/git_projects/Automatic_Gesture_Recognition/Speech/test_words.mlf", "w")
train_scp = open("/home/alex/Documents/git_projects/Automatic_Gesture_Recognition/Speech/Test.scp")
# Read the labels from csv.
df = pd.read_csv(path,'r',index_col = 0, delimiter = ',')
# Phonemes label file starts with #!MLF!#
mlf.write("#!MLF!#\n")

for line in train_scp:
	# We want to get the file name only.
	name = re.findall('.*/(\D*\d*).mfc',line)[0]
	file_num = re.findall('\D*(\d*)',name)[0]
	idx = int(file_num)
	lab_list = df.loc[idx].tolist()[0].split()
	# Write to master label file.
	mlf.write('"*/%s.lab"\n' % name)
	for lab in lab_list:
		gest = map_lab[int(lab)]
		wordlist = gest.split()
		for g in wordlist:
			mlf.write('%s\n'%g)
	mlf.write(".\n")
mlf.close()

