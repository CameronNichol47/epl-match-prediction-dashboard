import streamlit as st
from fixtures_api import gameweek_one
from datetime import datetime
from zoneinfo import ZoneInfo
from data.src.build_dataset import build



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



