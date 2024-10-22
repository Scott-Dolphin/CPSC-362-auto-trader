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




# @app.route('/api/sma', methods=['POST'])
# def get_sma():


#     try:


#         data = request.json
#         symbol = data.get('symbol')
#         ETF = yf.Ticker(symbol)
#         data = ETF.history(period='1y', actions=False)
#         data.index = data.index.strftime('%Y-%m-%d')
#         history_dict = data.to_dict(orient='index')

#         print(history_dict)



#         return jsonify({'sma': 'data'})
    

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# gpt code v1 sma 
@app.route('/api/sma', methods=['POST'])
def get_sma():
    try:
        # Capture incoming request data
        data = request.json
        symbol = data.get('symbol')
        period = data.get('period', 50)  # Default to 50 if no period provided

        print("Received symbol:", symbol)
        print("Received period:", period)

        # Fetch stock data from Yahoo Finance
        ETF = yf.Ticker(symbol)
        stock_data = ETF.history(period='1y', actions=False)

        # Log the stock data for debugging
        print(stock_data.head())  # Log first few rows of the data

        # Check if the 'Close' column exists
        if 'Close' not in stock_data.columns:
            raise ValueError("The 'Close' column is missing from the stock data.")

        # Calculate SMA
        stock_data['SMA'] = stock_data['Close'].rolling(window=period).mean()

        # Format data for JSON response
        stock_data.index = stock_data.index.strftime('%Y-%m-%d')
        sma_dict = stock_data[['SMA']].dropna().to_dict(orient='index')  # Drop rows with NaN SMA

        # Return calculated SMA as JSON
        return jsonify({'sma': sma_dict})

    except Exception as e:
        # Print the error to the console for debugging
        print("Error in /api/sma:", str(e))
        return jsonify({'error': str(e)}), 500

# gpt code crossover
@app.route('/api/sma_crossover', methods=['POST'])
def sma_crossover():
    try:
        data = request.json
        symbol = data.get('symbol')
        short_period = data.get('short_period', 50)  # Default short-term period is 50
        long_period = data.get('long_period', 200)  # Default long-term period is 200

        ETF = yf.Ticker(symbol)
        stock_data = ETF.history(period='2y', actions=False)  # Fetch 2 years of data
        
        stock_data['SMA_short'] = stock_data['Close'].rolling(window=short_period).mean()
        stock_data['SMA_long'] = stock_data['Close'].rolling(window=long_period).mean()

        stock_data.index = stock_data.index.strftime('%Y-%m-%d')

        # Generate Buy/Sell signals
        signals = []
        position = 0  # Track current position (1 for holding, 0 for no position)
        for i in range(1, len(stock_data)):
            if stock_data['SMA_short'].iloc[i] > stock_data['SMA_long'].iloc[i] and position == 0:
                signals.append({'date': stock_data.index[i], 'action': 'buy', 'price': stock_data['Close'].iloc[i]})
                position = 1  # Enter a position (bought)
            elif stock_data['SMA_short'].iloc[i] < stock_data['SMA_long'].iloc[i] and position == 1:
                signals.append({'date': stock_data.index[i], 'action': 'sell', 'price': stock_data['Close'].iloc[i]})
                position = 0  # Exit the position (sold)

        return jsonify({'signals': signals})

    except Exception as e:
        print("Error in SMA Crossover:", str(e))
        return jsonify({'error': str(e)}), 500

# gpt code backtest
@app.route('/api/backtest', methods=['POST'])
def backtest():
    try:
        data = request.json
        signals = data.get('signals')
        initial_balance = 100000  # Starting balance
        balance = initial_balance
        shares = 0
        log = []

        for signal in signals:
            date = signal['date']
            price = signal['price']
            action = signal['action']

            if action == 'buy':
                shares = balance // price  # Buy as many shares as we can
                transaction_amount = shares * price
                balance -= transaction_amount
                log.append({'date': date, 'action': 'buy', 'price': price, 'shares': shares, 'balance': balance})

            elif action == 'sell' and shares > 0:
                transaction_amount = shares * price
                balance += transaction_amount
                gain = transaction_amount - (shares * log[-1]['price'])
                log.append({'date': date, 'action': 'sell', 'price': price, 'shares': shares, 'gain': gain, 'balance': balance})
                shares = 0  # Reset shares after selling

        total_gain = balance - initial_balance
        annual_return = (total_gain / initial_balance) * 100  # Simplified annual return

        return jsonify({'log': log, 'total_gain': total_gain, 'annual_return': annual_return})

    except Exception as e:
        print("Error in backtesting:", str(e))
        return jsonify({'error': str(e)}), 500

# gpt code log v1 works
# import csv

# @app.route('/api/backtest_log', methods=['POST'])
# def backtest_log():
#     try:
#         data = request.json
#         signals = data.get('signals')
#         log_filename = 'trade_log.csv'

#         # Open the CSV file and write the log
#         with open(log_filename, mode='w', newline='') as file:
#             writer = csv.writer(file)
#             writer.writerow(['Date', 'Action', 'Price', 'Shares', 'Balance', 'Gain/Loss'])

#             initial_balance = 100000
#             balance = initial_balance
#             shares = 0

#             for signal in signals:
#                 date = signal['date']
#                 price = signal['price']
#                 action = signal['action']

#                 if action == 'buy':
#                     shares = balance // price
#                     balance -= shares * price
#                     writer.writerow([date, action, price, shares, balance, ''])

#                 elif action == 'sell' and shares > 0:
#                     transaction_amount = shares * price
#                     gain = transaction_amount - (shares * signal['price'])
#                     balance += transaction_amount
#                     writer.writerow([date, action, price, shares, balance, gain])
#                     shares = 0

#         return jsonify({'message': f'Trade log saved as {log_filename}'})

#     except Exception as e:
#         print("Error writing to CSV:", str(e))
#         return jsonify({'error': str(e)}), 500

# gpt code log v2
import csv
from datetime import datetime

@app.route('/api/backtest_log', methods=['POST'])
def backtest_log():
    try:
        data = request.json
        signals = data.get('signals')
        log_filename = 'trade_log.csv'

        initial_balance = 100000  # Starting balance
        balance = initial_balance
        total_gain = 0  # Track total gain/loss
        total_shares = 0  # Track total shares held
        cost_basis = 0  # Track the total cost of shares bought
        today = datetime.now().strftime('%Y-%m-%d')

        # Get the symbol explicitly from the request
        symbol = data.get('symbol')
        if not symbol and signals:
            last_signal = signals[-1]
            symbol = last_signal.get('symbol', 'FNGU')  # Default to FNGU if missing

        # Ensure the symbol is uppercase (avoiding NoneType errors)
        if symbol:
            symbol = symbol.upper()
        else:
            raise ValueError('Symbol is missing or None')

        # Get today's price for the current symbol using yfinance
        ETF = yf.Ticker(symbol)
        todays_data = ETF.history(period='1d')  # Fetch the most recent price
        today_price = todays_data['Close'].values[0]  # Today's price (if shares remain)

        # Open the CSV file and write the log
        with open(log_filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Action', 'Price', 'Shares', 'Balance', 'Gain/Loss'])

            # Process each signal
            for signal in signals:
                date = signal['date']
                price = signal['price']
                action = signal['action']

                if action == 'buy':
                    shares = balance // price  # Buy as many shares as possible
                    transaction_amount = shares * price
                    balance -= transaction_amount
                    total_shares += shares
                    cost_basis += transaction_amount  # Track how much was spent on buying these shares
                    writer.writerow([date, action, price, shares, balance, ''])

                elif action == 'sell' and total_shares > 0:
                    transaction_amount = total_shares * price
                    gain = transaction_amount - cost_basis  # Gain is the proceeds minus the cost basis
                    balance += transaction_amount
                    total_gain += gain  # Add this to the total gain
                    writer.writerow([date, action, price, total_shares, balance, gain])
                    
                    # Reset total_shares and cost_basis after selling
                    total_shares = 0
                    cost_basis = 0

            # Force the sale of any remaining shares at today's price
            if total_shares > 0:
                transaction_amount = total_shares * today_price
                gain_per_trade = transaction_amount - cost_basis
                balance += transaction_amount
                total_gain += gain_per_trade  # Include this in the total gain
                writer.writerow([today, 'sell (forced)', today_price, total_shares, balance, gain_per_trade])

            # Calculate total % return and annual % return
            total_return_percentage = (balance - initial_balance) / initial_balance * 100
            annual_return = (total_return_percentage / 100) * (365 / len(signals))  # Simplified

            # Add a summary row at the end
            writer.writerow([])
            writer.writerow(['Summary'])
            writer.writerow(['Total Gain/Loss', f"${total_gain:.2f}"])
            writer.writerow(['Annual Return (%)', f"{annual_return:.2f}%"])
            writer.writerow(['Total Return (%)', f"{total_return_percentage:.2f}%"])
            writer.writerow(['Current Balance', f"${balance:.2f}"])

        return jsonify({'message': f'Trade log saved as {log_filename}'})

    except Exception as e:
        print("Error writing to CSV:", str(e))
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
