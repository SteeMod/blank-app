import streamlit as st
from azure.storage.blob import BlobServiceClient

# Hardcoded Azure blob storage connection string
connection_string = "DefaultEndpointsProtocol=https;AccountName=devcareall;AccountKey=GEW0V0frElMx6YmZyObMDqJWDj3pG0FzJCTkCaknW/JMH9UqHqNzeFhF/WWCUKeIj3LNN5pb/hl9+AStHMGKFA==;EndpointSuffix=core.windows.net"

container_name = "data1/Misc"
blob_name = "comments.txt"

# Create a form with a text area in Streamlit
with st.form(key='Comment'):
    text_input = st.text_area(label='Enter your comment', value='', placeholder='Include who the message is from and give detailed comments.', max_chars=500)
    submit_button = st.form_submit_button(label='Submit')

    # If the form is submitted, write the comment to a file and upload it to Azure Blob Storage
    if submit_button:
        with open('comments.txt', 'a') as f:
            f.write(text_input + '\n')

        # Create a blob client using the local file name as the name for the blob
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

        # Upload the created file, overwriting if it already exists
        try:
            with open('comments.txt', 'rb') as data:
                blob_client.upload_blob(data, overwrite=True)
            st.success("Comment uploaded successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Display the contents of comments.txt from Azure Blob Storage
try:
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    blob_data = blob_client.download_blob().readall()
    comments = blob_data.decode('utf-8')
    st.write("Contents of comments.txt from Azure Blob Storage:")
    st.text(comments)
except Exception as e:
    st.error(f"An error occurred while retrieving the comments: {e}")
