import re

in_file = 'recout.mlf'
out_file = 'class_recout.mlf'

map_lab = {'Vattene':'VA_2', 'Vieni qui':'VQ_2', 'Perfetto':'PF_2', 'E\' un furbo':'FU_2', 'Che due palle':'CP_2', 'Che vuoi':'CV_2',
			'Vanno d\'accordo':'DC_2', 'Sei Pazzo':'SP_2', 'Cos\'hai combinato':'CN_2', 'Non me ne frega niente':'FN_2', 'ok':'OK_2', 
			'Cosa ti farei':'CF_2', 'Basta':'BS_2', 'Le vuoi prendere':'PR_2', 'Non ce n\'e piu':'NU_2', 'Ho fame':'FM_2', 
			'Tanto tempo fa':'TT_2', 'Buonissimo':'BN_2', 'Si sono messi d\'accordo':'MC_2', 'sono stufo':'ST_2', 'oov':'oov'}

in_f = open(in_file, 'r')
o_f = open(out_file, 'w')
first_line = in_f.readline()
o_f.write(first_line)
expr = []
expr_logl = 0
expr_start = '0'
expr_end = '0'
for line in in_f:
	line = line.rstrip()
	if line.startswith('"*'):
		num = re.findall('TestingSample(\d*)',line)[0] 
		o_f.write('"*/EmbeddedTesting_Sequence%s.rec"\n' %num)
	elif line.startswith('.'): o_f.write('%s\n' %line)
	elif line.startswith('///'): o_f.write('%s\n' %line)
	else:
		start, end, keyword, log_l = re.findall('(\d*) (\d*) (\D*) -(\d*)',line)[0]
		if len(expr) == 0: expr_start = start
		expr_logl += int(log_l)
		expr.append(keyword)
		try:
			out_class = map_lab[' '.join(expr)]
			expr_end = end
			expr_logl = expr_logl/len(expr)
			o_f.write('%s %s %s -%s\n' %(expr_start, expr_end, out_class, str(expr_logl)))
			expr = []
			expr_logl = 0
		except:
			pass

in_f.close()
o_f.close()