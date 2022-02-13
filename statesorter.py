import os
import pandas as pd

dir = "data/ddata"
li = []
for fn in os.scandir(dir):
    if fn.is_file():
        if fn.path == None:
            pass
        else:
            li.append(fn.path)
    
#print(li)
count = 0
adata = pd.DataFrame(columns=['Province_State','Country_Region','Last_Update','Confirmed','Deaths','Recovered'])
for i in li :
    data = pd.read_csv(i,index_col=False)
    collist1 = data.columns.tolist()
    print(collist1)
    if collist1[2] == 'Province_State':
        data = data[['Province_State','Country_Region','Last_Update','Confirmed','Deaths','Recovered']]
    elif collist1[0] == 'Province/State':
        data = data[['Province/State','Country/Region',"Last Update",'Confirmed','Deaths','Recovered']]
        data = data.rename(columns={'Province/State':'Province_State','Country/Region':'Country_Region',"Last Update":'Last_Update',})
    #print(data.head(10))
    statelist = data[data['Country_Region']=='India']
    count = count + 1
    if count == 1:
        #print(statelist.head(20))
        statelistname = statelist['Province_State'].tolist()
        #print(statelistname)
    adata = pd.concat([adata,statelist],ignore_index=True)
for state in statelistname:
    statedata = adata[adata['Province_State']==state]
    statedata = statedata.sort_values(by='Last_Update')
    statedata.to_csv('data/statedata/{}.csv'.format(state))




