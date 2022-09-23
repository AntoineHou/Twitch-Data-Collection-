# -*- coding: utf-8 -*-
"""
Created on Tue Feb 15 13:58:25 2022

@author: antoi
"""
import pandas as pd 
import time 
import json 
import numpy as np
import undetected_chromedriver as uc 

df=pd.read_csv('C:/Users/antoi/Downloads/twitch_earnings.csv')

df['a']=df.a.str.lower()

n = 500  
list_df = [df[i:i+n] for i in range(0,df.shape[0],n)]


def get_link (_id) : 
    return 'https://twitchtracker.com/{}/subscribers'.format(_id)


def open_driver () : 
    driver = uc.Chrome()
    return driver 


def driver_get (driver,link) : 
    driver.get(link)
    time.sleep(6)
    

def get_data (driver) :
    data=driver.find_element_by_xpath("/html/body").text
    return data


def parse_data (data) : 
    data=data.splitlines()
    try : 
        for i in range(len(data)) : 
            if data[i] == "CURRENT ACTIVE SUBSCRIPTIONS" : 
                return data[i-1]
    except : 
        return np.nan 
        

def main ( streamer_list ):
    driver=open_driver()
    dictionnary_streamer={}
    for stream in streamer_list :
        driver_get(driver , get_link(stream))
        dictionnary_streamer[stream]= parse_data(get_data(driver))
    driver.close()
    return dictionnary_streamer

if __name__=='__main__': 
    a=0
    while a != len(list_df) : 
        d=main(list_df[a]['a'])
        with open('Twitch_Tracker_{}.json'.format(str(a)), 'w') as fp:
            json.dump(d, fp)
        a=a+1