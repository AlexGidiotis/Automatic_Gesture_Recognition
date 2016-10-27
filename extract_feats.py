# THIS IS UNUSED AND MIGHT BE REMOVED.
#
#
#
#
import pandas as pd

data_set = pd.read_csv('training_label_file.csv')
data_set.columns =['index_old','Labels']
data_set = data_set.drop('index_old',axis=1)
data_set[data_set['Labels'] == 'None'] = 'sil'

data_set.to_csv('training_label_file.csv',index=False)

