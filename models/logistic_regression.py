from pathlib import Path
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import joblib



BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
MODEL_PATH = BASE_DIR / "logistic_regression.pkl"


df = pd.read_csv(PROJECT_DIR / "data" / "training" / "training_dataset.csv")

df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date").reset_index(drop=True)

X = df.drop(columns=["Date","Home","Away","Result"])
y = df["Result"]

#print(X.dtypes)

#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#Doing chronological split: 
split = int(len(df) * 0.8)

X_train = X.iloc[:split]
X_test = X.iloc[split:]

y_train = y.iloc[:split]
y_test = y.iloc[split:]

model = Pipeline([("scaler", StandardScaler()), 
                  ("classifier", LogisticRegression(max_iter=1000,random_state=42))
                  ])

model.fit(X_train, y_train)

predict = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, predict))
print(confusion_matrix(y_test, predict))
print(classification_report(y_test, predict))


# corr = X.corr(numeric_only=True)

# plt.figure(figsize=(20, 16))
# plt.imshow(corr, cmap="coolwarm", interpolation="nearest")
# plt.colorbar()
# plt.xticks(range(len(corr.columns)), corr.columns, rotation=90, fontsize=8)
# plt.yticks(range(len(corr.columns)), corr.columns, fontsize=8)
# plt.tight_layout()
# plt.show()

model_data = {
    "model": model,
    "feature_names": X.columns.tolist(),
    "class_labels": {
        0: "Away Win",
        1: "Draw",
        2: "Home Win",
    },
}

joblib.dump(model_data, MODEL_PATH)

print(f"Model saved to: {MODEL_PATH}")