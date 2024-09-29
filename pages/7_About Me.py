import streamlit as st
from azure.storage.blob import BlobServiceClient
from PIL import Image
import io
import os

def show_image():
    try:
        # Azure Blob Storage connection details from environment variables
        connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        container_name = "data1"  # Adjust container name
        blob_name = "photo.png"   # Adjust blob name

        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container_name, blob_name)

        blob_data = blob_client.download_blob().readall()
        image_data = Image.open(io.BytesIO(blob_data))

        return image_data

    except Exception as ex:
        st.error(f"Error retrieving image: {ex}")
        return None

# Create two columns
col1, col2 = st.columns(2)

# Use the first column for text
col1.title("About Me")
col1.write(
    "Stephen Modimakwane is a Management Information Systems Specialist with over 18 years of experience in the field. His expertise includes Data Analytics, Data Visualization, AI Infusion, and Strategy Execution. He has a passion for creating technology solutions that help organizations and communities. Email: stephenmodimakwane@gmail.com"
)

# Use the second column for the image
image = show_image()
if image:
    col2.image(image, caption='Stephen Modimakwane', width=200)
#praise ye the LORD