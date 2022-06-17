

import pandas as pd
#from matplotlib import pyplot as plt
#import seaborn as sns
import plotly.express as px
from plotly import graph_objects as go
from plotly.subplots import make_subplots as ms
import ujson as json
from statesorter import flsorter
from multiprocessing import process
import plotly.express as px

### Starting ###
class dataframes():
    def __init__(self) -> None:
        pass
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
def scatter():
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

dir = "data/ddata"
li = []
for fn in os.scandir(dir):
    if fn.is_file():
        if fn.path == None:
            pass
        else:
            li.append(fn.path)
    
#print(li)
###########################################################################################################################
def swsorter(li):
    count = 0
    adata = pd.DataFrame(columns=['Province_State','Country_Region','Last_Update','Confirmed','Deaths','Recovered'])
    for i in li :
        data = pd.read_csv(i,index_col=False)
        collist1 = data.columns.tolist()
        #print(collist1)
        if collist1[2] == 'Province_State':
            data = data[['Province_State','Country_Region','Last_Update','Confirmed','Deaths','Recovered','Active']]
        elif collist1[0] == 'Province/State':
            data = data[['Province/State','Country/Region',"Last Update",'Confirmed','Deaths','Recovered']]
            data = data.rename(columns={'Province/State':'Province_State','Country/Region':'Country_Region',"Last Update":'Last_Update',})
        #print(data.head(10))
        statelist = data[data['Country_Region']=='India']
        adata = pd.concat([adata,statelist],ignore_index=True)
        fulllist = adata.sort_values(by='Province_State')
        count = count + 1
        if count == 1:
            #print(statelist.head(20))
            statelistname = statelist['Province_State'].tolist()
            #print(statelistname)
    ################### Adding New Deaths & Cases Column ################
    newcases = fulllist['Confirmed'].tolist() 
    newcases1 = fulllist["Confirmed"].tolist()
    newcases1.insert(0,0)
    newdeath = fulllist['Deaths'].tolist()
    newdeath1 = fulllist['Deaths'].tolist()
    newdeath1.insert(0,0)
    new_cases = []
    new_deaths =[]
    zip1 = zip(newcases1,newcases)
    zip2 = zip(newdeath1,newdeath)
    for zi1_1,zi1_2 in zip1:
        new_cases.append(zi1_1 - zi1_2)
    for zi2_1,zi2_2 in zip2:
        new_deaths.append(zi2_1-zi2_2)
    
    ###Adding to Dataframe ###########
    fulllist['New Cases'] = new_cases
    fulllist["New Deaths"] = new_deaths
    ##################################
    for state in statelistname:
        statedata = fulllist[fulllist['Province_State']==state]
        statedata = statedata.sort_values(by='Last_Update')
        statedata.to_csv('data/statedata/{}.csv'.format(state),index=False)

    return fulllist
#########################################################################################################################
def flsorter():
    state_codedict={'Province_State':['Andaman and Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh',
    'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh', 'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa', 
    'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep', 
    'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 
    'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Unknown', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal'],
    'state_code':[35,37,12,18,10,4,22,26,7,30,24,6,2,1,20,29,32,38,31,23,27,14,17,15,13,21,34,3,8,11,33,36,16,97,9,5,19]}
    #print(len(state_codedict))
    sc = pd.DataFrame.from_dict(state_codedict)

    #print(sc)
    full= pd.merge(swsorter(li),sc,on='Province_State',how='left')
    full = full.sort_values(by='Last_Update')
    #print(full.head(20))
    col = np.array(full['state_code'],np.int64)
    full['state_code']=col
    full = full[full['Province_State'].notna()]
    fulldate = full['Last_Update'].tolist()
    for fu in fulldate:
        n = fu.split(" ")[0]
        full['Last_Update']= full['Last_Update'].replace(fu,n)
    full = full.drop(['Country_Region'],axis=1)
    full.to_csv('data/statedata/full.csv',index=False)
    print('Latest Save Done')
    return full


#fig1 = px.choropleth(full,geojson='data/INDIA_STATES.json',color_continuous_scale="Viridis",featureidkey='properties.state_code',locations=full['state_code'],color=full['Active'],range_color=(0,700000),animation_frame=full['Last_Update'],title='Covid-19 Data [ INDIA ]')
def coro():    
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
def bp():
    rp = px.bar(full,full['Province_State'],full['Confirmed'],full['Last_Update'])
    rp.plot(item_label="Confirmed Cases Covid-19 India",value_label="Population",frame_duration=600)

bp()
    
