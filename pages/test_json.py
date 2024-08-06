import streamlit as st
import pandas as pd
import json
from azure.storage.blob import BlobServiceClient
import io

# Azure Blob Storage connection details
connection_string = "DefaultEndpointsProtocol=https;AccountName=devcareall;AccountKey=GEW0V0frElMx6YmZyObMDqJWDj3pG0FzJCTkCaknW/JMH9UqHqNzeFhF/WWCUKeIj3LNN5pb/hl9+AStHMGKFA==;EndpointSuffix=core.windows.net"
container_name = "data1"
virtual_folder = "CookedFiles"

# Initialize the BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)

# Get the latest JSON file from the virtual folder
blobs = container_client.list_blobs(name_starts_with=virtual_folder)
latest_blob = max(blobs, key=lambda b: b.creation_time)

# Download the latest JSON file
blob_client = container_client.get_blob_client(latest_blob)
download_stream = blob_client.download_blob()
json_data = download_stream.readall()

# Load the JSON data into a pandas DataFrame
data = json.loads(json_data)
df = pd.json_normalize(data)

# Display the DataFrame in Streamlit
st.title("Latest JSON Data from Azure Blob Storage")
st.dataframe(df)

# Optionally, you can save the DataFrame back to Azure Blob Storage
if st.button("Save Data"):
    output = io.StringIO()
    df.to_csv(output, index=False)
    blob_client.upload_blob(output.getvalue(), overwrite=True)
    st.success("Data saved successfully!")
