import pandas as pd
import os
import copy
os.chdir('C:\\Studying\\myvenv\\study_n_assignment\\DB_PjQuery3')

testdata= pd.read_csv('.\\test-data.csv')

cols= list(testdata.columns)
features= copy.deepcopy(cols)
features.remove('A')
print(cols, features)
