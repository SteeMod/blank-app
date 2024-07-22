from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from azure.storage.blob import BlobServiceClient
import os
from csv import DictWriter
import asyncio

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')
        if file and file.filename:
            filename = secure_filename(file.filename)
            file_path = os.path.join('/tmp', filename)
            file.save(file_path)
            if os.path.exists(file_path):
                asyncio.run(process_file(file_path, filename))
                return 'File has been processed and saved to Blob Storage.'
            else:
                return 'Error: File was not saved correctly.'
        else:
            return 'No file provided or file is empty.'

async def process_file(file_path, filename):
    endpoint = os.getenv('FORM_RECOGNIZER_ENDPOINT', "https://new2two.cognitiveservices.azure.com/")
    credential = AzureKeyCredential(os.getenv('FORM_RECOGNIZER_API_KEY', "54b598653a314a04a52501abac2cc76e"))
    client = DocumentAnalysisClient(endpoint, credential)

    model_id = os.getenv('FORM_RECOGNIZER_CUSTOM_MODEL_ID', "Thessa5vs6")

    # Create BlobServiceClient
    blob_service_client = BlobServiceClient.from_connection_string(os.getenv('AZURE_STORAGE_CONNECTION_STRING', "DefaultEndpointsProtocol=https;AccountName=devcareall;AccountKey=GEW0V0frElMx6YmZyObMDqJWDj3pG0FzJCTkCaknW/JMH9UqHqNzeFhF/WWCUKeIj3LNN5pb/hl9+AStHMGKFA==;EndpointSuffix=core.windows.net"))
    container_client = blob_service_client.get_container_client(os.getenv('BLOB_CONTAINER_NAME', "data1"))
    blob_client = container_client.get_blob_client(filename)

    # Upload the PDF file to Azure Blob Storage
    with open(file_path, 'rb') as data:
        blob_client.upload_blob(data, overwrite=True)

    # Send PDF to Azure AI Document Intelligence
    with open(file_path, 'rb') as data:
        poller = await client.begin_analyze_document(model_id=model_id, document=data)
    result = await poller.result()

    if not result.documents:
        raise Exception("Expected at least one document in the result.")

    document = result.documents[0]

    # Save analysis result as CSV
    csv_filename = 'result_' + filename.split('.')[0] + '.csv'
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [name for name in document.fields.keys()]
        writer = DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        record = {key: field.content if field.content else field.value for key, field in document.fields.items()}
        writer.writerow(record)

    # Upload the CSV file to Azure Blob Storage
    csv_blob_client = container_client.get_blob_client('out1.csv')
    with open('out1.csv', 'rb') as data:
        csv_blob_client.upload_blob(data, overwrite=True)

    # Clean up local files
    os.remove(file_path)
    os.remove('out1.csv')

if __name__ == '__main__':
    app.run(debug=True)