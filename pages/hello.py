import streamlit as st
from azure.storage.blob import BlobServiceClient
from streamlit_pdf_viewer import pdf_viewer

# Azure Storage Account details
azure_storage_account_name = "devcareall"
azure_storage_account_key = "GEW0V0frElMx6YmZyObMDqJWDj3pG0FzJCTkCaknW/JMH9UqHqNzeFhF/WWCUKeIj3LNN5pb/hl9+AStHMGKFA=="
container_name = "data1"
blob_name = "MOUD Tracker Form.pdf"  # name of the blob (file) in Azure Storage

# Function to download file from Azure Storage
def download_from_azure_storage():
    blob_service_client = BlobServiceClient.from_connection_string(
        f"DefaultEndpointsProtocol=https;AccountName={azure_storage_account_name};AccountKey={azure_storage_account_key}"
    )
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    download_stream = blob_client.download_blob().readall()
    return download_stream

# Streamlit App
st.title("Download Form")

# Download the file from Azure Storage
pdf_file = download_from_azure_storage()

# Display the PDF in a PDF viewer
binary_data = pdf_file
pdf_viewer(input=binary_data, width=700)

# Provide a download button in Streamlit
st.download_button(
    'Download PDF',
    data=pdf_file,
    file_name='downloaded_file.pdf',
    mime='application/pdf'
)
