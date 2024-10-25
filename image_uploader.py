import requests
import google.generativeai as genai
from google.generativeai.files import upload_file
from dotenv import load_dotenv
import json
import os

load_dotenv()

genai.configure(api_key=os.environ['API_KEY'])
# model = genai.GenerativeModel("gemini-1.5-flash", generation_config={"response_mime_type": "application/json"})
model = genai.GenerativeModel("gemini-1.5-flash")

def upload_image(file_path):
    myimage = genai.upload_file(file_path)
    prompt = [myimage, "\n\n", """Identify all ingredients in the image and list three recipes you make with them in JSON format. 
            
    Use this JSON schema:
    {
        All ingredients: list(str)
        Recipes: [
            {'recipe name': str, 'ingredients': list[str], 'instructions': str}
        ]
    }

    Return: list[Ingredients, Recipe]"""]

    response = model.generate_content(prompt)
    json_text = response._result.candidates[0].content.parts[0].text

    # Remove the code block formatting
    if json_text.startswith("```json"):
        json_text = json_text[7:]  # Remove the ```json\n at the beginning
    if json_text.endswith("```"):
        json_text = json_text[:-3]  # Remove the ``` at the end

    # Now, load the cleaned JSON string into a Python dictionary
    try:
        json_data = json.loads(json_text)
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)

    return json_data

text_response = upload_image('test_image2.jpg')
print(text_response)

# myimage = genai.upload_file('test_image2.jpg')
# prompt = [myimage, "\n\n", """Identify all ingredients in the image and list three recipes you make with them in JSON format. 
            
#     Use this JSON schema:
#     {
#         All ingredients: list(str)
#         Recipes: [
#             {'recipe name': str, 'ingredients': list[str], 'instructions': str}
#         ]
#     }

#     Return: list[Ingredients, Recipe]"""]
# response = model.generate_content(prompt)
# print(response)