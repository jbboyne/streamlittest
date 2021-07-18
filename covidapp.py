import streamlit as st
import pandas as pd
import altair as alt

url = "https://raw.githubusercontent.com/datasets/covid-19/main/data/countries-aggregated.csv"
df = pd.read_csv(url)

df['NumDays'] = pd.to_datetime(df['Date']) - pd.to_datetime('2020-01-22')
df['NumDays'] = pd.to_numeric(df['NumDays'])/(60*60*12*1000000000)
df['NumDays'] = df['NumDays'].astype(int)

df['Date'] = pd.to_datetime(df['Date'])

st.title("COVID-19 Global Cases Time Series")

countries = st.sidebar.multiselect(
    "Select Countries",
    df['Country'].unique()
    )

statlist = df.columns.drop(['Date', 'Country', 'NumDays'])
stats = st.sidebar.multiselect("Select stat", statlist)
dropstats = statlist.drop(stats)

df_subset = df.loc[lambda d: d['Country'].isin(countries)]
df_dates = df_subset[['Date', 'Country']]
df_subset = df_subset.groupby(['Country'], as_index = False).rolling(window = 7).mean()
# df_subset = df_subset.join(df_dates, lsuffix = 'l', rsuffix = 'r')
# df_subset = df_subset.resample('7D', on = 'Date').last()
st.write(df_subset['Country'].unique())

# for country in countries:
#     st.write(country)
#     current_df = df_subset.loc[lambda d: d['Country'] == country]
#     current_df = current_df.drop(columns = dropstats)
#     current_df = current_df.drop(columns = ['NumDays', 'Country'])
#     current_df = pd.melt(current_df, id_vars = ['Date', 'Country'], value_vars = stats, var_name = 'Measure', value_name = 'Count')
#     st.write(current_df)
    
#     line_chart = alt.Chart(current_df).mark_line().encode(
#         x = 'Date',
#         y = 'Count',
#         color='Measure',
#         strokeDash = 'Measure'
#     ).properties(
#         title='title'
#     )

#     st.altair_chart(line_chart)

