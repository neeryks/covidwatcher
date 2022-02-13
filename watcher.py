
from matplotlib import animation
from matplotlib.pyplot import title
import pandas as pd
#from matplotlib import pyplot as plt
#import seaborn as sns
import plotly.express as px
from plotly import graph_objects as go
from plotly.subplots import make_subplots as ms


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

fig = ms(rows=3,cols=2,start_cell='bottom-left',subplot_titles=("People Vaccinated agaist Covid19","Every day Covid19 Cases","Deaths Every day Due to Covid19"
,"Total Deaths Covid19","Total Cases"))
fig.add_trace(go.Scatter(x=dataframes.new['date'],y=dataframes.new['people_vaccinated'],),row=1,col=1)
fig.add_trace(go.Scatter(x=dataframes.new['date'],y=dataframes.new['new_cases']),row=1,col=2)
fig.add_trace(go.Scatter(x=dataframes.new['date'],y=dataframes.new['new_deaths']),row=2,col=1)
fig.add_trace(go.Scatter(x=dataframes.new['date'],y=dataframes.new['total_deaths']),row=2,col=2)
fig.add_trace(go.Scatter(x=dataframes.new['date'],y=dataframes.new['total_cases']),row=3,col=1)

fig.update_layout(title_text="Covid19 Related Data INDIA")
fig.show()



    
