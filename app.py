import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from io import StringIO
import os
from function import *  # Assuming functions like prep_df, calculate_age_at_vaccination, etc. are defined here

import pendulum
now = pendulum.now()

st.set_page_config(page_title="ImmunizeMe", layout="wide")
st.sidebar.markdown("# :material/vaccines: Control Panel")

@st.cache_data(ttl=60 * 60)
def loadcsv(stringio):
    df = pd.read_csv(stringio, encoding='latin1')
    df.columns = ['Patient ID1', 'Patient ID2', 'Age', 'dob', 'First name', 'NHS', 'Sex',
                  'Surname', 'Deduction date', 'Registration date', 'Vaccination type', 'telephone',
                  'Event date', 'Event done at ID', 'Patient Count']
    df = prep_df(df)
    df = calculate_age_at_vaccination(df, 'dob', 'event_date')
    return df

# Sample data loading function
def load_sample_data():
    url = "images/sample_data2.csv"
    return loadcsv(url)

# File uploader logic and session state handling
def handle_file_upload():
    uploaded_file = st.sidebar.file_uploader("Upload .csv file", type="csv")
    if uploaded_file is not None:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        return loadcsv(stringio)
    return None

# Check if the data is already in session state, if not load it
if 'data' not in st.session_state:
    st.session_state.data = None

# Sidebar for file upload and loading sample data
st.sidebar.subheader("Upload Data")
toggle2 = st.sidebar.checkbox("Load sample data")
if toggle2:
    st.session_state.data = load_sample_data()
else:
    uploaded_data = handle_file_upload()
    if uploaded_data is not None:
        st.session_state.data = uploaded_data

st.sidebar.divider()
# Sidebar for navigation (this appears after file upload section)
st.sidebar.subheader("Navigation")
pages = st.sidebar.radio('Select a page', ['Childhood Imms - Heatmap', 'Childhood Imms - Searches', 'Influenza Stats', 'RSV Stats'])


if pages == 'Childhood Imms - Heatmap':
    st.title("ImmunizeMe - Childhood Imms: Heatmap")

    # If data exists in session state, proceed to display
    if st.session_state.data is not None:
        selected_age = st.slider(
            label="Select an **Age Group**",
            min_value=0,
            max_value=95,
            value=0,  # Default value
            help="Select the age group to display"
        )

        # Logic to display images based on selected age group
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
        age_group_heatmap(st.session_state.data, selected_age)

        # Toggle to show DataFrame
        st.sidebar.divider()
        show_dataframe_toggle = st.sidebar.checkbox("Show DataFrame", help="Show the corresponding DataFrame, allowing you to download a csv of the data.")

        if show_dataframe_toggle:
            st.divider()
            st.markdown("**DataFrame of Selected age**. - use the download `.csv` button at the top right to export this list to SMS patients.")
            st.dataframe(show_df(st.session_state.data, selected_age))


elif pages == 'Childhood Imms - Searches':
    st.title("ImmunizeMe - Childhood Imms: Searches")
    # Create a slider to select an age range between 0 and 95
    st.sidebar.divider()
    st.sidebar.header("Build Search")
    age_range = st.sidebar.slider(
        label="Select an **Age Range**",
        min_value=0,
        max_value=95,
        value=(0, 15),  # Default range, you can change this if needed
        help="Select the age range for your analysis"
    )

    # Display the selected range
    st.sidebar.markdown(f"Selected age range: **{age_range[0]} - {age_range[1]} years**")
    st.sidebar.divider()



    # Vaccination options for the first multiselect
    vaccination_groups = [
        "-NO-VACCINE", "DTaP/IPV/Hib/HepB", "MMR", "MenB", "Rotavirus", "Pneumococcal", "Hib/MenC", "HPV", "Influenza", "Shingles", "Covid-19", "RSV", "MenACWY"
    ]

    # First multiselect for choosing vaccination groups
    selected_vaccination_groups = st.sidebar.multiselect(
        label="Select **Vaccination Groups**",
        options=vaccination_groups,
        help="Select the vaccination groups to track dose status"
    )

    # Dynamically generate number selectors for each selected vaccination group
    dose_selection = {}
    st.sidebar.divider()
    if selected_vaccination_groups:
        st.write("### Select Number of Doses for Each Vaccination Group")
        for group in selected_vaccination_groups:
            # For each selected vaccination group, create a number selector with options 0, 1, 2, or 3
            doses = st.sidebar.selectbox(
                label=f"Number of doses for **{group}**:",
                options=[0, 1, 2, 3],
                index=0,  # Default to 0 doses
                key=group  # Unique key for each selectbox to avoid issues with Streamlit's state
            )
            # Store the selection in a dictionary
            dose_selection[group] = doses
    st.divider()
    # Display the user's selections
    if dose_selection:
        st.sidebar.write(dose_selection)



# Example base_df DataFrame (Assuming you have this in your code already)
# It should contain an 'age_years' column and columns named after each vaccine group
# with values indicating the number of doses a person has had.


    base_df = base_df_function(st.session_state.data)
    st.code(base_df.columns)

    # Age range selection
    age_range = st.slider(
        label="Select Age Range",
        min_value=0,
        max_value=95,
        value=(0, 95),  # Default range
        help="Select the age range to filter the patients"
    )

    # Vaccination options for the first multiselect
    vaccination_groups = [
        "DTaP/IPV/Hib/HepB", "MMR", "MenB", "Rotavirus", "Pneumococcal", "Influenza", "Shingles", "Covid-19"
    ]

    # First multiselect for choosing vaccination groups
    selected_vaccination_groups = st.multiselect(
        label="Select Vaccination Groups",
        options=vaccination_groups,
        help="Select the vaccination groups to filter by dose status"
    )

    # Initialize a dictionary to store the selected dose filters for each vaccine group
    dose_selection = {}

    # Dynamically generate number selectors for each selected vaccination group
    if selected_vaccination_groups:
        st.write("### Select Number of Doses for Each Vaccination Group")
        for group in selected_vaccination_groups:
            doses = st.selectbox(
                label=f"Number of doses for {group}:",
                options=[0, 1, 2, 3],
                index=0,  # Default to 0 doses
                key=group  # Unique key for each selectbox to avoid issues with Streamlit's state
            )
            dose_selection[group] = doses

    # Now apply the filters on base_df

    # 1. Filter based on age range
    filtered_df = base_df[(base_df['age_years'] >= age_range[0]) & (base_df['age_years'] <= age_range[1])]

    # 2. Filter based on vaccination group and doses
    for group, doses in dose_selection.items():
        if group in filtered_df.columns:
            filtered_df = filtered_df[filtered_df[group] == doses]

    # Display the filtered DataFrame
    st.write("### Filtered Data")
    st.dataframe(filtered_df)

    # Filter by Vaccine Group














elif pages == 'Influenza Stats':
    st.title("ImmunizeMe - Influenza Stats")
    # Implement your logic here for Influenza stats

elif pages == 'RSV Stats':
    st.title("ImmunizeMe - RSV Stats")
    # Implement your logic here for RSV stats
