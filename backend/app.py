# from flask import Flask, jsonify, request

# app = Flask(__name__)

# @app.route('/')
# def hello():
#     return jsonify(message="Hello from Flask!")

# @app.route('/data', methods=['POST'])
# def receive_data():
#     data = request.get_json()
#     return jsonify(status="success", received_data=data)

# @app.route('/meal_recommendation', methods=['POST'])
# def meal_recommendation():
#     """
#     Accepts user preferences or restrictions and recommends meals.
#     """
#     data = request.get_json()
#     preferred_ingredients = data.get('ingredients', [])
#     # Mock recipe data (replace with a database or API call)
#     recipes = [
#         {'name': 'Grilled Chicken Salad', 'ingredients': ['Chicken', 'Lettuce', 'Tomatoes']},
#         {'name': 'Vegetarian Stir Fry', 'ingredients': ['Broccoli', 'Carrots', 'Tofu']},
#         {'name': 'Beef Tacos', 'ingredients': ['Beef', 'Tortillas', 'Cheese']},
#     ]
#     # Filter recipes based on preferred ingredients
#     recommendations = [
#         recipe for recipe in recipes if any(ingredient in preferred_ingredients for ingredient in recipe['ingredients'])
#     ]
#     return jsonify(recommendations=recommendations)

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
import os
import utils.scan_image as scan_image
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def hello():
    return jsonify(message="Hello from Flask!")

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

if __name__ == '__main__':
    app.run(debug=True)



