import re
import os

flag = 'Training'
print flag

if flag == 'Training':
	path = 'C:\Users\Alex\Documents\University\Python\Data\MFC_audio'
	out_name = 'Train.scp'
elif flag == 'Testing':
	path = 'C:\Users\Alex\Documents\University\Python\Data\MFC_test_audio'
	out_name = 'Test.scp'


f_list = os.listdir(path)
of = open(out_name,'w')
for file in f_list:
	of.write('%s\%s\n' % (path,file))
of.close()