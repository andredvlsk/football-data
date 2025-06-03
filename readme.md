# Football Data Scraper (FBref)

This Python project scrapes and structures football stats from [FBref.com](https://fbref.com/en/). It collects both **team-level** and **player-level** data across multiple categories and seasons.

## Features

- Collects Premier League data from seasons **2017–18 to 2024–25**
- Supports multiple **player and team stat categories**
- Parses **HTML comments** to extract hidden tables
- Adds **random sleep** delays for responsible scraping avoiding "too many requests"
- Uses `pandas` for storing and handling data

---

### 1. Clone repository

```bash
git clone https://github.com/andredvlsk/football-data.git
```

### 2. Create a Virtual Environment (optional)

- You can create the way you prefer. I use conda.
- Check conda website for documentation on how to create venv.

[conda venv doc](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#)

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## How the Code Works

Project was divided between Team-Level Stats and Player-Level Stats

### Team-Level Stats

Using the base season URLs from FBref, the script scrapes all public HTML tables per season and stores them in a dictionary.

URL format:
https://fbref.com/en/comps/9/{season}/{season}-Premier-League-Stats

Uses pandas.read_html() to load visible HTML tables.

### Player-Level Stats

URL format:
https://fbref.com/en/comps/9/{season}/{category}/{season}-Premier-League-Stats

Target specific categories:

-Categories include:

    -Standard stats
    -Goalkeeping (basic & advanced)
    -Shooting
    -Passing & passing types
    -Goal and shot creation
    -Defensive actions
    -Possession metrics
    -Playing time
    -Miscellaneous stats

Scrapes tables within HTML comments, using BeautifulSoup and pandas.read_html.

### Output Structure

- squad_standard_stats_dict[season] → Team-level stats per season

- player_stats_dict[season][category] → Player-level stats per season and category

## Randomized Delay

To avoid overloading FBref servers, the scraper uses `time.sleep` to randomize delay before requests.

Make sure to use your own **"user-agent header"**.

## Project File Structure
```
football-data/
│
├── football-data.py         # Main script
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
└── data/                    # Output folder for CSVs
```
## Task List

- [x] Scrapping code
- [x] Premier League data import
- [ ] Export Premier League data to csv
- [ ] Clean/handle data in the dataframes
- [ ] Expand scrapping to other leagues
- [ ] ...

## Legal Notice

All data belongs to FBref.com.

## Contributions

If you want to share your ideas/improve this project, feel free to get in touch or open a pull request.

`by andredvlsk / adfsynced`