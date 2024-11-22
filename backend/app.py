from flask import Flask, jsonify, request
from flask_cors import CORS
from utils.scan_image import identify_ingredients
import uuid

app = Flask(__name__)
CORS(app)  # This enables CORS, allowing your Flutter app to make requests

# Tests communication between Flutter and Flask
@app.route('/hello', methods=['GET'])
def hello():
    return jsonify(message="Hello from Flask!")

image_data = {}

# Get image from frontend. Process and return JSON response
@app.route('/api/images/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    image = request.files('image')
    ingredients = identify_ingredients(image)

    image_id = str(uuid.uuid4())
    image_data[image_id] = {
        'ingredients': ingredients,
        'recipes': None  # Placeholder until recipes are generated
    }

    return jsonify({'image_id': image_id, 'ingredients': ingredients}), 200

@app.route('/api/images/update-ingredients', methods=['POST'])
def update_ingredients():
    data = request.get_json()
    image_id = data.get('image_id')
    updated_ingredients = data.get('ingredients')

    if not image_id or not updated_ingredients:
        return jsonify({'error': 'Missing image_id or ingredients'}), 400
    
    if image_id in image_data:
        image_data[image_id]['ingredients'] = updated_ingredients
        return jsonify({'message': 'Ingredients updated successfully'}), 200
    else:
        return jsonify({'error': 'Image not found'}), 404

@app.route('/calculate_macros', methods=['POST'])
def calculate_macros():
    """
    Accepts ingredient data from the frontend, fetches nutrition details,
    and calculates total calories and macros.
    """
    data = request.get_json()  # Expecting JSON with ingredient details
    ingredients = data.get('ingredients', [])

    # Placeholder: Replace this with the API call to fetch nutrition info
    nutrition_data = fetch_nutrition_data(ingredients)  

    # Aggregate calories and macros
    total_calories = sum(item['calories'] for item in nutrition_data)
    total_protein = sum(item['protein'] for item in nutrition_data)
    total_fat = sum(item['fat'] for item in nutrition_data)
    total_carbs = sum(item['carbs'] for item in nutrition_data)

    result = {
        'calories': total_calories,
        'protein': total_protein,
        'fat': total_fat,
        'carbs': total_carbs,
    }

    return jsonify(result)

def fetch_nutrition_data(ingredients):
    """
    Mock function to fetch nutrition data for ingredients.
    Replace this with your actual API call logic.
    """
    # Example mock data
    return [
        {'calories': 200, 'protein': 10, 'fat': 5, 'carbs': 30}
        for _ in ingredients
    ]


if __name__ == '__main__':
    app.run(debug=True)
