

import pandas as pd
#from matplotlib import pyplot as plt
#import seaborn as sns
import plotly.express as px
from plotly import graph_objects as go
from plotly.subplots import make_subplots as ms
import ujson as json
from statesorter import flsorter
from multiprocessing import process


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
    #print(new)

fig = ms(rows=3,cols=2,start_cell='bottom-left',subplot_titles=("People Vaccinated agaist Covid19","Every day Covid19 Cases","Deaths Every day Due to Covid19"
,"Total Deaths Covid19","Total Cases"))
fig.add_trace(go.Scatter(x=dataframes.new['date'],y=dataframes.new['people_vaccinated'],),row=1,col=1)
fig.add_trace(go.Scatter(x=dataframes.new['date'],y=dataframes.new['new_cases']),row=1,col=2)
fig.add_trace(go.Scatter(x=dataframes.new['date'],y=dataframes.new['new_deaths']),row=2,col=1)
fig.add_trace(go.Scatter(x=dataframes.new['date'],y=dataframes.new['total_deaths']),row=2,col=2)
fig.add_trace(go.Scatter(x=dataframes.new['date'],y=dataframes.new['total_cases']),row=3,col=1)

fig.update_layout(title_text="Covid19 Related Data INDIA")
fig.show()


flsorter()
full = pd.read_csv("data/statedata/full.csv")
geojson = json.load(open('data/INDIA_STATES.json','r'))

#fig1 = px.choropleth(full,geojson='data/INDIA_STATES.json',color_continuous_scale="Viridis",featureidkey='properties.state_code',locations=full['state_code'],color=full['Active'],range_color=(0,700000),animation_frame=full['Last_Update'],title='Covid-19 Data [ INDIA ]')
fig1 = px.choropleth_mapbox(full, geojson=geojson,
                      locations='state_code', 
                      color='New Deaths',
                      color_continuous_scale="thermal",
                      range_color=(0,70000),
                      featureidkey="properties.state_code", 
                      animation_frame='Last_Update',
                      mapbox_style="carto-positron",
                      hover_data=["Confirmed","Active","Recovered","Deaths","Last_Update"],
                      hover_name="Province_State",
                      center={"lat": 23, "lon": 88},
                      opacity=1,
                      zoom=3.45)

#fig1.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 60
#fig1.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 5

fig1.update_geos(fitbounds="locations", visible=False)
fig1.show()


    
