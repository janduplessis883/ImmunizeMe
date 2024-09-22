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
        try:
            # Try reading the file using UTF-8 encoding
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        except UnicodeDecodeError:
            # If it fails, try reading with Latin-1 encoding
            stringio = StringIO(uploaded_file.getvalue().decode("latin1"))

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

# Example base_df DataFrame (Assuming you have this in your code already)
# It should contain an 'age_years' column and columns named after each vaccine group
# with values indicating the number of doses a person has had.


    base_df = base_df_function(st.session_state.data)

    if 'Normal Immunoglobulin 1' in base_df.columns:
        base_df.drop(columns=['Normal Immunoglobulin 1'], inplace=True)
    if 'Adacel vaccine suspension for injection 0.5ml pre-filled syringes 1' in base_df.columns:
        base_df.drop(columns=['Adacel vaccine suspension for injection 0.5ml pre-filled syringes 1'], inplace=True)


    # Age range selection
    age_range = st.slider(
        label="Select **Age Range**",
        min_value=0,
        max_value=95,
        value=(0, 95),  # Default range
        help="Select the age range to filter the patients"
    )
    vacc_groups = list(base_df.columns)[7:]
    vacc_groups_sorted = sorted(vacc_groups)
    # st.code(vacc_groups_sorted)
    # Vaccination options for the first multiselect
    vaccination_groups = vacc_groups_sorted

    # First multiselect for choosing vaccination groups
    selected_vaccination_groups = st.multiselect(
        label="Select **Vaccination Groups**",
        options=vaccination_groups,
        help="Select the vaccination groups to filter by dose status - Adding more than one group works as an AND statement."
    )

    # Initialize a dictionary to store the selected dose filters for each vaccine group
    dose_selection = {}

    # Dynamically generate number selectors for each selected vaccination group
    if selected_vaccination_groups:
        st.write("### Select Number of Doses for Each Vaccination Group")
        for group in selected_vaccination_groups:
            if group == '-NO-VACCINE':
                doses = st.selectbox(
                    label=f"Number of doses for **{group}**:",
                    options=[1,],
                    index=0,  # Default to 0 doses
                    key=group  # Unique key for each selectbox to avoid issues with Streamlit's state
                )
            else:
                max_no = base_df[group].max()
                doses = st.selectbox(
                    label=f"Number of doses for **{group}**:",
                    options=list(range(0, max_no+1)),  # Ensure options are correctly defined
                    index=0,  # Default to 0 doses
                    key=group  # Unique key for each selectbox to avoid issues with Streamlit's state
                )
            dose_selection[group] = doses

    # Now apply the filters on base_df

    # 1. Filter based on age range
    filtered_df = base_df[(base_df['age_years'] >= age_range[0]) & (base_df['age_years'] <= age_range[1])]
    st.divider()
    st.write("### Filtered Data")
    # Create the plot
    fig, ax = plt.subplots(figsize=(20, 3))
    sns.histplot(filtered_df['age_years'], color='#edc55c')
    ax.yaxis.grid(True, linestyle="--", linewidth=0.5, color="#888888")
    ax.xaxis.grid(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig)

    # 2. Filter based on vaccination group and doses
    for group, doses in dose_selection.items():
        if group in filtered_df.columns:
            filtered_df = filtered_df[filtered_df[group] == doses]

    # Display the filtered DataFrame
    st.markdown(f"### No of Rows: {filtered_df.shape[0]}")
    st.dataframe(filtered_df)


    # Filter by Vaccine Group
















elif pages == 'Influenza Stats':
    st.title("ImmunizeMe - Influenza Stats")
    # Implement your logic here for Influenza stats

elif pages == 'RSV Stats':
    st.title("ImmunizeMe - RSV Stats")
    # Implement your logic here for RSV stats
