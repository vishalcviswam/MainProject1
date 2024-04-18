
import requests
from requests.exceptions import RequestException

def generate_3d_from_image(image_file):
    api_endpoint = 'http://example.com/api/triposr'
    headers = {'Authorization': 'Bearer YOUR_API_KEY'}
    files = {'file': image_file}

    try:
        response = requests.post(api_endpoint, headers=headers, files=files)
        response.raise_for_status()  # This will raise an exception for HTTP error codes
        return response.json()
    except RequestException as e:
        print(f"Request failed: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return None
