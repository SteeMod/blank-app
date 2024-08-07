import os
from azure.storage.blob import BlobServiceClient
import streamlit as st
from io import BytesIO

# Azure Blob Storage connection details
connection_string = "DefaultEndpointsProtocol=https;AccountName=devcareall;AccountKey=GEW0V0frElMx6YmZyObMDqJWDj3pG0FzJCTkCaknW/JMH9UqHqNzeFhF/WWCUKeIj3LNN5pb/hl9+AStHMGKFA==;EndpointSuffix=core.windows.net"
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
        # Create a BytesIO object from the downloaded blob
        pdf_file = BytesIO(downloaded_blob)
        
        # Display the PDF file using an iframe
        st.download_button(
            label="Download PDF",
            data=pdf_file,
            file_name=latest_blob.name,
            mime="application/pdf"
        )
        
        # Embed the PDF in an iframe
        st.components.v1.iframe(
            src=f"data:application/pdf;base64,{downloaded_blob.encode('base64')}",
            width=700,
            height=1000
        )
    except Exception as e:
        st.text(f"Error reading the PDF file: {e}")
else:
    st.text("The latest file is not a PDF.")