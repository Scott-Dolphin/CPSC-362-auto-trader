import React, { useState, useEffect } from 'react';
import { Button } from 'react-bootstrap';
import HistoryGraph from './HistoryGraph';
import StrategyDisplay from './StrategyDisplay';
import { handleDownload } from './controller';
import { use } from 'react';

export default function Navbar() {
    const [selectedValue, setSelectedValue] = useState('FNGU');
    const [downloaded, setDownloaded] = useState(false);
    const [showHistory, setShowHistory] = useState(false);
    const [showStrat, setShowStrat] = useState(false);
    const [data, setData] = useState(null);
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
        console.log('Data:', data);
    }, [data]);

    return (downloaded ? (
            showHistory ? (
                <HistoryGraph symbol={selectedValue} setShowHistory={setShowHistory} />
            ) : showStrat ? (
                <StrategyDisplay symbol={selectedValue} setShowStrat={setShowStrat}/>
            ) : (
                    <div className='navbar'>

                         <div>
                            <h1 className="head">{selectedValue} Selected</h1>
                            <h2>change</h2>
                        </div>

                        <div className="direct">

                        <Button onClick={get_history}>Show Historical Graph</Button>
                        <Button onClick={get_Strat}>Show Strategies</Button>
                        </div>

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