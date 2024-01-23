# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 15:28:47 2022

@author: antoi
"""
import json
import requests
import pandas as pd
from pandas.io.json import json_normalize
import random 
from sympy.solvers import solve
from sympy import Symbol

client_id= ""
client_secret= ""
access_code = requests.post(("https://id.twitch.tv/oauth2/token?client_id={}&client_secret={}&grant_type=client_credentials").format(client_id, client_secret))
access_token = json.loads(access_code.text)
access_token = access_token['access_token']
headers = {'client-id':client_id,'Authorization': 'Bearer '+access_token}
url="https://api.twitch.tv/helix/streams?first=100&game_id="

#Lists if you wish to delete some specific games or categories  
categories_to_delete = []


def get_top_games () : 
    games_response = requests.get('https://api.twitch.tv/helix/games/top?first=100', headers=headers)
    
    games_response_json = json.loads(games_response.text)
    topgames_data = games_response_json['data']
    topgames_df = pd.DataFrame.from_dict(json_normalize(topgames_data), orient='columns')
    return topgames_df


def get_top_games_streamers (topgames_df) : 
    list_df={}
        
    for games in topgames_df.iterrows() :
        a=games[1]["id"]
        r=requests.get(url+a,headers=headers) 
        r=r.json()
        r=r["data"]
        d=pd.DataFrame(r)
    
        list_df[games[1]["name"]]=d
    reform = {(outerKey, innerKey): values for outerKey, innerDict in list_df.items() for innerKey, values in innerDict.items()}
    df=pd.DataFrame.from_dict(reform, orient='index').transpose()
    df.columns = pd.MultiIndex.from_tuples(df.columns)
    list_games=list(topgames_df["name"])
    return df , list_games

def clean_df (df , list_games) :
    if len(categories_to_delete) > 0 : 
        games_to_keep = [x for x in list_games if x not in categories_to_delete]
        df=df.iloc[:, df.columns.get_level_values(0).isin(games_to_keep) ]
    return df , list_games        
                
def create_random_sample (df , list_games  , sample_size) :
    x = Symbol('x')
    n_streamer_per_game = int(solve(x*len(list_games) - sample_size , x )[0])
    random_streamer_sample = []
    for games in list_games: 
        list_streamer_game  = list(df[games]['user_name'])
        list_streamer_game = [x for x in list_streamer_game if str(x) != 'nan']
        if len(list_streamer_game) > 10 :
            random_streamer_sample.extend(random.sample(list_streamer_game, n_streamer_per_game))
    return random_streamer_sample 

def main () : 
    topgames_df = get_top_games()
    df , list_games = get_top_games_streamers(topgames_df)
    df , list_games = clean_df( df ,   list_games)
    sample_size  = int(input( 'Input the sample size you want : ') )
    random_streamer_sample = create_random_sample (df , list_games , sample_size )
    with open('random_streamers.txt', mode='wt', encoding='utf-8') as myfile:
        myfile.write('\n'.join(random_streamer_sample))

if __name__ == "__main__":
    main()
    
