from flask import Flask, jsonify, request
from flask_cors import CORS
import yfinance as yf

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)




# Example endpoint to return some data
@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({'message': 'Hello from Python!'})

# Example endpoint that accepts POST requests
@app.route('/api/echo', methods=['POST'])
def echo():
    data = request.json  # Get JSON data from request
    return jsonify({'you_sent': data})

@app.route('/api/stock/<symbol>', methods=['GET'])
def get_stock_data(symbol):
    try:
        ETF = yf.Ticker(symbol)
        data = ETF.info

        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
