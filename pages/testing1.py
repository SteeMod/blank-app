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

# Parse JSON data in the Form Recognizer output column
def parse_form_recognizer_output(json_data):
    try:
        data = json.loads(json_data)
        # Extract relevant information from the JSON data
        # This is an example, adjust based on your actual JSON structure
        extracted_data = {
            "Day1": data.get("Day1", ""),
            "Day1Yes": data.get("Day1Yes", ""),
            "Day1No": data.get("Day1No", "")
        }
        return extracted_data
    except json.JSONDecodeError:
        st.error(f"Invalid JSON data: {json_data}")
        return None

if 'MedicationIntakeTable' in df.columns:
    df['ParsedOutput'] = df['MedicationIntakeTable'].apply(parse_form_recognizer_output)
else:
    st.error("Column 'MedicationIntakeTable' not found in the CSV file.")

# Display the parsed data in Streamlit
st.title("Azure Form Recognizer Output")
if 'ParsedOutput' in df.columns:
    for index, row in df.iterrows():
        st.write(f"Row {index + 1}:")
        st.json(row['ParsedOutput'])
else:
    st.error("Parsed output not available.")

# Optionally, you can save the parsed DataFrame back to Azure Blob Storage
if st.button("Save Parsed Data"):
    output = io.StringIO()
    df.to_csv(output, index=False)
    blob_client.upload_blob(output.getvalue(), overwrite=True)
    st.success("Parsed data saved successfully!")
