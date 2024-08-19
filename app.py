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
    df.rename(columns={'ImmunizeMe - vaccines: Vaccination type': 'Vaccination type'}, inplace=True)
    df = map_vaccines(df)
    df = drop_vaccines(df)

    df['Date of birth'] = pd.to_datetime(df['Date of birth'], dayfirst=True)
    df['Deduction date'] = pd.to_datetime(df['Deduction date'], dayfirst=True)
    df['Registration date'] = pd.to_datetime(df['Registration date'], dayfirst=True)


    df["age_years"] = df["Date of birth"].apply(
        lambda x: now.diff(pendulum.instance(x)).in_years()
    )
    df["age_months"] = df["Date of birth"].apply(
        lambda x: (now.diff(pendulum.instance(x)).in_months())
    )
    df["age_weeks"] = df["Date of birth"].apply(
        lambda x: (now.diff(pendulum.instance(x)).in_weeks())
    )

    df.sort_values(by='age_weeks', inplace=True)
    df = update_column_names(df)
    df = drop_deducted(df, 'deduction_date')

    return df

st.sidebar.markdown("# :material/vaccines: Control Panel")


# Only display the file uploader if sample data is not selected
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

if 'data' in locals():
    st.sidebar.divider()
    st.sidebar.subheader("Selection Tools")
    selected_age = st.sidebar.slider(
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
    age_group_heatmap(data, age_in_years=selected_age)

    show_dataframe_toggle = st.sidebar.toggle("Show DataFrame", help="Show the corresponding DataFrame, allowing you to download a csv of the data.")
    if show_dataframe_toggle:
        st.divider()
        st.write("")
        st.subheader(":material/table: DataFrame")
        st.write(":material/download: Select export to csv to download this table. Top right of dataframe.")
        st.dataframe(show_df(data, age_in_years=selected_age))
else:
    st.image("images/big.png", caption="GitHub: janduplessis883")
    st.subheader("Quick Start Guide")
    st.markdown(""":material/download: Download the **ImmunizeMe Report** for SystmOne using the button below.
                After download :material/rotate_right: **import** to Clinical Reporting in SystmOne, selecting the default import location.
                You will find the report in :material/folder: **My Reports / Python Data**.""")

    with open("images/ImmunizeMe.rpt", "rb") as file:
        file_data = file.read()

    # Create a download button
    st.download_button(
        label="Download ImmunizeMe.rpt",
        data=file_data,
        file_name="ImmunizeMe.rpt",
        mime="application/octet-stream",
    )

    st.markdown(":material/play_circle: **Run** the Report.")
    st.markdown(":material/expand_circle_down: **Breakdown** the report selecting the following fields, remember to click **Refresh** once finished.")
    if st.toggle("Video with breakdown instructions."):
        st.video("images/video.mp4")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.code("""Demographics:
    - Age in years
    - Date of birth
    - First name
    - NHS Number
    - Sex
    - Surname

Event Details:
    - Event date

Registration:
    - Deduction date
    - Registration date

Vaccinations:
    - Vaccination type
        """)

    st.markdown(":material/csv: **Export** the report to CSV, saving it to a location of your choice.")
    st.markdown(":material/upload: **Upload** your saved CSV in the control panel on the left of the app.")

    st.markdown(":material/favorite: Enjoy!")
