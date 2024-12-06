from flask import Flask, jsonify, request
from dotenv import load_dotenv
import google.generativeai as genai
import os
import json
from retry import retry
from flask_cors import CORS
from werkzeug.utils import secure_filename
import utils.scan_image as scan_image
import re

# Load environment variables from the specified file
load_dotenv(dotenv_path="api.env")

# Get the API key from the environment variables
genai_api_key = os.getenv("API_KEY")

# Ensure the API key is loaded
if not genai_api_key:
    raise ValueError("API_KEY is missing in api.env")

app = Flask(__name__)

# Configure Generative AI
genai.configure(api_key=os.environ['API_KEY'])
model = genai.GenerativeModel("gemini-1.5-flash")
CORS(app)

UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image part in the request"}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({"error": "No selected image"}), 400

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # Create folder if it doesn't exist
        file.save(file_path)

        # Call your identify_ingredients function
        try:
            ingredients = scan_image.identify_ingredients(file_path)
            return jsonify({"ingredients": ingredients})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
def parse_response(response):
    try:
        # Assuming the AI response contains a text field in JSON format
        json_text = response._result.candidates[0].content.parts[0].text

        # Use regex to find the first valid JSON block in the response
        json_matches = re.findall(r'\{.*?\}', json_text, re.DOTALL)
        if not json_matches:
            raise ValueError("No valid JSON object found in the response")

        # Take the first match which is assumed to be the correct JSON
        json_text = json_matches[0]

        # Convert to dictionary
        return json.loads(json_text)
    except (AttributeError, IndexError) as e:
        print(f"Error accessing response attributes: {e}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return {}
    except ValueError as e:
        print(f"Error finding JSON: {e}")
        return {}


@app.route('/recipe_generation', methods=['POST'])
def generate_recipes():
    """
    Accepts user ingredients and generates recipe suggestions using Google Gemini AI.
    """
    data = request.get_json()
    ingredients = data.get('ingredients', [])

    if not ingredients:
        response = jsonify({"error": "No ingredients provided", "recipe": []})
        app.logger.debug(f"Response: {response.get_json()}")
        return response, 400

    # Build the AI prompt
    prompt = [
        """
        With the list of given ingredients below, generate three recipe suggestions. 
        The recipe should include:
        - Recipe name
        - Required ingredients
        - Step-by-step instructions
        Format the output in JSON as follows:

        {{"recipe name": "Recipe 1", "ingredients": ["ingredient1", "ingredient2"], "instructions": ["Step 1", "Step 2"]}, {"recipe name": "Recipe 1", "ingredients": ["ingredient1", "ingredient2"], "instructions": ["Step 1", "Step 2"]}, {"recipe name": "Recipe 1", "ingredients": ["ingredient1", "ingredient2"], "instructions": ["Step 1", "Step 2"]}}
        """
    ]

    # Add ingredients to the prompt
    prompt += [f"{ingredient}\n" for ingredient in ingredients]

    try:
        # Generate response from Gemini AI
        response = model.generate_content(prompt)
        recipe_data = parse_response(response)

        # Log the parsed recipe data to see what is received
        app.logger.debug(f"Parsed recipe data: {recipe_data}")

        # Validate the recipe data more carefully
        if recipe_data and isinstance(recipe_data, dict) and "recipe name" in recipe_data and "ingredients" in recipe_data and "instructions" in recipe_data:
            # If the parsed recipe data is valid, return it
            result = jsonify({"recipe": [recipe_data]})
        else:
            # If parsing fails or response is incomplete, return an empty list
            app.logger.debug("Invalid recipe data from AI")
            result = jsonify({"recipe": []})

        app.logger.debug(f"Final Response: {result.get_json()}")
        return result
    except Exception as e:
        print(f"Error generating recipes: {e}")
        return jsonify({"error": "Failed to generate recipes", "recipe": []}), 500

MAX_RESTRICTION_LENGTH = 10  # Allow max 10 restrictions

class DietaryRestrictions:
    def __init__(self):
        # List of valid dietary restrictions
        self.valid_restrictions = ["vegan", "gluten-free", "dairy-free", "keto", "paleo", "nut-free"]

    def validate_restrictions(self, restrictions):
        # Split and strip input restrictions by commas
        restriction_list = [r.strip() for r in restrictions.split(",")]

        # Check that all input restrictions are valid
        for r in restriction_list:
            if r not in self.valid_restrictions:
                return False
        
        # Check if there are more than the allowed maximum restrictions
        return len(restriction_list) <= MAX_RESTRICTION_LENGTH

# Route to validate dietary restrictions
@app.route('/validate_dietary_restrictions', methods=['POST'])
def validate_dietary_restrictions():
    data = request.get_json()  # Expecting JSON with dietary restrictions
    restrictions = data.get('restrictions', "")

    # Initialize the DietaryRestrictions class
    dietary_restrictions = DietaryRestrictions()

    # Validate the restrictions
    is_valid = dietary_restrictions.validate_restrictions(restrictions)

    if is_valid:
        return jsonify({"status": "success", "message": "Valid dietary restrictions"})
    else:
        return jsonify({"status": "error", "message": "Invalid dietary restrictions or too many restrictions"})

MAX_MEALS_PER_DAY = 3
MAX_EATING_OUT_DAYS = 1

def validate_meal_plan(meal_plan):
    eating_out_count = sum(1 for meals in meal_plan if meals == 0)
    if eating_out_count > MAX_EATING_OUT_DAYS:
        return False, "Too many eating out days. Only one is allowed."
    if any(meals != 0 and not (2 <= meals <= MAX_MEALS_PER_DAY) for meals in meal_plan):
        return False, "Invalid meal selection. Meals per day must be 2 or 3 (or 0 for eating out)."
    return True, "Valid meal plan."

@app.route('/validate_meal_plan', methods=['POST'])
def validate_meal_plan_api():
    data = request.get_json()
    meal_plan = data.get('meal_plan', [])
    if not meal_plan or len(meal_plan) != 7:
        return jsonify(success=False, message="Invalid input. Provide meal plan for 7 days."), 400

    is_valid, message = validate_meal_plan(meal_plan)
    return jsonify(success=is_valid, message=message)


    


if __name__ == '__main__':
    app.run(debug=True)
