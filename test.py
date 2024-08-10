import streamlit as st
import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import pandas as pd

# Load environment variables
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
AZURE_FORM_RECOGNIZER_ENDPOINT = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
AZURE_FORM_RECOGNIZER_KEY = os.getenv("AZURE_FORM_RECOGNIZER_KEY")

# Azure Blob Storage credentials
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
container_name = "your-container-name"

# Azure AI Document Intelligence credentials
endpoint = AZURE_FORM_RECOGNIZER_ENDPOINT
key = AZURE_FORM_RECOGNIZER_KEY

UPLOAD_FOLDER = 'CookedFiles'

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def list_blobs():
    container_client = blob_service_client.get_container_client(container_name)
    blob_list = container_client.list_blobs()
    return [blob.name for blob in blob_list]

def download_blob(blob_name):
    blob_client = blob_service_client.get_blob_client(container_name, blob_name)
    download_file_path = os.path.join(UPLOAD_FOLDER, blob_name)
    with open(download_file_path, "wb") as download_file:
        download_file.write(blob_client.download_blob().readall())
    return download_file_path

def process_file(file_path):
    client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    with open(file_path, "rb") as f:
        poller = client.begin_analyze_document("prebuilt-document", document=f)
    result = poller.result()
    
    # Process the result and save as CSV
    data = []
    for page in result.pages:
        for table in page.tables:
            for cell in table.cells:
                data.append([cell.content, cell.row_index, cell.column_index])
    df = pd.DataFrame(data, columns=["Content", "Row", "Column"])
    output_path = os.path.join(UPLOAD_FOLDER, "out1.csv")
    df.to_csv(output_path, index=False)

st.title("File Upload and Processing")

blob_files = list_blobs()
selected_file = st.selectbox("Choose a file from Azure Blob Storage", blob_files)

if st.button("Download and Process"):
    if selected_file:
        file_path = download_blob(selected_file)
        st.success(f"Downloaded file: {selected_file}")
        process_file(file_path)
        st.success("File processed and saved as out1.csv in CookedFiles folder")
