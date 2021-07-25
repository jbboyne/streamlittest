import streamlit as st
import pandas as pd
import locale
import altair as alt

df_disab_count = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vT7_v2esJv6ovgKoF8pMGT_A88Hm_nHOsfYcgOIaVqeUCv4KLJc2Zx2a9-8bq30EmbIqUCZHuPqasNh/pub?gid=2101361199&single=true&output=csv")
df_disab_count = df_disab_count[~df_disab_count['State Code'].isin(['FE', 'GU', 'EA', 'EO', 'EM', 'EV'])]

df_disab_count['Year'] = df_disab_count['Year'].astype(str)
df_disab_count['YOY change'] = df_disab_count.groupby(['State Code'])['All SSDI'].pct_change(1) * 100

df_disab_count['recent%'] =df_disab_count.groupby('State Code')['YOY change'].transform(lambda s: s.rolling(2, min_periods=1).mean())
changerates = df_disab_count[df_disab_count['Year'] == '2021'][['State Code', 'recent%']]
changerates['recent%bin'] = pd.cut(changerates['recent%'], bins=5, precision=0, include_lowest=True, labels=["Lowest", "2", "3", "4", "Highest"]) 

#Create sidebar widgets
states = st.sidebar.multiselect(
    "Select States",
    df_disab_count['State Code'].unique()
    )

chgpct = st.sidebar.selectbox(
    "Select recent change range",
    ["Lowest", "2", "3", "4", "Highest"]
)

if states == []:
        states = ['KY', 'TX', 'FL', 'GA']

df_subset = df_disab_count.loc[lambda d: d['State Code'].isin(states)]

st.title("New disability claims by state, Year over Year Change")
st.write("Choose different states with the widget in the left panel.")

line_chart_all_SSDI_claims = alt.Chart(df_subset).mark_line().encode(
        x = 'Year',
        y = 'YOY change',
        color='State Code',
        strokeDash='State Code'
)

st.altair_chart(line_chart_all_SSDI_claims)

state_selection = changerates[changerates['recent%bin'] == chgpct]['State Code'].unique()
df_subset2 = df_disab_count.loc[lambda d: d['State Code'].isin(state_selection)]

st.title("New disability claims by state, Year over Year Change")

#
# line_chart_SSDI_only = alt.Chart(df_disab_count).mark_line().encode(
#         x = 'Year',
#         y = '13 Receipts (Initial SSDI Only)')
# st.altair_chart(line_chart_SSDI_only)
