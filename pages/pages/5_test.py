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
endpoint = "your_endpoint"
key = "your_key"
print(check_service_status(endpoint, key))
