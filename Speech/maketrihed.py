
monolist = "monophones1"

mf = open(monolist, 'r')
of = open("mktri.hed", "w")

of.write("CL triphones1\n")

for line in mf:
	phone = line.rstrip()
	if phone != "":
		of.write("TI T_%s {(*-%s+*,%s+*,*-%s).transP}\n" %(phone,phone,phone,phone))

of.close()