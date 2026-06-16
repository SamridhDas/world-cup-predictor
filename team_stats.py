import pandas as pd
def tournament_weight(tournament):

    weights = {
        "Friendly": 1,
        "UEFA Nations League": 1.5,
        "FIFA World Cup qualification": 2,
        "UEFA Euro qualification": 2,
        "Copa América": 3,
        "UEFA Euro": 3,
        "FIFA World Cup": 5
    }

    return weights.get(tournament, 2)
 
 
#getting the teams and elo 
 
df = pd.read_csv("data/results.csv")
df["date"]=pd.to_datetime(df["date"])
df=df[df["date"]>="2018-01-01"]
df = df.dropna(
    subset=[
        "home_score",
        "away_score"
    ]
)
teams=set(df["home_team"]).union(set(df["away_team"]))
 
 
elo_df = pd.read_csv("data/eloratings.csv")
 
 
#getting team stats
 
team_stats=[]
for team in teams:
    home_matches=df[df["home_team"]==team]
    away_matches=df[df["away_team"]==team]
    matches_played=(len(home_matches)+len(away_matches))
 
    wins=0
    draws=0
    losses=0
    goals_scored=0
    goals_conceded=0
 
    for _,match in home_matches.iterrows():
        weight = tournament_weight(
            match["tournament"]
        )
        if match["home_score"]>match["away_score"]:
            wins+=weight
        elif match["home_score"]<match["away_score"]:
            losses+=weight
        else:
            draws+=weight
        goals_scored+=match["home_score"]
        goals_conceded+=match["away_score"]

    
    for _,match in away_matches.iterrows():
        if match["home_score"]<match["away_score"]:
            wins+=1
        elif match["home_score"]>match["away_score"]:
            losses+=1
        else:
            draws+=1
        goals_scored+=match["away_score"]
        goals_conceded+=match["home_score"]
        
    
    goals_per_game=goals_scored/matches_played
    goals_conceded_per_game=goals_conceded/matches_played
    win_rate = wins / matches_played
 
    #Recent Form
 
    team_matches=df[(df["home_team"]==team) | (df["away_team"]==team)]
    team_matches = team_matches.sort_values(by="date",ascending=False)
    recent_matches = team_matches.head(10)
    recent_form=""
    form_score=0
    for _, match in recent_matches.iterrows():
        weight = tournament_weight(
            match["tournament"]
        )
        if match["home_team"] == team:
            if match["home_score"] > match["away_score"]:
                recent_form += "W"
                form_score += 3*weight
            elif match["home_score"] == match["away_score"]:
                recent_form += "D"
                form_score += 1*weight
            else:
                recent_form+="L"
        else:
            if match["home_score"] < match["away_score"]:
                recent_form += "W"
                form_score += 3*weight
            elif match["home_score"] == match["away_score"]:
                recent_form += "D"
                form_score += 1*weight
            else:
                recent_form+="L"
  
 
 
 
 
    team_stats.append(
        {
            "Team":team,
            "Matches Played":matches_played,
            "Wins":wins,
            "Draws":draws,
            "Losses":losses,
            "Goals Scored": goals_scored,
            "Goals Conceded": goals_conceded,
            "Goals Per Game": round(goals_per_game, 2),
            "Goals Conceded Per Game": round(goals_conceded_per_game, 2),
            "Win Rate":round(win_rate,2),
            "Recent Form":recent_form,
            "Form Score":form_score,
 
 
 
        }
    )
 
#Make a dataframe and RATINGS
team_stats_df = pd.DataFrame(team_stats)
world_avg_goals = team_stats_df["Goals Per Game"].mean()
team_stats_df["Attack Rating"]=(team_stats_df["Goals Per Game"]/world_avg_goals)
team_stats_df["Defence Rating"]=(world_avg_goals/team_stats_df["Goals Conceded Per Game"])
team_stats_df["Defence Rating"]=team_stats_df["Defence Rating"].clip(upper=2)

 
 
team_stats_df["Attack Rating"]=team_stats_df["Attack Rating"].round(2)
team_stats_df["Defence Rating"]=team_stats_df["Defence Rating"].round(2)
 
team_stats_df["Strength Score"] = (
 
    team_stats_df["Attack Rating"] * 30
    +
    team_stats_df["Defence Rating"] * 30
    +
    team_stats_df["Win Rate"] * 0.3
    +
    team_stats_df["Form Score"] * 1
)
 
team_stats_df["Strength Score"] = (
    team_stats_df["Strength Score"]
    .round(2)
)
team_stats_df["Reliability"] = (
    team_stats_df["Matches Played"]
    /
    (
        team_stats_df["Matches Played"]
        + 20
    )
)
team_stats_df["Adjusted Strength Score"] = (
    team_stats_df["Strength Score"]
    *
    team_stats_df["Reliability"]
)
team_stats_df["Reliability"] = (
    team_stats_df["Reliability"]
    .round(3)
)
 
team_stats_df["Adjusted Strength Score"] = (
    team_stats_df["Adjusted Strength Score"]
    .round(2)
)
 
 
# ── ELO MERGE ──────────────────────────────────────────────────────────────────
# Keep only teams that appear in BOTH datasets (inner join on Team name)
team_stats_df["Team"] = team_stats_df["Team"].replace({
    "Czech Republic": "Czechia"
})
team_stats_df["Team"] = team_stats_df["Team"].replace({
    "Curaçao": "Curacao"
})
team_stats_df = team_stats_df.merge(
    elo_df[["Team", "Rating"]].rename(columns={"Rating": "Elo Rating"}),
    on="Team",
    how="inner"          # drops any team missing from either file
)
 
# Normalise Elo to a 0-100 scale so it's comparable to Adjusted Strength Score
elo_min = team_stats_df["Elo Rating"].min()
elo_max = team_stats_df["Elo Rating"].max()
team_stats_df["Elo Normalised"] = (
    (team_stats_df["Elo Rating"] - elo_min)
    / (elo_max - elo_min)
    * 100
).round(2)
 
# Normalise Adjusted Strength Score to 0-100 as well
adj_min = team_stats_df["Adjusted Strength Score"].min()
adj_max = team_stats_df["Adjusted Strength Score"].max()
team_stats_df["Stats Normalised"] = (
    (team_stats_df["Adjusted Strength Score"] - adj_min)
    / (adj_max - adj_min)
    * 100
).round(2)
 
# Final composite rating:

team_stats_df["Final Rating"] = (
    team_stats_df["Elo Normalised"] * 0.95
    + team_stats_df["Stats Normalised"] * 0.05
).round(2)
 
# ── CONVERT TO CSV ─────────────────────────────────────────────────────────────
team_stats_df = team_stats_df.sort_values(by="Final Rating", ascending=False)
 
team_stats_df.to_csv(
    "data/team_stats.csv",
    index=False
)
 
