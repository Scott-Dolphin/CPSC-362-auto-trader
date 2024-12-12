import React, { useState } from 'react';
import { BBAdapter } from './controller';
export default function BB({ symbol }) {
    const [period, setPeriod] = useState(20);  // Default SMA period
    const [stdDevMultiplier, setStdDevMultiplier] = useState(2);  // Default standard deviation multiplier
    const [signals, setSignals] = useState(null);  // Buy/Sell signals
    const [backtestData, setBacktestData] = useState(null); // Backtesting results
    const [loading, setLoading] = useState(false);  // Loading state
    const [error, setError] = useState(null);  // Error state
    const [graphUrl, setGraphUrl] = useState(null);  // URL for the graph image

    const adapter = new BBAdapter();


    const calculateBB = async () => {
        setLoading(true);
        setError(null);

        try {
            const data = await adapter.fetchData(symbol, { sma_period: period, std_dev_multiplier: stdDevMultiplier });
            if (data.signals) {
                setSignals(data.signals);
                const imageUrl = `data:image/png;base64,${data.image}`;
                setGraphUrl(imageUrl);
            } else {
                setSignals(null);
                setGraphUrl(null);
            }
        } catch (error) {
            console.error('Error fetching Bollinger Bands data:', error);
            setError('Failed to fetch Bollinger Bands signals and graph. Please try again.');
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
            <h3>Bollinger Bands Strategy for {symbol}</h3>

            {/* Input fields for the SMA period and standard deviation multiplier */}
            <label className="period-label">
                SMA Period:
                <input 
                    className="period-input"
                    type="number"
                    value={period}
                    onChange={(e) => setPeriod(Number(e.target.value))}
                    min="1"
                />
            </label>

            <label className="period-label">
                Standard Deviation Multiplier:
                <input
                    className="period-input"
                    type="number"
                    value={stdDevMultiplier}
                    onChange={(e) => setStdDevMultiplier(Number(e.target.value))}
                    min="1"
                />
            </label>

            <div className="button-container">
                <button className="calculate-btn" onClick={calculateBB}>Calculate Bollinger Bands</button>

                {signals && (
                    <div>
                        <button className="backtest-btn" onClick={runBacktest}>Run Backtest</button>
                        <button className="log-btn" onClick={logTrades}>Log Trades to CSV</button>
                    </div>
                )}
            </div>

            {loading ? <p>Loading...</p> : null}
            {error ? <p style={{ color: 'red' }}>{error}</p> : null}

            <div className="sma-content">
                <div className="sma-graph-signals">
                    {/* Display Bollinger Bands signals */}
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
                            <h4>Bollinger Bands Graph:</h4>
                            <img src={graphUrl} alt="Bollinger Bands Graph" className="sma-graph-img" />
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