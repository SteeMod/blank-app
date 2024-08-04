from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from azure.storage.blob import BlobServiceClient
import os
from csv import DictWriter

async def main():
    endpoint = os.getenv('FORM_RECOGNIZER_ENDPOINT', "https://new2two.cognitiveservices.azure.com/")
    credential = AzureKeyCredential(os.getenv('FORM_RECOGNIZER_API_KEY', "027ad9245a594c5886cf5d90abecb9d1"))
    client = DocumentAnalysisClient(endpoint, credential)

    model_id = os.getenv('FORM_RECOGNIZER_CUSTOM_MODEL_ID', "Thessa5vs6")

    # Create BlobServiceClient
    blob_service_client = BlobServiceClient.from_connection_string(os.getenv('AZURE_STORAGE_CONNECTION_STRING', "DefaultEndpointsProtocol=https;AccountName=devcareall;AccountKey=GEW0V0frElMx6YmZyObMDqJWDj3pG0FzJCTkCaknW/JMH9UqHqNzeFhF/WWCUKeIj3LNN5pb/hl9+AStHMGKFA==;EndpointSuffix=core.windows.net"))
    container_client = blob_service_client.get_container_client(os.getenv('BLOB_CONTAINER_NAME', "data1"))
    block_blob_client = container_client.get_blob_client(os.getenv('BLOB_NAME', "test4.pdf"))

    # Download blob content to a stream
    downloader = block_blob_client.download_blob()
    blob_stream = downloader.readall()

    poller = client.begin_analyze_document(model_id=model_id, document=blob_stream)
    result = poller.result()


    if not result.documents:
        raise Exception("Expected at least one document in the result.")

    document = result.documents[0]

    # Create a CSV writer
    with open('out1.csv', mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [name for name in document.fields.keys()]
        writer = DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Transform document.fields into a format suitable for csv-writer
        record = {}
        for key, field in document.fields.items():
            if field.value_type == 'dictionary' and field.value and 'rows' in field.value:
                # Check if the object is a table
                if isinstance(field.value['rows'], list):
                    # Handle table data
                    for rowIndex, row in enumerate(field.value['rows']):
                        if row and isinstance(row, list):
                            for cellIndex, cell in enumerate(row):
                                record[f"{key}_row{rowIndex}_cell{cellIndex}"] = cell.content
            else:
                # Handle regular fields
                record[key] = field.content if field.content else field.value

        writer.writerow(record)

    # Create a new blob client for the CSV file
    csv_blob_client = container_client.get_blob_client('out1.csv')

    # Upload the CSV file to Azure Blob Storage
    with open('out1.csv', 'rb') as data:
        csv_blob_client.upload_blob(data, overwrite=True)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())