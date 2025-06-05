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
import copy

#%%

## use your own User-Agent here.
headers = {"User-Agent": "Use your own"}

## Seasons that are being fetch.
seasons = ['2024-2025', '2023-2024', 
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
    time.sleep(random.uniform(3,88))
    response = urllib.request.Request(url, headers = headers)
    response_html = urllib.request.urlopen(response)
    return response_html.read()

#%%

## Funcition for squad stats scrapping

def squad_scrapping(seasons:list):

    squad_standard_stats_dict = {}

    for season in seasons:
        url = f"https://fbref.com/en/comps/9/{season}/{season}-Premier-League-Stats"
        soup = BeautifulSoup(check_connection(url, headers), "html.parser")
    
        # adding the raw data in a dataframe
        squad_standard_stats_dict[season] = pd.read_html(StringIO(str(soup)))

    return squad_standard_stats_dict

raw_data_squad = squad_scrapping(seasons)

#Copying dictionary to avoid changing raw data.
data = copy.deepcopy(raw_data_squad)

#%%

## Cleaning squad data and exporting to .csv

folderPL = ".\\data\\squad_stats\\PL"

def squad_clean_export(data, folder:str):

    tables_names_list = ['overall', 'home_away',
                     'stats', 'stats_vs',
                     'keepers','keepers_vs',
                     'keeper_adv','keepers_adv_vs',
                     'shooting','shooting_vs',
                     'passing','passing_vs',
                     'passing_types','passing_types_vs',
                     'gca','gca_vs',
                     'defense','defense_vs',
                     'possession','possession_vs',
                     'playingtime','playingtime_vs',
                     'misc', 'misc_vs']
    
#Cleaning and organizing headers and saving tables in .csv
    for key in data:
        for i in range(0, len(data[key])):
        #checking for MultiIdex in the headers and cleaning/organizing.
            if isinstance(data[key][i].columns, pd.MultiIndex):
                data[key][i].columns = [' '.join(col).strip() for col in data[key][i].columns.values]
                data[key][i].columns = data[key][i].columns.str.replace(r".*level\w\w\s", "", regex = True)
            else:
                data[key][i].columns = data[key][i].columns
        ## Saving to csv.
            data[key][i].to_csv(f"{folder}\\PL_{key}_{tables_names_list[i]}.csv", sep=',', header = True)

squad_clean_export(data = data, folder = folderPL)

#%%
## Defining function for player_stats

def player_scrapping(seasons:list, categories:list):

    player_stats_dict = {}

    for season in seasons:

        player_stats_cat_dict = {}

        for cat in categories:
            url = f"http://fbref.com/en/comps/9/{season}/{cat}/{season}-Premier-League-Stats"
            soup = BeautifulSoup(check_connection(url, headers = headers), "html.parser")
            comments = soup.findAll(string=lambda text: isinstance(text, Comment))

            for comment in comments:
                if "stats" in comment:
                    comment_soup = BeautifulSoup(comment, 'html.parser')
                    table = comment_soup.find("table")

                    player_stats_cat_dict[cat] = pd.read_html(StringIO(str(table)))
            player_stats_dict[season] = player_stats_cat_dict
       
    return player_stats_dict

raw_data_player = player_scrapping(seasons, categories)

#%%
## Cleaning player data and exporting to .csv

player_data = copy.deepcopy(raw_data_player)

for key in player_data:
    for cat in categories:

        # Checking for MultiIdex in the headers and organizing.
        if isinstance(player_data[key][cat][0].columns, pd.MultiIndex):
            player_data[key][cat][0].columns = [' '.join(col).strip() for col in player_data[key][cat][0].columns.values]
            player_data[key][cat][0].columns = player_data[key][cat][0].columns.str.replace(r".*level\w\w\s", "", regex = True)
        else:
            player_data[key][cat][0].columns = player_data[key][cat][0].columns
        
        # Dropping column "Matches" in all categories
        # This column has no information
        if "Matches" in player_data[key][cat][0].columns:
            player_data[key][cat][0].drop("Matches", axis = 1, inplace = True)
        else:
            player_data[key][cat][0].columns = player_data[key][cat][0].columns

        # Cleaning rows with no player information.
        # Rows in the scrapping that are the same as header
        header_df = list(player_data[key][cat][0].columns)
        set_header_df = set(header_df)
        index_list_row_remove = []

        for i in range(0, len(player_data[key][cat][0])):
            row = list(player_data[key][cat][0].iloc[i])
            set_row = set(row)
            if set_row.intersection(set_header_df):
                index_list_row_remove.append(i)
            else:
                continue

        player_data[key][cat][0].drop(index_list_row_remove, inplace = True)
        player_data[key][cat][0] = player_data[key][cat][0].reset_index(drop = True)

        ## Saving data to csv.
        player_data[key][cat][0].to_csv(f".\\data\\player_stats\\PL\\PL_{key}_{cat}.csv", sep=',', header = True)
