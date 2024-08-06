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
    if latest_blob is not None:
        data = download_blob_data(latest_blob)
        if data is not None:
            row_data = data.iloc[0]  # assuming you want to display the first row
            # Convert row data to DataFrame
            df = pd.DataFrame([row_data])

            # Extract columns containing "Day" and reshape to 31x7 table
            day_columns = [col for col in df.columns if "Day" in col]
            reshaped_data = df[day_columns].values.reshape(-1, 7)
            reshaped_df = pd.DataFrame(reshaped_data, columns=['Day', 'Yes', 'No', 'Dosage', 'Freq', 'Form', 'Route'])

            # Create a dictionary to store edited values
            edited_values = {}

            # Iterate through each row and create input fields
            for i, row in reshaped_df.iterrows():
                cols = st.columns(7)
                for j, col in enumerate(reshaped_df.columns):
                    key = f"{col}{i+1}"
                    edited_values[key] = cols[j].text_input(key, value=str(row[col]))

            # Submit button
            submitted = st.form_submit_button("Submit")
            if submitted:
                # Update the original DataFrame with the edited values
                for i, row in reshaped_df.iterrows():
                    for j, col in enumerate(reshaped_df.columns):
                        key = f"{col}{i+1}"
                        df.at[0, f"{col}{i+1}"] = edited_values[key]

                # Upload the updated DataFrame back to the blob storage
                timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                blob_name = f"ReviewedFiles/review_{timestamp}.csv"
                upload_blob_data('data1', blob_name, df)
                st.write("Data has been updated and uploaded successfully.")