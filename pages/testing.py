import streamlit as st
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import pandas as pd
import io
import datetime

st.title("Review Form For Accuracy")

# Create BlobServiceClient object with hardcoded connection string
connection_string = 'DefaultEndpointsProtocol=https;AccountName=devcareall;AccountKey=GEW0V0frElMx6YmZyObMDqJWDj3pG0FzJCTkCaknW/JMH9UqHqNzeFhF/WWCUKeIj3LNN5pb/hl9+AStHMGKFA==;EndpointSuffix=core.windows.net'
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

def get_latest_blob(container_name, folder_name):
    try:
        container_client = blob_service_client.get_container_client(container_name)
        blob_list = container_client.list_blobs(name_starts_with=folder_name)
        latest_blob = max(blob_list, key=lambda blob: blob.last_modified)
        return latest_blob
    except Exception as e:
        st.write(f"Error occurred: {e}")
        return None

def download_blob_data(blob):
    try:
        blob_client = blob_service_client.get_blob_client('data1', blob.name)
        stream = blob_client.download_blob().readall()
        return pd.read_csv(io.StringIO(stream.decode('utf-8', errors='ignore')))
    except Exception as e:
        st.write(f"Error occurred: {e}")
        return None

def upload_blob_data(container_name, blob_name, data):
    try:
        blob_client = blob_service_client.get_blob_client(container_name, blob_name)
        output = io.StringIO()
        data.to_csv(output, index=False)
        output.seek(0)
        blob_client.upload_blob(output.read(), overwrite=True)
    except Exception as e:
        st.write(f"Error occurred: {e}")

# Review form
with st.form("Review"):
    latest_blob = get_latest_blob('data1', 'CookedFiles/')
    if (latest_blob is not None):
        data = download_blob_data(latest_blob)
        if (data is not None):
            row_data = data.iloc[0]  # assuming you want to display the first row

            # Create a new DataFrame with 31 rows and 7 columns
            reshaped_data = []
            for i in range(31):
                row = [row_data.get(f'Column_{i*7+j}', '') for j in range(7)]
                reshaped_data.append(row)

            reshaped_df = pd.DataFrame(reshaped_data, columns=['Day', 'Yes', 'No', 'Dosage', 'Freq', 'Form', 'Route'])

            # Display the reshaped DataFrame in an editable table
            edited_data = st.experimental_data_editor(reshaped_df, num_rows="dynamic")

            # Submit button
            submitted = st.form_submit_button("Submit")
            if submitted:
                # Update the original DataFrame with the edited values
                for i in range(31):
                    for j, col in enumerate(reshaped_df.columns):
                        row_data[f'Column_{i*7+j}'] = edited_data.iloc[i, j]

                # Upload the updated DataFrame back to the blob storage
                timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                blob_name = f"ReviewedFiles/review_{timestamp}.csv"
                upload_blob_data('data1', blob_name, data)
                st.write("Data has been updated and uploaded successfully.")