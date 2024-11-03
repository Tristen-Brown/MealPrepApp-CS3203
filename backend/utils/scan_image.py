import requests
import google.generativeai as genai
from google.generativeai.files import upload_file
from dotenv import load_dotenv
import json
import os
from retry import retry

# TODO Configure necessary permissions for image access on Android (AndroidManifest.xml) and iOS (Info.plist)

load_dotenv()

genai.configure(api_key=os.environ['API_KEY'])
model = genai.GenerativeModel("gemini-1.5-flash")

# Extracts JSON data from Gemini's response. 
def parse_response(response):
    json_text = response._result.candidates[0].content.parts[0].text

    # Remove code block formatting
    if json_text.startswith("```json"):
        json_text = json_text[7:]
    if json_text.endswith("```"):
        json_text = json_text[:-3]

    # Load cleaned JSON string into dictionary
    try:
        json_data = json.loads(json_text)
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)

    return json_data

# Upload image to Gemini, get a response back
@retry((Exception), tries=3, delay=0, backoff=0)
def get_recipe_info(file_path):
    myimage = genai.upload_file(file_path)
    prompt = [myimage, "\n\n", """Identify all ingredients in the image and list three recipes you can make with them in JSON format.
            
    Use this JSON schema:
    {
        All ingredients: list(str)
        Recipes: [
            {'recipe name': str, 'ingredients': list[str], 'instructions': list(str)}
        ]
    }

    Return: list[Ingredients, Recipe]"""]

    response = model.generate_content(prompt)
    parsed_response = parse_response(response)

    return parsed_response
    
gemini_response = get_recipe_info('test_image_text.png')


