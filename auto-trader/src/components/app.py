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

def plot_with_signals(stock_data, signals, symbol, title, additional_plots=None):
    """
    General-purpose function to plot stock data with buy/sell signals.

    Parameters:
    - stock_data: DataFrame containing stock data with a DateTime index.
    - signals: List of dictionaries containing 'date', 'action', and 'price'.
    - symbol: Stock symbol.
    - title: Title of the plot.
    - additional_plots: List of tuples containing (column_name, label, color) for additional plots.
    """
    try:
        plt.figure(figsize=(10, 5))  # Adjust the size to make the graph smaller

        # Plot the Close price line
        plt.plot(stock_data.index, stock_data['Close'], label='Close Price', color='blue')

        # Plot additional data if provided
        if additional_plots:
            for column_name, label, color in additional_plots:
                plt.plot(stock_data.index, stock_data[column_name], label=label, color=color)

        # Flags to track if the legend labels have been added
        buy_label_added = False
        sell_label_added = False

        # Plot buy/sell signals with larger and more distinct markers
        for signal in signals:
            if signal['action'] == 'buy':
                if not buy_label_added:
                    plt.scatter(signal['date'], signal['price'], marker='^', color='green', label='Buy Signal', s=200, edgecolors='black', alpha=1)
                    buy_label_added = True
                else:
                    plt.scatter(signal['date'], signal['price'], marker='^', color='green', s=200, edgecolors='black', alpha=1)
            elif signal['action'] == 'sell':
                if not sell_label_added:
                    plt.scatter(signal['date'], signal['price'], marker='v', color='red', label='Sell Signal', s=200, edgecolors='black', alpha=1)
                    sell_label_added = True
                else:
                    plt.scatter(signal['date'], signal['price'], marker='v', color='red', s=200, edgecolors='black', alpha=1)

        plt.title(title)
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.grid()

        # Save the plot to a BytesIO object
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()
        return buf

    except Exception as e:
        print(f"Error in plot_with_signals: {str(e)}")
        raise


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

# endpoint that takes a json file or time range

@app.route('/api/stock/json/', methods=['POST'])
@log_request_response
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
    
@app.route('/api/stock/real/<symbol>', methods=['GET'])
def get_stock_real_data(symbol):

    ETF = yf.Ticker(symbol)
    day_price = round(ETF.history(period="1d")['Close'].iloc[0], 2)
    week_price = round(ETF.history(period="5d")['Close'].iloc[0], 2)
    rate_of_change = round((day_price - week_price) / (4), 2)

    return jsonify({'day_price': day_price, 'week_price': week_price, 'rate_of_change': rate_of_change})


# endpoint that 
@app.route('/api/stock/<symbol>', methods=['GET'])
@log_request_response
def get_download(symbol):
    ETF = yf.Ticker(symbol)
    data = ETF.history(start='2021-01-01', actions=False)
    data.index = data.index.strftime('%Y-%m-%d')
    history_dict = data.to_dict(orient='index')

    return jsonify(history_dict)


@app.route('/api/sma_crossover_plot', methods=['POST'])
@log_request_response
def sma_crossover_plot():
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
        ETF = yf.Ticker(symbol)
        stock_data = ETF.history(period='2y', actions=False)

        if len(stock_data) < long_period:
            raise ValueError("Not enough data to calculate the long-period SMA.")

        stock_data['SMA_short'] = stock_data['Close'].rolling(window=short_period).mean()
        stock_data['SMA_long'] = stock_data['Close'].rolling(window=long_period).mean()
        stock_data = stock_data.dropna()
        stock_data.index = stock_data.index.strftime('%Y-%m-%d')

        # Generate Buy/Sell signals
        signals = []
        position = 0
        for i in range(1, len(stock_data)):
            if (stock_data['SMA_short'].iloc[i] > stock_data['SMA_long'].iloc[i] and
                stock_data['SMA_short'].iloc[i - 1] <= stock_data['SMA_long'].iloc[i - 1] and
                position == 0):
                signals.append({'date': stock_data.index[i], 'action': 'buy', 'price': stock_data['Close'].iloc[i]})
                position = 1
            elif (stock_data['SMA_short'].iloc[i] < stock_data['SMA_long'].iloc[i] and
                  stock_data['SMA_short'].iloc[i - 1] >= stock_data['SMA_long'].iloc[i - 1] and
                  position == 1):
                signals.append({'date': stock_data.index[i], 'action': 'sell', 'price': stock_data['Close'].iloc[i]})
                position = 0

        # Force a sell if a position remains at the end
        if position == 1:
            last_date = stock_data.index[-1]
            last_price = stock_data['Close'].iloc[-1]
            signals.append({'date': last_date, 'action': 'sell', 'price': last_price})
            position = 0

        # Plot the data with signals
        buf = plot_with_signals(stock_data, signals, symbol, f'{symbol} Price with SMA Crossover Signals')

        # Encode the image in base64
        img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')

        return jsonify({'signals': signals, 'image': img_base64})

    except Exception as e:
        app.logger.error(f"Error in SMA Crossover Plot: {str(e)}")
        return jsonify({'error': str(e)}), 500
# backtest
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
        annual_return = (total_gain / initial_balance) * 100  # annual return

        return jsonify({'log': log, 'total_gain': total_gain, 'annual_return': annual_return})

    except Exception as e:
        print("Error in backtesting:", str(e))
        return jsonify({'error': str(e)}), 500

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

# Backtesting and logging helper function (for BB and macd)
def run_backtest_and_log(signals, strategy_name):
    initial_balance = 100000
    balance = initial_balance
    log = []
    total_gain = 0

    shares = 0

    for signal in signals:
        date = signal['date']
        price = signal['price']
        action = signal['action']

        if action == 'buy':
            shares = balance // price
            transaction_amount = shares * price
            balance -= transaction_amount
            log.append({'date': date, 'action': 'buy', 'price': price, 'shares': shares, 'balance': balance})

        elif action == 'sell' and shares > 0:
            transaction_amount = shares * price
            balance += transaction_amount
            gain = transaction_amount - (shares * log[-1]['price'])
            log.append({'date': date, 'action': 'sell', 'price': price, 'shares': shares, 'gain': gain, 'balance': balance})
            shares = 0

    total_gain = balance - initial_balance
    annual_return = (total_gain / initial_balance) * 100
    return jsonify({'log': log, 'total_gain': total_gain, 'annual_return': annual_return})


# Example usage in a trading strategy function for Bollinger Bands
@app.route('/api/bollinger_bands_plot', methods=['POST'])
def bollinger_bands_plot():
    try:
        data = request.json
        symbol = data.get('symbol')
        sma_period = data.get('sma_period', 20)
        std_dev_multiplier = data.get('std_dev_multiplier', 2)

        if not symbol:
            raise ValueError('Symbol is missing or None')

        symbol = symbol.upper()

        # Fetch historical data and calculate Bollinger Bands
        ETF = yf.Ticker(symbol)
        stock_data = ETF.history(period='2y', actions=False)

        stock_data['SMA'] = stock_data['Close'].rolling(window=sma_period).mean()
        stock_data['Upper Band'] = stock_data['SMA'] + (stock_data['Close'].rolling(window=sma_period).std() * std_dev_multiplier)
        stock_data['Lower Band'] = stock_data['SMA'] - (stock_data['Close'].rolling(window=sma_period).std() * std_dev_multiplier)
        stock_data = stock_data.dropna()
        stock_data.index = stock_data.index.strftime('%Y-%m-%d')

        # Generate Buy/Sell signals based on Bollinger Bands
        signals = []
        position = 0
        for i in range(1, len(stock_data)):
            if stock_data['Close'].iloc[i] < stock_data['Lower Band'].iloc[i] and position == 0:
                signals.append({'date': stock_data.index[i], 'action': 'buy', 'price': stock_data['Close'].iloc[i]})
                position = 1
            elif stock_data['Close'].iloc[i] > stock_data['Upper Band'].iloc[i] and position == 1:
                signals.append({'date': stock_data.index[i], 'action': 'sell', 'price': stock_data['Close'].iloc[i]})
                position = 0

        # Force a sell if a position remains at the end
        if position == 1:
            last_date = stock_data.index[-1]
            last_price = stock_data['Close'].iloc[-1]
            signals.append({'date': last_date, 'action': 'sell', 'price': last_price})
            position = 0

        # Plot the data with signals
        additional_plots = [
        ]
        buf = plot_with_signals(stock_data, signals, symbol, f'{symbol} Price with Bollinger Bands Signals', additional_plots)

        # Encode the image in base64
        img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')

        return jsonify({'signals': signals, 'image': img_base64})

    except Exception as e:
        app.logger.error(f"Error in Bollinger Bands Plot: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Backtest for Bollinger Bands
@app.route('/api/bb_backtest', methods=['POST'])
def bb_backtest():
    try:
        data = request.json
        signals = data.get('signals')
        return run_backtest_and_log(signals, 'BB')
    except Exception as e:
        print(f"Error in BB backtest: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/macd_plot', methods=['POST'])
def macd_plot():
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
        ETF = yf.Ticker(symbol)
        stock_data = ETF.history(period='2y', actions=False)

        stock_data['EMA_short'] = stock_data['Close'].ewm(span=short_period, adjust=False).mean()
        stock_data['EMA_long'] = stock_data['Close'].ewm(span=long_period, adjust=False).mean()
        stock_data['MACD'] = stock_data['EMA_short'] - stock_data['EMA_long']
        stock_data['Signal Line'] = stock_data['MACD'].ewm(span=signal_period, adjust=False).mean()
        stock_data = stock_data.dropna()
        stock_data.index = stock_data.index.strftime('%Y-%m-%d')

        # Generate Buy/Sell signals based on MACD
        signals = []
        position = 0
        for i in range(1, len(stock_data)):
            if stock_data['MACD'].iloc[i] > stock_data['Signal Line'].iloc[i] and stock_data['MACD'].iloc[i - 1] <= stock_data['Signal Line'].iloc[i - 1] and position == 0:
                signals.append({'date': stock_data.index[i], 'action': 'buy', 'price': stock_data['Close'].iloc[i]})
                position = 1
            elif stock_data['MACD'].iloc[i] < stock_data['Signal Line'].iloc[i] and stock_data['MACD'].iloc[i - 1] >= stock_data['Signal Line'].iloc[i - 1] and position == 1:
                signals.append({'date': stock_data.index[i], 'action': 'sell', 'price': stock_data['Close'].iloc[i]})
                position = 0

        # Force a sell if a position remains at the end
        if position == 1:
            last_date = stock_data.index[-1]
            last_price = stock_data['Close'].iloc[-1]
            signals.append({'date': last_date, 'action': 'sell', 'price': last_price})
            position = 0

        # Plot the data with signals
        additional_plots = [
        ]
        buf = plot_with_signals(stock_data, signals, symbol, f'{symbol} Price with MACD Signals', additional_plots)

        # Encode the image in base64
        img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')

        return jsonify({'signals': signals, 'image': img_base64})

    except Exception as e:
        app.logger.error(f"Error in MACD Plot: {str(e)}")
        return jsonify({'error': str(e)}), 500


# Backtest for MACD
@app.route('/api/macd_backtest', methods=['POST'])
def macd_backtest():
    try:
        data = request.json
        signals = data.get('signals')
        return run_backtest_and_log(signals, 'MACD')
    except Exception as e:
        print(f"Error in MACD backtest: {e}")
        return jsonify({'error': str(e)}), 500


# Example endpoint that accepts POST requests
@app.route('/api/echo', methods=['POST'])
def echo():
    data = request.json
    return jsonify({'you_sent': data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
