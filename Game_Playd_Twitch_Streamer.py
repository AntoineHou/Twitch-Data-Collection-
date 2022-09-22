# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 14:24:03 2022

@author: antoi
"""

import pandas as pd 
from bs4 import BeautifulSoup
import re 
import requests
from random import sample
import time 
from datetime import datetime
import json
import csv

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

df=pd.read_csv('top_0_10k.csv', index_col=[0,1])
df_earnings = pd.read_csv('twitch_earnings.csv')
list_streamer=list(set(df.transpose().columns.get_level_values('Channel name')))

df_earnings.a=df_earnings.a.str.lower()
df_earnings=df_earnings[df_earnings.a.isin (list_streamer)]

list_streamer = list(df_earnings.a)

url = 'https://twitchstats.net/streamer/{}'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

streamer_game={}

for names in list_streamer : 
    try : 
        games=[]
        r = requests.get(url.format(names ), headers=headers)
        time.sleep(1)
        if 'NO DATA' in str(r.content) : 
            pass 
        else : 
            soup = BeautifulSoup(r.text,"html.parser")
            n=str(soup.find_all('div' , 'progress-bar'))
            n=n.split('</a></div>')
            counter=0
            while counter != 5 : 
                try : 
                    t = find_between(str(n[counter]) , '<span class="barplayed">' , '</span>')
                    if int(re.findall(r'\d+', t)[0])> 0 and  find_between(str(n[counter]) , '<img alt="' ,'" class="lazy" ') not in games :
                        games.append(find_between(str(n[counter]) , '<img alt="' ,'" class="lazy" '))
                    elif int(re.findall(r'\d+', t)[0])> 12 and  find_between(str(n[counter]) , '<img alt="' ,'" class="lazy" ') not in games : 
                        games.append(find_between(str(n[counter]) , '<img alt="' ,'" class="lazy" '))
                    else : 
                        pass 
                    counter += 1
                except IndexError: 
                    counter += 1
        streamer_game[names] = games[:5]
        print(names , streamer_game[names] )
    except : 
        pass 
    
         
with open("twtitch_streamer_games_sampled.json", "w") as outfile:
    json.dump(streamer_game, outfile)
