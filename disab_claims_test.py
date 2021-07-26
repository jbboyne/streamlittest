import streamlit as st
import pandas as pd
import locale
import altair as alt

df_disab_count = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vT7_v2esJv6ovgKoF8pMGT_A88Hm_nHOsfYcgOIaVqeUCv4KLJc2Zx2a9-8bq30EmbIqUCZHuPqasNh/pub?gid=2101361199&single=true&output=csv")
df_disab_count = df_disab_count[~df_disab_count['State Code'].isin(['FE', 'GU', 'EA', 'EO', 'EM', 'EV'])]

# # df_disab_count['Year'] = df_disab_count['Year'].astype(str)
df_disab_count['MOM change'] = df_disab_count.groupby(['State Code'])['All SSDI'].pct_change(1) * 100

df_disab_count['recent%'] =df_disab_count.groupby('State Code')['MOM change'].transform(lambda s: s.rolling(2, min_periods=1).mean())
changerates = df_disab_count[df_disab_count['Year'] == '2021'][['State Code', 'recent%']]
changerates['recent%bin'] = pd.cut(changerates['recent%'], bins=5, precision=0, include_lowest=True, labels=["Lowest", "2", "3", "4", "Highest"]) 


# #Create sidebar widgets

# values = ['<select>', "Lowest", "2", "3", "4", "Highest"]
# default_ix = values.index("4")
# chgpct = st.sidebar.selectbox(
#     "Select 2020-2021 change rate quintile",
#     values, index=default_ix
# )

# states = st.sidebar.multiselect(
#     "Select States",
#     df_disab_count['State Code'].unique()
#     )

# # values = ['<select>', "Lowest", "2", "3", "4", "Highest"]
# # default_ix = values.index("4")
# # window_ANTICOR = st.sidebar.selectbox('Window ANTICOR', values, index=default_ix)

# if chgpct == []:
#     chgpct == '4'

# state_selection = changerates[changerates['recent%bin'] == chgpct]['State Code'].unique()
# df_subset2 = df_disab_count.loc[lambda d: d['State Code'].isin(state_selection)]

# if states == []:
#         states = state_selection
        
# df_subset = df_disab_count.loc[lambda d: d['State Code'].isin(states)]

# st.title("New disability claims by state, Month over Month Change")
# st.write("Select quintile of average 2020-2021 change with the widget in the left panel.")
# st.write("Quintile: ", chgpct)
# line_chart_by_quintile = alt.Chart(df_subset2).mark_line().encode(
#         x = 'Month',
#         y = 'YOY change',
#         color='State Code',
#         strokeDash='State Code'
# )

# st.altair_chart(line_chart_by_quintile)

# st.title("New disability claims by state, Month over Month Change")
# st.write("Choose different states with the widget in the left panel.")

# line_chart_all_SSDI_claims = alt.Chart(df_subset).mark_line().encode(
#         x = 'Month',
#         y = 'YOY change',
#         color='State Code',
#         strokeDash='State Code'
# )

# st.altair_chart(line_chart_all_SSDI_claims)

