from pathlib import Path
import pandas as pd
import numpy as np
import scraping

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

def roll_avg_five_poss(df):
    count = 0
    avg = 0
    lst = []

    for row in df["Poss"]:
        if count >= 5:
            avg = np.mean([df.loc[count - 5, 'Poss'].astype(float),
                   df.loc[count - 4, 'Poss'].astype(float), 
                   df.loc[count - 3, 'Poss'].astype(float),
                   df.loc[count - 2, 'Poss'].astype(float),
                   df.loc[count - 1, 'Poss'].astype(float)])
            
            lst.append(float(round(avg, 4)))
        else:
            lst.append(np.nan)
        count+=1

    df["Poss_last5"] = lst
    return df

def roll_avg_three_shots_for(df):
    count = 0
    avg = 0
    lst = []

    for row in df["Shots_For"]:
        if count >= 3:
            avg = np.mean([df.loc[count - 3, 'Shots_For'].astype(float),
                   df.loc[count - 2, 'Shots_For'].astype(float), 
                   df.loc[count - 1, 'Shots_For'].astype(float)])
            
            lst.append(float(round(avg, 4)))
        else:
            lst.append(np.nan)
        count+=1

    df["Shots_For_last3"] = lst
    return df

def roll_avg_five_shots_for(df):
    count = 0
    avg = 0
    lst = []

    for row in df["Shots_For"]:
        if count >= 5:
            avg = np.mean([df.loc[count - 5, 'Shots_For'].astype(float),
                   df.loc[count - 4, 'Shots_For'].astype(float), 
                   df.loc[count - 3, 'Shots_For'].astype(float),
                   df.loc[count - 2, 'Shots_For'].astype(float),
                   df.loc[count - 1, 'Shots_For'].astype(float)])
            
            lst.append(float(round(avg, 4)))
        else:
            lst.append(np.nan)
        count+=1

    df["Shots_For_last5"] = lst
    return df

def roll_avg_three_shotsT_for(df):
    count = 0
    avg = 0
    lst = []

    for row in df["SoT_For"]:
        if count >= 3:
            avg = np.mean([df.loc[count - 3, 'SoT_For'].astype(float),
                   df.loc[count - 2, 'SoT_For'].astype(float), 
                   df.loc[count - 1, 'SoT_For'].astype(float)])
            
            lst.append(float(round(avg, 4)))
        else:
            lst.append(np.nan)
        count+=1

    df["ShotsT_For_last3"] = lst
    return df
    
def roll_avg_five_shotsT_for(df):
    count = 0
    avg = 0
    lst = []

    for row in df["SoT_For"]:
        if count >= 5:
            avg = np.mean([df.loc[count - 5, 'SoT_For'].astype(float),
                   df.loc[count - 4, 'SoT_For'].astype(float), 
                   df.loc[count - 3, 'SoT_For'].astype(float),
                   df.loc[count - 2, 'SoT_For'].astype(float),
                   df.loc[count - 1, 'SoT_For'].astype(float)])
            
            lst.append(float(round(avg, 4)))
        else:
            lst.append(np.nan)
        count+=1

    df["ShotsT_For_last5"] = lst
    return df
    

def roll_avg_three_shots_against(df):
    count = 0
    avg = 0
    lst = []

    for row in df["Shots_Against"]:
        if count >= 3:
            avg = np.mean([df.loc[count - 3, 'Shots_Against'].astype(float),
                   df.loc[count - 2, 'Shots_Against'].astype(float), 
                   df.loc[count - 1, 'Shots_Against'].astype(float)])
            
            lst.append(float(round(avg, 4)))
        else:
            lst.append(np.nan)
        count+=1

    df["Shots_Against_last3"] = lst
    return df

def roll_avg_five_shots_against(df):
    count = 0
    avg = 0
    lst = []

    for row in df["Shots_Against"]:
        if count >= 5:
            avg = np.mean([df.loc[count - 5, 'Shots_Against'].astype(float),
                   df.loc[count - 4, 'Shots_Against'].astype(float), 
                   df.loc[count - 3, 'Shots_Against'].astype(float),
                   df.loc[count - 2, 'Shots_Against'].astype(float),
                   df.loc[count - 1, 'Shots_Against'].astype(float)])
            
            lst.append(float(round(avg, 4)))
        else:
            lst.append(np.nan)
        count+=1

    df["Shots_Against_last5"] = lst
    return df
    

def roll_avg_three_a():
    pass

def main():
    scraping.main()

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
        df = roll_avg_five_poss(df)
        df = roll_avg_three_shots_for(df)
        df = roll_avg_five_shots_for(df)
        df = roll_avg_three_shotsT_for(df)
        df = roll_avg_five_shotsT_for(df)
        df = roll_avg_three_shots_against(df)
    
        output_path = BASE_DIR.parent / "processed" / f"{team}.csv"
        df.to_csv(output_path, index=False)


if __name__ == "__main__":
    main()