import streamlit as st
import pandas as pd
import locale
import altair as alt

df_disab_count = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vT7_v2esJv6ovgKoF8pMGT_A88Hm_nHOsfYcgOIaVqeUCv4KLJc2Zx2a9-8bq30EmbIqUCZHuPqasNh/pub?gid=2101361199&single=true&output=csv")
df_disab_count['Year'] = df_disab_count['Year'].astype(str)
df_disab_count['YOY change'] = df_disab_count.groupby(['State Code'])['All SSDI'].pct_change(1) * 100
# df_disab_count['recent%'] = 
st.write(df_disab_count.groupby(['State Code'])[df_disab_count['Year'] == '2021'].sum())
#                                                 .isin(['2020', '2021'])])


#Create sidebar widgets
states = st.sidebar.multiselect(
    "Select States",
    df_disab_count['State Code'].unique()
    )

# chgpct = st.sidebar.selectbox(
#     "Select recent change range",
#     df_disab_count

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

#
# line_chart_SSDI_only = alt.Chart(df_disab_count).mark_line().encode(
#         x = 'Year',
#         y = '13 Receipts (Initial SSDI Only)')
# st.altair_chart(line_chart_SSDI_only)
