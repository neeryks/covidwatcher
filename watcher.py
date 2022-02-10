from email import header
from os import sep
from unittest import skip
from urllib import request
import pandas as pd
from pyparsing import col
from matplotlib import pyplot as pyp
import seaborn as sns
import plotly as pl
from sklearn.model_selection import learning_curve
import sklearn
import http

### Starting ###
dframe= pd.read_csv('data/data.csv')
lframe = pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/latest/owid-covid-latest.csv')
colu = pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-codebook.csv')
colu = colu['column'].values.tolist()
print(colu)
inddframe = dframe[dframe['iso_code']=='IND']
indlframe = lframe[lframe['iso_code']=='IND']

if str(inddframe['date'].iloc[-1]) != str(indlframe['last_updated_date'].iloc[0]) :
    indlframe = indlframe.values.tolist()
    inddframe = inddframe.append(pd.DataFrame(indlframe,columns=colu))
    print(inddframe)
    inddframe.to_csv('data/data.csv')

    

