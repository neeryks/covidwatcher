import os
from unittest import skip
import numpy
import pandas as pd
import numpy as np

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



flsorter()






