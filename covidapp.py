import streamlit as st
import pandas as pd
import altair as alt
import csv
import requests
from bs4 import BeautifulSoup

url = "https://raw.githubusercontent.com/datasets/covid-19/main/data/countries-aggregated.csv"
df = pd.read_csv(url)

url2 = "https://www.kaggle.com/tanuprabhu/population-by-country-2020?select=population_by_country_2020.csv"
pop = pd.read_csv(url2)

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
            strokeDash = 'Measure')
        st.altair_chart(line_chart)
        
else:
    this_df = pd.melt(df_subset, id_vars = ['Date', 'Country'], value_vars = stats, var_name = 'Measure', value_name = 'Count')
    for stat in stats:
        st.write(stat)
        current_df = this_df.loc[lambda d: d['Measure'] == stat]
        
        line_chart = alt.Chart(current_df).mark_line().encode(
            x = 'Date',
            y = 'Count',
            color = 'Country', 
            strokeDash = 'Country')
        st.altair_chart(line_chart)
        
        

url2 = "https://www.worldometers.info/world-population/population-by-country/"
r = requests.get(url2)

soup = BeautifulSoup(r.content, 'html.parser')


countries = soup.find_all("table")[0]
df2 = pd.read_html(str(countries))[0]

def function(a, b, c, d, e, f, g, h, i, j, k):
    data = pd.DataFrame(
        {'a': df2[a],
         'b': df2[b],
         'c': df2[c],
         'd': df2[d],
         'e': df2[e],
         'f': df2[f],
         'g': df2[g],
         'h': df2[h],
         'i': df2[i],
         'j': df2[j],
         'k': df2[k]
         }
    )

    return data

df_pop = function('Country (or dependency)', 'Population (2020)',
              'Yearly Change', 'Net Change', 'Density (P/Km²)',
              'Land Area (Km²)', 'Migrants (net)', 'Fert. Rate',
              'Med. Age', 'Urban Pop %', 'World Share')

df_pop.columns = ['Country (or dependency)', 'Population (2020)',
              'Yearly Change', 'Net Change', 'Density (P/Km²)',
              'Land Area (Km²)', 'Migrants (net)', 'Fert. Rate',
              'Med. Age', 'Urban Pop %', 'World Share']

