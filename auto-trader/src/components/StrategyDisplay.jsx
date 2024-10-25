import React from 'react';
import { useState } from 'react';
import SMACrossover from './SMACrossover';
import BB from './BB';
import MACD from './MACD';

export default function StrategyDisplay({symbol}) {

    const [selectedValue, setSelectedValue] = useState('SMA');


    const handleSelectChange = (event) => {
        setSelectedValue(event.target.value);
    };

    return (
        <div >
            <select value={selectedValue} onChange={handleSelectChange}>
                <option value="SMA">Simple Moving Average</option>
                <option value="BB">Bollinger Bands</option>
                <option value="MACD">Moving Average Convergence Divergence</option>
                </select>
        
            {(selectedValue) == "SMA" ? <SMACrossover symbol={symbol} /> : 
            (selectedValue) == "BB" ? <BB symbol={symbol}/> :
            (selectedValue) == "MACD" ? <MACD symbol={symbol}/> :
            <div>
                <h1>Strategy not Found</h1>
            </div>}
        <div >
            
        </div>

        </div>
    );
}