import React, { useState } from 'react';

export default function MACD({ symbol }) {
    const [shortPeriod, setShortPeriod] = useState(12);  // Default short-term EMA period
    const [longPeriod, setLongPeriod] = useState(26);   // Default long-term EMA period
    const [signalPeriod, setSignalPeriod] = useState(9);  // Default signal period
    const [signals, setSignals] = useState(null);  // Buy/Sell signals
    const [backtestData, setBacktestData] = useState(null); // Backtesting results
    const [loading, setLoading] = useState(false);  // Loading state
    const [error, setError] = useState(null);  // Error state

    const calculateMACD = async () => {
        setLoading(true);
        setError(null);

        try {
            const response = await fetch('http://127.0.0.1:3000/api/macd', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    symbol: symbol, 
                    short_ema_period: shortPeriod, 
                    long_ema_period: longPeriod, 
                    signal_period: signalPeriod 
                }),
            });

            const data = await response.json();
            if (data.signals) {
                setSignals(data.signals);
            } else {
                setSignals(null);  // Handle case where there are no signals
            }
        } catch (error) {
            console.error('Error calculating MACD:', error);
            setError('Failed to calculate MACD. Please try again.');
        }

        setLoading(false);
    };

    const runBacktest = async () => {
        setLoading(true);
        setError(null);

        try {
            const response = await fetch('http://127.0.0.1:3000/api/backtest', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ signals: signals }),
            });

            const data = await response.json();
            setBacktestData(data);
        } catch (error) {
            console.error('Error running backtest:', error);
            setError('Failed to backtest the strategy. Please try again.');
        }

        setLoading(false);
    };

    const logTrades = async () => {
        setLoading(true);
        setError(null);

        try {
            const response = await fetch('http://127.0.0.1:3000/api/backtest_log', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ signals: signals }),
            });

            const data = await response.json();
            alert(data.message);  // Show alert with confirmation
        } catch (error) {
            console.error('Error logging trades:', error);
            setError('Failed to log trades. Please try again.');
        }

        setLoading(false);
    };

    return (
        <div className="strategy-container">
            <h3>MACD Strategy for {symbol}</h3>

            {/* Input fields for the short-term and long-term EMA periods */}
            <label className="period-label">
                Short EMA Period:
                <input 
                    className="period-input"
                    type="number"
                    value={shortPeriod}
                    onChange={(e) => setShortPeriod(Number(e.target.value))}
                    min="1"
                />
            </label>

            <label className="period-label">
                Long EMA Period:
                <input
                    className="period-input"
                    type="number"
                    value={longPeriod}
                    onChange={(e) => setLongPeriod(Number(e.target.value))}
                    min="1"
                />
            </label>

            <label className="period-label">
                Signal Period:
                <input
                    className="period-input"
                    type="number"
                    value={signalPeriod}
                    onChange={(e) => setSignalPeriod(Number(e.target.value))}
                    min="1"
                />
            </label>

            <div className="button-container">
                <button className="calculate-btn" onClick={calculateMACD}>Calculate MACD</button>

                {signals && (
                    <div>
                        <button className="backtest-btn" onClick={runBacktest}>Run Backtest</button>
                        <button className="log-btn" onClick={logTrades}>Log Trades to CSV</button>
                    </div>
                )}
            </div>

            {loading ? <p>Loading...</p> : null}
            {error ? <p style={{ color: 'red' }}>{error}</p> : null}

            {signals ? (
                <div>
                    <h4>Signals:</h4>
                    <ul className="signal-list">
                        {signals.map((signal, index) => (
                            <li key={index} className="signal-item">
                                {signal.date}: {signal.action} at {signal.price}
                            </li>
                        ))}
                    </ul>
                </div>
            ) : null}

            {backtestData ? (
                <div>
                    <h4>Backtest Results:</h4>
                    <p>Total Gain: ${backtestData.total_gain.toFixed(2)}</p>
                    <p>Annual Return: {backtestData.annual_return.toFixed(2)}%</p>

                    <h4>Trade Log:</h4>
                    <ul className="trade-log">
                        {backtestData.log.map((entry, index) => (
                            <li key={index} className="trade-item">
                                {entry.date}: {entry.action} {entry.shares} shares at {entry.price}, Balance: ${entry.balance.toFixed(2)} {entry.gain ? `Gain/Loss: ${entry.gain.toFixed(2)}` : ''}
                            </li>
                        ))}
                    </ul>
                </div>
            ) : null}
        </div>
    );
}