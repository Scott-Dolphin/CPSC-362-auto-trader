import React, { useState } from 'react';
import { Button } from 'react-bootstrap';
import SMACrossover from './SMACrossover';
import BB from './BB';
import MACD from './MACD';

export default function StrategyDisplay({ symbol, setShowStrat }) {
    const [selectedValue, setSelectedValue] = useState('SMA');

    const handleSelectChange = (event) => {
        setSelectedValue(event.target.value);
    };

    return (
        <div style={{paddingTop: "100px"}}>
            <div><Button onClick={() => setShowStrat(false)}>Back</Button></div>
            <select value={selectedValue} onChange={handleSelectChange}>
                <option value="SMA">Simple Moving Average</option>
                <option value="BB">Bollinger Bands</option>
                <option value="MACD">MACD</option>
            </select>
            
            {(selectedValue === 'SMA') && <SMACrossover symbol={symbol} />}
            {(selectedValue === 'BB') && <BB symbol={symbol} />}
            {(selectedValue === 'MACD') && <MACD symbol={symbol} />}
        </div>
    );
}