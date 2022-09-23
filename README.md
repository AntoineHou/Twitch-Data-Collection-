# Twitch-Data-Collection

Collection of scripts related to the Twitch platform data written in the framework of the INDICIES project.

# Files

# Files

The repository is composed of different python script allowing to reproduce the data collection. 
The scripts allow to gather data from different sources both via API and web scrapping but do not contain the relevant key and proxy to conduct future collection. 
Most scripts take the top 10 000 streamers (ranked by revenue) leaked list as input. The list wont be provided here. 

## Script description 

 - **Twitch_top_API.py**  : Script allowing, for a given list of streamer, to collect the current number of View, Followers as well the streamer status (ergo the deal the streamer has with the platform). Returns a dataframe containing the streamers names and the relevant information. 
 - **Random_sample_creation.py** : A script, using the Twitch API, allowing to create a random sample of streamer. The script collects the name of streamers currently online, excludes the one in a defined list, and randomly select a sample. 
 - **Game_Playd_Twitch_Streamer.py** : Script allowing, for a given list of streamer, to scrap the twitchstats.net database for the game played by the streamer. Return for each streamer all the game played (for at least an hour over the course of a year) over the 2019-2021 period. 
 - **Scrapp_Twitch_URL** : Script allowing to collect the URL present in the Twitch streamer description. From the URL to the different description page return a set of generic URL present. 
 - **Streamers_Subscribers.py** : Scirpt allowing to collect the current number of paying subscribers from the https://twitchtracker.com/ website. The script scrapp the website and returns the number of subscribers if the information is present.
 - **Game_Genre.py** : Scrit which using Twitch API allows, for a list of game, to gather the genre of the games. Matches every game name scrapped to a game present in the database and for every game returns a list of associeted genre.
