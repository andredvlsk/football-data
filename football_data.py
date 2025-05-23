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

# Global
headers = {"User-Agent":
           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"}

# Seasons with information.
seasons = ['2023-2024', '2022-2023', 
           '2021-2022', '2020-2021',
           '2019-2020', '2018-2019',
           '2017-2018']

#%%

# Retrieving information on the squads.
squad_standard_stats_dict = {}
for season in seasons:

    #url with information from the league status
    url = f"https://fbref.com/en/comps/9/{season}/{season}-Premier-League-Stats"

    #fetching page information using a header and html code and parse data
    request = urllib.request.Request(url, headers=headers)
    response_html = urllib.request.urlopen(request)
    
    soup = BeautifulSoup(response_html.read(), "html.parser")

    # This code takes the stats tables from the squads
    # Squad standard stats and squad against stats.
    # Wrapping under StringIO
    # 24 tables
    # all 24 tables, from 0 to 23 index are inside the dictionary
    # each key is the season year
    # each item is the list of DF correspondent to the 23 tables with information on the squads

    squad_standard_stats_dict[season] = pd.read_html(StringIO(str(soup)))


#%%
for i in squad_standard_stats_dict:
    print(len(squad_standard_stats_dict[i]))


#%%

table_search = ['stats_standard', 'stats_keeper',
                'stats_keeper_adv', 'stats_shooting',
                'stats_passing', 'stats_passing_types',
                'stats_gca', 'stats_defense', 
                'stats_possession', 'stats_playing_time',
                'stats_misc']

#url for players
url = "http://fbref.com/en/comps/9/2023-2024/keepers/2023-2024-Premier-League-Stats"

request = urllib.request.Request(url, headers=headers)
response_html = urllib.request.urlopen(request)

soup = BeautifulSoup(response_html.read(), "html.parser")

# Some of the desired tables are under comments in the HTML code
# finding the comments
comments = soup.findAll(string=lambda text: isinstance(text, Comment))

# Search for the comment that contains the desired table:
for comment in comments:
#this is where switching the tables is possible
    if "stats" in comment:
        comment_soup = BeautifulSoup(comment, 'html.parser')
        table = comment_soup.find("table")


# adding the raw data in a pandas DF. id = 'stats_standard'
player_standard_stats = pd.read_html(StringIO(str(table)))

#%%
player_standard_stats


#%%

#table_search = ['stats_standard', 'stats_keeper',
#                'stats_keeper_adv', 'stats_shooting',
#                'stats_passing', 'stats_passing_types',
#                'stats_gca', 'stats_defense', 
#                'stats_possession', 'stats_playing_time',
#                'stats_misc']

#url for players
#%%

## This function gets the url, with specific headers for connection
## and tries the connectcion for a 429 error.
## if there is a 429 error, it will wait the retry-again header time
## if there is no retry-again header time, it will try again in t_seconds parameter

#%%

def fetch_url(url, headers):
    try:
        response = urllib.request.Request(url, headers = headers)
        response_html = urllib.request.urlopen(response)
        return response_html.read()
    
    except urllib.error.HTTPError as e:
        if e.code == 429:
            print("Received 429 Too Many Requests")
            retry_after = e.headers.get("Retry-After")
            if retry_after:
                print(f"Waiting for {retry_after} seconds...")
                time.sleep(int(retry_after))
                return fetch_url(url)  # Retry after waiting
            else:
               # Implement exponential backoff or other retry logic here
               print("No Retry-After header. Implementing backoff or other strategy")
               # Example of waiting for 1 second before retrying
               time.sleep(random.uniform(5,15))
               return fetch_url(url) # Retry

        else:
           print(f"HTTP error {e.code}: {e.reason}")

        return None  # Or handle other errors as needed


#%%
url = "http://fbref.com/en/comps/9/2023-2024/standard/2023-2024-Premier-League-Stats"
data = fetch_url(url, headers)

if data:
  print("Successfully fetched data!")
  print(data)

#%%

player_stats_dict = {}
player_stats_cat_dict = {}

categories = ['stats', 'keepers',
              'keeper_adv', 'shooting',
              'passing', 'passing_types',
              'gca', 'defense', 
              'possession', 'playingtime',
              'misc']

seasons = ['2023-2024', '2022-2023'] 
#           '2021-2022', '2020-2021',
#           '2019-2020', '2018-2019',
#           '2017-2018']

#%%

for season in seasons:
    for cat in categories:

        url = f"http://fbref.com/en/comps/9/{season}/{cat}/{season}-Premier-League-Stats"

        #request = urllib.request.Request(url, headers=headers)
        #response_html = urllib.request.urlopen(request)
        #response_read = response_html.read()

        soup = BeautifulSoup(fetch_url(url, headers), "html.parser")

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
player_stats_dict['2023-2024']['shooting'][0]