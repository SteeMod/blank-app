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

# Convert JSON data in the MedicationIntakeTable column to a dictionary
def safe_json_loads(x):
    try:
        return json.loads(x)
    except json.JSONDecodeError:
        st.error(f"Invalid JSON data: {x}")
        return None

if 'MedicationIntakeTable' in df.columns:
    df['MedicationIntakeTable'] = df['MedicationIntakeTable'].apply(safe_json_loads)
else:
    st.error("Column 'MedicationIntakeTable' not found in the CSV file.")

# Display the dataframe in Streamlit
st.title("Editable DataFrame - Medication Intake Table")
if 'MedicationIntakeTable' in df.columns:
    edited_df = st.data_editor(df)
else:
    st.error("Column 'MedicationIntakeTable' not found in the CSV file.")

# Optionally, you can save the edited DataFrame back to Azure Blob Storage
if st.button("Save Changes"):
    output = io.StringIO()
    edited_df.to_csv(output, index=False)
    blob_client.upload_blob(output.getvalue(), overwrite=True)
    st.success("Changes saved successfully!")
