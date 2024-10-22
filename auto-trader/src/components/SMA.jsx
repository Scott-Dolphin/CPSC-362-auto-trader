import React, { useState } from 'react';
import './SMA.css';  

export default function SMA({ symbol }) {
    const [smaData, setSmaData] = useState(null);
    const [period, setPeriod] = useState(50);  // Default period is 50
    const [loading, setLoading] = useState(false);  // Loading state
    const [error, setError] = useState(null);  // Error state

    const getSMA = async () => {
        setLoading(true);  // Start loading
        setError(null);  // Reset error
        try {
            // Validate that period is a valid number and greater than 0
            if (isNaN(period) || period <= 0) {
                setError("Please enter a valid positive number for the SMA period.");
                setLoading(false);
                return;
            }

            console.log("Fetching SMA for symbol:", symbol, "with period:", period);

            const response = await fetch('http://127.0.0.1:3000/api/sma', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ symbol: symbol, period: period }),  // Pass symbol and valid period
            });

            if (!response.ok) {
                throw new Error('Failed to fetch SMA data from the server');
            }
            
            const data = await response.json();
            if (data.sma) {
                setSmaData(data.sma);
            } else {
                setSmaData(null);  // Handle case where there's no SMA data
            }
        } catch (error) {
            console.error('Error fetching SMA data:', error);
            setError("Failed to fetch SMA data. Please try again.");
        }
        setLoading(false);  // Stop loading after request is done
    };

    return (
        <div className="sma-container">
            <h3>SMA for {symbol}</h3>
            <label className="period-label">
                Period: 
                <input 
                    className="period-input"
                    type="number" 
                    value={period} 
                    onChange={(e) => setPeriod(Number(e.target.value))}  // Ensure input is a number
                    min="1" 
                />
            </label>
            <button className="recalculate-btn" onClick={getSMA}>Recalculate SMA</button>

            {loading ? (
                <p>Loading SMA data...</p>
            ) : error ? (
                <p style={{ color: 'red' }}>{error}</p>
            ) : smaData ? (
                <div className="sma-list">
                    {Object.keys(smaData).map((date, index) => (
                        <div className="sma-item" key={index}>
                            <strong>Date:</strong> {date}, <strong>SMA:</strong> {smaData[date].SMA.toFixed(2)}
                        </div>
                    ))}
                </div>
            ) : (
                <p>No SMA data available</p>
            )}
        </div>
    );
}
