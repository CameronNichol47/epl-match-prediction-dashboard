from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent

df = pd.DataFrame()

def build_probabilities(home, away, probabilities):
    print(probabilities)
    data = {
        "Home": [home],
        "Away": [away],
        "Home_Prob": [probabilities[2]],
        "Draw_Prob": [probabilities[1]],
        "Away_Prob": [probabilities[0]]
    }
    
    df = pd.DataFrame(data)


    output_path = BASE_DIR.parent / "data" / "market_probabilities.csv"
    df.to_csv(output_path, index=False)