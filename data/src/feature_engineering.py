from pathlib import Path
import pandas as pd
import numpy as np

BASE_DIR = Path(__file__).resolve().parent
PRO_DIR = BASE_DIR.parent / "processed"

def load_csv(team):
    df = pd.read_csv(f"{PRO_DIR}/{team}.csv")
    df.columns = df.columns.str.strip()
    return df

def roll_avg_three_poss(df):
    count = 0
    avg = 0
    lst = []

    for row in df["Poss"]:
        if count >= 3:
            avg = np.mean([df.loc[count - 3, 'Poss'].astype(float),
                   df.loc[count - 2, 'Poss'].astype(float), 
                   df.loc[count - 1, 'Poss'].astype(float)])
            
            lst.append(float(round(avg, 4)))
        else:
            lst.append(np.nan)
        count+=1

    df["Poss_last3"] = lst
    return df

def roll_avg_five():
    pass

def roll_avg_ten():
    pass

def roll_avg_three_h():
    pass

def roll_avg_five_h():
    pass

def roll_avg_three_a():
    pass

def roll_avg_three_a():
    pass

def main():
    teams = [
        "Arsenal",
        "Aston Villa",
        "Bournemouth",
        "Brentford",
        "Brighton",
        "Chelsea",
        "Crystal Palace",
        "Everton",
        "Fulham",
        "Leeds United",
        "Liverpool",
        "Manchester City",
        "Manchester Utd",
        "Newcastle",
        "Nottingham",
        "Sunderland",
        "Tottenham",
    ]

    for team in teams:
        print(team)
        df = load_csv(team)
        df = roll_avg_three_poss(df)
    
        output_path = BASE_DIR.parent / "processed" / f"{team}.csv"
        df.to_csv(output_path, index=False)


if __name__ == "__main__":
    main()