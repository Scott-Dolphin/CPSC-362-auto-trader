import React, { useState, useEffect } from 'react';
import { Button, Card } from 'react-bootstrap';
import HistoryGraph from './HistoryGraph';
import StrategyDisplay from './StrategyDisplay';

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

    // Download file
    const downloadFile = () => {
        if(data==null) { return; }

        const fileName = 'data.json';
        const json = JSON.stringify(data);
        const blob = new Blob([json], { type: 'application/json' });
        const url = URL.createObjectURL(blob);

        const a = document.createElement('a');
        a.href = url;
        a.download = fileName;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    };

    // Fetch data from the server
    const Download = async () => {
        try {
            console.log('Downloading data for:', selectedValue);
            const response = await fetch(`http://ec2-3-138-198-12.us-east-2.compute.amazonaws.com/api/stock/${selectedValue}`, { // fixme: syntax error on downlaod
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
                mode: 'cors'
            });
            if (!response.ok) {
                // Handle HTTP errors
                throw new Error(`HTTP error! status: ${response.status}`);
              }
      
            const json = await response.json();
            setData(json);
            
        } catch (err) {
            // Handle fetch errors
           
            console.error('Error fetching data:', err.message);
          }  
        
        setDownloaded(true);

        console.log('Download');
    };

        const get_Strat = async () => {
            setShowStrat(true);
        }

        const get_history = async () => {
            setShowHistory(true);
        };

        useEffect(() => {
            if (data) {
                downloadFile();
                console.log(data);
            }
        }, [data]);

        if (downloaded) {
            return (
               <>
            
                
            {(showHistory) ? <HistoryGraph symbol={selectedValue}/> : 
            (showStrat) ? <StrategyDisplay symbol={selectedValue}/> :

            (
            <div>
            <Button onClick={() => get_history()}>Show Historical Graph</Button>
            <Button onClick={() => get_Strat()}>Show Strategies</Button>
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