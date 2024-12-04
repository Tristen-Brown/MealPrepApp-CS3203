from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify(message="Hello from Flask!")

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.get_json()
    return jsonify(status="success", received_data=data)

@app.route('/meal_recommendation', methods=['POST'])
def meal_recommendation():
    """
    Accepts user preferences or restrictions and recommends meals.
    """
    data = request.get_json()
    preferred_ingredients = data.get('ingredients', [])
    # Mock recipe data (replace with a database or API call)
    recipes = [
        {'name': 'Grilled Chicken Salad', 'ingredients': ['Chicken', 'Lettuce', 'Tomatoes']},
        {'name': 'Vegetarian Stir Fry', 'ingredients': ['Broccoli', 'Carrots', 'Tofu']},
        {'name': 'Beef Tacos', 'ingredients': ['Beef', 'Tortillas', 'Cheese']},
    ]
    # Filter recipes based on preferred ingredients
    recommendations = [
        recipe for recipe in recipes if any(ingredient in preferred_ingredients for ingredient in recipe['ingredients'])
    ]
    return jsonify(recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)