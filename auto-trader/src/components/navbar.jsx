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
    const Download = async () => {
        try {
            const response = await fetch(`http://127.0.0.1:3000/api/stock/${selectedValue}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                mode: 'cors',
                body: JSON.stringify({ period : '1y' }),
            });
      
            const json = await response.json();
            setData(json);
            //setData(json);
            
          } catch (error) {
            console.error('Error fetching data:', error);
          }  
        
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
                downloadFile();
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