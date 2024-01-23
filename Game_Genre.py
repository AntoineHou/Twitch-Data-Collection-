# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 10:43:00 2022

@author: antoi
"""
import requests
import json 
from igdb.wrapper import IGDBWrapper
from fuzzywuzzy import fuzz


authURL = ''
client_id ='' 
client_secret = ''

AutParams = {'client_id': client_id,
             'client_secret': client_secret,
             'grant_type': 'client_credentials'
             }

AutCall = requests.post(url=authURL, params=AutParams) 
access_token = AutCall.json()['access_token']

wrapper = IGDBWrapper(client_id,access_token )

def get_game_list(wrapper , game_name) : 
    byte_array = json.loads(wrapper.api_request(
                'games',
                'fields name, genres.*; search "{}";'.format(game_name)
              ))
    return byte_array

def find_best_match (game_name , game_list) : 
    genre=[]
    for items in game_list : 
        if items['name'].lower() == game_name.lower():
            for i in items['genres'] : 
                genre.append(i['name'])
            break     
    if len(genre) >  0 : 
        return genre
         
def find_close_match (game_name , game_list) : 
    potential = {}
    for items in game_list:
        if fuzz.partial_ratio( game_name  , items['name']) > 90 : 
            potential[items['name']] = fuzz.ratio(game_name  , items['name'])
    
    genre=[]
    for items in game_list:
        if items['name'] == sorted(potential, key=potential.get)[-1]:
             for i in items['genres'] : 
                genre.append(i['name']) 
    return genre  
            
            
