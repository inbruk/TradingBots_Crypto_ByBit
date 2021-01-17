import pandas as pd
from IPython.core.display import display

df = pd.DataFrame([[i, i+1.2, i+2, 'hi'] for i in range(10)],
                  columns=['foo', 'bar', 'baz', 'foobar'])

print('---------------------------------------------------')
display(df)
print('---------------------------------------------------')
display(df.mean())
print('---------------------------------------------------')
display(df.mean(axis=1))
print('---------------------------------------------------')
display(df['foo'])
print('---------------------------------------------------')
display(df.bar)
print('---------------------------------------------------')