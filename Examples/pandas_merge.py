import pandas as pd
from IPython.core.display import display

ratings_df = pd.read_csv('ratings.csv')
movies_df = pd.read_csv('movies.csv')

print('-------------------------------------------------------')

print(ratings_df.head())
print(movies_df.head())
print(movies_df.columns)

print('-------------------------------------------------------')

genres_vc = movies_df['genres'].value_counts()
display(genres_vc)

print('-------------------------------------------------------')

display(movies_df.columns.tolist())

print('-------------------------------------------------------')

display(ratings_df['rating'].min())
display(ratings_df['rating'].max())

print('-------------------------------------------------------')

movies_len = len(movies_df)
display(movies_len)

print('-------------------------------------------------------')

joined = ratings_df.merge(movies_df, on='movieId', how='left')
display(joined.head())
display(movies_df.columns)

print('-------------------------------------------------------')

ratings_ex = pd.read_csv('ratings_example.csv', sep = '\t')
movies_ex = pd.read_csv('movies_example.csv', sep = '\t')

display(ratings_ex)
display(movies_ex)

print('-------------------------------------------------------I')

joined_ex_inner = ratings_ex.merge(movies_ex, on='movieId', how='inner')
display(joined_ex_inner)

print('-------------------------------------------------------L')

joined_ex_left = ratings_ex.merge(movies_ex, on='movieId', how='left')
display(joined_ex_left)

print('-------------------------------------------------------R')

joined_ex_right = ratings_ex.merge(movies_ex, on='movieId', how='right')
display(joined_ex_right)

print('-------------------------------------------------------O')

joined_ex_outer = ratings_ex.merge(movies_ex, on='movieId', how='outer')
display(joined_ex_outer)

print('-------------------------------------------------------')

joined_deduplex = joined.drop_duplicates(subset = 'movieId', keep = 'first', inplace = False)
display(joined)
display(joined_deduplex)

print('-------------------------------------------------------')

items_dict = {

    'item_id': [417283, 849734, 132223, 573943, 19475, 3294095, 382043, 302948, 100132, 312394],

    'vendor': ['Samsung', 'LG', 'Apple', 'Apple', 'LG', 'Apple', 'Samsung', 'Samsung', 'LG', 'ZTE'],

    'stock_count': [54, 33, 122, 18, 102, 43, 77, 143, 60, 19]

}

purchase_log = {

    'purchase_id': [101, 101, 101, 112, 121, 145, 145, 145, 145, 221],

    'item_id': [417283, 849734, 132223, 573943, 19475, 3294095, 382043, 302948, 103845, 100132],

    'price': [13900, 5330, 38200, 49990, 9890, 33000, 67500, 34500, 89900, 11400]

}

items_df = pd.DataFrame(items_dict)
purchase_df = pd.DataFrame(purchase_log)

display(items_df)
display(purchase_df)

print('-------------------------------------------------------')

joined_pr = purchase_df.merge(items_df, on='item_id', how='right' )
joined_pr2 = joined_pr.get( joined_pr['price'] .isnull())
joined_pr3 = joined_pr2['item_id']
display( joined_pr3 )

print('-------------------------------------------------------')

joined_pr4 = purchase_df.merge(items_df, on='item_id', how='inner' )
display( joined_pr4 )

print('-------------------------------------------------------')

joined_sum = joined_pr

prSum = pd.Series( joined_sum['stock_count'] * joined_sum['price'], index=joined_sum.index)
joined_sum['prSum'] = prSum
display(joined_sum)

display( joined_sum['prSum'].sum() )

print('-------------------------------------------------------')







