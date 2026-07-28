import pandas as pd
training_df = pd.read_csv("/Users/cameronnichol/finance_project/data/training/training_dataset.csv")
elo_df = pd.read_csv("/Users/cameronnichol/finance_project/data/full_gamelog/all_matches_with_elo.csv")

training_df["Date"] = pd.to_datetime(training_df["Date"])
elo_df["Date"] = pd.to_datetime(elo_df["Date"])

current_teams = [
    "Arsenal",
    "Aston Villa",
    "Bournemouth",
    "Brentford",
    "Brighton",
    "Chelsea",
    "Crystal Palace",
    "Everton",
    "Fulham",
    "Leeds",
    "Liverpool",
    "Manchester City",
    "Manchester United",
    "Newcastle United",
    "Nottingham Forest",
    "Sunderland",
    "Tottenham",
]

elo_df = elo_df[
    elo_df["Home"].isin(current_teams)
    & elo_df["Away"].isin(current_teams)
    & (elo_df["Date"] >= "2025-10-25")
].copy().reset_index(drop=True)

training_df = training_df.merge(
    elo_df[
        [
            "Date",
            "Home",
            "Away",
            "Home_Elo",
            "Away_Elo",
            "Elo_Diff",
        ]
    ],
    on=["Date", "Home", "Away"],
    how="left",
)

training_df.to_csv("/Users/cameronnichol/finance_project/data/training/training_dataset_with_elo.csv", index=False)