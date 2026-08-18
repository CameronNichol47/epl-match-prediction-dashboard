import streamlit as st 
from pathlib import Path
from fixtures_api import gameweek_one
from datetime import datetime
from zoneinfo import ZoneInfo
import sys
from visualizations import pie_chart

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent

sys.path.insert(0, str(PROJECT_DIR))
from src.build_dataset import build
from src.predict_match import model
from src.shap_explainer import explain
from src.polymarket_api import load_slug
from src.build_market_probabilities import build_probabilities
from src.kelly_criterion import recommended_bets
st.title('Premier League Matchweek 1')

st.markdown(
    """
    <style>
    /* Targets the text inside the expander header */
    div[data-testid="stExpander"] summary p {
        font-size: 24px !important;
        font-weight: bold;
        text-align: center !important;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

@st.cache_data
def load_prediction_data(home, away, date):
    build(home, away)

    prob, shap_figure = model(home, away)

    polymarket = load_slug(home, away, date)

    build_probabilities(home, away, polymarket)

    kelly = recommended_bets(home, away)

    return prob, polymarket, kelly, shap_figure

for match in gameweek_one:
    home = match["strHomeTeam"]
    away = match["strAwayTeam"]
    date = match["dateEvent"]
    time = match.get("strTime", "Time TBD")
    venue = match["strVenue"]

    utc = datetime.fromisoformat(f"{date}T{time}").replace(
    tzinfo=ZoneInfo("UTC")
)
    
    toronto = utc.astimezone(ZoneInfo("America/Toronto"))
    uk = utc.astimezone(ZoneInfo("Europe/London"))

    with st.expander(f"{home} vs {away}"):
        st.write(f"Game: {home} vs {away}")
        st.write (f"Date: {date}")
        st.write(f"Time (UK): {uk.strftime("%Y-%m-%d %H:%M")}")
        st.write(f"Time (Toronto): {toronto.strftime("%Y-%m-%d %H:%M")}")
        st.write(f"Venue: {venue}")

        prediction_key = f"prediction_{match['idEvent']}"

        if st.button("Load Prediction", key=match["idEvent"]):
            st.session_state[prediction_key] = True

        if st.session_state.get(prediction_key, False):
            st.write(f"Creating prediction for {home} vs {away}...")

            prob, polymarket, kelly, shap_figure = load_prediction_data(home, away, date)

            pie_chart(home, away, prob, "Model")

            st.subheader("Why the model made this prediction")
            st.pyplot(shap_figure)

            pie_chart(home, away, polymarket, "Polymarket")

            best_kelly = max(
                kelly["home"],
                kelly["away"],
                kelly["draw"],
            )

            bankroll = st.number_input(
                "Enter your bankroll ($)",
                min_value=0.0,
                value=0.0,
                step=10.0,
                key=f"bankroll_{match['idEvent']}",
            )

            if best_kelly == kelly["home"]:
                home_kelly = float(kelly["home"])

                st.subheader(
                    f"Kelly percentage: {home_kelly * 100:.2f}% "
                    f"for {home} win"
                )

                st.subheader(
                    f"Kelly Allocation: ${home_kelly * bankroll:.2f}"
                )

            elif best_kelly == kelly["away"]:
                away_kelly = float(kelly["away"])

                st.subheader(
                    f"Kelly percentage: {away_kelly * 100:.2f}% "
                    f"for {away} win"
                )

                st.subheader(
                    f"Kelly Allocation: ${away_kelly * bankroll:.2f}"
                )

            else:
                draw_kelly = float(kelly["draw"])

                st.subheader(
                    f"Kelly percentage: {draw_kelly * 100:.2f}% "
                    f"for a draw"
                )

                st.subheader(
                    f"Kelly Allocation: ${draw_kelly * bankroll:.2f}"
                )