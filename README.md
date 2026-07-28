# Premier League Match Predictor

A machine learning project that predicts Premier League match outcomes using team statistics and rolling performance metrics.

## Features

- Automated match data collection
- Feature engineering pipeline
- Rolling averages (last 3 and last 5 matches)
- Home and away form features
- Training dataset generation
- Multiple machine learning models

## Models

- Logistic Regression
- Random Forest
- XGBoost

## Technologies

- Python
- pandas
- scikit-learn
- XGBoost
- Understat API

## Project Structure

finance_project/
├── app/
├── data/
├── models/
└── src/

## Current Results

| Model | Accuracy |
|-------|----------|
| Logistic Regression | 45.5% |
| XGBoost | 38.6% |
| Random Forest | 34.1% |

*Evaluated using a chronological train/test split.*

## Roadmap

- [ ] SHAP model explanations
- [ ] Streamlit dashboard
- [ ] Live fixture selection
- [ ] Probability visualization
- [ ] Kelly Criterion calculator
- [ ] Injury and lineup adjustments

## Author

Cameron Nichol