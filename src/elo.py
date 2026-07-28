from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
PRO_DIR = BASE_DIR.parent / "data" / "full_gamelog"

INITIAL_ELO = 1500.0
K_FACTOR = 20.0
HOME_ADVANTAGE = 65.0

ratings = {
    "Arsenal": INITIAL_ELO,
    "Aston Villa": INITIAL_ELO,
    "Bournemouth": INITIAL_ELO,
    "Brentford": INITIAL_ELO,
    "Brighton": INITIAL_ELO,
    "Burnley": INITIAL_ELO,
    "Chelsea": INITIAL_ELO,
    "Crystal Palace": INITIAL_ELO,
    "Everton": INITIAL_ELO,
    "Fulham": INITIAL_ELO,
    "Leeds": INITIAL_ELO,
    "Liverpool": INITIAL_ELO,
    "Manchester City": INITIAL_ELO,
    "Manchester Utd": INITIAL_ELO,
    "Newcastle": INITIAL_ELO,
    "Nottingham": INITIAL_ELO,
    "Sunderland": INITIAL_ELO,
    "Tottenham": INITIAL_ELO,
    "West Ham": INITIAL_ELO,
    "Wolves": INITIAL_ELO,
}

def expected_score(team_rating: float, opponent_rating: float) -> float:
    return 1 / (1 + 10 ** ((opponent_rating - team_rating) / 400))


def update_elo(home_elo, away_elo, result):
        effective_home_elo = home_elo + HOME_ADVANTAGE

        expected_home = expected_score(effective_home_elo, away_elo)
        expected_away = 1 - expected_home

        if result == 2:
            actual_home = 1.0
        elif result == 1:
            actual_home = 0.5
        else:
             actual_home = 0.0

        actual_away = 1 - actual_home

        new_home_elo = home_elo + K_FACTOR * (actual_home - expected_home)

        new_away_elo = away_elo + K_FACTOR * (actual_away - expected_away)

        return new_home_elo, new_away_elo

def add_elo_to_dataframe(df):
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").reset_index(drop=True)

    teams = set(df["Home"]).union(set(df["Away"]))

    ratings = {
        team: INITIAL_ELO
        for team in teams
    }

    home_elo_values = []
    away_elo_values = []
    elo_diff_values = []

    for _, row in df.iterrows():
        home_team = row["Home"]
        away_team = row["Away"]
        result = row["Result"]

        home_elo = ratings[home_team]
        away_elo = ratings[away_team]

        home_elo_values.append(home_elo)
        away_elo_values.append(away_elo)
        elo_diff_values.append(home_elo - away_elo)

        new_home_elo, new_away_elo = update_elo(home_elo, away_elo, result)

        ratings[home_team] = new_home_elo
        ratings[away_team] = new_away_elo

    df["Home_Elo"] = home_elo_values
    df["Away_Elo"] = away_elo_values
    df["Elo_Diff"] = elo_diff_values

    return df

def main():
    df = pd.read_csv(PRO_DIR / "all_matches.csv")

    output_path = PRO_DIR / "all_matches_with_elo.csv"

    df_with_elo = add_elo_to_dataframe(df)

    df_with_elo.to_csv(
        output_path,
        index=False,
    )

    print(df_with_elo.head())
    print(f"Saved to: {output_path}")

if __name__ == "__main__":
    main()