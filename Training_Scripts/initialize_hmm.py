import sys, subprocess

classes=['SIL', 'BN', 'BS', 'CF', 'CN', 'CP', 'CV', 'DC', 'FM', 'FN', 'FU', 'MC', 'NU', 'OK', 'PF', 'PR', 'SP', 'ST', 'TT', 'VA', 'VQ']

path = "C:\Users\Alex\Documents\University\Python\Automatic_Gesture_Recognition\Training_Scripts\hmm0"
pf = open(path+"/prototype",'r')
of = open(path+"/macros",'w')

lin1 = pf.readline()
lin2 = pf.readline()
lin3 = pf.readline()
pf.close()

of.write(lin1)
of.write(lin2)
of.write(lin3)

vf = open(path+"/vFloors", 'r')

for line in vf:
    of.write(line)

vf.close()
of.close()

deff = open(path+"/hmmdefs",'w')

for cl in classes:
    deff.write('~h "%s" \n' % cl)
    pf = open(path+"/prototype",'r')
    pf.readline()
    pf.readline()
    pf.readline()
    pf.readline()
    for line in pf:
        deff.write("    "+line)

    pf.close()
