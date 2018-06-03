import re

in_file = 'recout.mlf'
out_file = 'sec_recout.mlf'

in_f = open(in_file, 'r')
o_f = open(out_file, 'w')
first_line = in_f.readline()
o_f.write(first_line)

for line in in_f:
	line = line.rstrip()
	if line.startswith('"*'):
		num = re.findall('(\d*).rec',line)[0] 
		o_f.write('"*/EmbeddedTesting_Sequence%s.rec"\n' %num)
	elif line.startswith('.'): o_f.write('%s\n' %line)
	else:
		
		start, end, keyword, log_l = re.findall('(\d*) (\d*) (\D*_?2?) -(\d*)',line)[0]
		
		sec_start, sec_end = int(start)*5, int(end)*5
		o_f.write('%s %s %s -%s\n' %(sec_start, sec_end, keyword, log_l))

in_f.close()
o_f.close()