from pathlib import Path
import pandas as pd
from understatapi import UnderstatClient

BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR.parent / "data" / "raw"

fbref_name_map = {
    "Brighton": "Brighton & Hove Albion",
    "Manchester Utd": "Manchester United",
    "Newcastle": "Newcastle United",
    "Nottingham": "Nottingham Forest",
    "Tottenham": "Tottenham Hotspur",
    "Coventry": "Coventry City",
    "Hull": "Hull City",
    "Ipswich": "Ipswich Town"
}

understat_name_map = {
    "Leeds United": "Leeds",
    "Manchester Utd": "Manchester United",
    "Newcastle": "Newcastle United",
    "Nottingham": "Nottingham Forest",
}

def load_standard_data(folder, team):
    """
    Loads the standard FBref match log for a team and returns the
    core match statistics used throughout the data pipeline.
    """
    fbref_name = fbref_name_map.get(team, team)

    standard_html_path = (
        RAW_DIR
        / folder
        / f"{fbref_name} Stats, Premier League _ FBref.com.html"
    )

    print("LOOKING FOR:", standard_html_path)
    
    with standard_html_path.open("r", encoding="utf-8") as file:
        standard_tables = pd.read_html(file)

    df = standard_tables[1]

    columns = [
        "Date",
        "Comp",
        "Venue",
        "Result",
        "GF",
        "GA",
        "Opponent",
        "Poss",
    ]

    return df[columns].copy()

def load_shooting_tables(folder, team):
    """
    Loads the FBref shooting match log HTML and returns the
    'For' and 'Against' shooting tables.
    """
    fbref_name = fbref_name_map.get(team, team)

    shooting_html_path = (
        RAW_DIR
        / folder
        / f"{fbref_name} Match Logs (Shooting), All Competitions _ FBref.com.html"
    )

    with shooting_html_path.open("r", encoding="utf-8") as file:
        return pd.read_html(file)

def load_shooting(df, tables, team):
    """
    Extracts shooting statistics (shots, shots on target, and
    shot accuracy) for the selected team and merges them into
    the standard match dataframe.
    """

    shooting_for = tables[0]

    print(team)
    print(shooting_for.columns)

    fbref_name = fbref_name_map.get(team, team)


    shooting_for = shooting_for[
        [
            (f"For {fbref_name}", "Date"),
            (f"For {fbref_name}", "Comp"),
            (f"For {fbref_name}", "Venue"),
            (f"For {fbref_name}", "Opponent"),
            ("Standard", "Sh"),
            ("Standard", "SoT"),
            ("Standard", "SoT%"),
        ]
    ].copy()

    shooting_for.columns = [
        "Date",
        "Comp",
        "Venue",
        "Opponent",
        "Shots_For",
        "SoT_For",
        "SoT%_For",
    ]

    merge_columns = [
        "Date",
        "Comp",
        "Venue",
        "Opponent",
    ]

    df = df.merge(
        shooting_for,
        on=merge_columns,
        how="left",
    )

    return df

def load_shooting_against(df, tables, team):
    """
    Extracts opponent shooting statistics from the FBref
    shooting tables and merges them into the team's match
    dataframe.
    """

    shooting_against = tables[1]    

    fbref_name = fbref_name_map.get(team, team)

    shooting_against = shooting_against[
        [
            (f"Against {fbref_name}", "Date"),
            (f"Against {fbref_name}", "Comp"),
            (f"Against {fbref_name}", "Venue"),
            (f"Against {fbref_name}", "Opponent"),
            ("Standard", "Sh"),
            ("Standard", "SoT"),
            ("Standard", "SoT%"),
        ]
    ].copy()

    shooting_against.columns = [
        "Date",
        "Comp",
        "Venue",
        "Opponent",
        "Shots_Against",
        "SoT_Against",
        "SoT%_Against",
    ]

    df = df.merge(
        shooting_against,
        on=[
            "Date",
            "Comp",
            "Opponent",
        ],
        how="left",
    )

    return df

def add_xg(df, team, season):
    """
    Retrieves expected goals (xG) and expected goals against (xGA)
    for each Premier League match using the Understat API and
    appends them to the dataframe.
    """
    
    understat = UnderstatClient()

    understat_name = understat_name_map.get(team, team)

    matches = (
        understat
        .league("EPL")
        .get_match_data(season=season)
    )

    team_name_map = {
        "Wolves": "Wolverhampton Wanderers",
        "Leeds United": "Leeds",
        "Nottingham": "Nottingham Forest",
        "Manchester Utd": "Manchester United",
        "Newcastle": "Newcastle United",
        "Coventry City": "Coventry"
    }

    xg_values = []
    xga_values = []

    for _, row in df.iterrows():
        opponent = row["Opponent"]

        opponent = team_name_map.get(opponent, opponent)

        venue = row["Venue"]
        comp = row["Comp"]


        if venue == "Home" and comp == "Premier League":
            game = None

            for m in matches:
                if (m["h"]["title"] == understat_name and m["a"]["title"] == opponent):
                    game = m
                    break

            if (game and game["xG"]["h"] is not None and game["xG"]["a"] is not None):
                xg = float(game["xG"]["h"])
                xga = float(game["xG"]["a"])

                xg_values.append(xg)
                xga_values.append(xga)

            else:
                xg_values.append(float("nan"))
                xga_values.append(float("nan"))

        elif venue == "Away" and comp == "Premier League":
            game = None

            for m in matches:
                if (m["h"]["title"] == opponent and m["a"]["title"] == understat_name):
                    game = m
                    break

            if (game and game["xG"]["h"] is not None and game["xG"]["a"] is not None):
                xg = float(game["xG"]["a"])
                xga = float(game["xG"]["h"])

                xg_values.append(xg)
                xga_values.append(xga)

            else:
                xg_values.append(float("nan"))
                xga_values.append(float("nan"))

    df["XG_for"] = xg_values
    df["XG_against"] = xga_values

    return df

def preprocess_data(df):
    """
    Encodes categorical variables into numerical values for
    machine learning models.
    """

    df["Venue"] = df["Venue"].map({
        "Home": 1,
        "Away": 0
    })

    df["Result"] = df["Result"].map({
        "W": 3,
        "D": 1,
        "L": 0
    })

    return df

def main():
    """
    Executes the complete data collection pipeline for each
    Premier League team by loading match logs, merging shooting
    statistics, adding expected goals data, preprocessing the
    dataset, and exporting the final CSV files.
    """

    seasons = {
        "2025-26": "2025",
        "2026-27": "2026",
    }

    teams = {
        "Arsenal": "Arsenal",
        "Aston Villa": "Aston_Villa",
        "Bournemouth": "Bournemouth",
        "Brentford": "Brentford",
        "Brighton": "Brighton",
        "Chelsea": "Chelsea",
        "Coventry": "Coventry_City",
        "Crystal Palace": "Crystal_Palace",
        "Everton": "Everton",
        "Fulham": "Fulham",
        "Hull": "Hull_City",
        "Ipswich": "Ipswich_Town",
        "Leeds United": "Leeds_United",
        "Liverpool": "Liverpool",
        "Manchester City": "Manchester_City",
        "Manchester Utd": "Manchester_Utd",
        "Newcastle": "Newcastle",
        "Nottingham": "Nottingham",
        "Sunderland": "Sunderland",
        "Tottenham": "Tottenham"
    }

    for team, team_folder in teams.items():

        team_seasons = []

        for season_folder, understat_season in seasons.items():

            folder = Path(season_folder) / team_folder

            full_folder = RAW_DIR / folder

            if not full_folder.exists():
                print(
                    f"Skipping {team} for {season_folder} "
                    "- no data folder"
                )
                continue

            df = load_standard_data(folder, team)
            tables = load_shooting_tables(folder, team)

            df = load_shooting(df, tables, team)
            df = load_shooting_against(df, tables, team)

            df = df[(df["Comp"] == "Premier League") & (df["Result"].notna())].copy()

            df.rename(
                columns={"Venue_x": "Venue"},
                inplace=True,
            )

            if "Venue_y" in df.columns:
                df.drop(columns=["Venue_y"], inplace=True)

            df = add_xg(
                df,
                team,
                understat_season
            )

            df = preprocess_data(df)

            team_seasons.append(df)

        combined_df = pd.concat(
            team_seasons,
            ignore_index=True
        )

        combined_df["Date"] = pd.to_datetime(
            combined_df["Date"]
        )

        combined_df = combined_df.sort_values(
            "Date"
        ).reset_index(drop=True)

        output_path = (
            BASE_DIR.parent
            / "data"
            / "processed"
            / f"{team}.csv"
        )

        combined_df.to_csv(
            output_path,
            index=False
        )


if __name__ == "__main__":
    main()











 
        










