import React, { useState } from 'react';
import { Button } from 'react-bootstrap';
import { IoArrowBackCircleSharp } from "react-icons/io5";

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
            <IoArrowBackCircleSharp style={{padding:"10px", color: "#ce8f55", display: "flex", justifyContent: "space-between", alignItems: "flex-start"}} onClick={() => setShowStrat(false)}/>
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