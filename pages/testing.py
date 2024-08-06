import streamlit as st
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import pandas as pd
import io
import datetime

st.title("Review Form For Accuracy")

# Create BlobServiceClient object with hardcoded connection string
connection_string = 'DefaultEndpointsProtocol=https;AccountName=devcareall;AccountKey=GEWV0frElMx6YmZyObMDqJWDj3pG0FzJCTkCaknW/JMH9UqHqNzeFhF/WWCUKeIj3LNN5pb/hl9+AStHMGKFA==;EndpointSuffix=core.windows.net'
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

            # Create a DataFrame for Day29, Day30, and Day31
            days_df = pd.DataFrame({
                'Day': [row_data.get('Day29', ''), row_data.get('Day30', ''), row_data.get('Day31', '')],
                'Yes': [row_data.get('Day29Yes', ''), row_data.get('Day30Yes', ''), row_data.get('Day31Yes', '')],
                'No': [row_data.get('Day29No', ''), row_data.get('Day30No', ''), row_data.get('Day31No', '')],
                'Dosage': [row_data.get('Day29Dosage', ''), row_data.get('Day30Dosage', ''), row_data.get('Day31Dosage', '')],
                'Freq': [row_data.get('Day29Freq', ''), row_data.get('Day30Freq', ''), row_data.get('Day31Freq', '')],
                'Form': [row_data.get('Day29Form', ''), row_data.get('Day30Form', ''), row_data.get('Day31Form', '')],
                'Route': [row_data.get('Day29Route', ''), row_data.get('Day30Route', ''), row_data.get('Day31Route', '')]
            })

            # Display the DataFrame in an editable table
            edited_days_df = st.data_editor(days_df, key="editable_days_table")

            # Submit button
            submitted = st.form_submit_button("Submit")
            if submitted:
                # Update the original DataFrame with the edited values
                for i, day in enumerate(['Day29', 'Day30', 'Day31']):
                    df.at[0, f'{day}'] = edited_days_df.at[i, 'Day']
                    df.at[0, f'{day}Yes'] = edited_days_df.at[i, 'Yes']
                    df.at[0, f'{day}No'] = edited_days_df.at[i, 'No']
                    df.at[0, f'{day}Dosage'] = edited_days_df.at[i, 'Dosage']
                    df.at[0, f'{day}Freq'] = edited_days_df.at[i, 'Freq']
                    df.at[0, f'{day}Form'] = edited_days_df.at[i, 'Form']
                    df.at[0, f'{day}Route'] = edited_days_df.at[i, 'Route']

                # Upload the updated DataFrame back to the blob storage
                timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                blob_name = f"ReviewedFiles/review_{timestamp}.csv"
                upload_blob_data('data1', blob_name, df)
                st.write("Data has been updated and uploaded successfully.")