import os

writefile = open('File_list.txt','w')
#path = '/home/dimitris/GitProjects/Automatic_Gesture_Recognition/Speech/test_lattices/'
#path = '/home/dimitris/GitProjects/Automatic_Gesture_Recognition/Training_Scripts/sk_lattices/'
path = '/home/dimitris/GitProjects/Automatic_Gesture_Recognition/combined_Networks/'

for file in sorted(os.listdir(path)):
	writefile.write(path+file+'\n')
writefile.close()