from pathlib import Path
import sys
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(PROJECT_DIR))

from src import predict_match

PRO_DIR = PROJECT_DIR / "data"

def load_market_probability_csv():
    df = pd.read_csv(f"{PRO_DIR}/market_probabilities.csv")
    return df


def kelly_fraction(model_probability, market_probability):
    decimal_odds = 1 / market_probability
    b = decimal_odds - 1

    p = model_probability
    q = 1 - p

    kelly = (b * p - q) / b

    return max(0.0, kelly)

def get_model_probabilities(home, away):
        probabilities, _ = predict_match.model(home, away)

        away_prob = probabilities[0]
        draw_prob = probabilities[1]
        home_prob = probabilities[2]

        return home_prob, draw_prob, away_prob

def get_market_probabilities(home, away):
    df = load_market_probability_csv()

    for index, row in df.iterrows():
        if row['Home'] == home and row['Away'] == away:
             return row['Home_Prob'], row['Draw_Prob'], row['Away_Prob']

def recommended_bets(home, away):
    model_prob = get_model_probabilities(home, away)
    market_prob = get_market_probabilities(home, away)

    home_kelly = kelly_fraction(model_prob[0], market_prob[0])
    draw_kelly = kelly_fraction(model_prob[1], market_prob[1])
    away_kelly = kelly_fraction(model_prob[2], market_prob[2])
    
    return {
         "home": float(home_kelly),
         "draw": float(draw_kelly),
         "away": float(away_kelly)
    }


def main():
    print(recommended_bets("Manchester City", "Bournemouth"))

if __name__ == "__main__":
    main()