import requests

# TODO: Configure Gemini API (or whatever API we end up using)
# TODO: Write prompt to send to model

def upload_image(file_path):

    # TODO: Replace link with real API URL
    api_url = "https://example-llm-api.com"
    
    # TODO: Replace with real API key
    headers = {
        "Authorization": "Bearer API_KEY_HERE"
    }

    with open(file_path, 'rb') as image_file:
        files = {'file': image_file}
        response = requests.post(api_url, headers=headers, files=files)
        return response
    
upload_image('test_image.jpg')