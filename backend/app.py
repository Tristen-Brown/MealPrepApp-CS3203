from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This enables CORS, allowing your Flutter app to make requests

# TODO Write function that converts Gemini response to JSON to send to Flutter

@app.route('/hello', methods=['GET'])
def hello():
    return jsonify(message="Hello from Flask!")

# Example POST endpoint
@app.route('/data', methods=['POST'])
def receive_data():
    data = request.get_json()
    # Process data here (e.g., save to database, perform calculations)
    return jsonify(status="success", received_data=data)

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
