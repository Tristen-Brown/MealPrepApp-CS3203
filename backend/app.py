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

if __name__ == '__main__':
    app.run(debug=True)
