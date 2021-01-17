import pandas as pd
from IPython.core.display import display

football = pd.read_csv('data_sf.csv')

display(football.head())
print('-------------------------------------------------------')
display(football.tail())
print('-------------------------------------------------------')
display(football.info())
print('-------------------------------------------------------')

display(football.describe())
print('-------------------------------------------------------')
display(football.describe(include=['object']))
print('-------------------------------------------------------')
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    display(football.describe())
print('-------------------------------------------------------')
display(football['Value'].min())
print('-------------------------------------------------------')


