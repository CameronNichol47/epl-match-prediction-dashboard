from pathlib import Path
import pandas as pd
from understatapi import UnderstatClient

understat = UnderstatClient()
BASE_DIR = Path(__file__).resolve().parent
PRO_DIR = BASE_DIR.parent / "data" / "processed"



fixtures = []
def build(home, away, date, result):
    fixtures.append({"Date": date, 
                     "Home": home, 
                     "Away": away,
                     "Result": result,
                     })
   

    df = pd.DataFrame(fixtures)
    return df

def main():
    league = understat.league(league="EPL")
    matches = league.get_match_data(season="2025")

    games = []

    for match in matches:
        home_goals = int(match["goals"]["h"])
        away_goals = int(match["goals"]["a"])

        if home_goals > away_goals:
            result = 2  #Represent home win    
        elif home_goals == away_goals:
            result = 1     
        else:
            result = 0 #Represent away win

        games.append({
        "home": match['h']['title'],
        "away": match['a']['title'],
        "date": pd.to_datetime(match["datetime"]).date(),
        "result": result
        })
            
    for game in games:
        df = build(game['home'], game['away'], game['date'], game['result'])

    output_path = BASE_DIR.parent / "data" / "full_gamelog" / "all_matches.csv"
    df.to_csv(output_path, index=False)

if __name__ == "__main__":
    main()