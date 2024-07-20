# Import necessary libraries
import streamlit as st
from azure.ai.formrecognizer import FormRecognizerClient
from azure.core.credentials import AzureKeyCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import requests
import os
import json
import csv
import time

# Create the file uploader and specify that it should accept PDF files
uploaded_file = st.file_uploader("Choose a PDF file", type=['pdf'])

# Create a button for the user to click to upload file
if st.button('Submit'):
    if uploaded_file is not None:
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()

        # Azure connection string
        connect_str = 'DefaultEndpointsProtocol=https;AccountName=devcareall;AccountKey=GEW0V0frElMx6YmZyObMDqJWDj3pG0FzJCTkCaknW/JMH9UqHqNzeFhF/WWCUKeIj3LNN5pb/hl9+AStHMGKFA==;EndpointSuffix=core.windows.net'

        # Create the BlobServiceClient object which will be used to create a container client
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        # Create a unique name for the blob
        blob_name = "RawDoc2"

        # Create a blob client using the local file name as the name for the blob
        blob_client = blob_service_client.get_blob_client("data1", blob_name)

        # Upload the file
        blob_client.upload_blob(bytes_data)
        st.write('File uploaded to Azure Blob Storage')

        # Now we send the file to Azure AI Document Intelligence
        endpoint = "https://new2two.cognitiveservices.azure.com"
        apim_key = "54b598653a314a04a52501abac2cc76e"
        model_id = "Thessa5vs6"
        post_url = endpoint + "/formrecognizer/v3.1/custom/models/%s/analyze" % model_id
        params = {"includeTextDetails": True}

        headers = {
            # Request headers
            'Content-Type': 'application/pdf',
            'Ocp-Apim-Subscription-Key': apim_key,
        }

        try:
            resp = requests.post(url=post_url, data=bytes_data, headers=headers, params=params)
            if resp.status_code != 202:
                print("POST analyze failed:\n%s" % json.dumps(resp.json()))
                quit()
            print("POST analyze succeeded:\n%s" % resp.headers)
            get_url = resp.headers["operation-location"]
        except Exception as e:
            print("POST analyze failed:\n%s" % str(e))
            quit()

        # The recognized form data is returned in the response after the operation completes
        n_tries = 15
        n_try = 0
        wait_sec = 5
        while n_try < n_tries:
            try:
                resp = requests.get(url=get_url, headers=headers)
                resp_json = resp.json()
                if resp.status_code != 200:
                    print("GET analyze results failed:\n%s" % json.dumps(resp_json))
                    quit()
                status = resp_json["status"]
                if status == "succeeded":
                    print("Analysis succeeded:\n%s" % json.dumps(resp_json))
                    # Now we format the data as CSV and save it back to Blob Storage
                    fields = resp_json['analyzeResult']['documentResults'][0]['fields']
                    with open('output.csv', 'w', newline='') as csvfile:
                        fieldnames = list(fields.keys())
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerow({k: v['text'] for k, v in fields.items()})
                    # Create a blob client for the CSV file
                    csv_blob_client = blob_service_client.get_blob_client("RawDocuments", "output.csv")
                    # Upload the CSV file
                    with open("output.csv", "rb") as data:
                        csv_blob_client.upload_blob(data)
                    st.write('CSV file saved to Azure Blob Storage in the Raw documents folder')
                    break
                if status == "failed":
                    print("Analysis failed:\n%s" % json.dumps(resp_json))
                    quit()
                # Analysis still running. Wait and retry.
                time.sleep(wait_sec)
                n_try += 1
            except Exception as e:
                msg = "GET analyze results failed:\n%s" % str(e)
                print(msg)
                quit()
    else:
        st.write('No file selected')
