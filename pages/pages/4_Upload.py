import streamlit as st
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

# Create the file uploader and specify that it should accept PDF files
uploaded_file = st.file_uploader("Choose a PDF file", type=['pdf'])

# Create a button for the user to click to upload file
if st.button('Submit'):
    if uploaded_file is not None:
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()

        # Azure connection string
        connect_str = 'DefaultEndpointsProtocol=https;AccountName=devcareall;AccountKey=GEW0V0frElMx6YmZyObMDqJWDj3pG0FzJCTkCaknW/JMH9UqHqNzeFhF/WWCUKeIj3LNN5pb/hl9+AStHMGKFA==;EndpointSuffix=core.windows.net'

        # Create the BlobServiceClient object which will be used to create a container client
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        # Create a unique name for the blob
        blob_name = "RawDocuments"

        # Create a blob client using the local file name as the name for the blob
        blob_client = blob_service_client.get_blob_client("data1", blob_name)

        # Upload the file
        blob_client.upload_blob(bytes_data)
        st.write('File uploaded to Azure Blob Storage')
    else:
        st.write('No file selected')
