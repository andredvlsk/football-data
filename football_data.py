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
headers = {"User-Agent":
           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"}

def check_connection(url, headers = headers):
    time.sleep(random.uniform(5,88))
    response = urllib.request.Request(url, headers = headers)
    response_html = urllib.request.urlopen(response)
    return response_html.read()

#%%
headers = {"User-Agent":
           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"}

# Seasons we're scrapping.
seasons = ['2024-2025','2023-2024', 
           '2022-2023', '2021-2022', 
           '2020-2021', '2019-2020',
           '2018-2019', '2017-2018']

squad_standard_stats_dict = {}

for season in seasons:
    url = f"https://fbref.com/en/comps/9/{season}/{season}-Premier-League-Stats"
    soup = BeautifulSoup(check_connection(url, headers = headers), "html.parser")
    
    # adding the raw data in a dataframe
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

## Defining header for this extraction.
headers = {"User-Agent":
           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"}


## Categories based on the website link
categories = ['stats', 'keepers',
              'keeper_adv', 'shooting',
              'passing', 'passing_types',
              'gca', 'defense', 
              'possession', 'playingtime',
              'misc']

## Defining seasons to fetch data.
seasons = ['2024-2025', '2023-2024', 
           '2022-2023', '2021-2022', 
           '2020-2021', '2019-2020',
           '2018-2019', '2017-2018']


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

        # adding the raw data in a dataframe
                player_stats_cat_dict[cat] = pd.read_html(StringIO(str(table)))
                player_stats_dict[season] = player_stats_cat_dict

#%%

print(len(player_stats_dict))
print(len(player_stats_cat_dict))