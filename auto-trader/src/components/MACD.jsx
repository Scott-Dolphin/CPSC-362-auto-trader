import React, { useState } from 'react';
import { MACDAdapter } from './dataAdapters';

export default function MACD({ symbol }) {
    const [shortPeriod, setShortPeriod] = useState(20);  // Default short-term period
    const [longPeriod, setLongPeriod] = useState(40);   // Default long-term period
    const [signalPeriod, setSignalPeriod] = useState(9); // Default signal period
    const [signals, setSignals] = useState(null);        // Buy/Sell signals
    const [backtestData, setBacktestData] = useState(null); // Backtesting results
    const [loading, setLoading] = useState(false);       // Loading state
    const [error, setError] = useState(null);            // Error state
    const [graphUrl, setGraphUrl] = useState(null);      // URL for the graph image

    const adapter = new MACDAdapter();

    const calculateMACD = async () => {
        setLoading(true);
        setError(null);

        try {
            const data = await adapter.fetchData(symbol, { short_period: shortPeriod, long_period: longPeriod, signal_period: signalPeriod });
            if (data.signals) {
                setSignals(data.signals);
                const imageUrl = `data:image/png;base64,${data.image}`;
                setGraphUrl(imageUrl);
            } else {
                setSignals(null);
                setGraphUrl(null);
            }
        } catch (error) {
            console.error('Error fetching MACD data:', error);
            setError('Failed to fetch MACD signals and graph. Please try again.');
        }

        setLoading(false);
    };

    const runBacktest = async () => {
        setLoading(true);
        setError(null);

        try {
            const data = await adapter.runBacktest(signals);
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
            const data = await adapter.logTrades(signals);
            alert(data.message);  // Show alert with confirmation
        } catch (error) {
            console.error('Error logging trades:', error);
            setError('Failed to log trades. Please try again.');
        }

        setLoading(false);
    };

    return (
        <div className="sma-container">
            <h3>MACD Strategy for {symbol}</h3>

            {/* Input fields for the short-term, long-term, and signal periods */}
            <label className="period-label">
                Short Period:
                <input 
                    className="period-input"
                    type="number"
                    value={shortPeriod}
                    onChange={(e) => setShortPeriod(Number(e.target.value))}
                    min="1"
                />
            </label>

            <label className="period-label">
                Long Period:
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

            <div className="-content">
                <div className="-graph-signals">
                    {/* Display MACD signals */}
                    {signals ? (
                        <div className="sma-signals">
                            <h4>Signals:</h4>
                            <ul className="sma-list">
                                {signals.map((signal, index) => (
                                    <li key={index} className="sma-item">
                                        {signal.date}: {signal.action} at {signal.price}
                                    </li>
                                ))}
                            </ul>
                        </div>
                    ) : null}

                    {graphUrl ? (
                        <div className="sma-graph">
                            <h4>MACD Graph:</h4>
                            <img src={graphUrl} alt="MACD Graph" className="sma-graph-img" />
                        </div>
                    ) : null}
                </div>

                {backtestData ? (
                    <div className="backtest-results">
                        <h4>Backtest Results:</h4>
                        <p>Total Gain: ${backtestData.total_gain.toFixed(2)}</p>
                        <p>Annual Return: {backtestData.annual_return.toFixed(2)}%</p>

                        <h4>Trade Log:</h4>
                        <div className="trade-log-container">
                            <ul className="trade-log">
                                {backtestData.log.map((entry, index) => (
                                    <li key={index} className="trade-item">
                                        {entry.date}: {entry.action} {entry.shares} shares at {entry.price}, Balance: ${entry.balance.toFixed(2)} {entry.gain ? `Gain/Loss: ${entry.gain.toFixed(2)}` : ''}
                                    </li>
                                ))}
                            </ul>
                        </div>
                    </div>
                ) : null}
            </div>
        </div>
    );
}