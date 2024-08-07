import os
from azure.storage.blob import BlobServiceClient
import streamlit as st
from io import BytesIO
import base64

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
        
        # Encode the PDF content to base64
        base64_pdf = base64.b64encode(downloaded_blob).decode('utf-8')
        
        # Embed the PDF in an iframe
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
    except Exception as e:
        st.text(f"Error reading the PDF file: {e}")
else:
    st.text("The latest file is not a PDF.")