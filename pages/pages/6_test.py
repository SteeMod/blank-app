from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.ai.formrecognizer import FormRecognizerClient
from azure.core.credentials import AzureKeyCredential
import csv

# Initialize BlobServiceClient
blob_service_client = BlobServiceClient(account_url="your_storage_account_url", credential="your_storage_account_key")

# Upload file to Azure Blob Storage
def upload_file_to_blob(file_path, container_name, blob_name):
    blob_client = blob_service_client.get_blob_client(container_name, blob_name)
    with open(file_path, "rb") as data:
        blob_client.upload_blob(data)

# Use Azure Document Intelligence to extract data
def extract_data_from_document(container_name, blob_name):
    form_recognizer_client = FormRecognizerClient(endpoint="your_form_recognizer_endpoint", credential=AzureKeyCredential("your_form_recognizer_key"))
    blob_sas_url = blob_service_client.get_blob_client(container_name, blob_name).url
    poller = form_recognizer_client.begin_recognize_content_from_url(blob_sas_url)
    result = poller.result()
    return result

# Save extracted data to CSV and upload back to Azure Blob Storage
def save_data_to_csv_and_upload(data, container_name, csv_blob_name):
    with open('temp.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)
    upload_file_to_blob('temp.csv', container_name, csv_blob_name)

# Main function to use the above functions
def main():
    file_path = "your_file_path"
    container_name = "your_container_name"
    blob_name = "your_blob_name"
    csv_blob_name = "your_csv_blob_name"

    upload_file_to_blob(file_path, container_name, blob_name)
    data = extract_data_from_document(container_name, blob_name)
    save_data_to_csv_and_upload(data, container_name, csv_blob_name)

if __name__ == "__main__":
    main()
