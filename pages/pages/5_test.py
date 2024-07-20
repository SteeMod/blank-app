import requests
import streamlit as st

def check_url(url):
    try:
        headers = {
            # Replace 'your-key' with your Cognitive Services key
            'Ocp-Apim-Subscription-Key': '1dc611154da945a39a3368b10fd088a7',
            'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=headers)
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

# Replace 'new2two' with your resource name and 'Thessa5v6' with your model ID
url = "https://new1one.cognitiveservices.azure.com/v3.1/custom/models/Thessa5v6/analyze"
st.write(check_url(url))

