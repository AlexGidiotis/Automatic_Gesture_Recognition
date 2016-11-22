import pandas as pd
import os
import re
import subprocess

words = {'vieniqui':'Vieni qui','prendere':'Le vuoi prendere','sonostufo':'sono stufo','chevuoi':'Che vuoi',
		'daccordo':'Vanno d\'accordo','perfetto':'Perfetto','vattene':'Vattene','basta':'Basta','buonissimo':'Buonissimo',
		'cheduepalle':'Che due palle','cosatifarei':'Cosa ti farei','fame':'Ho fame','noncenepiu':'Non ce n\'e piu',
		'furbo':'E\' un furbo','combinato':'Cos\'hai combinato','freganiente':'Non me ne frega niente','seipazzo':'Sei Pazzo',
		'tantotempo':'Tanto tempo fa','messidaccordo':'Si sono messi d\'accordo','ok':'ok'}

flag = 'Testing'
print flag

if flag == 'Training':
	if not os.path.exists("train_labels"):
		os.makedirs("train_labels")

	# Create the output .mlf file
	mlf = open("words.mlf", "w")

	in_file = 'Train_labels.csv'
	out_words = 'words.mlf'
	out_name = 'TrainingSample'
	out_phones = 'phones0.mlf'
	lab_path = 'C:\Users\Alex\Documents\University\Python\Automatic_Gesture_Recognition\Speech\\train_labels'
	#scp_file = 'Train.scp'

elif flag == 'Testing':
	if not os.path.exists("test_labels"):
		os.makedirs("test_labels")

	# Create the output .mlf file
	mlf = open("test_words.mlf", "w")

	in_file = 'Test_labels.csv'
	out_words = 'test_words.mlf'
	out_name = 'TestingSample'
	out_phones = 'test_phones0.mlf'
	lab_path = 'C:\Users\Alex\Documents\University\Python\Automatic_Gesture_Recognition\Speech\\test_labels'
	#scp_file = 'Test.scp'


# Phonemes label file starts with #!MLF!#
mlf.write("#!MLF!#\n")

lf = pd.read_csv(in_file)
for file in lf['file'].unique():
	file_num = int(file)
	label_list = []
	file_labs = lf.ix[lf['file'] == file, 'label'].as_matrix()
	for lab in file_labs:
		if lab == 'sil': continue
		if len(label_list) == 0:
			label_list.append('noise')
			label_list.append(words[lab])
		elif label_list[-1] != words[lab]:
			label_list.append('noise')
			label_list.append(words[lab])
	mlf.write('"*/%s%d.lab"\n' % (out_name,file_num))
	for word in label_list:
		# Write to master label file.
		for item in word.split():
			mlf.write("%s\n"% item)
	mlf.write(".\n")

mlf.close()
print out_words,'created'
hled = subprocess.Popen(['HLEd', '-l', '*', '-d', 'dictionary', '-i', out_phones, 'mkphones0.led', out_words])
hled.wait()
print out_phones,'created'

phones_mlf = open(out_phones)
fline = phones_mlf.readline()
print fline
for line in phones_mlf:
	line = line.rstrip()
	if line.startswith('"*'):
		f_name = re.findall('"*/(\D+\d+).lab',line)[0]
		lab_f = open(os.path.join(lab_path,f_name + '.lab'),'w')
	elif line.startswith('.'):
		lab_f.close()
	else:
		lab_f.write('%s\n' % line)


