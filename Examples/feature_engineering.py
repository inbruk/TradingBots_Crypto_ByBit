import pandas as pd
from IPython.core.display import display

log = pd.read_csv("log.csv", header=None)
sample = pd.read_csv('sample.csv')
users = pd.read_csv('users.csv', delimiter='\t', encoding='koi8_r')

print('-------------------------------------------------------')

log.columns = ['user_id', 'time', 'bet', 'win']
sample.columns = ['name', 'city', 'age', 'profession']
users.columns = ['user_id', 'email', 'geo']

print('-------------------------------------------------------')

display(log.head())
display(log.head().isna())

print('-------------------------------------------------------')

ser = log.time.isna()
res = ser[ lambda x : x==True ]
display(res.count())

print('-------------------------------------------------------')

log2 = log.copy(True)
display(log2)
display(log2.dropna(axis=1))

print('-------------------------------------------------------')

log2 = log.copy(True)
display(log2)
display(log2.dropna(axis=0))

print('-------------------------------------------------------')

log2 = log.copy(True)
display(log2)
log3 = log2.dropna(axis=1)
display(log3)

log2 = log.copy(True)
log3['bet'] = log2['bet']
log3['win'] = log2['win']
display(log3)

print('-------------------------------------------------------')

log2 = log.copy(True)
display(log2)
log3 = log2.drop_duplicates(subset=['user_id', 'time'])
display(log3)

print('-------------------------------------------------------')

log2 = log.copy(True)

col_time = log.time
display(col_time)

col_time = col_time.dropna()
display(col_time)

def prepare_time(s):
    res = s.replace('[','')
    return res

col_time = col_time.astype(str).apply( prepare_time )
display(col_time)

display(col_time.max())

print('-------------------------------------------------------')

log = pd.read_csv("log.csv")
log = log.dropna()
log.columns = ['user_id', 'time', 'bet', 'win']
log['time'] = log['time'].apply(lambda x: x[1:])
log['time'] = pd.to_datetime(log['time'])
log['time'] = log['time'].apply(lambda x: x.minute)
display(log['time'].head())

print('-------------------------------------------------------')

log = pd.read_csv("log.csv")
log.columns = ['user_id', 'time', 'bet', 'win']

log2 = log.copy(True)
log2 = log2.dropna(subset=['time'],axis=0)
log2['time'] = log2['time'].apply(lambda x: x[1:])
log2['time'] = pd.to_datetime(log2['time'])
col_min = log2.time.dt.minute
col_mon = log2.time.dt.month
display(col_min.value_counts())
display(col_mon.value_counts())

print('-------------------------------------------------------')

log = pd.read_csv("log.csv")
log.columns = ['user_id', 'time', 'bet', 'win']
log2 = log.copy(True)
log2 = log2.dropna(subset=['time'],axis=0)
log2['time'] = log2['time'].apply(lambda x: x[1:])
log2['time'] = pd.to_datetime(log2['time'])
display(log2)

col_min = log2.time.dt.minute
col_mon = log2.time.dt.month
display(col_min.value_counts())
display(col_mon.value_counts())







