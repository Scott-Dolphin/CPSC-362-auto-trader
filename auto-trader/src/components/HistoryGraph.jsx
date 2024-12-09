import React, { useState, useEffect } from 'react';
import { Button, Card } from 'react-bootstrap';
import { IoArrowBackCircleSharp } from "react-icons/io5";

import DatePicker from 'react-datepicker';
import { format, set } from 'date-fns';
import 'react-datepicker/dist/react-datepicker.css';

export default function HistoryGraph({symbol, setShowHistory}) {

    const [startDate, setStartDate] = useState(new Date('2021-01-01'));
    const [endDate, setEndDate] = useState(null);
    const [data, setData] = useState(null);
    const [fileDisplay, setFileDisplay] = useState(true);
    const [fileContent, setFileContent] = useState(null);

    // Handle start date change
    const handleStartDateChange = (date) => {
        setStartDate(date);
    };

    // Handle end date change
    const handleEndDateChange = (date) => {
        setEndDate(date);
    };


    // Fetch historical data based on selected date range
    const fetch_history = async () => {
        console.log('showing history');

        try {
            const response = await fetch('http://ec2-3-138-198-12.us-east-2.compute.amazonaws.com/api/stock/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                mode: 'cors',
                body: JSON.stringify({ symbol: symbol,
                    start: format(startDate, 'yyyy-MM-dd'),
                    end: endDate ? format(endDate, 'yyyy-MM-dd') : null,
                 }),
            });
      
            const json = await response.json();
            setData(`data:image/png;base64,${json.image}`);
            //setData(json);
        } catch (error) {
            console.error('Error fetching data:', error);
        }
          
    };  

        useEffect(() => {
            fetch_history();    
        }, []);

        return ((
                <div>
                    <IoArrowBackCircleSharp style={{padding:"10px", color: "#ce8f55", display: "flex", justifyContent: "space-between", alignItems: "flex-start"}}
                                            onClick={() => setShowHistory(false)}/>
                    <Card>
                        <Card.Img src={data} />
                    </Card>
                    <div className="date-picker">
                        <DatePicker
                            selected={startDate}
                            onChange={handleStartDateChange}
                            selectsStart
                            startDate={startDate}
                            endDate={endDate}
                            dateFormat="yyyy-MM-dd"
                        />
                        <DatePicker
                            selected={endDate}
                            onChange={handleEndDateChange}
                            selectsEnd
                            startDate={startDate}
                            endDate={endDate}
                            minDate={startDate}
                            dateFormat="yyyy-MM-dd"
                        />
                        <Button onClick={fetch_history}>Change Range</Button>
                    </div>
                </div>
            )
        );

}