import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def visualisation():
    data = pd.read_excel('RCDCFundingSummary_06242024.xlsx')
    df = pd.DataFrame()

    for i in data.columns:
        colz = data[i].replace('+',0).replace('*',0.5).replace('-',0)
        df[i] = colz
    df['2021 US Prevalence SE 19'] = df['2021 US Prevalence SE 19'].apply(lambda x: str(x))
    df['Only <18'] = np.where(df['2021 US Prevalence SE 19'].str.contains('\*\*', regex=True), 1, 0)
    df.set_index('Research/Disease Areas \n (Dollars in millions and rounded)',inplace=True)


    # Original column list and columns to delete
    col_list = list(df.columns[:-1])
    col_del = ['2009 ARRA', '2010 ARRA']
    col_lis = [col for col in col_list if col not in col_del]

    # Transpose the DataFrame
    dt = df[col_lis].T
    dt.columns = df.index
    dt.reset_index(inplace=True)
    dt.rename(columns={'index': 'Year'}, inplace=True)

    col_dlt = ['Year'] 
    col_liz = [col for col in dt.columns if col not in col_dlt]

    # Streamlit application
    st.title('Interactive Line Plot')

    # Dropdown for selecting variables
    selected_columns = st.multiselect('Select variables to plot', 
                                    options=col_liz)#, default=col_liz)


    # Filter DataFrame based on selection
    filtered_dt = dt[['Year'] + selected_columns]

    # Plotting
    fig = go.Figure()

    for col in selected_columns:
        fig.add_trace(go.Scatter(
            x=filtered_dt['Year'],
            y=filtered_dt[col],
            mode='lines',
            name=col
        ))

    fig.update_layout(
        title='Line plots for selected columns',
        xaxis_title='Year',
        yaxis_title='Count'
    )

    # Display the plot
    st.plotly_chart(fig)