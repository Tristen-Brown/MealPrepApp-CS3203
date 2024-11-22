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

@retry((Exception), tries=3, delay=0, backoff=1)
def identify_ingredients(file_path):
    user_image = genai.upload_file(file_path)
    prompt = [user_image, "\n\n", """
        Identify all ingredients in the image. IMPORTANT: The output should be in JSON format.

        If some of the ingredients are unidentifiable, ignore them and only add what you can confidently identify.
        If there are no ingredients, just leave the ingredients list empty.
        
        Example output:
        
        {"ingredients": ["ingredient 1", "ingredient 2", "ingredient 3"]}
    """]

    model_response = model.generate_content(prompt)
    ingredients_list = parse_response(model_response)
    return ingredients_list

def generate_recipe_suggesetions(ingredients):
    prompt = ["""
        With the list of given ingredients below, generate three recipe suggestions. List all ingredients required for each recipe. Provide instructions.
        
        IMPORTANT: The output should be in JSON format.
              
        Example output:
              
        {"recipes": [{"recipe name": "Recipe 1 Name, "ingredients": ["ingredient 1", "ingredient 2", "ingredient 3"], "instructions": ["Step 1", "Step 2", "Step 3]},
            {"recipe name": "Recipe 2 Name, "ingredients": ["ingredient 1", "ingredient 2", "ingredient 3"], "instructions": ["Step 1", "Step 2", "Step 3]},
            {"recipe name": "Recipe 3 Name, "ingredients": ["ingredient 1", "ingredient 2", "ingredient 3"], "instructions": ["Step 1", "Step 2", "Step 3]}
        ]}\n\n
    """]

    for item in ingredients:
        prompt += f"{item}\n"

    model_response = model.generate_content(prompt)
    recipe_suggestions = parse_response(model_response)
    return recipe_suggestions

# ingredients = identify_ingredients("test_image2.jpg")
# recipes = generate_recipe_suggesetions(ingredients)
# print(recipes)
