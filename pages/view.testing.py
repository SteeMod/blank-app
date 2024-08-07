import os
from azure.storage.blob import BlobServiceClient
import streamlit as st
import PyPDF2
from io import BytesIO

# Azure Blob Storage connection details
connection_string = "DefaultEndpointsProtocol=https;AccountName=devcareall;AccountKey=GEWV0frElMx6YmZyObMDqJWDj3pG0FzJCTkCaknW/JMH9UqHqNzeFhF/WWCUKeIj3LNN5pb/hl9+AStHMGKFA==;EndpointSuffix=core.windows.net"
container_name = "data1"
folder_name = "RawFiles"

# Initialize the BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)

# Get the latest file from the folder
blobs = container_client.list_blobs(name_starts_with=folder_name)
latest_blob = max(blobs, key=lambda b: b.creation_time)

# Download the latest file
blob_client = container_client.get_blob_client(latest_blob.name)
downloaded_blob = blob_client.download_blob().readall()

# Display the file content on Streamlit
st.title("Latest Reviewed File")

# Check if the file is a PDF
if latest_blob.name.endswith('.pdf'):
    try:
        # Read the PDF file
        pdf_reader = PyPDF2.PdfReader(BytesIO(downloaded_blob))
        pdf_text = ""
        for page in pdf_reader.pages:
            pdf_text += page.extract_text()
        st.text(pdf_text)
    except Exception as e:
        st.text(f"Error reading the PDF file: {e}")
else:
    try:
        st.text(downloaded_blob.decode('utf-8'))
    except UnicodeDecodeError:
        st.text("Error decoding the file content. The file may not be in UTF-8 format.")