# -*- coding: utf-8 -*-
"""1stquestion.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tfGvTFx9dCRTkgdifZvPhgGDGXk5-Aa8
"""

import numpy as np
import pandas as pd

data = pd.read_csv('/content/drive/MyDrive/sports dataset/results.csv')

"""Checking is there any missing values in the given data set . we do not have any missing values """

data.isnull().sum()

"""

```
# This is formatted as code
```

IT contains 2 seasons already seasonID 1,2. i was asked to determine the winner of season 1. so dropping season id 2"""

data1 = data.drop(data[data.SeasonID >1].index)
data1

"""In the below code i created columns for the each teamid"""

team_ids_list = list(set(data1['HomeTeamID'].tolist()))
for each_team_id in team_ids_list:
  data1[each_team_id]=0
data1.head(5)

"""assigning 3 points to the team which won the match and assigning 1 point for the draw """

def cal_points(row):
  if row['HomeScore']> row['AwayScore']:
    row[row['HomeTeamID']]+=3
  elif row['HomeScore']< row['AwayScore']:
    row[row['AwayTeamID']]+=3
  else:
    row[row['HomeTeamID']]+=1
    row[row['AwayTeamID']]+=1
  
  return row

data1= data1.apply(cal_points,axis=1)
data1.head(10)

groupby_agg = {id_: 'sum' for id_ in team_ids_list}
groupby_agg

"""grouping the game week and summing the match points ."""

df_gameweek = data1.groupby(['Gameweek']).agg(groupby_agg).reset_index()
df_gameweek = df_gameweek.set_index('Gameweek')
df_gameweek.head(10)

"""creating a cummilative sum for the match weeks """

df_gw_cum = df_gameweek.cumsum(axis = 0)
df_gw_cum.tail(10)

df_gw_cum

teams = pd.read_csv('/content/drive/MyDrive/sports dataset/teams.csv')
teams

"""The winner of the leauge in season 1 is ID 15 which is miami

by using this logic we can determine at what stage the title is secured by the winning team 
points( a/ gw p) - points( b/ gw p ) > ( 54 - gw ) * 3 the a team  won at that match week definetly
"""

from collections import Counter
N = 54
def find_winner_by_gw(row):
  gw = Counter(dict(row))
  game_week_num = row.name
  most_common = gw.most_common(2)
  most_common_keys = [key for key, val in most_common]
  a = row[most_common_keys[0]]
  b = row[most_common_keys[1]]
  dif = a-b
  max_points = (54-game_week_num)*3
  if dif > max_points :
    row['gw_winner'] = True
  else:
    row['gw_winner'] = False

  return row

  

res = df_gw_cum.apply(find_winner_by_gw,axis=1)
res.tail(10)

res_gw = res[res['gw_winner']==1]
print( res_gw.index.to_list()[0])

"""At 50th match week the team miami won the title

code for biggest upset of the season
"""

d1 = pd.read_csv('/content/drive/MyDrive/sports dataset/odds.csv')
results = pd.read_csv('/content/drive/MyDrive/sports dataset/results.csv')

d1['gd'] = abs(results['HomeScore']- results['AwayScore'])
d1['Homeid'] = results['HomeTeamID']
d1['Awayid'] = results['AwayTeamID']
d1['homescore'] = results['HomeScore']
d1['awayscore'] = results['AwayScore']
d1

"""one way of finding out the biggest upset match is finding out the goal diffrence the matches with big goal differnce and chances of winning for both teams is almost equal.

I have added the home id and away id to the odds data set and i also have added the gd. considering home team
"""

d2 = d1.loc[d1['gd']>4]
d2

"""the above is the table of matches which have goal difference more than 5 which can be considered as big difference. team which has the low odds is most likely to win the match . and if the goals scored by that team then it is not a dissapointment or it is expected result.

from the above table the match number 465 the home and away odds ratio is almost equal i.e home- 1.95 away-3.50 but the home team won with a margin of 6 goals so the gd is bigger wrt to the other teams and the score margins
"""

from google.colab import drive
drive.mount('/content/drive')