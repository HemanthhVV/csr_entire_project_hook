import streamlit as st
from functions import *
st.set_page_config(page_title="Coats-Kidney Analysis",page_icon="coats.png")
# st.toast("hello universe!",icon='❤')
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 200px !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.write("Hello Universe!")