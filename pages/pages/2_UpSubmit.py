import streamlit as st
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from azure.storage.blob import BlobServiceClient
import os
from csv import DictWriter
import asyncio
import threading

# Define a function to handle the asynchronous processing
async def process_file(blob_stream, model_id, container_client):
    endpoint = os.getenv('FORM_RECOGNIZER_ENDPOINT', "https://new2two.cognitiveservices.azure.com/")
    credential = AzureKeyCredential(os.getenv('FORM_RECOGNIZER_API_KEY', "a1fb5ca25a77422590c3f85c8961de47"))
    client = DocumentAnalysisClient(endpoint, credential)

    poller = await client.begin_analyze_document(model_id=model_id, document=blob_stream)
    result = await poller.result()

    if not result.documents:
        raise Exception("Expected at least one document in the result.")

    document = result.documents[0]

    # Create a CSV writer
    with open('out1.csv', mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [name for name in document.fields.keys()]
        writer = DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Transform document.fields into a format suitable for csv-writer
        record = {key: field.content if field.content else field.value for key, field in document.fields.items()}
        writer.writerow(record)

    # Upload the CSV file to Azure Blob Storage
    csv_blob_client = container_client.get_blob_client('out1.csv')
    with open('out1.csv', 'rb') as data:
        await csv_blob_client.upload_blob(data, overwrite=True)

# Define the main function to use Streamlit for UI
def main():
    st.title('Azure AI Document Intelligence with Streamlit')
    uploaded_file = st.file_uploader("Choose a PDF file", type=['pdf'])

    if st.button('Submit') and uploaded_file is not None:
        # Setup Azure Blob Storage
        blob_service_client = BlobServiceClient.from_connection_string(os.getenv('AZURE_STORAGE_CONNECTION_STRING', "DefaultEndpointsProtocol=https;AccountName=devcareall;AccountKey=GEW0V0frElMx6YmZyObMDqJWDj3pG0FzJCTkCaknW/JMH9UqHqNzeFhF/WWCUKeIj3LNN5pb/hl9+AStHMGKFA==;EndpointSuffix=core.windows.net"))
        container_client = blob_service_client.get_container_client(os.getenv('BLOB_CONTAINER_NAME', "data1"))
        blob_client = container_client.get_blob_client(uploaded_file.name)

        # Upload the PDF file to Azure Blob Storage
        blob_client.upload_blob(uploaded_file.getvalue(), overwrite=True)

        # Get model ID
        model_id = os.getenv('FORM_RECOGNIZER_CUSTOM_MODEL_ID', "Thessa5vs6")

        # Run the async process in a thread
        def run_async(blob_stream, model_id, container_client):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(process_file(blob_stream, model_id, container_client))

        thread = threading.Thread(target=run_async, args=(uploaded_file.getvalue(), model_id, container_client))
        thread.start()
        thread.join()

        st.success('File has been processed and saved to Blob Storage.')

if __name__ == '__main__':
    main()