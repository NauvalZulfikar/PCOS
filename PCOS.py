import fitz
import os
import pandas as pd
import streamlit as st
from visualisation import visualisation

# Function to load keywords from file
def load_keywords(file_path):
    with open(file_path, 'r') as f:
        keywords = [line.strip() for line in f]
    return keywords

# Function to save keywords to file
def save_keywords(file_path, keywords):
    with open(file_path, 'w') as f:
        for keyword in keywords:
            f.write(f"{keyword}\n")

# Load keywords
keywords_file = 'keywords.txt'
all_keywords = load_keywords(keywords_file)

def dataframe():
    # Streamlit app
    st.title('PDF Keyword Search')

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
    
    excel = pd.read_excel('RCDC Language.xlsx')
    st.dataframe(excel)

    # # Use multiselect for keyword selection
    # selected_keywords = st.multiselect('Select keywords to search for:', all_keywords, default=[])

    # File uploader
    uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)

    # # Add new keyword
    # new_keyword = st.text_input('Add a new keyword:')
    # if st.button('Add Keyword'):
    #     if new_keyword and new_keyword not in all_keywords:
    #         all_keywords.append(new_keyword)
    #         save_keywords(keywords_file, all_keywords)
    #         st.success(f'Keyword "{new_keyword}" added.')

    # # Delete existing keywords
    # keywords_to_delete = st.multiselect('Delete keywords:', all_keywords, default=[])
    # if st.button('Delete Selected Keywords'):
    #     all_keywords = [kw for kw in all_keywords if kw not in keywords_to_delete]
    #     save_keywords(keywords_file, all_keywords)
    #     st.success(f'Selected keywords deleted.')

# st.sidebar.title("Navigation")
# page = st.sidebar.radio("Go to", [
#     "Table", 
#     "Visualisation"])

# # Display the selected page
# if page == "Table":
#     dataframe()
# else:
#     visualisation()
