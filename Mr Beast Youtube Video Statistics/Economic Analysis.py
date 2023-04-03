import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

# plt.style.use('fivethirtyeight')
# pd.set_option('max_columns', 500)
# color_pal = plt.rcParamas['axes.prop_cycle'].by_key()['color']
from fredapi import Fred

fred_key = 'f16c75b70435294b649e7a3bd0b95f9b'


##  Create the Fred Object

fred = Fred(api_key= fred_key)  

## Search for economic data!

print(fred.search('S&P'))

sp_search = fred.search('S&P', order_by= 'popularity')

## Pull Raw Data   
sp500 = fred.get_series(series_id = 'SP500')

sp500.plot()