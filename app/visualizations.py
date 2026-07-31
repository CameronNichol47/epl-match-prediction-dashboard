import pandas as pd
import plotly.express as px
import streamlit as st

def pie_chart(home, away, probabilities):
    data = {
        "Category": [f"{away} Win", "Draw", f"{home}"],
        "Quantity": probabilities,
    }
    df = pd.DataFrame(data)

    fig = px.pie(df, values="Quantity", names="Category", title="Fruit Distribution")

    st.plotly_chart(fig)