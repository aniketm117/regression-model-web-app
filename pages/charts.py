import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
import altair as alt

data_unf = pd.read_csv('csv files/IPL IMB381IPL2013.csv')

st.title('Data Visualization of IPL players')

# get numeric columns
num_col = data_unf.select_dtypes(include=np.number).columns.tolist()

# Unresolved issue: density plot not working with big numbers
num_col.remove('BASE PRICE')
num_col.remove('SOLD PRICE')
num_col.remove('ODI-RUNS-S')
num_col.remove('T-RUNS')

col_ch = ["COUNTRY", "ODI-RUNS-S", "ODI-SR-B", "T-WKTS", "AGE", "ODI-WKTS",
          "TEAM", "PLAYING ROLE", "T-RUNS", "ODI-SR-BL", "CAPTAINCY EXP",
          "RUNS-S", "HS", "AVE", "SR-B", "SIXERS", "RUNS-C", "WKTS",
          "AVE-BL", "ECON", "SR-BL", "AUCTION YEAR", "BASE PRICE", "SOLD PRICE"]

plyrRole = ['Allrounder', 'Batsman', 'Bowler', "W. Keeper"]

with st.sidebar:
    plyrRole_col = st.multiselect("Select playing role by which the player stats are to"
                                  " be shown in the graph(s)",
                                  plyrRole,
                                  default='Allrounder',
                                  key="rolChart")

try:
    data = data_unf[data_unf['PLAYING ROLE'].isin(plyrRole_col)]
except NameError:
    st.info("Sorry, something went wrong",
            icon="🫠")

chart_list = ['Bar', 'Scatter', 'Plotly']

with st.sidebar:
    option = st.selectbox("Select data to view on x-axis", col_ch,
                          key='chart_op')

# define a list to store df on the basis of plyr role and option to be used in
# dist plot

dfs = []

for rol in plyrRole_col:
    dfs.append(data_unf[data_unf['PLAYING ROLE'] == rol][option])

pop_var = col_ch.index(option)

col_ch.pop(pop_var)

with st.sidebar:
    option_2 = st.selectbox("Select data to view on y-axis", col_ch,
                            key='chart_op_2')

pop_var = col_ch.index(option_2)

col_ch.pop(pop_var)
with st.sidebar:
    option_col = st.selectbox("Select data to to be shown by its colour intensity in the graph", col_ch,
                              key='chart_op_col')

# append density chart to chart list

if option in num_col:
    chart_list.append('Density Plot')

with st.sidebar:
    chart_op = st.multiselect('Select Chart(s) you want to see',
                              chart_list,
                              key='chart_type',
                              default=chart_list[0],
                              help="Density Plots will be shown for x-axis data",
                              )

# Create plot
with st.container():
    if plyrRole_col:

        st.subheader(f"Plots of {option} and {option_2}"
                     f" indicating {option_col} by colour intensity for "
                     f"{', '.join(plyrRole_col)} playing role(s).")

        for chart in chart_op:
            match chart:
                case 'Bar':
                    st.bar_chart(data, x=option, y=option_2,
                                 color=option_col,
                                 use_container_width=True)
                case 'Scatter':
                    st.scatter_chart(data, x=option, y=option_2,
                                     color=option_col,
                                     use_container_width=True)
                case 'Plotly':
                    fig = px.scatter(data, x=option, y=option_2,
                                     color=option_col)
                    st.plotly_chart(fig, use_container_width=True)

                    fig_2 = px.bar(data, x=option, y=option_2,
                                   color=option_col)
                    st.plotly_chart(fig_2, use_container_width=True)

                case 'Density Plot':
                    fig = px.histogram(data[data['PLAYING ROLE'].isin(plyrRole_col)],
                                       x=option,
                                       color='PLAYING ROLE')
                    st.plotly_chart(fig, use_container_width=True)

                    fig_ff = ff.create_distplot(dfs,
                                                group_labels=plyrRole_col)
                    st.plotly_chart(fig_ff, use_container_width=True)

                # chart not ready
                # case 'Altair':
                #     c = (
                #         alt.Chart(data)
                #         .mark_circle()
                #          .encode(x=option, y=option_2, size='SOLD PRICE',
                #                color=option_col,
                #                tooltip=["SOLD PRICE", "PLAYING ROLE"])
                #     )

                #     st.altair_chart(c, use_container_width=True)
