import requests

def check_service_status(endpoint, key):
    url = f"{endpoint}/formrecognizer/v3.1/custom/models"
    headers = {
        'Ocp-Apim-Subscription-Key': key
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return "Service is available"
    else:
        return f"Service unavailable. Status code: {response.status_code}"

# Replace 'your_endpoint' and 'your_key' with your actual values
endpoint = "https://new1one.cognitiveservices.azure.com/"
key = "1dc611154da945a39a3368b10fd088a7"
print(check_service_status(endpoint, key))
