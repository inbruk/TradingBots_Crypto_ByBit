import pandas as pd
import matplotlib.pyplot as plt
import cufflinks as cf
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

init_notebook_mode(connected = True)
cf.go_offline()
df = pd.read_csv('tips.csv')

print('-------------------------------------------------------')

df.plot()
plt.show()

print('-------------------------------------------------------')

