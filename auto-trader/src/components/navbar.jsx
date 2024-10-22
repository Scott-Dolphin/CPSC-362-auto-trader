import React, { useState, useEffect } from 'react';
import { Button, Card } from 'react-bootstrap';
import HistoryGraph from './HistoryGraph';
import SMA from './SMA';

export default function Navbar() {
    const [selectedValue, setSelectedValue] = useState('FNGU');
    const [data, setData] = useState(null);
    const [downloaded, setDownloaded] = useState(false);
    const [showHistory, setShowHistory] = useState(false);
    const [showSMA, setShowSMA] = useState(false);
    const handleSelectChange = (event) => {
        setSelectedValue(event.target.value);
    };

    const Download = async () => {
          setDownloaded(true);
            console.log('Download');
        };

        const get_SMA = async () => {
            setShowSMA(true);
        }

        const get_history = async () => {
            setShowHistory(true);
        };

        useEffect(() => {
            if (data) {
                console.log(data);
            }
        }, [data]);
        if (downloaded) {
            return (
               <>
            
                
            {(showHistory) ? <HistoryGraph value={selectedValue}/> : 
            (showSMA) ? <SMA data={selectedValue}/> :

            (
            <div>
            <Button onClick={() => get_history()}>Show Historical Graph</Button>
            <Button onClick={() => get_SMA()}>Show SMA</Button>
            </div>
            )}

            </>
            
            );
        } else {
            return (
                <div>
                    <div className="nav">
                        <select value={selectedValue} onChange={handleSelectChange}>
                            <option value="FNGU">FNGU</option>
                            <option value="FNGD">FNGD</option>
                        </select>
                    
                        <Button onClick={() => Download()}>Download</Button>
                    </div>
                
                </div>
            );
        }
}