import pandas as pd

# estimate the rest position as the median position of all segments with low velocity
# args: df: dataframe with skeleton joints
# returns: df: dataframe with the 'low_velocity' column added
#		   rp: a tuple of 16 integers with the rest position of both hands (lsx,lsy,lex,ley,lwx,lwy,lhx,lhy,rsx,rsy,rex,rey,rwx,rwy,rhx,rhy)
def estimate_rest_position(df):
	median_left = df['lh_v'].mean()
	median_right = df['rh_v'].mean()

	#flag as low velocity all frames that have both hands under velocity threshold
	df['low_velocity'] = (df['lh_v']<median_left)&(df['rh_v']<median_right)
	low_v = df[df['low_velocity'] == True]

	# estimate the rest position
	rp = int(low_v['lsX'].median()),int(low_v['lsY'].median()),int(low_v['leX'].median()),int(low_v['leY'].median()),\
		int(low_v['lwX'].median()),int(low_v['lwY'].median()),int(low_v['lhX'].median()), int(low_v['lhY'].median()),\
		int(low_v['rsX'].median()), int(low_v['rsY'].median()),int(low_v['reX'].median()), int(low_v['reY'].median()),\
		int(low_v['rwX'].median()), int(low_v['rwY'].median()),int(low_v['rhX'].median()), int(low_v['rhY'].median())
	return df, rp

# under development
def calc_distance_from_rp(df):
	return df
