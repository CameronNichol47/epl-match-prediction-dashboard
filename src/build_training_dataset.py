from pathlib import Path
from understatapi import UnderstatClient
import pandas as pd
import feature_engineering

understat = UnderstatClient()
BASE_DIR = Path(__file__).resolve().parent
PRO_DIR = BASE_DIR.parent / "data" / "processed"

TEAM_FILE_NAMES = {
    "Newcastle United": "Newcastle",
    "Manchester United": "Manchester Utd",
    "Nottingham Forest": "Nottingham",
    "Tottenham Hotspur": "Tottenham",
    "Brighton and Hove Albion": "Brighton",
    "Wolverhampton Wanderers": "Wolves",
    "Leeds": "Leeds United"
}

def load_team(team):
    file_team = TEAM_FILE_NAMES.get(team, team)
    file_path = PRO_DIR / f"{file_team}.csv"
    
    if not file_path.exists():
        raise FileNotFoundError(f"Could not find {file_path}")

    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()

    return df

def build_training(home, away, match_date):
    home_df = load_team(home)
    away_df = load_team(away)

    home_df["Date"] = pd.to_datetime(home_df["Date"]).dt.date
    away_df["Date"] = pd.to_datetime(away_df["Date"]).dt.date

    home_df = home_df[home_df["Date"] < match_date]
    away_df = away_df[away_df["Date"] < match_date]

    if len(home_df) < 5 or len(away_df) < 5:
        return None

    general_stats = [
        "Poss_last3",
        "Poss_last5",
        "Shots_For_last3",
        "Shots_For_last5",
        "ShotsT_For_last3",
        "ShotsT_For_last5",
        "Shots_Against_last3",
        "Shots_Against_last5",
        "ShotsT_Against_last3",
        "ShotsT_Against_last5",
        "XG_for_last3",
        "XG_for_last5",
        "XG_against_last3",
        "XG_against_last5",
        "GF_last3",
        "GF_last5",
        "GA_last3",
        "GA_last5",
        "Result_last3",
        "Result_last5",
        "XG_Diff_last3",
        "XG_Diff_last5",
        "Goal_Diff_last3",
        "Goal_Diff_last5",
    ]

    home_venue_features = [
        "Home_Poss_last3",
        "Home_XG_for_last3",
        "Home_XG_against_last3",
        "Home_Result_last3",
        "Home_XG_Diff_last3",
        "Home_Goal_Diff_last3",
    ]

    away_venue_features = [
        "Away_Poss_last3",
        "Away_XG_for_last3",
        "Away_XG_against_last3",
        "Away_Result_last3",
        "Away_XG_Diff_last3",
        "Away_Goal_Diff_last3",
    ]

    home_general = home_df[general_stats].iloc[[-1]].copy()
    away_general = away_df[general_stats].iloc[[-1]].copy()

    home_venue_df = home_df.dropna(subset=["Home_XG_for_last3"])
    away_venue_df = away_df.dropna(subset=["Away_XG_for_last3"])

    if home_venue_df.empty or away_venue_df.empty:
        return None

    home_venue = home_venue_df[home_venue_features].iloc[[-1]].copy()
    away_venue = away_venue_df[away_venue_features].iloc[[-1]].copy()

    home_features = pd.concat([home_general.reset_index(drop=True),
                               home_venue.reset_index(drop=True),]
                               ,axis=1,)

    away_features = pd.concat([away_general.reset_index(drop=True),
                               away_venue.reset_index(drop=True),]
                               ,axis=1,)

    home_features = home_features.rename(columns={col: f"Home_{col}" for col in home_features.columns})

    away_features = away_features.rename(columns={col: f"Away_{col}" for col in away_features.columns})

    df = pd.concat([home_features.reset_index(drop=True), 
                    away_features.reset_index(drop=True),]
                    ,axis=1,)

    df.insert(0, "Date", match_date)
    df.insert(1, "Home", home)
    df.insert(2, "Away", away)



    output_path = BASE_DIR.parent / "data" / "matches_historical" / f"{home + "_VS_" + away + "_training"}.csv"
    df.to_csv(output_path, index=False)

def main():
    feature_engineering.main()
    league = understat.league(league="EPL")
    matches = league.get_match_data(season="2025")
    #print(matches)

    games = []
    relegated_teams = ['West Ham',
                       'Wolverhampton Wanderers',
                       'Burnley'
                      ]

    for match in matches:
        if match['h']['title'] not in relegated_teams and match['a']['title'] not in relegated_teams:
            games.append({
            "home": match['h']['title'],
            "away": match['a']['title'],
            "date": pd.to_datetime(match["datetime"]).date()
        })
            
    #print(games)

    for game in games:
        build_training(game['home'], game['away'], game['date'])
        

if __name__ == "__main__":
    main()