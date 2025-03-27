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

winners_list = []
for _, row in finals_df.iterrows():
    team_code = row["Team"]
    years_won_str = row["Years won"]
    if years_won_str and years_won_str != "-":
        for y in years_won_str.split(","):
            y = y.strip()
            if y.isdigit():
                winners_list.append({"Year": int(y), "Winner": team_code})
winners_df = pd.DataFrame(winners_list)

runners_list = []
for _, row in finals_df.iterrows():
    team_code = row["Team"]
    years_runners_str = row["Years runners-up"]
    if years_runners_str and years_runners_str != "-":
        for y in years_runners_str.split(","):
            y = y.strip()
            if y.isdigit():
                runners_list.append({"Year": int(y), "Runner-up": team_code})
runners_df = pd.DataFrame(runners_list)

finals_yearly_df = pd.merge(winners_df, runners_df, on="Year", how="outer")

print(finals_yearly_df)

app = dash.Dash(__name__)
server = app.server
app.title = "FIFA World Cup Dashboard"

fig_choropleth = px.choropleth(
    wins_count_df,
    locations="Team",         
    color="Wins",
    hover_name="Team",
    hover_data=["Runner ups"],
    color_continuous_scale=px.colors.sequential.Plasma,
    title="FIFA World Cup Wins by Country"
)

app.layout = html.Div([
    html.H1("FIFA World Cup Winners and Runner-ups Dashboard"),

    dcc.Graph(
        id="worldcup-choropleth",
        figure=fig_choropleth
    ),

    html.Div([
        html.Label("Select a country to view number of wins:"),
        dcc.Dropdown(
            id="country-dropdown",
            options=[{"label": code, "value": code} for code in wins_count_df["Team"].unique()],
            placeholder="Select a country"
        ),
        html.Div(id="country-wins-output", style={"marginTop": 20, "fontSize": "20px"})
    ], style={"width": "48%", "display": "inline-block", "verticalAlign": "top"}),

    html.Div([
        html.Label("Select a year to view final match result:"),
        dcc.Dropdown(
            id="year-dropdown",
            options=[{"label": str(y), "value": y} for y in sorted(finals_yearly_df["Year"].unique())],
            placeholder="Select a year"
        ),
        html.Div(id="year-result-output", style={"marginTop": 20, "fontSize": "20px"})
    ], style={"width": "48%", "display": "block", "verticalAlign": "top"})
])

@app.callback(
    Output("country-wins-output", "children"),
    Input("country-dropdown", "value")
)
def update_country_wins(selected_country):
    if selected_country:
        row = wins_count_df[wins_count_df["Team"] == selected_country]
        if not row.empty:
            wins = row["Wins"].values[0]
            runner_ups = row["Runner ups"].values[0]
            return f"{selected_country} has won the World Cup {wins} time(s) and been runner-up {runner_ups} time(s)."
        return f"No record found for {selected_country}."
    return "Select a country to see its number of wins and runner-ups."

@app.callback(
    Output("year-result-output", "children"),
    Input("year-dropdown", "value")
)
def update_year_result(selected_year):
    if selected_year:
        row = finals_yearly_df[finals_yearly_df["Year"] == selected_year]
        if not row.empty:
            winner = row["Winner"].values[0] if "Winner" in row.columns else "Unknown"
            runner_up = row["Runner-up"].values[0] if "Runner-up" in row.columns else "Unknown"
            return f"In {selected_year}, {winner} won the World Cup, defeating {runner_up}."
        else:
            return f"No data for the year {selected_year}."
    return "Select a year to view the final match result."

if __name__ == "__main__":
    app.run(debug=True)
