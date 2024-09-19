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
    df = calculate_age_at_vaccination(df, 'dob', 'event_date')

    return df

st.sidebar.markdown("# :material/vaccines: Control Panel")
pages = st.sidebar.radio('Select a page', ['Childhood Imms - Heatmap', 'Childhood Imms - Searches', 'Influenza Stats', 'RSV Stats'])


if pages == 'Childhood Imms - Heatmap':
    st.title("ImmunizeMe - Childhood Imms")

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
            selected_age = st.slider(
                label="Select an **Age Group**",
                min_value=0,
                max_value=95,
                value=0,  # Default value
                help="Select the age group to display"
            )


            if selected_age < 1:
                with st.expander(":material/kitchen: Immunisation Schedule: **8 - 16 weeks**"):
                    st.image('images/8to16weeks.png')

            elif selected_age == 1:
                with st.expander(":material/kitchen: Immunisation Schedule: **1 year**"):
                    st.image('images/1yr.png')

            elif selected_age == 3 or (selected_age >= 12 and selected_age <= 13):
                with st.expander(":material/kitchen: Immunisation Schedule: **3 years**"):
                    st.image('images/3yrs.png')

            elif selected_age >= 12 and selected_age <= 14:
                with st.expander(":material/kitchen: Immunisation Schedule: **14 years**"):
                    st.image('images/14yrs.png')

            elif selected_age == 65:
                with st.expander(":material/kitchen: Immunisation Schedule: **65 years**"):
                    st.image('images/65.png')

            elif selected_age >= 70 and selected_age <= 79:
                with st.expander(":material/kitchen: Immunisation Schedule: **70 - 79 years**"):
                    st.image('images/70to79.png')

            st.markdown(f"### :material/face: Selected Age {selected_age} yrs")
            age_group_heatmap(data, selected_age)

            show_dataframe_toggle = st.sidebar.toggle("Show DataFrame", help="Show the corresponding DataFrame, allowing you to download a csv of the data.")


            if show_dataframe_toggle:
                st.divider()
                st.markdown("**DataFrame of Selected age**. - use the download `.csv` button at the top right to export this list to SMS patients.")
                st.dataframe(show_df(data, selected_age))



elif pages == 'Childhood Imms - Searches':
    st.title("ImmunizeMe - Childhood Imms - Searches")


elif pages == 'Influenza Stats':
    st.title("ImmunizeMe - Influensza Stats")



elif pages == 'RSV Stats':
    st.title("ImmunizeMe - RSV Stats")
