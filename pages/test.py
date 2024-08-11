import streamlit as st
from azure.storage.blob import BlobServiceClient
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from csv import DictWriter
from datetime import datetime
import io
import tempfile
from streamlit_pdf_viewer import pdf_viewer
import logging
import os

st.title("Medication Intake Tracker Form")

# Azure blob storage details
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
container_name = "data1"

# Create the BlobServiceClient object
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Function to get file content given file name
def get_file_content(file_name):
    blob_client = blob_service_client.get_blob_client(container_name, file_name)
    download_stream = blob_client.download_blob().readall()
    pdf_data = io.BytesIO(download_stream)
    return pdf_data

# Function to display PDF
def display_pdf(pdf_data, selected_file):
    st.text("Displaying the selected file:")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(pdf_data.getbuffer())
        tmp_file_path = tmp_file.name
    pdf_viewer(tmp_file_path)

# Function to process uploaded file
def process_uploaded_file(uploaded_file):
    try:
        endpoint = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
        credential = AzureKeyCredential(os.getenv("AZURE_FORM_RECOGNIZER_KEY"))
        client = DocumentAnalysisClient(endpoint, credential)
        model_id = "Thessa5vs6"

        # Generate a timestamped filename
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        original_blob_name = uploaded_file.name
        file_extension = os.path.splitext(original_blob_name)[1]
        timestamped_blob_name = f"RawFiles/{timestamp}{file_extension}"

        # Create a new blob client for the PDF file
        pdf_blob_client = blob_service_client.get_blob_client(container_name, timestamped_blob_name)
        pdf_blob_client.upload_blob(uploaded_file, overwrite=True)
        logging.info(f"PDF file '{timestamped_blob_name}' uploaded successfully.")

        # Analyze the document from the uploaded file
        uploaded_file.seek(0)
        poller = client.begin_analyze_document(model_id=model_id, document=uploaded_file.read())
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
            record = {}
            for key, field in document.fields.items():
                if field.value_type == 'dictionary' and field.value and 'rows' in field.value:
                    if isinstance(field.value['rows'], list):
                        for rowIndex, row in enumerate(field.value['rows']):
                            if row and isinstance(row, list):
                                for cellIndex, cell in enumerate(row):
                                    record[f"{key}_row{rowIndex}_cell{cellIndex}"] = cell.content
                else:
                    record[key] = field.content if field.content else field.value
            writer.writerow(record)

        # Create a new blob client for the CSV file
        csv_blob_name = f"CookedFiles/{csv_filename}"
        csv_blob_client = blob_service_client.get_blob_client(container_name, csv_blob_name)
        with open(csv_filename, 'rb') as data:
            csv_blob_client.upload_blob(data, overwrite=True)
        logging.info(f"CSV file '{csv_blob_name}' uploaded successfully.")
        st.success("File uploaded successfully!")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        st.error(f"An error occurred: {e}")

# Main function
def main():
    try:
        # Get a list of blobs in the container
        blob_list = blob_service_client.get_container_client(container_name).list_blobs()
        file_list = [blob.name for blob in blob_list if blob.name.startswith('form_')]

        if not file_list:
            st.warning("No files found with the prefix 'form_'.")
            st.stop()

        # Create a dropdown list for the user to select a file
        selected_file = st.selectbox('Select a file to download', file_list)
        file_content = get_file_content(selected_file)
        display_pdf(file_content, selected_file)

        # File uploader
        uploaded_file = st.file_uploader("Choose a file", type=['pdf'])
        submit_button = st.button('Upload')
        if uploaded_file is not None and submit_button:
            process_uploaded_file(uploaded_file)

    except Exception as e:
        st.error(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
