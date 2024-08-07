import streamlit as st
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import pandas as pd
import io
import datetime
from io import BytesIO
from streamlit_pdf_viewer import pdf_viewer

# Azure Blob Storage connection details
connection_string = "DefaultEndpointsProtocol=https;AccountName=devcareall;AccountKey=GEW0V0frElMx6YmZyObMDqJWDj3pG0FzJCTkCaknW/JMH9UqHqNzeFhF/WWCUKeIj3LNN5pb/hl9+AStHMGKFA==;EndpointSuffix=core.windows.net"
container_name = "data1"
raw_folder_name = "RawFiles"
reviewed_folder_name = "ReviewedFiles"

# Initialize the BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)

# Get the latest file from the folder
blobs = container_client.list_blobs(name_starts_with=raw_folder_name)
latest_blob = max(blobs, key=lambda b: b.creation_time)

# Download the latest file
blob_client = container_client.get_blob_client(latest_blob.name)
downloaded_blob = blob_client.download_blob().readall()

# Display the file content on Streamlit
st.title("Latest Reviewed File")

# Check if the file is a PDF
if latest_blob.name.endswith('.pdf'):
    try:
        # Create a BytesIO object from the downloaded blob
        pdf_file = BytesIO(downloaded_blob)
        
        # Use streamlit-pdf-viewer to display the PDF
        pdf_viewer(pdf_file.getvalue())
    except Exception as e:
        st.text(f"Error reading the PDF file: {e}")
else:
    st.text("The latest file is not a PDF.")

st.title("Review Form For Accuracy")

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

def move_blob_to_reviewed(blob_name):
    try:
        source_blob = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{blob_name}"
        destination_blob_name = blob_name.replace(raw_folder_name, reviewed_folder_name)
        blob_client = blob_service_client.get_blob_client(container_name, destination_blob_name)
        blob_client.start_copy_from_url(source_blob)
        container_client.delete_blob(blob_name)
    except Exception as e:
        st.write(f"Error occurred while moving the blob: {e}")

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
            
            treatment_plan_data = {
                'MedCheck': [str(row_data.get(f"Med{i}Check", '')) for i in range(1, 5)],
                'MedName': [str(row_data.get(f"Med{i}Name", '')) for i in range(1, 5)],
                'DayDosage': [str(row_data.get(f"Day{i}Dosage", '')) for i in range(1, 5)],
                'DayFreq': [str(row_data.get(f"Day{i}Freq", '')) for i in range(1, 5)],
                'DayForm': [str(row_data.get(f"Day{i}Form", '')) for i in range(1, 5)],
                'DayRoute': [str(row_data.get(f"Day{i}Route", '')) for i in range(1, 5)],
                'DayInstruction': [str(row_data.get(f"Day{i}Instruction", '')) for i in range(1, 5)]
            }
            treatment_plan_df = pd.DataFrame(treatment_plan_data)
            edited_treatment_plan_df = st.data_editor(treatment_plan_df)

            # Treatment Plan table
            treatment_plan_data = {
                'Day': [f"Day{i}" for i in range(1, 32)],
                'Yes': [str(row_data.get(f"Day{i}Yes", '')) for i in range(1, 32)],
                'No': [str(row_data.get(f"Day{i}No", '')) for i in range(1, 32)],
                'Dosage': [str(row_data.get(f"Day{i}Dosage", '')) for i in range(1, 32)],
                'Frequency': [str(row_data.get(f"Day{i}Freq", '')) for i in range(1, 32)],
                'Form': [str(row_data.get(f"Day{i}Form", '')) for i in range(1, 32)],
                'Route': [str(row_data.get(f"Day{i}Route", '')) for i in range(1, 32)]
            }
            treatment_plan_df = pd.DataFrame(treatment_plan_data)
            edited_treatment_plan_df = st.data_editor(treatment_plan_df)

            submit_button = st.form_submit_button("Submit")
            if submit_button:
                # Update the row_data with edited values
                for index, row in edited_treatment_plan_df.iterrows():
                    row_data[f"Day{index+1}Yes"] = row['Yes']
                    row_data[f"Day{index+1}No"] = row['No']
                    row_data[f"Day{index+1}Dosage"] = row['Dosage']
                    row_data[f"Day{index+1}Freq"] = row['Frequency']
                    row_data[f"Day{index+1}Form"] = row['Form']
                    row_data[f"Day{index+1}Route"] = row['Route']
                
                # Save the updated data back to the blob
                upload_blob_data('data1', latest_blob.name, data)
                
                # Move the blob to the ReviewedFiles folder
                move_blob_to_reviewed(latest_blob.name)
                
                st.success("Data updated and file moved to ReviewedFiles successfully!")

    else:
        st.write("No files found in the specified container.")
