import pandas as pd
import plotly.express as px
import streamlit as st

def pie_chart(home, away, probabilities, type):
    data = {
        "Category": [f"{away} Win", "Draw", f"{home}"],
        "Quantity": probabilities,
    }
    df = pd.DataFrame(data)

    fig = px.pie(df, values="Quantity", names="Category", title=f"{home} VS {away} {type} Predictons")

    home_probability = probabilities[2] * 100
    draw_probability = probabilities[1] * 100
    away_probability = probabilities[0] * 100

    st.plotly_chart(fig)

    col1, col2, col3 = st.columns(3)

    col1.metric(f"{home} Win", f"{home_probability:.1f}%")
    col2.metric("Draw", f"{draw_probability:.1f}%")
    col3.metric(f"{away} Win", f"{away_probability:.1f}%")