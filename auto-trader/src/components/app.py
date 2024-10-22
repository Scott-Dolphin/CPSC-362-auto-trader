from flask import Flask, jsonify, request
from flask_cors import CORS
import yfinance as yf
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
from io import BytesIO, StringIO
import json
from matplotlib.ticker import MaxNLocator

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Set maximum request size to 16 MB

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

# endpoint that takes a json file or time range

@app.route('/api/stock/json/', methods=['POST'])
def plot_json():
    try:
        data = request.json
        symbol = data.get('symbol')
        file_content = data.get('file')
        return plot(history_dict=file_content, symbol=symbol)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


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
            df = ETF.history(start=start_date, actions=False)
        else:
            df = ETF.history(start=start_date, end=end_date, actions=False)

        
        df.index = df.index.strftime('%Y-%m-%d')
        history_dict = df.to_dict(orient='index')
        return plot(history_dict=history_dict, symbol=symbol)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

# sma endpoint
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



# endpoint that 
@app.route('/api/stock/<symbol>', methods=['GET'])
def get_download(symbol):
    ETF = yf.Ticker(symbol)
    data = ETF.history(start='2021-01-01', actions=False)
    data.index = data.index.strftime('%Y-%m-%d')
    history_dict = data.to_dict(orient='index')

    return jsonify(history_dict)

# Example endpoint that accepts POST requests
@app.route('/api/echo', methods=['POST'])
def echo():
    data = request.json
    return jsonify({'you_sent': data})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
