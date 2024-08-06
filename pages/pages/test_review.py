import streamlit as st
import pandas as pd
import json
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

# Check if the 'Medication plan' column exists
if 'Medication plan' in df.columns:
    # Extract the 'Medication plan' column data
    medication_plan_data = df[['Medication plan']]

    # Convert the extracted data to a dictionary
    medication_plan_dict = medication_plan_data.to_dict(orient='records')

    # Convert the dictionary to a DataFrame
    medication_plan_df = pd.DataFrame(medication_plan_dict)

    # Display the DataFrame as a table on the webpage
    st.title("Medication Plan Data Table")
    st.table(medication_plan_df)
else:
    st.error("Column 'Medication plan' not found in the CSV file.")

# Optionally, you can save the DataFrame back to Azure Blob Storage
if st.button("Save Data"):
    output = io.StringIO()
    df.to_csv(output, index=False)
    blob_client.upload_blob(output.getvalue(), overwrite=True)
    st.success("Data saved successfully!")
