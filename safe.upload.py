import streamlit as st
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from azure.storage.blob import BlobServiceClient
from csv import DictWriter
from datetime import datetime
import logging
import os

st.title("Upload Completed Form")

# Configure logging
logging.basicConfig(level=logging.INFO)

def main(uploaded_file):
    try:
        endpoint = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
        credential = AzureKeyCredential(os.getenv("AZURE_FORM_RECOGNIZER_KEY"))
        client = DocumentAnalysisClient(endpoint, credential)

        model_id = "Thessa5vs6"

        # Create BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(os.getenv("AZURE_STORAGE_CONNECTION_STRING"))
        container_client = blob_service_client.get_container_client("data1")

        # Generate a timestamped filename
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        original_blob_name = uploaded_file.name
        file_extension = os.path.splitext(original_blob_name)[1]
        timestamped_blob_name = f"RawFiles/{timestamp}{file_extension}"

        # Create a new blob client for the PDF file
        pdf_blob_client = container_client.get_blob_client(timestamped_blob_name)
        # Upload the PDF to Azure Blob Storage
        pdf_blob_client.upload_blob(uploaded_file, overwrite=True)
        logging.info(f"PDF file '{timestamped_blob_name}' uploaded successfully.")

        # Download the blob to a stream
        downloaded_blob = pdf_blob_client.download_blob().readall()

        # Analyze the document from the blob
        poller = client.begin_analyze_document(model_id=model_id, document=downloaded_blob)
        result = poller.result()
        if not result.documents:
            raise Exception("Expected at least one document in the result.")
        document = result.documents[0]

        # Create a CSV writer
        csv_filename = f'result_{timestamp}.csv'
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
        csv_blob_name = f"CookedFiles/{csv_filename}"
        csv_blob_client = container_client.get_blob_client(csv_blob_name)
        # Upload the CSV file to Azure Blob Storage
        with open(csv_filename, 'rb') as data:
            csv_blob_client.upload_blob(data, overwrite=True)
        logging.info(f"CSV file '{csv_blob_name}' uploaded successfully.")
        
        # Display success message
        st.success("File uploaded successfully!")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        st.error(f"An error occurred: {e}")

if __name__ == '__main__':
    uploaded_file = st.file_uploader("Choose a file", type=['pdf'])
    submit_button = st.button('Submit')
    if uploaded_file is not None and submit_button:
        main(uploaded_file)
