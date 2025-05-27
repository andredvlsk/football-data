#%%
## Collecting football data from Premier League from fbref.com
## Packages required
import urllib
import pandas as pd
import requests
from bs4 import BeautifulSoup, Comment
from io import StringIO
import time
import random

# %%

## This function gets the url, with specific headers
## for connection, trying to avoid blocks and errors,
## we connect looking for a 429 error.
## if there is a 429 error, it will wait the retry-again header time from the server
## if there is no retry-again header time, it will try again in a uniform random interval
## Specify your own header.

headers = {"User-Agent":
           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"}

def check_connection(url, headers):
    try:
        response = urllib.request.Request(url, headers = headers)
        response_html = urllib.request.urlopen(response)
        return response_html.read()
    
    except urllib.error.HTTPError as err:
        if err.code == 429:
            print("Received 429 Too Many Requests")
            retry_after = err.headers.get("Retry-After")
            if retry_after:
                print(f"Waiting for {retry_after} seconds...")
                time.sleep(int(retry_after))
                #Retrying
                return check_connection(url)
            else:
               # Retrying with another strategy
               print("No Retry-After header. Using random uniform interval")
               time.sleep(random.uniform(5,15))
               return check_connection(url)

        else:
           print(f"HTTP error {err.code}: {err.reason}")

        return None


#%%
# Seasons we're scrapping.
seasons = ['2024-2025', '2023-2024', 
           '2022-2023', '2021-2022', 
           '2020-2021', '2019-2020',
           '2018-2019', '2017-2018']

# Retrieving information on the squads.
squad_standard_stats_dict = {}
for season in seasons:
    url = f"https://fbref.com/en/comps/9/{season}/{season}-Premier-League-Stats"
    soup = BeautifulSoup(check_connection(url, headers), "html.parser")
    squad_standard_stats_dict[season] = pd.read_html(StringIO(str(soup)))

#%%

## Checking if all tables are imported worked.
for i in squad_standard_stats_dict:
    if len(squad_standard_stats_dict[i]) == 24:
        print("CORRECT")
        print("The number of tables imported in each season is: " 
              + str(len(squad_standard_stats_dict[i]))
              + "\n")
    else:
        print("NOT CORRECT")
        print(len(squad_standard_stats_dict[i])
              + "\n")


#%%
## Connection check/waiting time for next try.
## url = "http://fbref.com/en/comps/9/2023-2024/standard/2023-2024-Premier-League-Stats"
## data = check_connection(url, headers)

##if data:
##  print("Connection ok!")
##  print(data)

#%%


## Seasons defined before

## Categories based on the website link

categories = ['stats', 'keepers',
              'keeper_adv', 'shooting',
              'passing', 'passing_types',
              'gca', 'defense', 
              'possession', 'playingtime',
              'misc']

player_stats_dict = {}
player_stats_cat_dict = {}

for season in seasons:
    for cat in categories:
        url = f"http://fbref.com/en/comps/9/{season}/{cat}/{season}-Premier-League-Stats"
        soup = BeautifulSoup(check_connection(url, headers), "html.parser")
        comments = soup.findAll(string=lambda text: isinstance(text, Comment))

        for comment in comments:
            if "stats" in comment:
                comment_soup = BeautifulSoup(comment, 'html.parser')
                table = comment_soup.find("table")

# adding the raw data in a pandas DF. id = table_search list
                player_stats_cat_dict[cat] = pd.read_html(StringIO(str(table)))
                player_stats_dict[season] = player_stats_cat_dict


#%%
print(len(player_stats_cat_dict))
print(len(player_stats_dict['2023-2024']))
print(len(player_stats_dict['2022-2023']))

#%%
player_stats_dict['2024-2025']