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

#%%

## use your own User-Agent here.
headers = {"User-Agent": "Use your own"}

## Seasons that are being fetch.
seasons = ['2024-2025','2023-2024', 
           '2022-2023', '2021-2022', 
           '2020-2021', '2019-2020',
           '2018-2019', '2017-2018']

## categories that are being fetch for player stats, based on the url.
categories = ['stats', 'keepers',
              'keeper_adv', 'shooting',
              'passing', 'passing_types',
              'gca', 'defense', 
              'possession', 'playingtime',
              'misc']

## Adding random time intervals for request.
def check_connection(url, headers = headers):
    time.sleep(random.uniform(5,88))
    response = urllib.request.Request(url, headers = headers)
    response_html = urllib.request.urlopen(response)
    return response_html.read()

#%%

## Function that receives a list of strings (seasons) and loop
## requesting team stats data by season.
## Finally saves raw data in csv.

def squad_scrapping(seasons:list):

    squad_standard_stats_dict = {}

    for season in seasons:
        url = f"https://fbref.com/en/comps/9/{season}/{season}-Premier-League-Stats"
        soup = BeautifulSoup(check_connection(url, headers), "html.parser")
    
        # adding the raw data in a dataframe
        squad_standard_stats_dict[season] = pd.read_html(StringIO(str(soup)))

    return squad_standard_stats_dict

#%%
raw_data = squad_scrapping(seasons)

#%%
## Defining function for player_stats

player_stats_dict = {}
player_stats_cat_dict = {}

for season in seasons:
    for cat in categories:
        url = f"http://fbref.com/en/comps/9/{season}/{cat}/{season}-Premier-League-Stats"
        soup = BeautifulSoup(check_connection(url, headers = headers), "html.parser")
        comments = soup.findAll(string=lambda text: isinstance(text, Comment))

        for comment in comments:
            if "stats" in comment:
                comment_soup = BeautifulSoup(comment, 'html.parser')
                table = comment_soup.find("table")

        # adding the raw data in a dict.
                player_stats_cat_dict[cat] = pd.read_html(StringIO(str(table)))
                player_stats_dict[season] = player_stats_cat_dict