import pandas as pd
from IPython.core.display import display

football = pd.read_csv('data_sf.csv')

print('-------------------------------------------------------')
display(round(football[ football.Wage > football.Wage.mean() ].SprintSpeed.mean(), 2))
print('-------------------------------------------------------')

display(round(football[ football.Wage < football.Wage.mean() ].SprintSpeed.mean(), 2))
print('-------------------------------------------------------')

display( football[ football.Wage == football.Wage.max() ].Position )
print('-------------------------------------------------------')

display( football[ football.Nationality == 'Brazil' ].Penalties.sum() )
print('-------------------------------------------------------')

display( round(football[ football.HeadingAccuracy > 50 ].Age.mean(), 2) )
print('-------------------------------------------------------')

display( football[
             ( football.Composure > 0.9*football.Composure.max() ) &
             ( football.Reactions > 0.9*football.Reactions.max() )
    ].Age.min() )
print('-------------------------------------------------------')

print( round(
        ( football[ football.Age == football.Age.max() ].Reactions.mean() -
          football[ football.Age == football.Age.min() ].Reactions.mean() )
       , 2)
     )
print('-------------------------------------------------------')

print( football[ football.Value > football.Value.mean() ].Nationality.value_counts().idxmax() )
print('-------------------------------------------------------')

print( round(
        ( football[ football.Aggression == football.Aggression.max() ].ShotPower.mean() /
          football[ football.Aggression == football.Aggression.min() ].ShotPower.mean() )
       , 2)
     )
print('-------------------------------------------------------')
