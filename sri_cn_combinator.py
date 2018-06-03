import os
import subprocess 
import re

# flag 0: Combines the meshes to one from both streams
# flag 1: Generates the combined lattice in htk format

flag = 1

sk_path = '/home/dimitris/GitProjects/Automatic_Gesture_Recognition/sk_meshes/'
sp_path = '/home/dimitris/GitProjects/Automatic_Gesture_Recognition/Speech/test_lattices/'
combined_Networks_path = '/home/dimitris/GitProjects/Automatic_Gesture_Recognition/combined_Networks/'
fusion_path = '/home/dimitris/GitProjects/Automatic_Gesture_Recognition/combined_htk_lattices/'

if flag == 0:
	for file in sorted(os.listdir(sk_path)):
		#Take the number from file
		file_number = re.findall('\d+',file,flags=0)[0]
		print file_number
		command = subprocess.Popen(['lattice-tool','-posterior-prune','0.001', '-init-mesh', sk_path+'EmbeddedTesting_Sequence'+file_number+'.mfc.gz',
			 '-in-lattice', sp_path+'TestingSample'+file_number+'.lat', '-read-htk', '-write-mesh', combined_Networks_path+'combined_mesh_'+file_number+'.mfc']) 
		command.wait()
elif flag == 1:
	for file in sorted(os.listdir(combined_Networks_path)):
		#Take the number from file
		file_number = re.findall('\d+',file,flags=0)[0]
		print file_number
		command = subprocess.Popen(['lattice-tool', '-read-mesh', '-in-lattice', combined_Networks_path +'combined_mesh_'+file_number+'.mfc', '-write-htk', '-out-lattice',
		 fusion_path+'fusion_lattice_'+ file_number+ '.lat']) 
		command.wait()
		