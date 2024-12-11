from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import yfinance as yf
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
import os
from io import BytesIO, StringIO
import json
from matplotlib.ticker import MaxNLocator
import csv
from datetime import datetime
from functools import wraps
from flask import request, jsonify

from dataModel import get_stock_history, get_stock_real_data
from calc import *


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Set maximum request size to 16 MB

CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

@app.route('/api/stock/', methods=['POST'])
def get_stock_history_plot():
    try:
        data = request.json
        symbol = data.get('symbol')
        start_date = data.get('start')
        end_date = data.get('end')
        period = data.get('period', '1d')  # Default period to '1d' if not provided


        history = get_stock_history(symbol, start_date=start_date, end_date=end_date)
        print(history)
        image = plot(history, symbol)

        return jsonify(image)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/sma_crossover_plot', methods=['POST'])
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



def get_stock_real_data(symbol):
    #stock = StockModel(symbol)
    #day_price = stock.get_day_price()
    #week_price = stock.get_week_price()
    #rate_of_change = stock.get_rate_of_change()
    #return {'day_price': day_price, 'week_price': week_price, 'rate_of_change': rate_of_change}
    pass


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=3000)
