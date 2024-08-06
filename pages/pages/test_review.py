import streamlit as st
import pandas as pd
from azure.storage.blob import BlobServiceClient
import io

# Azure Blob Storage connection details
connection_string = "DefaultEndpointsProtocol=https;AccountName=devcareall;AccountKey=GEW0V0frElMx6YmZyObMDqJWDj3pG0FzJCTkCaknW/JMH9UqHqNzeFhF/WWCUKeIj3LNN5pb/hl9+AStHMGKFA==;EndpointSuffix=core.windows.net"
container_name = "data1"

# Initialize the BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)

# Get the latest CSV file
blobs = container_client.list_blobs()
latest_blob = max(blobs, key=lambda b: b.creation_time)

# Download the latest CSV file
blob_client = container_client.get_blob_client(latest_blob)
download_stream = blob_client.download_blob()
csv_data = download_stream.readall()

# Load the CSV data into a pandas DataFrame
df = pd.read_csv(io.BytesIO(csv_data))

# Extract the Form Recognizer output from the relevant column
form_recognizer_output = df['MedicationIntakeTable']

# Convert the Form Recognizer output to a DataFrame
form_recognizer_df = pd.DataFrame.from_records(form_recognizer_output.apply(eval).tolist())

# Display the DataFrame in Streamlit
st.title("Form Recognizer Output")
st.dataframe(form_recognizer_df)
