import re
import pandas as pd
import numpy as np

#activity_file = 'C:\Users\Alex\Documents\University\Python\Automatic_Gesture_Recognition\\Test_labels.csv'
activity_file = '/home/dimitris/GitProjects/Automatic_Gesture_Recognition/Test_labels.csv'
fps = 20.0

print 'Loading activity labels...'
af = pd.read_csv(activity_file)
out_f = open('aligned_speech_recout.mlf','w')
#in_f = open('C:\Users\Alex\Documents\University\Python\Automatic_Gesture_Recognition\Speech\\recout.mlf', 'r')
in_f = open('/home/dimitris/GitProjects/Automatic_Gesture_Recognition/Speech/recout.mlf', 'r')
out_f.write("#!MLF!#\n")
line = in_f.readline()

# Read silences and put in dictionary
sil_dict = {}
list_file_nums = [int(fNum) for fNum in af['file'].unique()]
for file in af['file'].unique():
	df = af[af['file'] == file]
	sil_labs = df[df['label'] == 'sil']
	file_sil_list = []
	file_index = str(int(file))
	for k,g in sil_labs.groupby(sil_labs['frame'] - np.arange(sil_labs.shape[0])):
		start,end = g.iloc[0]['frame'],g.iloc[-1]['frame']
		file_sil_list.append((int(start/fps * 10000000),int(end/fps * 10000000),'sil'))
	sil_dict[file_index] = file_sil_list

# Read prediction and put in dictionary
input_dict = {}
for line in in_f:
	if line.startswith('\"\'*\''):
		file_list = []
		fileNum = re.findall('\"\'*\'\D*(\d+).rec',line)[0]
		file_list.append(line)
		
	elif line.startswith('.'):
		file_list.append(line)
		input_dict[fileNum] = file_list
	else:
		word = re.findall(' (\D+) -\d',line)[0]
		sp_start,sp_end = re.findall('(^\d+) \d',line)[0],re.findall('^\d+ (\d+) \D',line)[0]
		file_list.append((int(sp_start),int(sp_end),word))
in_f.close()
		
# Do the cross matching
for file in list_file_nums:
	input_predictions = input_dict[str(file)]
	sil_list = sil_dict[str(file)]
	input_list = input_predictions[1:-1]
	complete_list = []
	for s in range(0,len(sil_list)-1):
		sil_start,sil_end,sil_word = sil_list[s][0],sil_list[s][1],sil_list[s][2]
		next_sil_start,next_sil_end,next_sil_word = sil_list[s+1][0],sil_list[s+1][1],sil_list[s+1][2]
		complete_list.append((sil_start,sil_end,sil_word))
		for i in input_list:
			speech_start,speech_end,speech_word = i[0],i[1],i[2]
			if (speech_start > (sil_end - 100000)) & (speech_start < (next_sil_start + 100000)):
				complete_list.append((i[0],i[1],i[2]))

	complete_list.append((sil_list[-1][0],sil_list[-1][1],sil_list[-1][2]))

	out_f.write(input_predictions[0])
	for i in range(0,len(complete_list)):
		start,end,word = complete_list[i][0],complete_list[i][1],complete_list[i][2]
		out_f.write("%s %s %s\n" %(start,end,word))
	out_f.write(input_predictions[-1])


out_f.close()

#