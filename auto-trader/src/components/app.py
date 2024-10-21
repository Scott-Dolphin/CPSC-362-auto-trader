from flask import Flask, jsonify, request
from flask_cors import CORS
import yfinance as yf

import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from matplotlib.dates import DateFormatter
from matplotlib.ticker import MaxNLocator

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

def plot(history_dict, symbol):
    # Sample data
    dates = []
    opens = []
    closes = []
    highs = []
    lows = []
    for date, data in history_dict.items():
        if 'Open' in data:
            
            dates.append(date)
            opens.append(data['Open'])
            closes.append(data['Close'])
            highs.append(data['High'])
            lows.append(data['Low'])

    print(dates)
    print(opens)
    df = pd.DataFrame({
        'x': dates,
        'Open': opens,
        'Close': closes,
        'High': highs,
        'Low': lows
    })

    # Create a plot
    plt.figure()
    plt.plot(df['x'], df['Open'], label='Open')
    plt.plot(df['x'], df['Close'], label='Close')
    plt.plot(df['x'], df['High'], label='High')
    plt.plot(df['x'], df['Low'], label='Low')
    plt.title(f"{symbol} History")
    plt.legend()

    #plt.gca().xaxis.set_major_formatter(DateFormatter('%Y-%m'))
    plt.gca().xaxis.set_major_locator(MaxNLocator(nbins=6))  # Limit the number of x-axis labels
    plt.xticks(rotation=45)  # Rotate date labels
    plt.tight_layout()  

    # Save to a BytesIO object and encode it
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    return jsonify({'image': img_base64})

@app.route('/api/stock/<symbol>', methods=['GET'])
def get_stock_data(symbol):
    try:
        ETF = yf.Ticker(symbol)
        data = ETF.history(start="2021-01-01", actions=False)
        data.index = data.index.strftime('%Y-%m-%d')
        history_dict = data.to_dict(orient='index')
        return plot(history_dict=history_dict, symbol=symbol)
    except Exception as e:
        return jsonify({'error': str(e)}), 500





# Example endpoint to return some data
@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({'message': 'Hello from Python!'})

# Example endpoint that accepts POST requests
@app.route('/api/echo', methods=['POST'])
def echo():
    data = request.json  # Get JSON data from request
    return jsonify({'you_sent': data})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
