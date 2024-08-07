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

            # Treatment Plan table
            Med1Check, Med1Name, Med1Dosage, Med1Frequency, Med1Form, Med1Route, Med1Instructions = st.columns(7)
            Med1Check = Med1Check.text_input("Select [x]1", value=str(row_data.get('Med1Check', '')))
            Med1Name = Med1Name.text_input("Medication1", value=str(row_data.get('Med1Name', '')))
            Med1Dosage = Med1Dosage.text_input("Dosage1", value=str(row_data.get('Med1Dosage', '')))
            Med1Frequency = Med1Frequency.text_input("Frequency1", value=str(row_data.get('Med1Frequency', '')))
            Med1Form = Med1Form.text_input("Form1", value=str(row_data.get('Med1Form', '')))
            Med1Route = Med1Route.text_input("Route1", value=str(row_data.get('Med1Route', '')))
            Med1Instructions = Med1Instructions.text_input("Instructions1", value=str(row_data.get('Med1Instructions', '')))

            Med2Check, Med2Name, Med2Dosage, Med2Frequency, Med2Form, Med2Route, Med2Instructions = st.columns(7)
            Med2Check = Med2Check.text_input("Select [x]2", value=str(row_data.get('Med2Check', '')))
            Med2Name = Med2Name.text_input("Medication2", value=str(row_data.get('Med2Name', '')))
            Med2Dosage = Med2Dosage.text_input("Dosage2", value=str(row_data.get('Med2Dosage', '')))
            Med2Frequency = Med2Frequency.text_input("Frequency2", value=str(row_data.get('Med2Frequency', '')))
            Med2Form = Med2Form.text_input("Form2", value=str(row_data.get('Med2Form', '')))
            Med2Route = Med2Route.text_input("Route2", value=str(row_data.get('Med2Route', '')))
            Med2Instructions = Med2Instructions.text_input("Instructions2", value=str(row_data.get('Med2Instructions', '')))

            Med3Check, Med3Name, Med3Dosage, Med3Frequency, Med3Form, Med3Route, Med3Instructions = st.columns(7)
            Med3Check = Med3Check.text_input("Select [x]3", value=str(row_data.get('Med3Check', '')))
            Med3Name = Med3Name.text_input("Medication3", value=str(row_data.get('Med3Name', '')))
            Med3Dosage = Med3Dosage.text_input("Dosage3", value=str(row_data.get('Med3Dosage', '')))
            Med3Frequency = Med3Frequency.text_input("Frequency3", value=str(row_data.get('Med3Frequency', '')))
            Med3Form = Med3Form.text_input("Form3", value=str(row_data.get('Med3Form', '')))
            Med3Route = Med3Route.text_input("Route3", value=str(row_data.get('Med3Route', '')))
            Med3Instructions = Med3Instructions.text_input("Instructions3", value=str(row_data.get('Med3Instructions', '')))

            Med4Check, Med4Name, Med4Dosage, Med4Frequency, Med4Form, Med4Route, Med4Instructions = st.columns(7)
            Med4Check = Med4Check.text_input("Select [x]4", value=str(row_data.get('Med4Check', '')))
            Med4Name = Med4Name.text_input("Medication4", value=str(row_data.get('Med4Name', '')))
            Med4Dosage = Med4Dosage.text_input("Dosage4", value=str(row_data.get('Med4Dosage', '')))
            Med4Frequency = Med4Frequency.text_input("Frequency4", value=str(row_data.get('Med4Frequency', '')))
            Med4Form = Med4Form.text_input("Form4", value=str(row_data.get('Med4Form', '')))
            Med4Route = Med4Route.text_input("Route4", value=str(row_data.get('Med4Route', '')))
            Med4Instructions = Med4Instructions.text_input("Instructions4", value=str(row_data.get('Med4Instructions', '')))

            # Treatment Plan table
            day_fields = [f"Day{i}" for i in range(1, 32)]
            day_table = [["" for _ in range(7)] for _ in range(31)]
            for i, day in enumerate(day_fields):
                day_table[i][0] = st.text_input(day, value=str(row_data.get(day, '')))
                day_table[i][1] = st.text_input(f"yes_{i+1}", value=str(row_data.get(f"Day{i+1}yes", '')))
                day_table[i][2] = st.text_input(f"No_{i+1}", value=str(row_data.get(f"Day{i+1}No", '')))
                day_table[i][3] = st.text_input(f"Dosage_{i+1}", value=str(row_data.get(f"Day{i+1}Dosage", '')))
                day_table[i][4] = st.text_input(f"Frequency_{i+1}", value=str(row_data.get(f"Day{i+1}Freq", '')))
                day_table[i][5] = st.text_input(f"Form_{i+1}", value=str(row_data.get(f"Day{i+1}Form", '')))
                day_table[i][6] = st.text_input(f"Route_{i+1}", value=str(row_data.get(f"Day{i+1}Route", '')))

            # Submit button
            submitted = st.form_submit_button("Submit")
            if submitted:
                # Update the data with the new values
                for i, day in enumerate(day_fields):
                    data.at[0, day] = day_table[i][0]
                    data.at[0, f"Day{i+1}yes"] = day_table[i][1]
                    data.at[0, f"Day{i+1}No"] = day_table[i][2]
                    data.at[0, f"Day{i+1}Dosage"] = day_table[i][3]
                    data.at[0, f"Day{i+1}Freq"] = day_table[i][4]
                    data.at[0, f"Day{i+1}Form"] = day_table[i][5]
                    data.at[0, f"Day{i+1}Route"] = day_table[i][6]

                # Upload the updated data back to the blob
                upload_blob_data('data1', latest_blob.name, data)
                st.success("Data updated and uploaded successfully!")
