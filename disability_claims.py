import streamlit as st
import pandas as pd
import locale
import altair as alt

# st.beta_set_page_config(layout="wide")
col1, col2 = st.beta_columns(2)

# Read in subset of SSDI data at "https://www.ssa.gov/disability/data/SSA-SA-MOWL.csv"
# Processed in file disability_pickle.py and manually uploaded to and published on Gdrive

df_disab_count = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vSTMpMSdP4qQl0yYntV-_X33w1J0AhoKHM_O4PMaBC7-RKeLJlH_lSOu7mvJm_seKU4hTsf-eBBB5pY/pub?gid=1080384046&single=true&output=csv")
df_disab_count = df_disab_count[~df_disab_count['State Code'].isin(['FE', 'GU', 'EA', 'EO', 'EM', 'EV'])]  #Remove territories with little data
df_disab_count['Year'] = df_disab_count['Year'].astype(str) #Convert year to string so it displays without comma on axis

#Create a normalized measure so states can be compared on the same axis
avg_monthly_claims_byyear = df_disab_count.groupby(['Year', 'State Code'])['All SSDI'].mean().astype(int).to_frame() 
avg_monthly_claims_byyear = avg_monthly_claims_byyear.rename(columns={'All SSDI': 'Avg monthly SSDI claims'})
avg_monthly_claims_byyear.index = avg_monthly_claims_byyear.index.set_names(['Year', 'State Code'])
avg_monthly_claims_byyear.reset_index(inplace=True)
avg_monthly_claims_byyear['YOY change'] = avg_monthly_claims_byyear.groupby(['State Code'])['Avg monthly SSDI claims'].pct_change(1) * 100

#Merge the normalized measure into the original data
df_disab_count = df_disab_count.drop(columns= ['Year-Month', 'Unnamed: 0', 'All SSDI', 'Receipts (Initial SSDI Only)'])
df_disab_count = avg_monthly_claims_byyear.merge(df_disab_count, how='right', on=['Year', 'State Code'])
df_disab_count = df_disab_count.drop_duplicates()

#Create bins to categorize states by recent change in claims
changerates = df_disab_count[df_disab_count['Year'].isin(['2020', '2021'])][['Year', 'State Code', 'YOY change']].groupby(['State Code']).mean()
changerates.index = changerates.index.set_names(['State Code'])
changerates.reset_index(inplace=True)
changerates = changerates.rename(columns={'YOY change': 'Avg change 2020-2021'})
changerates['bin'] = pd.cut(changerates['Avg change 2020-2021'], 5, labels=["Lowest", "2", "3", "4", "Highest"])
#--------------------------------------------------------------------------------------

#Create sidebar widgets

values = ['<select>', "Lowest", "2", "3", "4", "Highest"]
default_ix = values.index("4")
chgpct = st.sidebar.selectbox(
    "Select 2020-2021 change rate quintile",
    values, index=default_ix
)

states = st.sidebar.multiselect(
    "Select States",
    df_disab_count['State Code'].unique()
    )
#--------------------------------------------------------------------------------------


#Set defaults

if chgpct == []:
    chgpct == '4'

state_selection = changerates[changerates['bin'] == chgpct]['State Code'].unique()
df_subset2 = df_disab_count.loc[lambda d: d['State Code'].isin(state_selection)]

if states == []:
        states = state_selection
else: 
    states = states
#--------------------------------------------------------------------------------------


#Define chart-specific dataframes and charts

df_subset = df_disab_count.loc[lambda d: d['State Code'].isin(states)]

st.title("New disability claims by state, average monthly change per year")
st.write("Select quintile of average 2020-2021 change with the widget in the left panel.")
st.write("Quintile: ", chgpct)
line_chart_by_quintile = alt.Chart(df_subset2).mark_line().encode(
        x = 'Year',
        y = 'YOY change',
        color='State Code',
        strokeDash='State Code'
)

st.altair_chart(line_chart_by_quintile)

st.title("New disability claims by state, average monthly change per year")
st.write("Choose different states with the widget in the left panel.")

line_chart_all_SSDI_claims = alt.Chart(df_subset).mark_line().encode(
        x = 'Year',
        y = 'YOY change',
        color='State Code',
        strokeDash='State Code'
)

st.altair_chart(line_chart_all_SSDI_claims)

st.title("New disability claims by state, average monthly count per year")

line_chart_all_SSDI_claims_count = alt.Chart(df_subset).mark_line().encode(
        x = 'Year',
        y = 'Avg monthly SSDI claims',
        color='State Code',
        strokeDash='State Code'
)

st.altair_chart(line_chart_all_SSDI_claims_count)
