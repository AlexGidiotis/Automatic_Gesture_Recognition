import re
import pandas as pd

speech_input = '/home/alex/Documents/git_projects/Automatic_Gesture_Recognition/Speech/class_recout.mlf'
skeletal_input = '/home/alex/Documents/git_projects/Automatic_Gesture_Recognition/Training_Scripts/sec_recout.mlf'
output = 'rescored_recout.mlf'

speech_f = open(speech_input, 'r')
skeletal_f = open(skeletal_input, 'r')
out_f = open(output, 'w')
#==================================================================================================================================
# Read speech
speech_f.readline()
speech_list = []
for line in speech_f:
	if line.startswith('"*'):
		file_name = re.findall('"*/(EmbeddedTesting_Sequence\d+.rec)',line)[0]
		df = pd.DataFrame()
	elif line.startswith('.'):
		speech_list.append((file_name, df))
	else:
		start, end, keyword, log_l = re.findall('(\d*) (\d*) (\D*_?2?) -(\d*)',line)[0]
		df = df.append([[start, end, keyword, log_l]], ignore_index=True)
#print speech_list[10][1]
#==================================================================================================================================
# Read skeletal
skeletal_f.readline()
skeletal_list = []
for line in skeletal_f:
	if line.startswith('"*'):
		file_name = re.findall('"*/(EmbeddedTesting_Sequence\d+.rec)',line)[0]
		df = pd.DataFrame()
	elif line.startswith('.'):
		skeletal_list.append((file_name, df))
	else:
		start, end, keyword, log_l = re.findall('(\d*) (\d*) (\D*_?2?) -(\d*)',line)[0]
		df = df.append([[start, end, keyword, log_l]], ignore_index=True)
#print skeletal_list[10][1]
#==================================================================================================================================
# Rescore both lists
new_list = []
for speech, skeletal in zip(speech_list, skeletal_list):
	name = speech[0]
	sp_df = speech[1]
	sk_df = skeletal[1]
	new_df = pd.DataFrame()
	sp_starts = sp_df[0].tolist()
	sp_ends = sp_df[1].tolist()
	sp_keys = sp_df[2].tolist()
	sp_logl = sp_df[3].tolist()
	sk_starts = sk_df[0].tolist()
	sk_ends = sk_df[1].tolist()
	sk_keys = sk_df[2].tolist()
	sk_logl = sk_df[3].tolist()
	new_starts = []
	new_ends = []
	new_keys = []
	new_logl = []
	while ((len(sp_starts)>1) and (len(sk_starts)>1)):
#================================================================================================================================
# Speech starts first and is compared with other skeletals to find the one aligned with it
		if int(sp_starts[0]) < int(sk_starts[0]): 
			start = sp_starts[0]
			end = sp_ends[0]
			key = sp_keys[0]
			logl = sp_logl[0]
			sp_starts.pop(0)
			sp_ends.pop(0)
			sp_keys.pop(0)
			sp_logl.pop(0)
			for i in range(len(sk_starts)):
				other_start = sk_starts[i]
				other_end = sk_ends[i]
				other_key = sk_keys[i]
				other_logl = sk_logl[i]
				# The other starts after this one ends. (ignore it)
				if int(other_start) > int(end): break
				# THe other one starts and ends before this one ends
				elif int(other_end) < int(end):
					if len(new_keys)>0:
						if new_keys[-1] != key:
							new_starts.append(start)
							new_ends.append(end)
							new_keys.append(key)
							new_logl.append(logl)
					else:
						new_starts.append(start)
						new_ends.append(end)
						new_keys.append(key)
						new_logl.append(logl)

					sk_starts.pop(i)
					sk_ends.pop(i)
					sk_keys.pop(i)
					sk_logl.pop(i)
					break
				# THe other starts before this one ends and ends after this one
				else:
					if len(new_keys)>0:
						if new_keys[-1] != key:
							new_starts.append(start)
							new_ends.append(end)
							new_keys.append(key)
							new_logl.append(logl)
					else:
						new_starts.append(start)
						new_ends.append(end)
						new_keys.append(key)
						new_logl.append(logl)

					sk_starts.pop(i)
					sk_ends.pop(i)
					sk_keys.pop(i)
					sk_logl.pop(i)
					break

#================================================================================================================================
# Skeletal starts first and is compared with other speech to find the one aligned with it
		else:
			start = sk_starts[0]
			end = sk_ends[0]
			key = sk_keys[0]
			logl = sk_logl[0]
			sk_starts.pop(0)
			sk_ends.pop(0)
			sk_keys.pop(0)
			sk_logl.pop(0)
			for i in range(len(sp_starts)):
				other_start = sp_starts[i]
				other_end = sp_ends[i]
				other_key = sp_keys[i]
				other_logl = sp_logl[i]
				# The other starts after this one ends. (ignore it)
				if int(other_start) > int(end): break
				# THe other one starts and ends before this one ends
				elif int(other_end) < int(end):
					if len(new_keys)>0:
						if new_keys[-1] != other_key:	
							new_starts.append(other_start)
							new_ends.append(other_end)
							new_keys.append(other_key)
							new_logl.append(other_logl)
					else:
						new_starts.append(other_start)
						new_ends.append(other_end)
						new_keys.append(other_key)
						new_logl.append(other_logl)

					sp_starts.pop(i)
					sp_ends.pop(i)
					sp_keys.pop(i)
					sp_logl.pop(i)
					break
				# THe other starts before this one ends and ends after this one
				else:
					if len(new_keys)>0:
						if new_keys[-1] != other_key:	
							new_starts.append(other_start)
							new_ends.append(other_end)
							new_keys.append(other_key)
							new_logl.append(other_logl)
					else:
						new_starts.append(other_start)
						new_ends.append(other_end)
						new_keys.append(other_key)
						new_logl.append(other_logl)

					sp_starts.pop(i)
					sp_ends.pop(i)
					sp_keys.pop(i)
					sp_logl.pop(i)
					break
#==================================================================================================================================
	# Last rep
	if int(sp_starts[0]) < int(sk_starts[0]):
		if int(sk_starts[0]) > int(sp_ends[0]): pass									
		else:
			if len(new_keys)>0:
				if new_keys[-1] != sp_keys[0]:
					new_starts.append(sp_starts[0])
					new_ends.append(sp_ends[0])
					new_keys.append(sp_keys[0])
					new_logl.append(sp_logl[0])
			else:
				new_starts.append(sp_starts[0])
				new_ends.append(sp_ends[0])
				new_keys.append(sp_keys[0])
				new_logl.append(sp_logl[0])

	else:
		if int(sp_starts[0]) > int(sk_ends[0]): pass
		else:
			if len(new_keys)>0:
				if new_keys[-1] != sp_keys[0]:
					new_starts.append(sp_starts[0])
					new_ends.append(sp_ends[0])
					new_keys.append(sp_keys[0])
					new_logl.append(sp_logl[0])
			else:
				new_starts.append(sp_starts[0])
				new_ends.append(sp_ends[0])
				new_keys.append(sp_keys[0])
				new_logl.append(sp_logl[0])

	new_df[0], new_df[1], new_df[2], new_df[3] = new_starts, new_ends, new_keys, new_logl
	new_list.append((name, new_df))

#==================================================================================================================================
# Write output
out_f.write('#!MLF!#\n')
for file in new_list:
	name = file[0]
	out_f.write('"*/%s"\n' %name)
	df = file[1].as_matrix()
	for i in range(df.shape[0]):
		out_f.write('%s %s %s -%s\n' %(df[i][0], df[i][1], df[i][2], df[i][3]))

	out_f.write('.\n')
#==================================================================================================================================
speech_f.close()
skeletal_f.close()
out_f.close()