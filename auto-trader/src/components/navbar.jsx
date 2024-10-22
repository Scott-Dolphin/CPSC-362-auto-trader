// backtesting v1 

import React, { useState } from 'react';
import { Button } from 'react-bootstrap';
import HistoryGraph from './HistoryGraph';
import SMACrossover from './SMACrossover';

export default function Navbar() {
    const [selectedValue, setSelectedValue] = useState('FNGU');  // Default symbol
    const [downloaded, setDownloaded] = useState(false);
    const [showHistory, setShowHistory] = useState(false);
    const [showSMACrossover, setShowSMACrossover] = useState(false);

    const handleSelectChange = (event) => {
        setSelectedValue(event.target.value);
    };

    const Download = async () => {
        setDownloaded(true);
    };

    const getSMACrossover = async () => {
        setShowSMACrossover(true);
        setShowHistory(false);
    };

    const getHistory = async () => {
        setShowHistory(true);
        setShowSMACrossover(false);
    };

    return (
        <div>
            <div className="nav">
                <select value={selectedValue} onChange={handleSelectChange}>
                    <option value="FNGU">FNGU</option>
                    <option value="FNGD">FNGD</option>
                </select>
                <Button onClick={Download}>Download</Button>
            </div>

            {downloaded && (
                <>
                    {showHistory ? (
                        <HistoryGraph value={selectedValue} />
                    ) : showSMACrossover ? (
                        <SMACrossover symbol={selectedValue} /> 
                    ) : (
                        <div>
                            <Button onClick={getHistory}>Show Historical Graph</Button>
                            <Button onClick={getSMACrossover}>Show SMA Crossover</Button>
                        </div>
                    )}
                </>
            )}
        </div>
    );
}
