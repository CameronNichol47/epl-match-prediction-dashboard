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

        if st.button("Load Prediction", key=match["idEvent"]):
            st.write(f"Creating prediction for {home} vs {away}...")
            build(home, away)

            prob, shap_figure = model(home, away)

            pie_chart(home, away, prob)

            st.subheader("Why the model made this prediction")
            st.pyplot(shap_figure)
            
            




