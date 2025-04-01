import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
import pendulum

now = pendulum.now()
current_year = now.year

reverse_name_mapping = {
    "DTaP/IPV/Hib/HepB": [
        "DTaP/IPV/Hib/HepB 1",
        "DTaP/IPV/Hib/HepB 2",
        "DTaP/IPV/Hib/HepB 3",
        "Infanrix Hexa 1",
        "Infanrix Hexa 1st Scheduled Booster",
        "Infanrix Hexa 2",
        "Infanrix Hexa 3",
        "Infanrix Hexa Booster",
        "Infanrix-IPV 1st Scheduled Booster",
        "Infanrix-IPV 2nd Scheduled Booster",
        "Infanrix-IPV Booster",
        "Infanrix-IPV+HIB 1",
        "Infanrix-IPV+HIB 1st Scheduled Booster",
        "Infanrix-IPV+HIB 2",
        "Infanrix-IPV+HIB 3",
        "Vaxelis 1",
        "Vaxelis 2",
        "Vaxelis 3",
    ],
    "DTaP/IPV/Hib": [
        "DTaP/IPV/Hib 1",
        "DTaP/IPV/Hib 1st Scheduled Booster",
        "DTaP/IPV/Hib 2",
        "DTaP/IPV/Hib 3",
        "DTaP/IPV/Hib 4",
        "DTaP/IPV/Hib Booster",
        "Pediacel 1st Scheduled Booster",
        "Pediacel 2",
        "Pediacel 3",
    ],
    "Men B": [
        "Meningitis B 1",
        "Meningitis B 2",
        "Meningitis B 3",
        "Meningitis B 4",
        "Bexsero 1",
        "Bexsero 2",
        "Bexsero 3",
        "Bexsero 4",
        "Bexsero",
    ],
    "Pneumococcal 13": [
        "Pneumococcal polysaccharide conjugated vaccine (PCV) 1",
        "Pneumococcal polysaccharide conjugated vaccine (PCV) 2",
        "Pneumococcal polysaccharide conjugated vaccine (PCV) 3",
        "Pneumococcal polysaccharide conjugated vaccine (PCV) Booster",
        "Prevenar - 13",
        "Prevenar - 13 1",
        "Prevenar - 13 2",
        "Prevenar - 13 3",
        "Prevenar - 13 Booster",
        "Pneumococcal polysaccharide vaccine (PPV) Booster",
    ],
    "MMR": [
        "Measles/Mumps/Rubella 1",
        "Measles/Mumps/Rubella Under 1 yr",
        "Measles/Mumps/Rubella 1st Scheduled Booster",
        "Measles/Mumps/Rubella 2nd Scheduled Booster",
        "MMRvaxPRO 1",
        "MMRvaxPRO 1st Scheduled Booster",
        "MMRvaxPRO Booster",
        "MMRvaxPRO Under 1 yr",
        "MMR 1",
        "MMR Booster 1",
        "MMR Booster 2",
        "Priorix 1st Scheduled Booster",
        "Priorix 1",
        "Priorix 1st Scheduled Booster",
        "Priorix Booster",
        "Priorix Under 1 yr",
    ],
    "Hep B": [
        "Hepatitis B 10 mcg/ml 1st Scheduled Booster",
        "Hepatitis B 10 mcg/ml 2",
        "Hepatitis B 10 mcg/ml 2nd Scheduled Booster",
        "Hepatitis B 10 mcg/ml 3",
        "Hepatitis B 20 mcg/ml 1",
        "Hepatitis B 20 mcg/ml 2",
        "Hepatitis B 20 mcg/ml Booster",
        "Hepatitis B Immunoglobulin (HBIG) 1",
        "Hepatitis B Strength Unspecified 1",
        "Hepatitis B Strength Unspecified 2",
        "Hepatitis B Strength Unspecified Booster",
        "Hepatyrix 1",
        "Hepatyrix 2",
        "Engerix B 1",
        "Engerix B 1st Scheduled Booster",
        "Engerix B 2",
        "Engerix B 3",
        "Engerix B Booster",
        "Engerix B paediatric 0.5ml 1",
        "Engerix B paediatric 0.5ml 1st Scheduled Booster",
        "Engerix B paediatric 0.5ml 2",
        "Engerix B paediatric 0.5ml 3",
        "Engerix B paediatric 0.5ml Booster",
        "Engerix B prefilled syringe 1ml 1",
        "Engerix B prefilled syringe 1ml 1st Scheduled Booster",
        "Engerix B prefilled syringe 1ml 2",
        "Engerix B prefilled syringe 1ml 3",
        "Engerix B prefilled syringe 1ml Booster",
        "Hepatitis B 10 mcg/ml 1",
    ],
    "Influenza": [
        "Adjuvanted quadrivalent flu vacc (SA, inact) inj 0.5ml pfs (Seqirus UK Ltd) 1",
        "Quadrivalent Influenza Vaccine (split virion, inactivated) (MASTA) 1",
        "Quadrivalent influenza vaccine Split Virion inactivated (Sanofi Pasteur) 1",
        "Influvac sub-unit Tetra (Viatris formerly Mylan) 1",
        "Influenza Vaccine 1",
        "Cell-based quadrivalent Flu/Vac/SA inj 0.5ml pfs (Seqirus UK Ltd) 1",
        "Influvac sub-unit Tetra (Viatris formerly Mylan) 1",
        "Influenza Tetra MYL vacc inj 0.5ml pre-filled syringes (Viatris UK Healthcare Ltd) 1",
        "Quadrivalent Flu/Vac/Split High-Dose inj 0.7ml pfs (Sanofi) Single",
    ],
    "HPV": [
        "Gardasil 1",
        "Gardasil 2",
        "Gardasil 3",
        "Human Papillomavirus 1",
        "Human Papillomavirus 2",
        "Human Papillomavirus 3",
    ],
    "HPV9": ["Gardasil9 1", "Gardasil9 2", "Gardasil9 3"],
    "Rotavirus": [
        "Rotarix 1",
        "Rotarix 2",
        "Rotarix",
        "Rotavirus - Oral 1",
        "Rotavirus - Oral 2",
        "Rotavirus - Oral 3",
    ],
    "Fleunz Tetra": [
        "Fluenz Tetra (AstraZeneca UK Ltd) 1",
        "Fluenz Tetra (AstraZeneca UK Ltd) 2",
        "Fluenz (trivalent) vaccine nasal suspension 0.2ml unit dose (AstraZeneca UK Ltd) 1",
        "Fluenz (trivalent) vaccine nasal suspension 0.2ml unit dose (AstraZeneca UK Ltd) 2",
    ],
    "Covid-19": [
        "COVID-19 Vacc Spikevax Orig/Omicron BA.4/BA.5 inj md vials Booster",
        "COVID-19 Vacc VidPrevtyn (B.1.351) 0.5ml inj multidose vials Booster",
        "COVID-19 mRNA Vaccine Comirnaty Children 5-11yrs 10mcg/0.2ml dose conc for disp for inj MDV (Pfizer) 1",
        "COVID-19 mRNA Vaccine Comirnaty Children 5-11yrs 10mcg/0.2ml dose conc for disp for inj MDV (Pfizer) 2",
        "COVID-19 Vacc Spikevax (XBB.1.5) 0.1mg/1ml inj md vials Booster",
        "Comirnaty Omicron XBB.1.5 COVID-19 Vacc md vials Booster",
        "Comirnaty Original/Omicron BA.4-5 COVID-19 Vacc md vials Booster",
    ],
    "BCG": ["BCG 1", "Infant BCG 1"],
    "DTP": [
        "Revaxis 1",
        "Revaxis 1st Scheduled Booster",
        "Revaxis 2",
        "Revaxis 2nd Scheduled Booster",
        "Revaxis 3",
        "Revaxis Booster",
        "Adacel vaccine suspension for injection 0.5ml pre-filled syringes 1",
        "DTaP/IPV 1",
        "DTaP/IPV 2",
        "DTaP/IPV 3",
    ],
    "Hep A": [
        "Havrix Mono Junior Monodose Booster",
        "Havrix Monodose 1",
        "Havrix Monodose 2",
        "Havrix Monodose Booster",
        "Heaf Test 1",
        "Hep B",
        "Hepatitis A + Typhoid 1",
        "Hepatitis A 1",
        "Hepatitis A 2",
        "Hepatitis A Booster",
    ],
    "Vericella Zoster": [
        "VAQTA Adult 1",
        "VARILRIX live vaccine 1",
        "VARILRIX live vaccine 2",
        "VARIVAX live vaccine 1",
        "VARIVAX live vaccine 2",
        "Varicella-Zoster live vaccine 1",
        "Varicella-Zoster live vaccine 2",
        "ViATIM 1",
        "Vivotif - oral 1",
        "Yellow Fever Single",
        "Zostavax 1",
        "Herpes Zoster vaccination (generic) 1",
        "Shingrix 2",
        "Shingrix 1",
    ],
    "Typhoid": [
        "Typherix - Single Dose Single",
        "Typhim VI - Single Dose Single",
        "Typhoid - Oral 1",
        "Typhoid 1",
        "Typhoid 2",
        "Typhoid Booster",
        "Typhoid Single",
    ],
    "Boostrix-IPV": [
        "Boostrix-IPV 1st Scheduled Booster",
        "Boostrix-IPV 2nd Scheduled Booster",
        "Boostrix-IPV Booster",
    ],
    "Men ACWY": [
        "Meningococcal conjugate A,C, W135 + Y 1",
        "MenQuadfi vaccine solution for injection 0.5ml vials (Sanofi) Single",
    ],
    "Pneumococcal 23": [
        "Pneumococcal Polysaccharide Vaccination (sanofi pasteur MSD Ltd) 1",
        "Pneumococcal Polysaccharide Vaccine (MSD) 1",
        "Pneumococcal polysaccharide vaccine (PPV) 1",
        "Pneumovax 23 1",
        "Pneumovax 23 Booster",
    ],
    "RSV": [
        "Abrysvo vaccine powder and solvent for solution for injection 0.5ml vials (Pfizer) Single",
        "Respiratory Syncytial Virus (RSV) vaccine Single",
    ],
    "Men C": [
        "Meningitec 2nd Scheduled Booster",
        "Meningitec Booster",
        "Meningitis C Conjugate Vaccine (Unspecified) Single",
        "Menitorix 1st Scheduled Booster",
        "NeisVac-C 1",
        "NeisVac-C Booster",
        "NeisVac-C Single",
    ],
    "dTaP/IPV": [
        "dTaP/IPV 1",
        "dTaP/IPV 1st Scheduled Booster",
        "dTaP/IPV 2nd Scheduled Booster",
        "DTaP/IPV 1st Scheduled Booster",
        "DTaP/IPV 2nd Scheduled Booster",
        "DTaP/IPV Booster",
        "dTaP/IPV 2",
        "dTaP/IPV 3",
        "dTaP/IPV 4",
    ],
}

vaccines_to_drop = [
    "Adacel vaccine suspension for injection 0.5ml pre-filled syringes 1",
    "Ambirix 1",
    "Anti-D Immunoglobulin 1",
    "Avaxim 1",
    "Avaxim 2",
    "Avaxim Booster",
    "Cervarix 1",
    "Cervarix 2",
    "Cervarix 3",
    "Chicken pox 1",
    "Cholera 1",
    "Cholera 2",
    "Combined Hep A / Hep B 1",
    "Combined Hep A / Hep B 2",
    "Combined Hep A / Hep B 3",
    "Fendrix 1",
    "HBVAXPRO 10 1",
    "HBVAXPRO 5 3",
    "HIB + Meningitis C 1st Scheduled Booster",
    "Havrix Mono Junior Monodose 1",
    "Ixiaro 1",
    "Ixiaro 2",
    "Japanese Encephalitis 1",
    "Japanese Encephalitis 2",
    "Japanese Encephalitis 3",
    "MENVEO Vaccine 1",
    "Mantoux test 1",
    "HNIG 1",
    "Pandemrix 1",
    "Pandemrix 2",
    "Pediacel 1",
    "Rabies Vaccine 1",
    "Rabies Vaccine 2",
    "Rabies Vaccine 3",
    "Rabies Vaccine BP (Sanofi Pasteur MSD) 1",
    "Rabies Vaccine BP (Sanofi Pasteur MSD) 3",
    "Rabies Vaccine Booster",
    "Rabipur 1",
    "Rabipur 2",
    "Rabipur 3",
    "Rabipur Booster",
    "Repevax 1",
    "Repevax 1st Scheduled Booster",
    "Repevax 2nd Scheduled Booster",
    "Repevax 3",
    "Repevax Booster",
    "STAMARIL Aventis Pasteur MSD; 1",
    "Td/IPV 1",
    "Td/IPV 1st Scheduled Booster",
    "Td/IPV 2",
    "Td/IPV 2nd Scheduled Booster",
    "Tetanus Diphtheria LD and Polio 1",
    "Tick Born Encephalitis 1",
    "Twinrix Adult 1",
    "Twinrix Adult 2",
    "Twinrix Adult 3",
    "Twinrix Adult Booster",
    "Twinrix Paediatric 1",
    "Twinrix Paediatric 2",
    "Twinrix Paediatric 3",
    "Supemtek Quadrivalent influenza  vaccine (recombinant) (Sanofi Pasteur) 1",
    "Smallpox 1",
]


def map_vaccines(df):
    for new_name, old_names in reverse_name_mapping.items():
        df["vaccination_type"] = df["vaccination_type"].replace(old_names, new_name)
    return df


def drop_vaccines(df):
    filtered_df = df[~df["vaccination_type"].isin(vaccines_to_drop)]
    return filtered_df


def prep_df(df):
    df = update_column_names(df)
    df["vaccination_type"] = df["vaccination_type"].replace("unknown", "-NO-VACCINE")

    df = map_vaccines(df)
    df = drop_vaccines(df)

    df["dob"] = pd.to_datetime(df["dob"], dayfirst=True)
    df["deduction_date"] = pd.to_datetime(df["deduction_date"], dayfirst=True)
    df["registration_date"] = pd.to_datetime(df["registration_date"], dayfirst=True)
    df["event_date"] = pd.to_datetime(df["event_date"], dayfirst=True)

    df["age_years"] = df["dob"].apply(
        lambda x: now.diff(pendulum.instance(x)).in_years()
    )
    df["age_months"] = df["dob"].apply(
        lambda x: (now.diff(pendulum.instance(x)).in_months())
    )
    df["age_weeks"] = df["dob"].apply(
        lambda x: (now.diff(pendulum.instance(x)).in_weeks())
    )

    df.sort_values(by="age_weeks", inplace=True)

    return df


def drop_deducted(df, col_name):
    return df[df[col_name].isnull()]


def age_group_heatmap(df, age_in_years=0):

    age_0 = df[df["age_years"] == age_in_years]
    result = (
        age_0.groupby(["surname", "age_weeks", "vaccination_type"])
        .size()
        .unstack(fill_value=0)
    )
    sorted_df = result.sort_values("age_weeks")

    st.write(f"Patient Count: {sorted_df.shape[0]}")
    df_length = round((sorted_df.shape[0] * 0.45), 0)
    # Create a heatmap
    # Assuming `sorted_df` is your dataset and `df_length` is its length
    plt.figure(figsize=(18, df_length))

    # Create the heatmap
    ax = sns.heatmap(sorted_df, annot=True, fmt="d", cmap="BuPu", cbar=True)

    # Set transparent background
    ax.set_facecolor((0, 0, 0, 0))  # Transparent axis background
    plt.gcf().patch.set_alpha(0)  # Transparent figure background
    plt.gca().patch.set_alpha(0)  # Transparent axis background

    # Adding title and labels
    plt.title(
        "Heatmap of Number of Vaccinations by Surname and Vaccination Type, Sorted by Age Weeks"
    )
    plt.xlabel("vaccination_type")
    plt.ylabel("surname")

    # Show the plot in Streamlit
    st.pyplot(plt)


def update_column_names(df):

    df.rename(columns=lambda x: x.lower().replace(" ", "_"), inplace=True)
    return df


def show_df(df, age_in_years=0):
    age_0 = df[df["age"] == age_in_years]
    result = (
        age_0.groupby(
            [
                "nhs",
                "first_name",
                "surname",
                "dob",
                "telephone",
                "age_years",
                "age_weeks",
                "vaccination_type",
            ]
        )
        .size()
        .unstack(fill_value=0)
    )
    sorted_df = result.sort_values("age_weeks")
    return sorted_df


def base_df_function(df):
    age_0 = df.copy()
    result = (
        age_0.groupby(
            [
                "nhs",
                "first_name",
                "surname",
                "dob",
                "telephone",
                "age_years",
                "age_weeks",
                "vaccination_type",
            ]
        )
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )
    sorted_df = result.sort_values("age_weeks")
    # Separate the first column and the rest of the columns
    first_column = [
        "nhs",
        "first_name",
        "surname",
        "dob",
        "telephone",
        "age_years",
        "age_weeks",
    ]
    other_columns = sorted_df.columns.difference(
        first_column
    )  # Get all columns except 'name'

    # Sort the rest of the columns alphabetically
    sorted_columns = sorted(other_columns)

    # Combine the first column and the sorted columns
    new_column_order = first_column + sorted_columns

    # Reorder the DataFrame based on the new column order
    new_df = sorted_df[new_column_order]

    return new_df


def calculate_age_at_vaccination(df, dob_col="dob", event_date_col="event_date"):
    """
    Calculate the age of a patient at the time of vaccination.

    Parameters:
    df (DataFrame): The DataFrame containing 'dob' and 'event_date'.
    dob_col (str): Column name for date of birth.
    event_date_col (str): Column name for the event date (vaccination date).

    Returns:
    DataFrame: A DataFrame with an additional column 'age_at_vaccination' containing the calculated ages.
    """
    # Ensure the dob and event_date columns are in datetime format
    df[dob_col] = pd.to_datetime(df[dob_col], errors="coerce")
    df[event_date_col] = pd.to_datetime(df[event_date_col], errors="coerce")

    # Calculate age at the time of vaccination
    df["age_at_vaccination"] = df.apply(
        lambda row: row[event_date_col].year
        - row[dob_col].year
        - (
            (row[event_date_col].month, row[event_date_col].day)
            < (row[dob_col].month, row[dob_col].day)
        ),
        axis=1,
    )

    return df


def update_location(df):
    most_frequent_location = df["event_done_at_id"].mode()[0]

    # Replace all other locations with 'Elsewhere'
    df["event_done_at_id"] = df["event_done_at_id"].apply(
        lambda x: x if x == most_frequent_location else "Elsewhere"
    )
    return df


def influezenza_stats_df(df):
    inf_df = df.copy()
    influenza_df = inf_df[
        (
            (inf_df["vaccination_type"] == "Influenza")
            | (inf_df["vaccination_type"] == "Fleunz Tetra")
        )
    ]
    influenza_df = update_location(influenza_df)
    return influenza_df


def to_timeseries(df, column, time_period="M"):
    # Resample and count occurrences in each period
    m_count = df.resample(time_period, on=column).size()

    # Convert to DataFrame
    m_count_df = m_count.reset_index()

    # Rename columns
    m_count_df.columns = ["date", "count"]
    ts = m_count_df[m_count_df["date"] >= "2018-08-30"]
    return ts


def make_dropdown_list(data):
    return list(data["event_done_at_id"].unique())


def count_year(df, years_back=0):
    filtered_df = df[
        (df["event_date"] > pd.Timestamp(f"{current_year-years_back-1}-09-01"))
        & (df["event_date"] < pd.Timestamp(f"{current_year-years_back}-03-31"))
    ]
    # Count vaccines for each age group
    children_count = filtered_df[filtered_df["age_at_vaccination"] <= 18][
        "patient_count"
    ].sum()
    adult_count = filtered_df[
        (filtered_df["age_at_vaccination"] > 18)
        & (filtered_df["age_at_vaccination"] < 65)
    ]["patient_count"].sum()
    senior_count = filtered_df[filtered_df["age_at_vaccination"] >= 65][
        "patient_count"
    ].sum()

    return [children_count, adult_count, senior_count]
