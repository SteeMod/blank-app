import streamlit as st
import pandas as pd
import requests
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

# Streamlit app
def main():
    st.title('PDF File Upload')

    with st.form(key='upload_form'):
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
        submit_button = st.form_submit_button(label='Submit')

        if uploaded_file is not None and submit_button:
            # Create a temporary file
            with open('temp.pdf', 'wb') as f:
                f.write(uploaded_file.getbuffer())
            
            # Send the file to Azure AI Document Intelligence Studio
            headers = {
                'Ocp-Apim-Subscription-Key': '54b598653a314a04a52501abac2cc76e',
            }
            params = {
                'modelId': 'Thessa5vs6',
            }
            data = open('temp.pdf', 'rb').read()
            response = requests.post('https://new2two.cognitiveservices.azure.com/formrecognizer/v2.1-preview.3/custom/models/Thessa5vs6/analyze', headers=headers, params=params, data=data)
            response.raise_for_status()
            result = response.json()

            # Convert the result to a DataFrame
            df = pd.DataFrame(result)

            # Save the DataFrame to a CSV file
            df.to_csv('temp.csv', index=False)

            # Upload the CSV file to Azure Blob Storage
            blob_service_client = BlobServiceClient.from_connection_string('DefaultEndpointsProtocol=https;AccountName=devcareall;AccountKey=GEW0V0frElMx6YmZyObMDqJWDj3pG0FzJCTkCaknW/JMH9UqHqNzeFhF/WWCUKeIj3LNN5pb/hl9+AStHMGKFA==;EndpointSuffix=core.windows.net')
            blob_client = blob_service_client.get_blob_client('data1', 'RawDocuments/temp.csv')
            with open('temp.csv', 'rb') as f:
                blob_client.upload_blob(f)

            st.success('File uploaded successfully!')

if __name__ == '__main__':
    main()

