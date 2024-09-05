import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from io import StringIO
import os
from function import *

import pendulum
now = pendulum.now()

st.set_page_config(page_title="ImmunizeMe", layout="wide")
st.logo("images/logo.png")

html = """
<style>
.gradient-text {
    background: linear-gradient(45deg, #284d74, #d8ad45, #b2d9db, #e16d33);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    font-size: 52px;
    font-weight: bold;
}
</style>
<div class="gradient-text">ImmunizeMe</div>
"""
st.markdown(html, unsafe_allow_html=True)


@st.cache_data(ttl=60 * 60)
def loadcsv(stringio):
    df = pd.read_csv(stringio)
    df.columns = ['Patient ID1', 'Patient ID2',
       'Age', 'dob', 'First name', 'NHS', 'Sex',
       'Surname', 'Deduction date', 'Registration date',
       'Vaccination type', 'telephone',
       'Event date',
       'Event done at ID', 'Patient Count']
    df = prep_df(df)

    return df

def calculate_age_at_vaccination(df, dob_col='dob', event_date_col='event_date'):
    """
    Calculate the age of a patient at the time of vaccination.

    Parameters:
    df (DataFrame): The DataFrame containing 'dob' and 'event_date'.
    dob_col (str): Column name for date of birth.
    event_date_col (str): Column name for the event date (vaccination date).

    Returns:
    DataFrame: A DataFrame with an additional column 'age_at_vaccination' containing the calculated ages.
    """
    # Convert dob and event_date columns to pendulum date objects
    df[dob_col] = df[dob_col].apply(lambda x: pendulum.parse(x))
    df[event_date_col] = df[event_date_col].apply(lambda x: pendulum.parse(x))

    # Calculate age at the time of vaccination
    df['age_at_vaccination'] = df.apply(lambda row: row[event_date_col].diff(row[dob_col]).years, axis=1)

    return df



st.sidebar.markdown("# :material/vaccines: Control Panel")

toggle2 = st.sidebar.checkbox("Load sample data")
if toggle2:
    url = "images/sample_data2.csv"
    data = loadcsv(url)
else:
    st.sidebar.subheader("Upload data")
    uploaded_file = st.sidebar.file_uploader("Upload .csv file", type="csv")
    if uploaded_file is not None:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        data = loadcsv(stringio)


pages = st.sidebar.radio('Select a page', ['Childhood Imms', 'Search Tool', 'Influenza'])

# Only display the file uploader if sample data is not selected

if pages == 'Childhood Imms':


    if 'data' in locals():
        st.subheader("Selection Tools")
        selected_age = st.slider(
            label="Select an **Age Group**",
            min_value=0,
            max_value=95,
            value=0,  # Default value
            help="Select the age group to display"
        )


        if selected_age < 1:
            st.image('images/8to16weeks.png')
        elif selected_age == 1:
            st.image('images/1yr.png')
        elif selected_age == 3 or (selected_age >= 12 and selected_age <= 13):
            st.image('images/3yrs.png')
        elif selected_age >= 12 and selected_age <= 14:
            st.image('images/14yrs.png')
        elif selected_age == 65:
            st.image('images/65.png')
        elif selected_age >= 70 and selected_age <= 79:
            st.image('images/70to79.png')
        st.markdown(f"### :material/face: Selected Age {selected_age} yrs")
        age_group_heatmap(data, selected_age)

        show_dataframe_toggle = st.sidebar.toggle("Show DataFrame", help="Show the corresponding DataFrame, allowing you to download a csv of the data.")

        data = calculate_age_at_vaccination(data, 'dob', 'event_date')
        st.dataframe(data)
