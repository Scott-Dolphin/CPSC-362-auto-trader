from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)


# Example endpoint to return some data
@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({'message': 'Hello from Python!', 'number': 42})

# Example endpoint that accepts POST requests
@app.route('/api/echo', methods=['POST'])
def echo():
    data = request.json  # Get JSON data from request
    return jsonify({'you_sent': data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
