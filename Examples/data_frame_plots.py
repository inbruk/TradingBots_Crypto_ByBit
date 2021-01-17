import matplotlib.pyplot as plt
import  pandas as pd
from IPython.core.display import display

print('-------------------------------------------------------')

df = pd.read_csv('tips.csv')
display(df)

print('-------------------------------------------------------')

display(df["total_bill"].max())

print('-------------------------------------------------------')

df.plot()
plt.show()

print('-------------------------------------------------------')

df['total_bill'].plot(kind = 'hist', grid = True, title = 'Общая сумма счёта')
plt.show()

print('-------------------------------------------------------')

df['day'].value_counts().plot(kind = 'bar',
                              grid = True,
                              colormap = 'coolwarm',
                              title = 'Количество посетителей по дням')
plt.show()

print('-------------------------------------------------------')

df[['total_bill', 'tip']].plot(kind = 'hist',
                               grid = True,
                               subplots = True,
                               title = ['Общая сумма счёта', 'Сумма чаевых'],
                               legend = False)
plt.show()

print('-------------------------------------------------------')

df.plot(x = 'total_bill',
        y = 'tip',
        kind = 'scatter',
        grid = True,
        title = 'Общая сумма счёта Vs сумма чаевых')
plt.show()

print('-------------------------------------------------------')

df2 = df.pivot_table(values = ['total_bill', 'tip'],
               index = 'day',
               aggfunc = 'mean')
display(df2)
df2.plot(kind = 'bar')
plt.show()

print('-------------------------------------------------------')

