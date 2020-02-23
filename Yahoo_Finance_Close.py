from bs4 import BeautifulSoup
import requests
import csv 
import pandas as pd 
from datetime import datetime

prices=[]
df = pd.DataFrame(columns = ['underlying', 'time', 'spot', 'change',
                             'prev_close', 'open', 'volume', 
                             'avg_volume'])
df_url = pd.read_csv('RefLevels.csv')

for und in df_url.Underlying.unique().tolist():
    Url = df_url[df_url.Underlying == und].iloc[0,-1:].iloc[0]
    print(Url)
    r= requests.get(Url)
    data=r.text
    soup=BeautifulSoup(data)
    
    for name in soup.find_all('h1', attrs={'class':'D(ib)'}):
        prices.append(name.text)
        #for time in soup.find_all('div', attrs = {'class':'C($tertiaryColor)'}):
        for time in soup.find_all('div', attrs = {'id':'quote-market-notice'}):
            print(time.text)
            prices.append(time.text)
        for row in soup.find_all('span', attrs = {'class': 'Trsdu(0.3s)'}):
            #print(row)
            for price in row:
                #print(price)
                prices.append(price)
                #print(prices)
        
    df.loc[len(df)] = prices
    prices=[]

df.to_csv('RefLevels_Corridor_' + str(datetime.now().strftime("%Y%m%d%H%M%S")) + '.csv')
