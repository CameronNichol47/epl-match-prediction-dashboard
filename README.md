# ⚽ Premier League Match Outcome Predictor

A machine learning project that predicts Premier League match outcomes (Home Win, Draw, Away Win) using historical match statistics, rolling averages, Elo ratings, and XGBoost.

The project compares multiple machine learning models and demonstrates how feature engineering and feature selection can significantly improve predictive performance.

---

## Features

The model uses historical statistics from previous Premier League matches to generate rolling features for both teams.

### Match Statistics
- Possession
- Shots
- Shots on Target
- Goals For
- Goals Against
- Expected Goals (xG)
- Expected Goals Against (xGA)
- Goal Difference
- xG Difference
- Recent Match Results

### Rolling Features

The final model uses rolling averages over each team's **last 5 matches**.

Examples include:

- Home xG For (Last 5)
- Home xG Against (Last 5)
- Home Goal Difference (Last 5)
- Away xG Difference (Last 5)
- Away Shots on Target (Last 5)
- Away Possession (Last 5)

---

## Elo Ratings

An Elo rating system is implemented to capture each team's long-term strength.

For every fixture the model uses:

- Elo Difference (Home Elo − Away Elo)

Feature selection experiments showed that using only the Elo difference produced better results than including separate Home and Away Elo ratings.

---

## Machine Learning Models

The project compares multiple models:

- Logistic Regression
- Random Forest
- XGBoost

---

## Feature Selection

Several feature engineering experiments were performed to improve model performance.

Experiments included:

- Removing redundant Last 3 rolling statistics
- Removing venue-specific Last 3 statistics
- Comparing Last 3 vs Last 5 rolling windows
- Comparing multiple Elo representations
- Analyzing XGBoost feature importance
- Removing highly correlated features

These experiments significantly improved model performance while reducing model complexity.

---

## Results

| Model | Accuracy |
|--------|----------|
| Logistic Regression | 40.9% |
| Random Forest | 34.1% |
| Initial XGBoost | 38.6% |
| Final XGBoost | **59.1%** |

The final XGBoost model achieved approximately **59% accuracy** on a chronological hold-out test set.

---

## Technologies Used

- Python
- Pandas
- NumPy
- XGBoost
- Scikit-learn

---

## Project Structure

```
finance_project/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── training/
│
├── models/
│   ├── logistic_regression.py
│   ├── random_forest.py
│   └── xgboost_model.py
│
├── src/
│   ├── feature_engineering.py
│   ├── elo.py
│   ├── merge_elo.py
│   └── predict_match.py
│
└── README.md
```

---

## Future Improvements

- Hyperparameter tuning
- Multi-season training data
- SHAP model explanations
- Streamlit dashboard
- Live fixture predictions
- Polymarket odds comparison
- Kelly Criterion value calculator
- Injury and lineup adjustments

---

## Author

**Cameron Nichol**

Computer Science & Applied Mathematics Student

Interested in Machine Learning, Sports Analytics, Data Science, and Quantitative Finance.