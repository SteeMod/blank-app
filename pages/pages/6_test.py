import streamlit as st
import pandas as pd
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os
from io import StringIO

# Azure Blob Storage settings
connect_str = os.getenv('DefaultEndpointsProtocol=https;AccountName=devcareall;AccountKey=GEW0V0frElMx6YmZyObMDqJWDj3pG0FzJCTkCaknW/JMH9UqHqNzeFhF/WWCUKeIj3LNN5pb/hl9+AStHMGKFA==;EndpointSuffix=core.windows.net')
container_name = 'data1'

# Initialize the BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_client = blob_service_client.get_container_client(container_name)

def download_csv_data(blob_name):
    # Get a blob client using the blob name
    blob_client = container_client.get_blob_client(blob_name)
    try:
        # Download the blob data
        blob_data = blob_client.download_blob().readall()
        # Convert to pandas DataFrame
        data = pd.read_csv(StringIO(blob_data.decode('utf-8')))
        return data
    except Exception as e:
        # Handle the case where the blob does not exist or cannot be accessed
        return None

# Streamlit UI
st.title('Review Results')

if st.button('Review results'):
    blob_name = 'out1.csv'
    data = download_csv_data(blob_name)
    if data is not None:
        st.write(data)
    else:
        st.error(f"Failed to retrieve or load the CSV file named '{blob_name}'. It may not exist.")