import yfinance as yf

def get_stock_history(symbol, start_date=None, end_date=None, period=None):
    ETF = yf.Ticker(symbol)
    if period:
        return ETF.history(period=period, actions=False)
    elif start_date and end_date:
        return ETF.history(start=start_date, end=end_date, actions=False)
    elif start_date:
        return ETF.history(start=start_date, actions=False)
    else:
        raise ValueError("Either period or start_date must be provided")

def get_stock_real_data(symbol):
    ETF = yf.Ticker(symbol)
    day_price = round(ETF.history(period="1d")['Close'].iloc[0], 2)
    week_price = round(ETF.history(period="5d")['Close'].iloc[0], 2)
    return day_price, week_price