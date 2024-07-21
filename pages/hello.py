
import streamlit as st
import base64

def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{bin_file}">Download {file_label}</a>'
    return href

# Create a button to download the PDF file
if st.button('Download PDF'):
    st.markdown(get_binary_file_downloader_html('MOUD Tracker Form', 'PDF'), unsafe_allow_html=True)
