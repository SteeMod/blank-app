import streamlit as st
from azure.storage.blob import BlobServiceClient
import io
import tempfile
from streamlit_pdf_viewer import pdf_viewer
import os

st.title("Download Medication Intake Tracker Form")

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
    selected_file = st.selectbox('Select a file to download', file_list)

    # Function to get file content given file name
    def get_file_content(file_name):
        blob_client = blob_service_client.get_blob_client(container_name, file_name)
        download_stream = blob_client.download_blob().readall()

        # Create a BytesIO object
        pdf_data = io.BytesIO(download_stream)

        return pdf_data

    # Function to display PDF
    def display_pdf(pdf_data):
        st.text("Displaying the selected file:")

        # Save the PDF to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(pdf_data.getbuffer())
            tmp_file_path = tmp_file.name

        # Use the temporary file path with pdf_viewer
        pdf_viewer(tmp_file_path)

        st.download_button(
            label="Download PDF",
            data=pdf_data,
            file_name=selected_file,
            mime="application/pdf"
        )

    # Get the content of the selected file
    file_content = get_file_content(selected_file)

    # Display the PDF
    display_pdf(file_content)

except Exception as e:
    st.error(f"An error occurred: {e}")
