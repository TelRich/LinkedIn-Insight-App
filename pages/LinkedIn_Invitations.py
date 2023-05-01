"""
@Created on: Monday, May 1, 2023, 7:20:02 AM WAT

@Author: TelRich Data

"""


import streamlit as st
import pandas as pd
import plotly.express as px

st.markdown("<h3 style='text-align:center;'>LinkedIn Invitations</h3>", unsafe_allow_html=True)
file = st.file_uploader('Upload Invitations', type="csv")

@st.cache_data
def save_upload():
    uploaded_file = pd.read_csv(file)
    return uploaded_file
df = save_upload()

if df is not None:
    st.write(df)
