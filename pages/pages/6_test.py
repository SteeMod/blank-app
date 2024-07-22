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

def get_latest_csv_blob(container_client):
    # List all blobs in the container and find the latest CSV file
    blobs_list = list(container_client.list_blobs())
    # Assuming the blobs are named with a timestamp or in a way that the latest file appears last
    csv_blobs = [blob for blob in blobs_list if blob.name.endswith('.csv')]
    latest_csv_blob = sorted(csv_blobs, key=lambda x: x.name, reverse=True)[0]
    return latest_csv_blob

def download_csv_data(blob_name):
    # Get a blob client using the blob name
    blob_client = container_client.get_blob_client(blob_name)
    # Download the blob data
    blob_data = blob_client.download_blob().readall()
    # Convert to pandas DataFrame
    data = pd.read_csv(StringIO(blob_data.decode('utf-8')))
    return data

# Streamlit UI
st.title('Review Latest Results')

if st.button('Review results'):
    try:
        latest_csv_blob = get_latest_csv_blob(container_client)
        data = download_csv_data(latest_csv_blob.name)
        st.write(data)
    except Exception as e:
        st.error(f"Failed to retrieve or load the latest CSV file: {e}")