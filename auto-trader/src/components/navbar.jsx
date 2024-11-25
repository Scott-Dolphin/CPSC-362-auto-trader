import React, { useState, useEffect } from 'react';
import { Button } from 'react-bootstrap';
import HistoryGraph from './HistoryGraph';
import StrategyDisplay from './StrategyDisplay';
import { handleDownload, handleFileDownload } from './controller';

export default function Navbar() {
    const [selectedValue, setSelectedValue] = useState('FNGU');
    const [data, setData] = useState(null);
    const [downloaded, setDownloaded] = useState(false);
    const [showHistory, setShowHistory] = useState(false);
    const [showStrat, setShowStrat] = useState(false);

    // Handle select change
    const handleSelectChange = (event) => {
        setSelectedValue(event.target.value);
    };

    // Fetch data from the server
    const Download = async () => {
        await handleDownload(selectedValue, setData, setDownloaded);
    };

    const get_history = () => {
        setShowHistory(true);
    };

    const get_Strat = () => {
        setShowStrat(true);
    };

    useEffect(() => {
        handleFileDownload(data);
    }, [data]);

    return (
        downloaded ? (
            showHistory ? (
                <HistoryGraph symbol={selectedValue} />
            ) : showStrat ? (
                <StrategyDisplay symbol={selectedValue} />
            ) : (
                <div>
                    <Button onClick={get_history}>Show Historical Graph</Button>
                    <Button onClick={get_Strat}>Show Strategies</Button>
                </div>
            )
        ) : (
            <div>
                <div className="nav">
                    <select value={selectedValue} onChange={handleSelectChange}>
                        <option value="FNGU">FNGU</option>
                        <option value="FNGD">FNGD</option>
                    </select>
                    <Button onClick={Download}>Download</Button>
                </div>
            </div>
        )
    );
}
