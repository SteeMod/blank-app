import requests
import streamlit as st

def check_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return "Connection successful"
    except requests.exceptions.HTTPError as errh:
        return f"HTTP Error: {errh}"
    except requests.exceptions.ConnectionError as errc:
        return f"Error Connecting: {errc}"
    except requests.exceptions.Timeout as errt:
        return f"Timeout Error: {errt}"
    except requests.exceptions.RequestException as err:
        return f"Something went wrong: {err}"

url = "https://new2two.cognitiveservices.azure.com/formrecognizer/v2.1-preview.3/custom/models/Thessa5vs6/analyze?modelId=Thessa5vs6"
st.write(check_url(url))
