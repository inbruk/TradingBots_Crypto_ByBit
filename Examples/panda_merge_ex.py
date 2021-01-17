import pandas as pd
from IPython.core.display import display

ratings_df = pd.read_csv('ratings.csv')
movies_df = pd.read_csv('movies.csv')

display(ratings_df)
display(movies_df)

print('-------------------------------------------------------')

ratings_v = ratings_df['rating'].value_counts()
print(ratings_v)

print('-------------------------------------------------------')

joined = ratings_df.merge(movies_df, on='movieId', how='outer')
display(joined)

print('-------------------------------------------------------')

display(joined.columns)
film = joined[ joined.movieId==3456 ]
display(film)

print('-------------------------------------------------------')





