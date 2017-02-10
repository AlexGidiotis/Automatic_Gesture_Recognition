import os
import re
import pandas as pd

map_lab = {1:'Vattene', 2:'Vieni qui', 3:'Perfetto', 4:'E\' un furbo', 5:'Che due palle', 6:'Che vuoi', 7:'Vanno d\'accordo', 
			8:'Sei Pazzo', 9:'Cos\'hai combinato', 10:'Non me ne frega niente', 11:'ok', 12:'Cosa ti farei',
			13:'Basta', 14:'Le vuoi prendere', 15:'Non ce n\'e piu', 16:'Ho fame', 17:'Tanto tempo fa', 18:'Buonissimo', 
			19:'Si sono messi d\'accordo', 20:'sono stufo'}

#path = 'C:\Users\Alex\Documents\University\Python\Data\MFC_test_data\\labels.csv'
path = '/home/dimitris/GitProjects/Automatic_Gesture_Recognition/Data/MFC_test_data/labels.csv'
#mlf = open("C:\Users\Alex\Documents\University\Python\Automatic_Gesture_Recognition\\Speech\\test_words.mlf", "w")
mlf = open("/home/dimitris/GitProjects/Automatic_Gesture_Recognition/Speech/test_words.mlf", "w")

#train_scp = open("C:\Users\Alex\Documents\University\Python\Automatic_Gesture_Recognition\\Speech\\Test.scp")
train_scp = open("/home/dimitris/GitProjects/Automatic_Gesture_Recognition/Speech/Test.scp")

df = pd.read_csv(path,'r',index_col = 0, delimiter = ',')
# Phonemes label file starts with #!MLF!#
mlf.write("#!MLF!#\n")

for line in train_scp:
	# We want to get the file name only.
	#print line
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