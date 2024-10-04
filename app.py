import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from io import StringIO
import os
from function import *  # Assuming functions like prep_df, calculate_age_at_vaccination, etc. are defined here
import streamlit_shadcn_ui as ui
import pendulum
now = pendulum.now()
current_year = now.year
from time import sleep
from stqdm import stqdm

st.set_page_config(page_title="ImmunizeMe", layout="wide")
st.title("ImmunizeMe")
pages = ui.tabs(
    options=[
        "Quick Start",
        "Childhood Imms - Heatmap",
        "All Immunisations - Search",
        "Influenza Stats",
        "RSV Stats",
    ],
    default_value="Quick Start",
    key="mainnav",
)
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
    url = "images/sample_data3.csv"
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



if pages == 'Childhood Imms - Heatmap':
    st.header("Childhood Imms - Heatmap")
    if st.session_state.data is None:
        st.warning("No data loaded. Load Sample data or upload your own dataset.")
        st.stop()
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

        show_dataframe_toggle = st.sidebar.checkbox("Show DataFrame", help="Show the corresponding DataFrame, allowing you to download a csv of the data.")

        if show_dataframe_toggle:
            st.divider()
            st.markdown("**DataFrame of Selected age**. - use the download `.csv` button at the top right to export this list to SMS patients.")
            st.dataframe(show_df(st.session_state.data, selected_age))


elif pages == 'All Immunisations - Search':
    st.header("All Immunisations - Search")
    if st.session_state.data is None:
        st.warning("No data loaded. Load Sample data or upload your own dataset.")
        st.stop()
# Example base_df DataFrame (Assuming you have this in your code already)
# It should contain an 'age_years' column and columns named after each vaccine group
# with values indicating the number of doses a person has had.


    base_df = base_df_function(st.session_state.data)

    if 'Normal Immunoglobulin 1' in base_df.columns:
        base_df.drop(columns=['Normal Immunoglobulin 1'], inplace=True)
    if 'Adacel vaccine suspension for injection 0.5ml pre-filled syringes 1' in base_df.columns:
        base_df.drop(columns=['Adacel vaccine suspension for injection 0.5ml pre-filled syringes 1'], inplace=True)

    # Age range selection
    age_range = st.sidebar.slider(
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
    selected_vaccination_groups = st.sidebar.multiselect(
        label="Select **Vaccination Groups**",
        options=vaccination_groups,
        help="Select the vaccination groups to filter by dose status - Adding more than one group works as an AND statement."
    )

    # Initialize a dictionary to store the selected dose filters for each vaccine group
    dose_selection = {}
    if not dose_selection:
        pass
    else:
        st.sidebar.divider()
    # Dynamically generate number selectors for each selected vaccination group
    if selected_vaccination_groups:
        st.sidebar.write("Select **Number of Doses** for Each Vaccination Group")
        for group in selected_vaccination_groups:
            if group == '-NO-VACCINE':
                doses = st.sidebar.selectbox(
                    label=f"Number of doses for **{group}**:",
                    options=[1,],
                    index=0,  # Default to 0 doses
                    key=group  # Unique key for each selectbox to avoid issues with Streamlit's state
                )
                st.write("-NO-VACCINE = 1 (List all Patients who has no vaccination record.)")
            else:
                max_no = base_df[group].max()
                doses = st.sidebar.selectbox(
                    label=f"Number of doses for **{group}**:",
                    options=list(range(0, max_no+1)),  # Ensure options are correctly defined
                    index=0,  # Default to 0 doses
                    key=group  # Unique key for each selectbox to avoid issues with Streamlit's state
                )
            dose_selection[group] = doses

    # Now apply the filters on base_df

    # 1. Filter based on age range
    filtered_df = base_df[(base_df['age_years'] >= age_range[0]) & (base_df['age_years'] <= age_range[1])]
    st.write("### Filtered Data")
    st.markdown(f"Searching Age Range **{age_range[0]} - {age_range[1]} yrs**")
    # Create the plot

    # 2. Filter based on vaccination group and doses
    for group, doses in dose_selection.items():
        if group in filtered_df.columns:
            filtered_df = filtered_df[filtered_df[group] == doses]

    fig, ax = plt.subplots(figsize=(20, 3))
    sns.histplot(filtered_df['age_years'], color='#edc55c')
    ax.yaxis.grid(True, linestyle="--", linewidth=0.5, color="#888888")
    ax.xaxis.grid(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig)

    # Display the filtered DataFrame
    st.markdown(f"### Patient Count: {filtered_df.shape[0]}")
    st.dataframe(filtered_df)


    # Filter by Vaccine Group
















elif pages == 'Influenza Stats':
    st.header("Influenza Stats")
    # Implement your logic here for Influenza stats
    if st.session_state.data is None:
        st.warning("No data loaded. Load Sample data or upload your own dataset.")
        st.stop()

    influenza_df = influezenza_stats_df(st.session_state.data)

    location = st.sidebar.selectbox("Select **Vaccination Location**", options=make_dropdown_list(influenza_df), index=0)

    influenza_df = influenza_df[influenza_df['event_done_at_id'] == location]

    month_df = to_timeseries(influenza_df, 'event_date', time_period='M')

    fig, ax = plt.subplots(figsize=(20, 6))

    # Create the bar plot
    sns.barplot(x='date', y='count', data=month_df, ax=ax)

    # Customize grid and remove unnecessary spines
    ax.yaxis.grid(True, linestyle="--", linewidth=0.5, color="#888888")
    ax.xaxis.grid(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

    # Add data points above each bar
    for p in ax.patches:
        ax.text(
            p.get_x() + p.get_width() / 2,  # X-position at the center of each bar
            p.get_height(),  # Y-position just above the bar
            f'{int(p.get_height())}',  # Text to display (rounded to integer)
            ha='center',  # Horizontal alignment
            va='bottom'  # Vertical alignment
        )

    # Set title
    plt.title(f"Influenza vaccines administered - {location} (Children, Under & Over)")

    # Rotate x-ticks for better visibility if needed
    plt.xticks(rotation=90)

    # Ensure layout looks nice
    plt.tight_layout()

    # Display the plot in Streamlit
    st.pyplot(fig)



    for i in range(0, 2):
        years_back = i
        child, under, over = count_year(influenza_df, years_back=years_back)

        c1, c2, c3, c4 = st.columns(4, gap='medium')
        with c1:
            st.markdown(f"### {current_year-years_back-1}/{current_year-years_back}")
        with c2:
            st.metric("Children < 18", child)
        with c3:
            st.metric("18 - 64yrs", under)
        with c4:
            st.metric("65yrs and over", over)

        st.divider()









elif pages == 'RSV Stats':
    st.header("RSV Stats")
    # Implement your logic here for RSV stats
    if st.session_state.data is None:
        st.warning("No data loaded. Load Sample data or upload your own dataset.")
        st.stop()



elif pages == 'Quick Start':
    st.header("Quick Start")
    # Implement your logic here for RSV stats
    st.subheader("SystmOne")
    st.markdown("Download the ImmunizeMe SystmOne Search, and import with default settings to SystmOne.")

    # File path
    file_path = 'images/ImmunizeMe.rpt'

    # Open the file in binary mode
    with open(file_path, 'rb') as file:
        file_data = file.read()

    # Create a download button
    st.download_button(
        label="Download ImmunizeMe Report",
        data=file_data,
        file_name="ImmunizeMe.rpt",
        mime='application/octet-stream'
    )

    st.markdown("Within **Clinical Reporting** navigate to where the search is located: **My Reports/Python-data/ImmunizeMe - RUN ME**")
    st.markdown("Right Click ImmunizeMe - RUN ME and **breakdown** results. Export the result to `.csv`")
    c1, c2 = st.columns(2)
    with c1:
        with st.container(height=400, border=True):
            st.image('images/systmone.png')
    with c2:
        st.write()

    c3, c4 = st.columns([8,1])
    with c3:
        st.markdown("### Update the **date format** of your `.csv` ")
        with st.container(height=400, border=True):
            st.image('images/excels.png')
    with c4:
        st.write()
