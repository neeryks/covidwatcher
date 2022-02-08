from email import header
from os import sep
from unittest import skip
import pandas as pd
from pyparsing import col
from matplotlib import pyplot as pyp
import seaborn as sns
import plotly as pl
from sklearn.model_selection import learning_curve
import sklearn

### Starting ###
dframe= pd.read_csv('data/owid-covid-data.csv')
ldata = pd.read_csv('https://github.com/owid/covid-19-data/blob/master/public/data/latest/owid-covid-latest.csv')
inddf = dframe[dframe['iso_code']=='IND']
ldata = ldata[ldata['iso_code']=='IND']
print(ldata,inddf)
if inddf['Date'].iloc[-1] == ldata['Date']:
    pass
elif inddf['Date'].iloc[-1] != ldata['Date']:
    dframe = pd.concat(inddf,ldata)
    dframe.to_csv('data/owid-covid-data.csv')


print(dframe)
