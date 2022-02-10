import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import plotly as pl
from sklearn.model_selection import learning_curve
import sklearn

### Starting ###
dframe= pd.read_csv('data/data.csv',index_col=False)
lframe = pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/latest/owid-covid-latest.csv',index_col=False)
inddframe = dframe[dframe['iso_code']=='IND']
indlframe = lframe[lframe['iso_code']=='IND']
indlframe = indlframe.rename({'last_updated_date':'date'},axis=1)


if str(inddframe['date'].iloc[-1]) != str(indlframe['date'].iloc[0]) :
    inddframe = pd.concat([inddframe,indlframe])
    inddframe = inddframe[['iso_code','location','date','total_cases','new_cases','total_deaths','new_deaths','reproduction_rate']].dropna(axis=0)
    print(inddframe.head(20))
    inddframe.to_csv('data/data.csv',index=False)

sns.relplot(data=inddframe,x=inddframe['date'],y=inddframe['new_deaths'],sizes=(15,200),size='reproduction_rate')
plt.show()

    
