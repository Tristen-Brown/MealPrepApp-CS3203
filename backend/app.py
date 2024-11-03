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

if __name__ == '__main__':
    app.run(debug=True)
