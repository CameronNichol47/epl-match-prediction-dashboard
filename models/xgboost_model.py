from pathlib import Path
import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent

df = pd.read_csv(PROJECT_DIR / "data" / "training" / "training_dataset_with_elo.csv")
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date").reset_index(drop=True)

X = df.drop(columns=["Date","Home","Away","Result", "Home_Elo",
        "Away_Elo", "Home_Poss_last3",
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
    "Away_Goal_Diff_last3",])
y = df["Result"]

# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # #Doing chronological split: 
split = int(len(df) * 0.8)

X_train = X.iloc[:split]
X_test = X.iloc[split:]

y_train = y.iloc[:split]
y_test = y.iloc[split:]

model = XGBClassifier(
    objective="multi:softprob",
    num_class=3,
    random_state=42,
    eval_metric="mlogloss",
    n_estimators=300,
    learning_rate=0.05,
    max_depth=4,
    min_child_weight=3,
    subsample=0.8,
    colsample_bytree=0.8,
)
model.fit(X_train, y_train)
predictions = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, predictions))
print(confusion_matrix(y_test, predictions))
print(classification_report(y_test, predictions))

importance = pd.Series(
    model.feature_importances_,
    index=X.columns
).sort_values(ascending=False)

# print(df["Elo_Diff"].describe())
# print(importance.sort_values(ascending=False).head(20))

pd.set_option("display.max_rows", None)
print(importance)