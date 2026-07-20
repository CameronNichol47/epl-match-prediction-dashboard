from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent

html_path = (
    BASE_DIR.parent
    / "raw"
    / "Arsenal Stats, Premier League _ FBref.com.html"
)

with html_path.open("r", encoding="utf-8") as file:
    tables = pd.read_html(file)
    afc_df = tables[1]

for col in tables[1].columns:
    print(col)

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

afc_df=afc_df[columns].copy()

afc_df.to_csv('Arsenal.csv', index=False)

afc_df = pd.read_csv("Arsenal.csv")

for opponent in afc_df["Opponent"]:
    print(opponent)

