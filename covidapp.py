import streamlit as st
import pandas as pd
import altair as alt

#Get Covid-19 data by country
url = "https://raw.githubusercontent.com/datasets/covid-19/main/data/countries-aggregated.csv"
df = pd.read_csv(url)

#Get country population data
url2 = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQWDB7LlBd2xZivtvv4T_Wh7Bmqh79Ed6CWAZnyMB23-Q-yHpGGew9_0OLV2xWqVXDywBV07FFe7YhL/pub?gid=1075357968&single=true&output=csv"
pop = pd.read_csv(url2)
pop = pop.rename(columns={'Country (or dependency)': 'Country'})

#dictionary for renaming population data to match covid country names
dict = {'Myanmar': 'Burma', 'Côte d\'Ivoire':'Cote d\'Ivoire', 'South Korea': 'Korea, South',
        'Saint Kitts & Nevis': 'Saint Kitts and Nevis', 'St. Vincent & Grenadines': 'Saint Vincent and the Grenadines',
        'United States': 'US', 'Czech Republic (Czechia)': 'Czechia'}

pop['Country'] = pop['Country'].replace(dict)

df = pd.merge(df, pop[['Country', 'Population (2020)']], on='Country', how='left')

#Add a number of days count to each set of country data
df['NumDays'] = pd.to_datetime(df['Date']) - pd.to_datetime('2020-01-22')
df['NumDays'] = pd.to_numeric(df['NumDays'])/(60*60*12*1000000000)
df['NumDays'] = df['NumDays'].astype(int)

#Change Date from string to datetime format
df['Date'] = pd.to_datetime(df['Date'])

#Add page title and intro
st.title("COVID-19 Global Time Series")
st.write("Select a country or countries and measures from the panel at the left.")

#Create sidebar widgets
countries = st.sidebar.multiselect(
    "Select Countries",
    df['Country'].unique()
    )

statlist = df.columns.drop(['Date', 'Country', 'NumDays', 'Population (2020)'])
stats = st.sidebar.multiselect("Select stat", statlist)
dropstats = statlist.drop(stats)

type = st.sidebar.selectbox("Chart Type", ["Compare countries by each measure", "Compare measures for each country"])

#Apply widget selections to covid dataset
df_subset = df.loc[lambda d: d['Country'].isin(countries)]
df_dates = df_subset['Date']
df_subset = df_subset.groupby(['Country'], as_index = False).rolling(window = 7).mean()
df_subset = df_subset.join(df_dates)
df_subset = df_subset.groupby(['Country'], as_index = False).resample('7D', on = 'Date').last()

if type == "Compare measures for each country":
    for country in countries:
        st.write(country)
        current_df = df_subset.loc[lambda d: d['Country'] == country]
        popn = current_df['Population (2020)'].iloc[1]
        current_df = current_df.drop(columns = dropstats)
        current_df = current_df.drop(columns = ['NumDays', 'Country'])
        current_df = pd.melt(current_df, id_vars = ['Date'], value_vars = stats, var_name = 'Measure', value_name = 'Count')
        current_df['Per Capita'] = (current_df['Count']/popn) * 100000

        line_chart = alt.Chart(current_df).mark_line().encode(
            x = 'Date',
            y = 'Per Capita',
            color='Measure',
            strokeDash = 'Measure')
        st.altair_chart(line_chart)
        
else:
    this_df = pd.melt(df_subset, id_vars = ['Date', 'Country'], value_vars = stats, var_name = 'Measure', value_name = 'Count')
    st.write(this_df)
    for stat in stats:
        st.write(stat)
        current_df = this_df.loc[lambda d: d['Measure'] == stat]
        
        line_chart = alt.Chart(current_df).mark_line().encode(
            x = 'Date',
            y = 'Count',
            color = 'Country', 
            strokeDash = 'Country')
        st.altair_chart(line_chart)
        



