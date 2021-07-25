import streamlit as st
import pandas as pd
import locale
import altair as alt


pd.set_option("max_columns", 30)
pd.set_option("max_rows", 100)

cols = ['SSA File',
     'Version',
     'Update Date',
     'Region Code',
     'State Code',
     'Date Type',
     'Date',
     'Formatted Date',
     '8 Receipts (All Initial)',
     '9 Closing Pending (All Initial)',
     '10 Determinations (All Initial)',
     '11 Allowances (All Initial)',
     '12 Allowance Rate (All Initial)',
     '13 Receipts (Initial SSDI Only)',
     '14 Closing Pending (Initial SSDI Only)',
     '15 Determinations (Initial SSDI Only)',
     '16 Allowances (Initial SSDI Only)',
     '17 Allowance Rate (Initial SSDI Only)',
     '18 Receipts (Initial SSI Only)',
     '19 Closing Pending (Initial SSI Only)',
     '20 Determinations (Initial SSI Only)',
     '21 Allowances (Initial SSI Only)',
     '22 Allowance Rate (Initial SSI Only)',
     '23 Receipts (Initial Concurrent Only)',
     '24 Closing Pending (Initial Concurrent Only)',
     '25 Determinations (Initial Concurrent Only)',
     '26 Allowances (Initial Concurrent Only)',
     '27 Allowance Rate (Initial Concurrent Only)',
     '28 Receipts (Initial SSI DC Only)',
     '29 Receipts (Initial SSI DC Only)',
     '30 Closing Pending (Initial SSI DC Only)',
     '31 Determinations (Initial SSI DC Only)',
     '32 Allowances (Initial SSI DC Only)',
     '33 Allowance Rate (Initial SSI DC Only)',
     '34 Prototype State',
     '35 Receipts (All Recon)',
     '36 Closing Pending (All Recon)',
     '37 Determinations (All Recon)',
     '38 Allowances (All Recon)',
     '39 Allowance Rate (All Recon)',
     '40 Receipts (Recon SSDI Only)',
     '41 Closing Pending (Recon SSDI Only)',
     '42 Determinations (Recon SSDI Only)',
     '43 Allowances (Recon SSDI Only)',
     '44 Allowance Rate (Recon SSDI Only)',
     '45 Receipts (Recon SSI Only)',
     '46 Closing Pending (Recon SSI Only)',
     '47 Determinations (Recon SSI Only)',
     '48 Allowances (Recon SSI Only)',
     '49 Allowance Rate (Recon SSI Only)',
     '50 Receipts (Recon Concurrent Only)',
     '51 Closing Pending (Recon Concurrent Only)',
     '52 Determinations (Recon Concurrent Only)',
     '53 Allowances (Recon Concurrent Only)',
     '54 Allowance Rate (Recon Concurrent Only)',
     '55 Receipts (Recon SSI DC Only)',
     '56 Closing Pending (Recon SSI DC Only)',
     '57 Determinations (Recon SSI DC Only)',
     '58 Allowances (Recon SSI DC Only)',
     '59 Allowance Rate (Recon SSI DC Only)',
     '60 Receipts (All CDR)',
     '61 Closing Pending (All CDR)',
     '62 Determinations (All CDR)',
     '63 Continuations (All CDR)',
     '64 Continuation Rate (All CDR)',
     '65 Receipts (CDR SSDI Only)',
     '66 Closing Pending (CDR SSDI Only)',
     '67 Determinations (CDR SSDI Only)',
     '68 Continuations (CDR SSDI Only)',
     '69 Continuation Rate (CDR SSDI Only)',
     '70 Receipts (CDR SSI Only)',
     '71 Closing Pending (CDR SSI Only)',
     '72 Determinations (CDR SSI Only)',
     '73 Continuations (CDR SSI Only)',
     '74 Continuation Rate (CDR SSI Only)',
     '75 Receipts (CDR Concurrent Only)',
     '76 Closing Pending (CDR Concurrent Only)',
     '77 Determinations (CDR Concurrent Only)',
     '78 Continuations (CDR Concurrent Only)',
     '79 Continuation Rate (CDR Concurrent Only)']
df_disab = pd.read_csv("https://www.ssa.gov/disability/data/SSA-SA-MOWL.csv", index_col=False,
                       sep=',', thousands=',', low_memory=False, names=cols,
                       usecols=[3, 4, 6, 13, 23])

df_disab = df_disab.drop(df_disab.columns[80:], axis=1)
df_disab['Date'] = pd.to_datetime(df_disab['Date'])
df_disab['Year-Month'] = df_disab['Date'].dt.strftime('%Y-%m')
df_disab['Year'] = pd.DatetimeIndex(df_disab['Date']).year.astype(str)
df_disab['All SSDI'] = df_disab['13 Receipts (Initial SSDI Only)'] + df_disab['23 Receipts (Initial Concurrent Only)']

df_disab_count = df_disab[['Year', 'Region Code', 'State Code', 'All SSDI', '13 Receipts (Initial SSDI Only)']].groupby(['Year', 'State Code']).mean()
df_disab_count.reset_index(inplace=True)

#Create sidebar widgets
states = st.sidebar.multiselect(
    "Select States",
    df_disab_count['State Code'].unique()
    )

# if states == []:
#         states = ['AZ']


df_subset = df_disab_count.loc[lambda d: d['State Code'].isin(states)]

line_chart_all_SSDI_claims = alt.Chart(df_subset).mark_line().encode(
        x = 'Year',
        y = 'All SSDI',
        color='State Code',
        strokeDash='State Code'
)

st.altair_chart(line_chart_all_SSDI_claims)

#
# line_chart_SSDI_only = alt.Chart(df_disab_count).mark_line().encode(
#         x = 'Year',
#         y = '13 Receipts (Initial SSDI Only)')
# st.altair_chart(line_chart_SSDI_only)
