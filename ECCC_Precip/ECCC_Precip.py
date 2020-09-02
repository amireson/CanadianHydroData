# Library of functions to list, download and save ECCC Precipitation data
# Andrew Ireson
# 17-March-2020

import pandas as pd
import matplotlib.pyplot as pl
import numpy as np

def StationList():
    return pd.read_csv('ECCC_Precip/Station Inventory EN.csv',skiprows=3)

def SearchByProvince(SearchTerm,stations):
    provs=stations['Province']
    i=[count for count, prov in enumerate(provs) if SearchTerm.lower() in prov.lower()]
    provsfound=sorted(set(provs[i]))
    if len(provsfound)>1: 
        print('Multiple provinces found - consider improving your search term')
        print('%d stations found'%(len(stations.iloc[i])))
    elif len(provsfound)==0:
        print('No provinces found - improve your search term')
    else:
        print('%d stations found in province %s'%(len(stations.iloc[i]),provsfound[0]))
      
    return stations.iloc[i]

def SearchByName(SearchTerms,stations):
    names=stations['Name']
    i=[]
    for SearchTerm in SearchTerms:
        j=[count for count, name in enumerate(names) if SearchTerm.lower() in name.lower()]
        if i==[]:
            i=j
        else:
            i=[ind for ind in j if ind in i]
    
    PrintSummary(stations.iloc[i])
    return stations.iloc[i]

def PrintSummary(stations):
    print('%d stations found'%len(stations))
    print(38*' '+'Station name:   Station ID     From  To ')
    for a,b,c,d in zip(stations['Name'],stations['Station ID'],stations['First Year'],stations['Last Year']): print('%50s:   %s           %d  %d'%(a,b,c,d))
        
def GetURL(StationID,Year):
    url_template='https://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID=XXX_StationID&Year=XXX_Year&timeframe=2&submit=%20Download+Data'
    MyURL=url_template.replace('XXX_StationID',StationID)
    MyURL=MyURL.replace('XXX_Year','%04d' % Year)
    return MyURL

def PreviewData(StationID,Year):
    print("downloading %4d" % Year)
    df=GetDataFrame(GetURL(StationID,Year))
    print(df.head())
    return 

def GetDataFrame(MyURL):
    df=pd.read_csv(MyURL, index_col='Date/Time', parse_dates=True, encoding='latin1')
    return df

def GetAllData(StartYear,EndYear,StationID):
    Years = np.arange(StartYear,EndYear+1)
    print("downloading %4d" % StartYear)
    df=GetDataFrame(GetURL(StationID,Years[0]))
    weather=df[['Total Rain (mm)','Total Snow (cm)','Total Precip (mm)']]
    n=len(Years)
    for i in range(1,n):
        print("downloading %4d" % Years[i])
        df=GetDataFrame(GetURL(StationID,Years[i]))
        df=df[['Total Rain (mm)','Total Snow (cm)','Total Precip (mm)']]
        weather=pd.concat([weather,df])
    return weather
