import React, { useState, useEffect } from 'react';
import { Button } from 'react-bootstrap';
import { IoMdArrowDropupCircle, IoMdArrowDropdownCircle } from "react-icons/io";
import { IoArrowBackCircleSharp } from "react-icons/io5";

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
    const [showChange, setShowChange] = useState(true);
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

    return (
        
        downloaded ? (
            showHistory ? (
                <HistoryGraph symbol={selectedValue} setShowHistory={setShowHistory} />
            ) : showStrat ? (
                <StrategyDisplay symbol={selectedValue} setShowStrat={setShowStrat}/>
            ) : (
                
                    <div className='navbar'>
                        
                        <IoArrowBackCircleSharp style={{color: "#ce8f55"}} onClick={() => setDownloaded(false)}/>
                            <div>Show Change<input type="checkbox" checked={showChange} onChange={() => setShowChange(!showChange)} /></div>
                         <div>
                            
                            {showChange && (
                            <>
                            <h1 className="head">{selectedValue} Change</h1>
                            {data ? (
                                <div>
                                    
                                <h3><strong style={{color: "#ce8f55"}}>Last Close price</strong>:&nbsp;&nbsp;&nbsp;{data.day_price}</h3>
                                <h3><strong style={{color: "#ce8f55"}}>Price 5 days ago</strong>:&nbsp;&nbsp;&nbsp;{data.week_price}</h3>
                                <h3><strong style={{color: "#ce8f55"}}>Rate of Change</strong>:&nbsp;&nbsp;&nbsp;{data.rate_of_change} {data.rate_of_change > 0 ?
                                 (<IoMdArrowDropupCircle style={{color: "green"}}/>):(<IoMdArrowDropdownCircle style={{color: "red"}}/>)}</h3>
                                
                                </div>
                                ) : (
                                <h2>Loading...</h2>
                                )}
                            </>
                            )}

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