import pandas as pd
from IPython.core.display import display

football = pd.read_csv('data_sf.csv')
df = football

print('-------------------------------------------------------')

small_df = df[df.columns[1:8]].head(25)
display(small_df)

print('-------------------------------------------------------')

s = small_df['Nationality'].value_counts()
display(s)

print('-------------------------------------------------------')

fk = df['Club'].value_counts()
print(len(fk))

print('-------------------------------------------------------')

a = df['Age'].value_counts(normalize=True)
display(a)

print('-------------------------------------------------------')

w = df['Wage'].value_counts(bins=4)
display(w)

print('-------------------------------------------------------')

ws = small_df['Wage'].value_counts(bins=4)
display(small_df.loc[(small_df['Wage'] > ws.index[3].left) & (small_df['Wage'] <= ws.index[3].right)])

print('-------------------------------------------------------')

ak = df['FKAccuracy'].value_counts(bins=5)
display(ak)
display(ak.index[4].left)
display(ak.index[4].right)

print('-------------------------------------------------------')

display(df['Position'].nunique())

print('-------------------------------------------------------')

sn = small_df['Nationality'].value_counts()
sn_df = sn.reset_index()
sn_df.columns = ['Nationality', 'Players Count']
display(sn_df)

print('-------------------------------------------------------')

spa = df[df.Nationality == 'Spain']
display(len(spa))
spa_wage_vc = spa['Wage'].value_counts(bins=4)
display(spa_wage_vc)

display(round(651.0 / 671.0, 2))

print('-------------------------------------------------------')

age = df[df.Age > 35]
age_club = age[(age.Club == 'Nagoya Grampus') | (age.Club == 'Club Atlético Huracán') | (age.Club == 'LA Galaxy')]
age_club_vk = age_club['Club'].value_counts()
display(age_club_vk)

print('-------------------------------------------------------')

club = df[(df.Nationality == 'Argentina')]
club_age = club['Age'].value_counts(bins=4)
display(club_age)

print('-------------------------------------------------------')

spain = df[df.Nationality == 'Spain']
spain_age = spain[spain.Age == 21]
display(round(len(spain_age)*100/len(spain),2))

print('-------------------------------------------------------')

grouped_df = df.groupby(['Position'])['Wage'].sum().reset_index()
filtered_df = grouped_df[ grouped_df.Wage > 5000000 ]
display( filtered_df )

print('-------------------------------------------------------')

pwv = df.groupby(['Position'])[['Wage','Value']].mean()
pwv_sort = pwv.sort_values(by=['Value'],ascending=False)
display(pwv_sort)

print('-------------------------------------------------------')

wage_m = df.groupby(['Club'])['Wage'].agg(['mean','median']).reset_index()
wage_me = wage_m[(wage_m['mean']==wage_m['median'])]
display(wage_me)
display(len(wage_me))

print('-------------------------------------------------------')

wage_me_max = wage_me['mean'].max()
display(wage_me_max)

print('-------------------------------------------------------')

chels = df[(df.Club=='Chelsea')]
chels_sum = chels['Wage'].sum()
display(chels_sum)

print('-------------------------------------------------------')

arg = df[(df.Nationality=='Argentina') & (df.Age==30)]
arg_min = arg['Wage'].min()
display(arg_min)

print('-------------------------------------------------------')

club = df[(df.Nationality=='Argentina') & (df.Club=='FC Barcelona')]
str_max = club['Strength'].max()
bal_max = club['Balance'].max()
display(str_max)
display(bal_max)

print('-------------------------------------------------------')

df2 = df.pivot_table(columns = 'Position', index = 'Club', values = 'Wage', aggfunc = 'max')
display(df2.loc['Manchester City']['GK'])

print('-------------------------------------------------------')

df3 = df.pivot_table(columns = 'Position', index = 'Club', values = 'Wage', aggfunc = 'count', fill_value=0)
display(round(df3['GK'].mean(),3))

df4 = df3['CM'].reset_index()
display( df4[(df4.CM==0)])

print('-------------------------------------------------------')

df5 = df[(df.Nationality=='Russia') & (df.Club=='AS Monaco')]
display(df5['Wage'])

print('-------------------------------------------------------')

df3 = df.pivot_table(columns = 'Position', index = 'Club', values = 'SprintSpeed', aggfunc = 'mean', fill_value=0, margins=True)
display(df3)

df4 = df3.loc['All'].reset_index()
df5 = df4[(df4.Position=='RB') | (df4.Position=='LM') | (df4.Position=='RM') | (df4.Position=='CF') | (df4.Position=='RWM') | (df4.Position=='RS')]
display(df5)

df6 = df5.sort_values('All')
display(df6)

print('-------------------------------------------------------')

df3 = df.pivot_table(columns = 'Position', index = 'Club', values = 'SprintSpeed', aggfunc = 'mean', fill_value=0, margins=True)
display(df3)

df4 = df3['ST'].reset_index().sort_values('ST', ascending=False).head(3)
display(df4)

print('-------------------------------------------------------')

