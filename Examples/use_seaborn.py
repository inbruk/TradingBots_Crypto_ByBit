import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings; warnings.simplefilter('ignore')

df = pd.read_csv('tips.csv')
sns.set()
sns.distplot(df['total_bill'])
plt.show()

print('-------------------------------------------------------')

sns.jointplot(x = 'total_bill', y = 'tip', data = df, kind = 'reg')
plt.show()

print('-------------------------------------------------------')

sns.pairplot(df)
plt.show()

print('-------------------------------------------------------')

sns.countplot(x = 'day', data = df)
plt.show()

print('-------------------------------------------------------')

sns.barplot(x = 'sex', y = 'total_bill', data = df)
plt.show()

print('-------------------------------------------------------')

sns.boxplot(x = 'day', y = 'tip', data = df, hue = 'smoker')
plt.show()

print('-------------------------------------------------------')

correlation = df.corr()
sns.heatmap( correlation, annot=True, cmap='coolwarm' )
plt.show()

print('-------------------------------------------------------')




