import streamlit as st
import pandas as pd
import altair as alt

url = "https://raw.githubusercontent.com/datasets/covid-19/main/data/countries-aggregated.csv"
df = pd.read_csv(url)

df['NumDays'] = pd.to_datetime(df['Date']) - pd.to_datetime('2020-01-22')
df['NumDays'] = pd.to_numeric(df['NumDays'])/(60*60*12*1000000000)
df['NumDays'] = df['NumDays'].astype(int)

df['Date'] = pd.to_datetime(df['Date'])

st.title("COVID-19 Global Time Series")
st.write("Select a country or countries and measures from the panel at the left.")

countries = st.sidebar.multiselect(
    "Select Countries",
    df['Country'].unique()
    )

statlist = df.columns.drop(['Date', 'Country', 'NumDays'])
stats = st.sidebar.multiselect("Select stat", statlist)
dropstats = statlist.drop(stats)

type = st.sidebar.selectbox("Chart Type", ["Compare countries by each measure", "Compare measures for each country"])

df_subset = df.loc[lambda d: d['Country'].isin(countries)]
df_dates = df_subset['Date']
df_subset = df_subset.groupby(['Country'], as_index = False).rolling(window = 7).mean()
st.write(df_subset)
df_subset = df_subset.join(df_dates)
df_subset = df_subset.groupby(['Country'], as_index = False).resample('7D', on = 'Date').last()

if type == "Compare measures for each country":
    for country in countries:
        st.write(country)
        current_df = df_subset.loc[lambda d: d['Country'] == country]
        current_df = current_df.drop(columns = dropstats)
        current_df = current_df.drop(columns = ['NumDays', 'Country'])
        current_df = pd.melt(current_df, id_vars = 'Date', value_vars = stats, var_name = 'Measure', value_name = 'Count')

        line_chart = alt.Chart(current_df).mark_line().encode(
            x = 'Date',
            y = 'Count',
            color='Measure',
            strokeDash = 'Measure'
        ).properties(
            title='title'
        )

        st.altair_chart(line_chart)
        
else:
    for stat in stats:
        st.write(stat)
        current_df = pd.melt(df_subset, id_vars = 'Date', value_vars = stats, var_name = 'Measure', value_name = 'Count')
        st.write(current_df)
