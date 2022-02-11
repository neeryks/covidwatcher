from hashlib import new
from numpy import cov
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.model_selection import learning_curve
import sklearn

### Starting ###
class dataframes():
    def covidstat():
        dframe= pd.read_csv('data/data.csv',index_col=False)
        lframe = pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/latest/owid-covid-latest.csv',index_col=False)
        inddframe = dframe[dframe['iso_code']=='IND']
        indlframe = lframe[lframe['iso_code']=='IND']
        indlframe = indlframe.rename({'last_updated_date':'date'},axis=1)
        #print(inddframe.head())


        if str(inddframe['date'].iloc[-1]) != str(indlframe['date'].iloc[0]) :
            inddframe = pd.concat([inddframe,indlframe])
            inddframe = inddframe[['iso_code','location','date','total_cases','new_cases','total_deaths','new_deaths','reproduction_rate']].dropna(axis=0)
            #print(inddframe.head(20))
            inddframe.to_csv('data/data.csv',index=False)

        return(inddframe)
    
    def vaccstat():
        vaccdata = pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/country_data/India.csv',index_col=False)
        vaccdata = vaccdata[['date','people_vaccinated']]
        vaccdata = vaccdata[1::].dropna(axis= 0)
        #print(vaccdata.head())

        return(vaccdata)

    

    new = pd.merge(covidstat(),vaccstat(),on='date',how='left')
    new.to_csv('data/new.csv')
    print(new)

fig = px.scatter(dataframes.new,x='date',y=['new_cases','new_deaths'],title='Covid Cases with the span of time')
fig.show()






    
