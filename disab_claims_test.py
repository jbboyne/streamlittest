import streamlit as st
import pandas as pd
import locale
import altair as alt

df_disab_count = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vSTMpMSdP4qQl0yYntV-_X33w1J0AhoKHM_O4PMaBC7-RKeLJlH_lSOu7mvJm_seKU4hTsf-eBBB5pY/pub?gid=1080384046&single=true&output=csv")
df_disab_count = df_disab_count[~df_disab_count['State Code'].isin(['FE', 'GU', 'EA', 'EO', 'EM', 'EV'])]
df_disab_count['Year'] = df_disab_count['Year'].astype(str)
df_disab_count['MOM change'] = df_disab_count.groupby(['State Code'])['All SSDI'].pct_change(1) * 100

avg_rate_by_year = df_disab_count.groupby(['Year', 'State Code'])['MOM change'].mean().to_frame()
avg_rate_by_year.index = avg_rate_by_year.index.set_names(['Year', 'State Code'])

df_disab_count = avg_rate_by_year.merge(df_disab_count, how='right', on=['Year', 'State Code'])
df_disab_count = df_disab_count.rename(columns={'MOM change_x': 'Avg Monthly Change Per Year'})
df_disab_count = df_disab_count.groupby(['Year', 'State Code']).mean()
df_disab_count.index = df_disab_count.index.set_names(['Year', 'State Code'])
df_disab_count.reset_index(inplace=True)
df_disab_count = df_disab_count.drop(columns='Unnamed: 0')

changerates = df_disab_count[df_disab_count['Year'].isin(['2020', '2021'])][['Year', 'State Code', 'Avg Monthly Change Per Year']]
changerates = changerates.groupby(['State Code']).mean()
changerates.index = changerates.index.set_names(['State Code'])
changerates.reset_index(inplace=True)
changerates['bin'] = pd.cut(changerates['Avg Monthly Change Per Year'], 5, labels=["Lowest", "2", "3", "4", "Highest"])

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

if chgpct == []:
    chgpct == '4'

state_selection = changerates[changerates['bin'] == chgpct]['State Code'].unique()
df_subset2 = df_disab_count.loc[lambda d: d['State Code'].isin(state_selection)]

if states == []:
        states = state_selection
        
df_subset = df_disab_count.loc[lambda d: d['State Code'].isin(states)]

st.title("New disability claims by state, Year over Year Change")
st.write("Select quintile of average 2020-2021 change with the widget in the left panel.")
st.write("Quintile: ", chgpct)
line_chart_by_quintile = alt.Chart(df_subset2).mark_line().encode(
        x = 'Year',
        y = 'Avg Monthly Change Per Year',
        color='State Code',
        strokeDash='State Code'
)

st.altair_chart(line_chart_by_quintile)

# st.title("New disability claims by state, Year over Year Change")
# st.write("Choose different states with the widget in the left panel.")

# line_chart_all_SSDI_claims = alt.Chart(df_subset).mark_line().encode(
#         x = 'Year',
#         y = 'YOY change',
#         color='State Code',
#         strokeDash='State Code'
# )

# st.altair_chart(line_chart_all_SSDI_claims)
