import os
import pandas as pd
from IPython.core.display import display

files = os.listdir('data')
display(files)

print('-------------------------------------------------------')

files = ['setup.py', 'ratings.txt', 'stock_stats.txt', 'movies.txt', 'run.sh', 'game_of_thrones.mov']
data = list( filter( lambda x : 'txt' in x, files) )
display(files)
display(data)

print('-------------------------------------------------------')

for root, dirs, files in os.walk('data'):
    print('root=', root)
    print('dirs=', dirs)
    print('files=', files)
    print('..............')

print('-------------------------------------------------------')

data_df = pd.DataFrame( columns = ['userId', 'movieId', 'rating', 'timestamp'] )
for i in range(1,11):
    filename = 'ratings_' + str(i) + '.txt'
    path = os.path.join('data', filename )
    temp_df = pd.read_csv( path, names = ['userId', 'movieId', 'rating', 'timestamp'] )
    data_df = pd.concat([data_df, temp_df])

display(data_df)

print('-------------------------------------------------------')