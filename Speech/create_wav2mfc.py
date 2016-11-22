import os
import re



flag = 'Testing'
print flag

if flag == 'Training':
	path = 'C:\Users\Alex\Documents\University\Python\Data\Train_audio'
	out_path = 'C:\Users\Alex\Documents\University\Python\Data\MFC_audio'
	out_name = 'TrainingSample'
elif flag == 'Testing':
	path = 'C:\Users\Alex\Documents\University\Python\Data\Test_audio'
	out_path = 'C:\Users\Alex\Documents\University\Python\Data\MFC_test_audio'
	out_name = 'TestingSample'

f_list = os.listdir(path)
of = open('wav2mfc.scp','w')
for file in f_list:
	fileNum = re.findall('Sample0+(\d+)_',file)[0]
	out_file = out_name + fileNum + '.mfc'
	of.write('%s\%s %s\%s\n' % (path,file,out_path,out_file))
of.close()


