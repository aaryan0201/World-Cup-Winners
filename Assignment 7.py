# Published dashboard: https://your-deployed-dashboard-url (Password: yourpassword)
# CP 321 – Data Visualization Assignment 7

import re
import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

url = "https://en.wikipedia.org/wiki/List_of_FIFA_World_Cup_finals"
tables = pd.read_html(url)

finals_df = None
for table in tables:
    cols = [str(col) for col in table.columns]
    if "Years won" in cols and "Team" in cols and "Years runners-up" in cols:
        finals_df = table
        break

country_iso = {
    "Uruguay": "URY",
    "Argentina": "ARG",
    "Italy": "ITA",
    "Czechoslovakia": "TCH",
    "Hungary": "HUN",
    "Brazil": "BRA",
    "Sweden": "SWE",
    "Germany": "DEU",
    "England": "GBR",
    "Netherlands": "NLD",
    "France": "FRA",
    "Spain": "ESP",
    "Croatia": "HRV"
}
finals_df["Team"] = finals_df["Team"].map(country_iso)

print(finals_df)

wins_count_df["Team"] = finals_df["Team"]
wins_count_df["Wins"] = finals_df["Winners"]
wins_count_df["Runner ups"] = finals_df["Runners-up"]

print(wins_count_df)

