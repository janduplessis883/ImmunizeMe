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
st. markdown("# :material/vaccines: ImmunizeMe")
st.logo("images/logo.png")


@st.cache_data(ttl=60 * 60)
def loadcsv(stringio):
    df = pd.read_csv(stringio)
    df = map_vaccines(df)
    df = drop_vaccines(df)

    df['Date of birth'] = pd.to_datetime(df['Date of birth'], dayfirst=True)
    df['Deduction date'] = pd.to_datetime(df['Deduction date'], dayfirst=True)
    df['Registration date'] = pd.to_datetime(df['Registration date'], dayfirst=True)
    df['Event date'] = pd.to_datetime(df['Event date'], dayfirst=True)

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


st.sidebar.title("Configure")
    # Only display the file uploader if sample data is not selected
uploaded_file = st.sidebar.file_uploader("Choose a .csv or .xslx file", type="csv")

if uploaded_file is not None:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    data = loadcsv(stringio)

    if data is not None:
        selected_age = st.sidebar.slider(
        label="Select an **Age Group**",
        min_value=0,
        max_value=99,
        value=0,  # Default value
        help="Select the age group to display"
        )

        if selected_age < 1:
            st.image('images/8to16weeks.png')
        elif selected_age == 1:
            st.image('images/1yr.png')
        elif selected_age == 3:
            st.image('images/3yrs.png')
        elif selected_age == 14:
            st.image('images/14yrs.png')
        elif selected_age == 65:
            st.image('images/65.png')
        elif selected_age >= 70 and selected_age <= 79:
            st.image('images/70to79.png')
        st.markdown(f"### Seleceted Age {selected_age} yrs")
        age_group_heatmap(data, age_in_years=selected_age)
