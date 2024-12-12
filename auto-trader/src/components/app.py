from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import random
import threading
import time
from functools import wraps
from flask import request, jsonify
from flask_socketio import SocketIO, emit
from dataModel import get_stock_history, get_stock_real_data
from calc import *


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Set maximum request size to 16 MB
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

global_symbol = None

def log_request_response(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Log the request
        app.logger.info(f"Request: {request.method} {request.url}")
        app.logger.info(f"Request data: {request.get_json()}")

        # Call the original function
        response = f(*args, **kwargs)

        # Log the response
        app.logger.info(f"Response: {response.status_code}")
        
        return response
    return decorated_function


def send_realtime_update(today, five_day, rate_of_change):
    if today is not None and five_day is not None and rate_of_change is not None:
        data = {
            'today': today,
            'five_day': five_day,
            'rate_of_change': rate_of_change
        }
        socketio.emit('realtime_update', data)
    else:
        print("Error: 'today' or 'five_day' is None")

def background_thread():
    while True:
        if global_symbol:
            today, five_day = get_stock_real_data(global_symbol)
            rate_of_change = round((today - five_day) / (4), 2)
            print('Emitting updates')
            today = random.randint(100, 200)
            rate_of_change = random.randint(100, 200)
            five_day = random.randint(100, 200)
            send_realtime_update(today, five_day, rate_of_change)
        time.sleep(1)  # Emit updates every 5 seconds

@app.route('/api/symbol/', methods=['PUT'])
def api():
    global global_symbol
    data = request.json
    global_symbol = data.get('symbol')
    return jsonify({'message': f'Symbol set to {global_symbol}'})


@app.route('/api/stock/', methods=['POST'])
def get_stock_history_plot():
    try:
        data = request.json
        symbol = data.get('symbol')
        start_date = data.get('start')
        end_date = data.get('end')
        period = data.get('period', '1d')  # Default period to '1d' if not provided

        history = get_stock_history(symbol, start_date=start_date, end_date=end_date)
        image = plot(history, symbol)

        return jsonify(image)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/sma_crossover_plot', methods=['POST'])
@log_request_response
def sma_crossover():
    try:
        data = request.json
        symbol = data.get('symbol')
        short_period = data.get('short_period', 50)
        long_period = data.get('long_period', 200)

        if not symbol:
            raise ValueError('Symbol is missing or None')
        if short_period >= long_period:
            raise ValueError("Short period must be less than long period.")

        symbol = symbol.upper()

        # Fetch historical data and calculate SMAs
        stock_data = get_stock_history(symbol, period='2y')

        return sma_crossover_plot(stock_data, short_period, long_period, symbol)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/bollinger_bands_plot', methods=['POST'])
@log_request_response
def bollinger_bands():
    try:
        data = request.json
        symbol = data.get('symbol')
        period = data.get('sma_period', 20)
        num_std = data.get('std_dev_multiplier', 2)

        if not symbol:
            raise ValueError('Symbol is missing or None')

        symbol = symbol.upper()

        # Fetch historical data and calculate Bollinger Bands
        stock_data = get_stock_history(symbol, period='2y')

        return bollinger_bands_plot(stock_data, period, num_std, symbol)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/api/macd_plot', methods=['POST'])
@log_request_response
def macd():
    try:
        data = request.json
        symbol = data.get('symbol')
        short_period = data.get('short_period', 12)
        long_period = data.get('long_period', 26)
        signal_period = data.get('signal_period', 9)

        if not symbol:
            raise ValueError('Symbol is missing or None')

        symbol = symbol.upper()

        # Fetch historical data and calculate MACD
        stock_data = get_stock_history(symbol, period='2y')
        return macd_plot(stock_data, short_period, long_period, signal_period, symbol)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/backtest', methods=['POST'])
def api_backtest():
    try:
        data = request.json
        signals = data.get('signals')
        return(backtest(signals))
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/backtest_log', methods=['POST'])
def api_backtest_log():
    try:
        data = request.json
        symbol = data.get('symbol')
        signals = data.get('signals')
        if not symbol and signals:
            last_signal = signals[-1]
            symbol = last_signal.get('symbol', 'FNGU')  # Default to FNGU if missing

        # Ensure the symbol is uppercase (avoiding NoneType errors)
        if symbol:
            symbol = symbol.upper()
        else:
            raise ValueError('Symbol is missing or None')
        
        todays_data = get_stock_history(symbol, period='1d')
        filename = symbol + '_backtest_log.csv'
        return(backtest_log(todays_data, signals, log_filename=filename))
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def log_request_response(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Log the request
        app.logger.info(f"Request: {request.method} {request.url}")
        app.logger.info(f"Request data: {request.get_json()}")

        # Call the original function
        response = f(*args, **kwargs)

        # Log the response
        app.logger.info(f"Response: {response.status_code} {response.get_json()}")
        print(f"Response: {response.status_code} {request.method} {request.url}")

        return response
    return decorated_function



@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    thread = threading.Thread(target=background_thread)
    thread.daemon = True
    thread.start()
    socketio.run(app, host='0.0.0.0', port=3000, debug=True)