from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent

def main():
    merged_df = pd.DataFrame()
    folder_path = PROJECT_DIR / "data" / "matches_historical"

    for csv_file in folder_path.glob("*.csv"):
        df = pd.read_csv(csv_file)
        merged_df = pd.concat([merged_df, df], ignore_index=True)
    
    merged_df = (merged_df.sort_values("Date").reset_index(drop=True))
    
    output_path = BASE_DIR.parent / "data" / "training" / "training_dataset.csv"
    merged_df.to_csv(output_path, index=False)

if __name__ == "__main__":
    main()