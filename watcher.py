from base64 import encode
from os import sep
import pandas as pd
from matplotlib import pyplot as pyp
import seaborn as sns
import plotly as pl
from sklearn.model_selection import learning_curve
import sklearn

### Starting ###
dframe= pd.read_csv('data/data.csv',index_col=False)
lframe = pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/latest/owid-covid-latest.csv',index_col=False)
colu = pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-codebook.csv')
colu = colu['column'].values.tolist()
inddframe = dframe[dframe['iso_code']=='IND']
indlframe = lframe[lframe['iso_code']=='IND']
indlframe = indlframe.rename({'last_updated_date':'date'},axis=1)


if str(inddframe['date'].iloc[-1]) != str(indlframe['date'].iloc[0]) :
    inddframe = pd.concat([inddframe,indlframe])
    print(inddframe)
    inddframe.to_csv('data/data.csv',index=False)

    

