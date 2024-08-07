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

            col1, col2 = st.columns(2)
            FirstName = col1.text_input("FirstName", value=str(row_data.get('FirstName', '')))
            LastName = col2.text_input("LastName", value=str(row_data.get('LastName', '')))
            Address = st.text_input("Address", value=str(row_data.get('Address', '')))
            City, State = st.columns(2)
            City = City.text_input("City", value=str(row_data.get('City', '')))
            State = State.text_input("State", value=str(row_data.get('State', '')))
            ZipCode, Phone = st.columns(2)
            ZipCode = ZipCode.text_input("ZipCode", value=str(row_data.get('ZipCode', '')))
            Phone = Phone.text_input("Phone", value=str(row_data.get('Phone', '')))
            Allergy1, Allergy2 = st.columns(2)
            Allergy1 = Allergy1.text_input("Allergy1", value=str(row_data.get('Allergy1', '')))
            Allergy2 = Allergy2.text_input("Allergy2", value=str(row_data.get('Allergy2', '')))

            # Medication details section
            MedIntakeName, MedIntakeMonth, MedIntakeYear = st.columns(3)
            MedIntakeName = MedIntakeName.text_input("MEDICATION NAME", value=str(row_data.get('MedIntakeName', '')))
            MedIntakeMonth = MedIntakeMonth.text_input("MONTH", value=str(row_data.get('MedIntakeMonth', '')))
            MedIntakeYear = MedIntakeYear.text_input("YEAR", value=str(row_data.get('MedIntakeYear', '')))

            # Editable table for fields containing "Med"
            med_fields = [field for field in row_data.index if "Med" in field]
            med_values = [str(row_data.get(field, '')) for field in med_fields]

            # Create a 4-column, 7-row layout
            cols = st.columns(4)
            for i, field in enumerate(med_fields):
                col = cols[i % 4]
                col.text_input(field, value=med_values[i])

            submit_button = st.form_submit_button("Submit")
            if submit_button:
                # Update the row_data with edited values
                for field in med_fields:
                    row_data[field] = st.session_state.get(field, row_data[field])
                
                # Save the updated data back to the blob
                upload_blob_data('data1', latest_blob.name, data)
                st.success("Data updated successfully!")

    else:
        st.write("No files found in the specified container.")