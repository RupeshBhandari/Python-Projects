import pandas as pd
import numpy as np


## Creating series data structure


my_data = ['Boat', 'test1', 'test222']
series = pd.Series(my_data)

### Checking data types
print(series)

my_data = [1, 2, 3, 4, 5]
series = pd.Series(my_data)


### Checking data types
print(series)


## DataFrames

my_data = [['chen', 1], ['zhew', 2], ['ada', 3]]

df = pd.DataFrame(my_data, columns = ['Name', 'Age'])

print(df)

### Checking data types
print(df.dtypes)


## Reading in Data

df = pd.read_csv('.\MrBeast_youtube_stats.csv')

print(df.head())