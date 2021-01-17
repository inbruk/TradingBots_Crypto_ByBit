import pandas as pd
from IPython.core.display import display

log = pd.read_csv('log.csv')
display(log)

sample = pd.read_csv('sample.csv')
display(sample)

print('-------------------------------------------------------')

columns = sample.columns
display( columns )

print('-------------------------------------------------------')

sample.columns = ['name', 'city', 'age', 'profession']
columns = sample.columns
display( columns )

print('-------------------------------------------------------')

display(log.columns)
log.columns = [ 'user_id', 'time', 'bet', 'win' ]
display(log.columns)

print('-------------------------------------------------------')

users = pd.read_csv('users.csv', delimiter='\t', encoding='koi8_r')
users.columns = [ 'user_id', 'email', 'geo' ]
display(users)

print('-------------------------------------------------------')

sample = pd.read_csv('sample.csv')
display(sample.Name.unique())

print('-------------------------------------------------------')

display(sample.info())

print('-------------------------------------------------------')

display(log.user_id.unique())

print('-------------------------------------------------------')

display(sample)
sample2 = sample[ sample.Age < 30 ]
display(sample2)

print('-------------------------------------------------------')

log = pd.read_csv("log.csv",header=None)
log.columns = ['user_id', 'time', 'bet', 'win']
display(log)

log_win = log[ log.win.notnull() ]
display(log_win)

win_count = len(log_win.index)
display(win_count)

print('-------------------------------------------------------')

display(sample)
sample2 = sample[ (sample.Age < 30) & ( sample.Profession=='Рабочий' ) ]
display(sample2)

print('-------------------------------------------------------')

log = pd.read_csv("log.csv",header=None)
log.columns = ['user_id','time', 'bet','win']
log2 = log.query( 'bet<2000 & win>0' )
display(log2)

print('-------------------------------------------------------')

sample = pd.read_csv("sample.csv")
display(sample)

print('-------------------------------------------------------')

sample3 = sample[ sample.City.str.contains("о", na=False) ]
display(sample3)

print('-------------------------------------------------------')

sample4 = sample[ ~sample.City.str.contains("о", na=False) ]
display(sample4)

print('-------------------------------------------------------')

log = pd.read_csv("log.csv",header=None)
log.columns = ['user_id','time', 'bet','win']
new_log = log[  log.user_id.str.contains("#error", na=False)==False  ]
display(new_log)

print('-------------------------------------------------------')

sample = pd.read_csv("sample.csv")
display(sample)
sample2 = sample.copy(True)
sample2.Age = sample2.Age.apply( lambda x: x+1 )
display(sample2)

print('-------------------------------------------------------')

sample = pd.read_csv("sample.csv")
display(sample)
sample2 = sample.copy(True)
sample2.City = sample2.City.astype(str).apply(lambda x: x.lower())
display(sample2)

print('-------------------------------------------------------')

sample = pd.read_csv("sample.csv")
sample2 = sample.copy(True)

def profession_code(s):
    if s == "Рабочий":
        return 0
    elif s == "Менеджер":
        return 1
    return 2

sample2.Profession = sample2.Profession.astype(str).apply( profession_code )
display(sample2)

print('-------------------------------------------------------')

sample = pd.read_csv("sample.csv")

def age_category(a):
    if a < 23:
        return "молодой"
    elif 23 <= a <= 35 :
        return "средний"
    return "зрелый"

sample['Age_category']  = sample.Age.apply( age_category )

print('-------------------------------------------------------')

log = pd.read_csv('log.csv', header=None)
log.columns = ['user_id','time','bet','win']
display(log)

def prepare_user_id(s):
    arr_str = s.split(' - ')
    if len(arr_str)>1:
        return arr_str[1]
    else:
        return ''

log['user_id'] = log.user_id.apply( prepare_user_id )
display(log)

print('-------------------------------------------------------')

log = pd.read_csv("log.csv",header=None)
log.columns = ['user_id','time','bet','win']
t = log.time[0]
t = t.replace('[','')
display(t)

print('-------------------------------------------------------')

log = pd.read_csv('log.csv', header=None)
log.columns = ['user_id','time','bet','win']
display(log)


def prepare_time(s):
    res = s.replace('[','')
    #res = res.replace('nan','')
    return res

log['time'] = log.time.astype(str).apply( prepare_time )
display(log)

print('-------------------------------------------------------')

log = pd.read_csv('log.csv', header=None)
log.columns = ['user_id','time','bet','win']

log = log[ log.user_id!='#error' ]


def prepare_user_id(s):
    arr_str = s.split(' - ')
    if len(arr_str)>1:
        return arr_str[1]
    else:
        return ''
log['user_id'] = log.user_id.apply( prepare_user_id )


def prepare_time(s):
    res = s.replace('[','')
    return res


log['time'] = log.time.astype(str).apply( prepare_time )
display(log)




