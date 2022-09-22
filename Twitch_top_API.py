# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 10:07:46 2022

@author: antoi
"""
import requests
import pandas as pd
import json

df=pd.read_csv("twitch_earnings.csv",index_col="n")

URLI = 'https://api.twitch.tv/helix/users?login='
authURL = 'https://id.twitch.tv/oauth2/token'
Client_ID = ''
Secret  = ''

URLT = 'https://api.twitch.tv/helix/users/follows?to_id='

AutParams = {'client_id': Client_ID,
             'client_secret': Secret,
             'grant_type': 'client_credentials'
             }

def Twitch(url):
    try :
        AutCall = requests.post(url=authURL, params=AutParams)
        access_token = AutCall.json()['access_token']
        head = {
        'Client-ID' : Client_ID,
        'Authorization' :  "Bearer " + access_token
        }
        r = requests.get(url  , headers = head).json()
        return r
    except :
        return "off"
    
    
d={}

for items in df['a'].str.lower() : 
    d[items]= {"Status" : None  , "Followers" : None , 'View_Count' : None }
    

for item in df["a"].str.lower() : 
    try : 
        a=Twitch(URLI+item.lower())['data'][0]
        ID=a["id"]
        d[item]['View_Count'] = a["view_count"]
        d[item]['Status'] = a['broadcaster_type']
        d[item]['Followers'] = Twitch(URLT+ID)['total']
        print(d[item])
    except : 
        pass 
    

with open('Twitch_Top_10K.json', 'w') as fp:
    json.dump(d, fp)