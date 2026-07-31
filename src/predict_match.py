from pathlib import Path
import pandas as pd
import joblib

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "xgboost_model.pkl"

def model(home, away):
    MATCH_PATH = BASE_DIR / "data" / "matches" / f"{home}_VS_{away}.csv"

    model = joblib.load(MODEL_PATH)

    match_df = pd.read_csv(MATCH_PATH)

    X = match_df.drop(columns=[ "Home",
                                "Away",
                                "Home_Poss_last3",
                                "Home_Shots_For_last3",
                                "Home_ShotsT_For_last3",
                                "Home_Shots_Against_last3",
                                "Home_ShotsT_Against_last3",
                                "Home_XG_for_last3",
                                "Home_XG_against_last3",
                                "Home_GF_last3",
                                "Home_GA_last3",
                                "Home_Result_last3",
                                "Home_XG_Diff_last3",
                                "Home_Goal_Diff_last3",

                                "Away_Poss_last3",
                                "Away_Shots_For_last3",
                                "Away_ShotsT_For_last3",
                                "Away_Shots_Against_last3",
                                "Away_ShotsT_Against_last3",
                                "Away_XG_for_last3",
                                "Away_XG_against_last3",
                                "Away_GF_last3",
                                "Away_GA_last3",
                                "Away_Result_last3",
                                "Away_XG_Diff_last3",
                                "Away_Goal_Diff_last3",
                                "Home_Home_Poss_last3",
                                "Home_Home_XG_for_last3",
                                "Home_Home_XG_against_last3",
                                "Home_Home_Result_last3",
                                "Home_Home_XG_Diff_last3",
                                "Home_Home_Goal_Diff_last3",

                                "Away_Away_Poss_last3",
                                "Away_Away_XG_for_last3",
                                "Away_Away_XG_against_last3",
                                "Away_Away_Result_last3",
                                "Away_Away_XG_Diff_last3",
                                "Away_Away_Goal_Diff_last3",])

    prediction = model.predict(X)[0]
    probabilities = model.predict_proba(X)[0]

    print("Prediction:", prediction)
    print("Probabilities:", probabilities) #[Away Win, Draw, Home Win]
