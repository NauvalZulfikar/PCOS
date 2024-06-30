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

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "Table", 
    "Visualisation"])

# Display the selected page
if page == "Table":
    dataframe()
else:
    visualisation()