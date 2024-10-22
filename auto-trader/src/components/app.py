from flask import Flask, jsonify, request
from flask_cors import CORS
import yfinance as yf

import pandas as pd
import matplotlib
matplotlib.use('Agg')
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
    plt.gca().xaxis.set_major_locator(MaxNLocator(nbins=10))  # Limit the number of x-axis labels
    plt.xticks(rotation=45)  # Rotate date labels
    plt.tight_layout()  

    # Save to a BytesIO object and encode it
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    return jsonify({'image': img_base64})

@app.route('/api/stock/', methods=['POST'])
def get_stock_data():
    
    try:
        data = request.json
        symbol = data.get('symbol')
        start_date = data.get('start')
        end_date = data.get('end')
        print(start_date)
        print(end_date)
        ETF = yf.Ticker(symbol)

        if(end_date == "none"):
            data = ETF.history(start=start_date, actions=False)
        else:
            data = ETF.history(start=start_date, end=end_date, actions=False)

        
        data.index = data.index.strftime('%Y-%m-%d')
        history_dict = data.to_dict(orient='index')
        return plot(history_dict=history_dict, symbol=symbol)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/sma', methods=['POST'])
def get_sma():


    try:


        data = request.json
        symbol = data.get('symbol')
        ETF = yf.Ticker(symbol)
        data = ETF.history(period='1y', actions=False)
        data.index = data.index.strftime('%Y-%m-%d')
        history_dict = data.to_dict(orient='index')
        print(history_dict)



        return jsonify({'sma': 'data'})
    

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
    app.run(host='0.0.0.0', port=3000)
