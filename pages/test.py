import streamlit as st
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from azure.storage.blob import BlobServiceClient
from csv import DictWriter
from datetime import datetime
import logging
import os
import io
import tempfile
from streamlit_pdf_viewer import pdf_viewer

st.title("Upload Completed Form")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Azure blob storage details
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
container_name = "data1"

# Create the BlobServiceClient object
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

try:
    # Get a list of blobs in the container
    blob_list = blob_service_client.get_container_client(container_name).list_blobs()

    # Get the names of the blobs (files) in the container
    # Only select files with prefix 'form_'
    file_list = [blob.name for blob in blob_list if blob.name.startswith('form_')]

    if not file_list:
        st.warning("No files found with the prefix 'form_'.")
        st.stop()

    # Create a dropdown list for the user to select a file
    selected_file = st.selectbox('Select a file to upload', file_list)

    # Function to get file content given file name
    def get_file_content(file_name):
        blob_client = blob_service_client.get_blob_client(container_name, file_name)
        download_stream = blob_client.download_blob().readall()

        # Create a BytesIO object
        pdf_data = io.BytesIO(download_stream)

        return pdf_data

    # Function to process the uploaded file
    def process_file(uploaded_file):
        try:
            endpoint = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
            credential = AzureKeyCredential(os.getenv("AZURE_FORM_RECOGNIZER_KEY"))
            client = DocumentAnalysisClient(endpoint, credential)

            model_id = "Thessa5vs6"

            # Create a new blob client for the PDF file
            pdf_blob_client = blob_service_client.get_blob_client(container_name, f"RawFiles/{selected_file}")
            # Upload the PDF to Azure Blob Storage
            pdf_blob_client.upload_blob(uploaded_file, overwrite=True)
            logging.info(f"PDF file '{selected_file}' uploaded successfully.")

            # Download the blob to a stream
            downloaded_blob = pdf_blob_client.download_blob().readall()

            # Analyze the document from the blob
            poller = client.begin_analyze_document(model_id=model_id, document=downloaded_blob)
            result = poller.result()
            if not result.documents:
                raise Exception("Expected at least one document in the result.")
            document = result.documents[0]

            # Create a CSV writer
            csv_filename = '8/8/24.csv'
            with open(csv_filename, mode='w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [name for name in document.fields.keys()]
                writer = DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                # Transform document.fields into a format suitable for csv-writer
                record = {}
                for key, field in document.fields.items():
                    if field.value_type == 'dictionary' and field.value and 'rows' in field.value:
                        # Check if the object is a table
                        if isinstance(field.value['rows'], list):
                            # Handle table data
                            for rowIndex, row in enumerate(field.value['rows']):
                                if row and isinstance(row, list):
                                    for cellIndex, cell in enumerate(row):
                                        record[f"{key}_row{rowIndex}_cell{cellIndex}"] = cell.content
                    else:
                        # Handle regular fields
                        record[key] = field.content if field.content else field.value
                writer.writerow(record)

            # Create a new blob client for the CSV file
            csv_blob_name = f"CookedFiles/8_8_24.csv"
            csv_blob_client = blob_service_client.get_blob_client(container_name, csv_blob_name)
            # Upload the CSV file to Azure Blob Storage
            with open(csv_filename, 'rb') as data:
                csv_blob_client.upload_blob(data, overwrite=True)
            logging.info(f"CSV file '{csv_blob_name}' uploaded successfully.")
            
            # Display success message
            st.success("File uploaded and processed successfully!")

        except Exception as e:
            logging.error(f"An error occurred: {e}")
            st.error(f"An error occurred: {e}")

    # Get the content of the selected file
    file_content = get_file_content(selected_file)

    # Display the PDF
    st.text("Displaying the selected file:")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(file_content.getbuffer())
        tmp_file_path = tmp_file.name
    pdf_viewer(tmp_file_path)

    # Upload button
    if st.button('Upload'):
        process_file(file_content)

except Exception as e:
    st.error(f"An error occurred: {e}")
