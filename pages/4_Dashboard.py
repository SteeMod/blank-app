import pandas as pd
import streamlit as st
import plotly.express as px
from io import BytesIO
from azure.storage.blob import BlobServiceClient
import os

st.title("Medication Intake Dashboard")

try:
    # Azure Blob Storage connection details from environment variables
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    container_name = 'data1'
    folder_name = 'ReviewedFiles/'

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    # List all blobs in the virtual folder 'ReviewedFiles'
    blob_list = container_client.list_blobs(name_starts_with=folder_name)

    # Find the latest blob
    latest_blob = max(blob_list, key=lambda blob: blob.last_modified)

    # Download the latest blob as a pandas DataFrame
    blob_client = blob_service_client.get_blob_client(container_name, latest_blob.name)
    df = pd.read_csv(BytesIO(blob_client.download_blob().readall()))

    # Select only columns with names containing 'Day' and either 'Yes' or 'yes' (case-insensitive)
    df = df[[col for col in df.columns if 'Day' in col and ('Yes' in col or 'yes' in col)]]

    # Transpose the DataFrame
    df = df.transpose()

    # Sort the DataFrame by column names
    df = df.sort_index(axis=1)

    # Rename the first column to 'Yes'
    df.rename(columns={df.columns[0]: 'Yes'}, inplace=True)

    # Count the rows where 'Yes' is ':selected:'
    numerator = df[df['Yes'] == ':selected:'].shape[0]

    # Count the rows where 'Yes' is either ':selected:' or ':unselected:'
    denominator = df[(df['Yes'] == ':selected:') | (df['Yes'] == ':unselected:')].shape[0]

    # Create a pie chart using Plotly
    fig = px.pie(values=[numerator, denominator - numerator], names=['Selected', 'Unselected'], title='Your Statistics')

    # Create two columns
    col1, col2 = st.columns(2)

    # Display the DataFrame in the first column and the pie chart in the second column
    with col1:
        st.dataframe(df)
    with col2:
        st.plotly_chart(fig)

except Exception as ex:
    st.error(f'Exception: {ex}')
