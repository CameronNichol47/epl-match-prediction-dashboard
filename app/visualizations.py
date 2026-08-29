import pandas as pd
import plotly.express as px
import streamlit as st

def pie_chart(home, away, probabilities, type):

    away_prob = probabilities[0]
    draw_prob = probabilities[1]
    home_prob = probabilities[2]

    data = {
        "Category": [
            f"{home} Win",
            "Draw",
            f"{away} Win",
        ],
        "Quantity": [
            home_prob,
            draw_prob,
            away_prob,
        ],
    }

    df = pd.DataFrame(data)

    fig = px.pie(
        df,
        values="Quantity",
        names="Category",
        title=f"{home} VS {away} {type} Predictions"
    )

    st.plotly_chart(fig)

    col1, col2, col3 = st.columns(3)

    col1.metric(
        f"{home} Win",
        f"{home_prob * 100:.1f}%"
    )

    col2.metric(
        "Draw",
        f"{draw_prob * 100:.1f}%"
    )

    col3.metric(
        f"{away} Win",
        f"{away_prob * 100:.1f}%"
    )