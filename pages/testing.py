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
        return pd.read_csv(io.StringIO(stream.decode('utf-8', errors='ignore')), on_bad_lines='skip')
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

# Review button
with st.form("Review"):
    latest_blob = get_latest_blob('data1', 'CookedFiles/')
    if latest_blob is not None:
        data = download_blob_data(latest_blob)
        if data is not None:
            row_data = data.iloc[0]  # assuming you want to display the first row
            df = pd.DataFrame([row_data])

            # Display the DataFrame in an editable table
            edited_df = st.data_editor(df)

            # Extract the edited values
            Day30 = edited_df.at[0, 'Day30']
            Day30Yes = edited_df.at[0, 'Day30Yes']
            Day30No = edited_df.at[0, 'Day30No']
            Day30Dosage = edited_df.at[0, 'Day30Dosage']
            Day30Freq = edited_df.at[0, 'Day30Freq']
            Day30Form = edited_df.at[0, 'Day30Form']
            Day30Route = edited_df.at[0, 'Day30Route']
            Day31 = edited_df.at[0, 'Day31']
            Day31Yes = edited_df.at[0, 'Day31Yes']
            Day31No = edited_df.at[0, 'Day31No']
            Day31Dosage = edited_df.at[0, 'Day31Dosage']
            Day31Freq = edited_df.at[0, 'Day31Freq']
            Day31Form = edited_df.at[0, 'Day31Form']
            Day31Route = edited_df.at[0, 'Day31Route']

            # Display the updated values
            st.write("Updated Values:")
            st.write(f"Day30: {Day30}")
            st.write(f"Yes30: {Day30Yes}")
            st.write(f"No30: {Day30No}")
            st.write(f"Dosage30: {Day30Dosage}")
            st.write(f"Frequency30: {Day30Freq}")
            st.write(f"Form30: {Day30Form}")
            st.write(f"Route30: {Day30Route}")
            st.write(f"Day31: {Day31}")
            st.write(f"Yes31: {Day31Yes}")
            st.write(f"No31: {Day31No}")
            st.write(f"Dosage31: {Day31Dosage}")
            st.write(f"Frequency31: {Day31Freq}")
            st.write(f"Form31: {Day31Form}")
            st.write(f"Route31: {Day31Route}")

            # Submit button
            submitted = st.form_submit_button("Submit")
            if submitted:
                # Update the DataFrame with the edited values
                edited_df.at[0, 'Day30'] = Day30
                edited_df.at[0, 'Day30Yes'] = Day30Yes
                edited_df.at[0, 'Day30No'] = Day30No
                edited_df.at[0, 'Day30Dosage'] = Day30Dosage
                edited_df.at[0, 'Day30Freq'] = Day30Freq
                edited_df.at[0, 'Day30Form'] = Day30Form
                edited_df.at[0, 'Day30Route'] = Day30Route
                edited_df.at[0, 'Day31'] = Day31
                edited_df.at[0, 'Day31Yes'] = Day31Yes
                edited_df.at[0, 'Day31No'] = Day31No
                edited_df.at[0, 'Day31Dosage'] = Day31Dosage
                edited_df.at[0, 'Day31Freq'] = Day31Freq
                edited_df.at[0, 'Day31Form'] = Day31Form
                edited_df.at[0, 'Day31Route'] = Day31Route

                # Upload the updated DataFrame back to the blob storage
                upload_blob_data('data1', latest_blob.name, edited_df)
                st.write("Data has been updated and uploaded successfully.")