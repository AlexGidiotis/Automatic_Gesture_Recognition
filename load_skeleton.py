import pandas as pd
import re

# filters a vector for irrelevant values(e.g x>=640 or y>=480) and replaces them with their mean(e.g x=320 and y=240)
# args: data_vector: a vector of integers with joint indices
# returns: data_vector: the filtered data vector
def filter_values(data_vector):
	# x values data_vector[1,3,5,7,9,11,13,15,17,19] must be < 640
	for i in [1,3,5,7,9,11,13,15,17,19]:
		if data_vector[i] >= 640: data_vector[i] = 320

	# y values data_vector[2,4,6,8,10,12,14,16,18,20] must be < 480
	for j in [2,4,6,8,10,12,14,16,18,20]:
		if data_vector[j] >= 480: data_vector[j] = 240

	return data_vector

# Opens a data file and imports values
# args:	sk_data_path: path to the data folder
#		data_file: file to be imported
# returns:	df: a dataframe with all the imported values

# skeletal data files come in the following format:	
# Frame: f Hip: hx,hy Shoulder_Center: scx,scy Left: lsx,lsy lex,ley lwx,lwy lhx,lhy Right: rsx,rsy rex,rey rwx,rwy rhx,rhy
def import_data(sk_data_path, data_file):
	tf = open(sk_data_path + '/' + data_file, 'r')
	df = pd.DataFrame()
	for line in tf:
		#frame
		frame = int(re.findall('Frame: (\d+) ', line)[0])
		# hip
		hx, hy = int(re.findall('Hip: (\d{1,3}),', line)[0]), int(re.findall('Hip: \d{1,3},(\d{1,3})', line)[0])
		# shoulder center
		scx, scy = int(re.findall('Shoulder_Center: (\d{1,3}),', line)[0]), int(re.findall('Shoulder_Center: \d{1,3},(\d{1,3})', line)[0])
		# left shoulder, elbow, wrist and hand
		lsx, lsy = int(re.findall('Left: (\d{1,3}),', line)[0]), int(re.findall('Left: \d{1,3},(\d{1,3})', line)[0])
		lex, ley = int(re.findall('Left: \d{1,3},\d{1,3} (\d{1,3}),', line)[0]), int(re.findall('Left: \d{1,3},\d{1,3} \d{1,3},(\d{1,3})', line)[0])
		lwx, lwy = int(re.findall('Left: \d{1,3},\d{1,3} \d{1,3},\d{1,3} (\d{1,3}),', line)[0]), int(re.findall('Left: \d{1,3},\d{1,3} \d{1,3},\d{1,3} \d{1,3},(\d{1,3})', line)[0])
		lhx, lhy = int(re.findall('Left: \d{1,3},\d{1,3} \d{1,3},\d{1,3} \d{1,3},\d{1,3} (\d{1,3}),', line)[0]), int(re.findall('Left: \d{1,3},\d{1,3} \d{1,3},\d{1,3} \d{1,3},\d{1,3} \d{1,3},(\d{1,3})', line)[0])

		# right shoulder, elbow, wrist and hand
		rsx, rsy = int(re.findall('Right: (\d{1,3}),', line)[0]), int(re.findall('Right: \d{1,3},(\d{1,3})', line)[0])
		rex, rey = int(re.findall('Right: \d{1,3},\d{1,3} (\d{1,3}),', line)[0]), int(re.findall('Right: \d{1,3},\d{1,3} \d{1,3},(\d{1,3})', line)[0])
		rwx, rwy = int(re.findall('Right: \d{1,3},\d{1,3} \d{1,3},\d{1,3} (\d{1,3}),', line)[0]), int(re.findall('Right: \d{1,3},\d{1,3} \d{1,3},\d{1,3} \d{1,3},(\d{1,3})', line)[0])
		rhx, rhy = int(re.findall('Right: \d{1,3},\d{1,3} \d{1,3},\d{1,3} \d{1,3},\d{1,3} (\d{1,3}),', line)[0]), int(re.findall('Right: \d{1,3},\d{1,3} \d{1,3},\d{1,3} \d{1,3},\d{1,3} \d{1,3},(\d{1,3})', line)[0])

		# create a vector and append it to the dataframe
		data_vector = [frame, hx, hy, scx, scy, lsx, lsy, lex, ley, lwx, lwy, lhx, lhy, rsx, rsy, rex, rey, rwx, rwy, rhx, rhy]
		# filter irelevant values
		data_vector = filter_values(data_vector)
		df = df.append([data_vector], ignore_index=True)

	# rename columns
	df.columns = ['frame','hipX','hipY','shcX','shcY','lsX','lsY','leX','leY','lwX','lwY','lhX','lhY',
				'rsX','rsY','reX','reY','rwX','rwY','rhX','rhY']
	
	return df