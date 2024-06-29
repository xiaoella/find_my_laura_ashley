import os
import requests

# Retrieve API key securely
api_key = os.environ.get('ETSY_API_KEY')

def test_etsy_api(api_key, url = "https://openapi.etsy.com/v3/application/openapi-ping"):
    # Set up the header as per Etsy's requirement for endpoint requests
    headers = {
        "x-api-key": api_key
        }
    
    # Send a request to the Etsy ping endpoint
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("API key is working!")
        print(response.json())
    else:
        print("Failed to authenticate API key")
        print(f"Status Code: {response.status_code}")
        print(response.json())

if __name__ == "__main__":
    test_etsy_api(api_key)