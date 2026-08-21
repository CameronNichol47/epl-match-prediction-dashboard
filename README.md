# Premier League Match Prediction Platform

An end-to-end machine learning platform for predicting Premier League match
outcomes using historical match data, engineered team-performance features,
Elo ratings, and XGBoost.

The application generates probabilities for a home win, draw, and away win,
explains individual predictions using SHAP, and compares the model's
probabilities with prediction-market probabilities from Polymarket.

The project also includes a Kelly Criterion implementation for comparing model
probabilities with market probabilities and estimating theoretical bankroll
allocation.

## Features

- Premier League match outcome prediction (Home Win / Draw / Away Win)
- XGBoost multiclass classification model
- Automated match-data processing pipeline
- Rolling team performance statistics
- Home and away specific features
- Elo rating system
- Offseason Elo regression
- Support for newly promoted teams
- SHAP explanations for individual predictions
- Polymarket probability integration
- Kelly Criterion calculations
- Interactive Streamlit dashboard
- Cached predictions and API results to avoid unnecessary repeated processing

## Machine Learning Pipeline

The prediction pipeline follows the general structure:

Raw Match Data
      ↓
Data Cleaning
      ↓
Feature Engineering
      ↓
Rolling Team Statistics
      ↓
Elo Ratings
      ↓
Match Feature Dataset
      ↓
XGBoost Model
      ↓
Prediction Probabilities
      ↓
SHAP Explanations
      ↓
Polymarket Comparison
      ↓
Kelly Criterion
      ↓
Streamlit Dashboard

## Feature Engineering

The model uses historical team performance rather than statistics from the
match being predicted.

Features currently include rolling 3-match and 5-match statistics such as:

- Possession
- Shots
- Shots on target
- Expected goals (xG)
- Expected goals against (xGA)
- Goals scored
- Goals conceded
- Match results
- Goal difference
- xG difference

The dataset also contains venue-specific rolling features to represent how
teams perform specifically at home or away.

## Elo Rating System

An Elo rating system is used as an additional measure of team strength.

Each team's rating is updated after every match based on:

- The team's current Elo rating
- The opponent's Elo rating
- Match result
- Home-field advantage

The current implementation uses:

- Initial Elo: `1500`
- K-factor: `20`
- Home advantage: `65`

At the beginning of a new season, existing Premier League teams undergo
offseason regression toward the league-average Elo:

    new_elo = 0.67 * previous_elo + 0.33 * 1500

This prevents ratings from carrying over unchanged between seasons while still
preserving information about team strength.

Newly promoted teams that do not have an existing Premier League Elo history
are initialized separately.

Both pre-match and post-match Elo ratings are stored so that the prediction
pipeline can retrieve the latest available rating without introducing
post-match information into historical training features.

## Model

The primary model is an XGBoost multiclass classifier.

For each fixture, the model outputs probabilities in the form:

    [Away Win, Draw, Home Win]

Example:

    Away Win: 18%
    Draw:     24%
    Home Win: 58%

The model uses engineered historical features and Elo differences to estimate
the probability of each match outcome.

## SHAP Explanations

SHAP is used to explain individual model predictions.

For each selected match, the dashboard displays which features contributed
most strongly to the model's predicted outcome.

This makes it possible to inspect whether factors such as recent xG,
possession, goal difference, venue performance, or Elo difference influenced
a prediction.

## Polymarket Comparison

The project retrieves publicly available event probability data from the
Polymarket Gamma API.

For supported Premier League fixtures, the dashboard compares:

    Model Probability
            vs.
    Polymarket Probability

This makes it possible to examine differences between the machine learning
model's estimated probabilities and prediction-market probabilities.

Polymarket data is cached where appropriate to avoid unnecessary repeated API
requests when Streamlit reruns the application.

## Kelly Criterion

The project includes a Kelly Criterion implementation that compares the
model's estimated probability with the market-implied probability.

For a model probability `p` and market probability `m`:

    decimal_odds = 1 / m

    b = decimal_odds - 1
    q = 1 - p

    Kelly Fraction = (b * p - q) / b

Negative Kelly values are treated as zero.

The Streamlit interface displays the calculated Kelly percentage and can
convert the fraction into a theoretical dollar allocation based on an entered
bankroll.

This component is included for analytical and educational purposes.

## Streamlit Dashboard

The Streamlit frontend allows users to select Premier League fixtures and
generate predictions interactively.

For each match, the dashboard displays:

1. Match information
2. Model probability pie chart
3. Home / Draw / Away probabilities
4. SHAP prediction explanation
5. Polymarket probability pie chart
6. Kelly Criterion percentage
7. Theoretical Kelly allocation

Prediction results are cached so that changing interactive UI elements does
not require the complete data/model pipeline to run again.

## Project Structure

    finance_project/
    │
    ├── data/
    │   ├── raw/
    │   ├── processed/
    │   ├── matches/
    │   └── full_gamelog/
    │
    ├── models/
    │   └── xgboost_model.pkl
    │
    ├── src/
    │   ├── feature_engineering.py
    │   ├── build_dataset.py
    │   ├── predict_match.py
    │   ├── elo.py
    │   ├── shap_explainer.py
    │   ├── polymarket_api.py
    │   ├── build_market_probabilities.py
    │   └── kelly_criterion.py
    │
    ├── app/
    │   ├── frontend.py
    │   ├── fixtures_api.py
    │   └── visualizations.py
    │
    └── README.md

## Technologies

### Machine Learning
- XGBoost
- Scikit-learn
- SHAP

### Data Processing
- Python
- Pandas
- NumPy

### Data / APIs
- Football data APIs
- Historical match data
- Polymarket Gamma API

### Visualization / Frontend
- Streamlit
- Plotly
- Matplotlib

## Current Status

The project currently supports:

- Automated feature generation
- Rolling team statistics
- Elo-based team strength
- Offseason Elo regression
- XGBoost match predictions
- SHAP explanations
- Polymarket probability retrieval
- Kelly Criterion calculations
- Streamlit visualization
- Prediction/API caching

## Planned Improvements

Future development may include:

- Model probability calibration
- More extensive backtesting
- Comparison with Logistic Regression and Random Forest baselines
- Improved treatment of promoted/relegated teams
- Player availability and injury information
- Starting lineup information
- Additional team-strength metrics
- Automated weekly data updates
- Improved Streamlit UI
- Historical model-vs-market evaluation

## Disclaimer

This project is intended for educational, research, and machine-learning
purposes. Market probability and Kelly Criterion components are used to
analyze and compare probabilistic predictions and should not be interpreted as
financial or wagering advice.

## Current Predictions

The model is currently being used to generate predictions for upcoming
Premier League fixtures.

Current predictions include:

| Fixture | Model Prediction |
|---|---|
| Everton vs Crystal Palace | Draw |
| Nottingham Forest vs Leeds United | Draw |
| Brentford vs Tottenham Hotspur | Tottenham Win |
| Manchester City vs Bournemouth | Manchester City Win |
| Brighton vs Aston Villa | Brighton Win |
| Newcastle United vs Liverpool | Newcastle United Win |
| Fulham vs Chelsea | Chelsea Win |

### Prediction Limitations

Matches involving newly promoted teams are currently excluded from model
predictions.

The model relies heavily on rolling Premier League statistics from previous
matches, including recent xG, possession, shots, goals, and venue-specific
performance. Newly promoted teams do not yet have sufficient Premier League
match history for these rolling features to be generated consistently.

As the season progresses and promoted teams accumulate enough Premier League
matches, they can be incorporated into the prediction pipeline.

The Elo system itself supports newly promoted teams by assigning them an
initial rating, but the lack of historical rolling features is currently the
main limitation preventing full predictions for these fixtures.