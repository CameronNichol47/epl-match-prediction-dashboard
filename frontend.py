import streamlit as st
from testing import matches

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

for match in matches:
    with st.expander(match["home"] + " vs " +  match["away"]):
        st.write(...)


