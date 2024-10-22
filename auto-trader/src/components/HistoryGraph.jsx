import React, { useState, useEffect } from 'react';
import { Button, Card } from 'react-bootstrap';
import DatePicker from 'react-datepicker';
import { format } from 'date-fns';
import 'react-datepicker/dist/react-datepicker.css';

export default function HistoryGraph({value}) {

    const [startDate, setStartDate] = useState("2021-01-01");
    const [endDate, setEndDate] = useState(null);
    const [data, setData] = useState(null);

    const handleStartDateChange = (date) => {
        setStartDate(date);
    };

    const handleEndDateChange = (date) => {
        setEndDate(date);
    };

    const handleSubmit = () => {
        // Handle the date range submission
        setStartDate(format(startDate, 'yyyy-MM-dd'));
        setEndDate(format(endDate, 'yyyy-MM-dd'));

        console.log('Start Date:', startDate);
        if(endDate != null) {
        console.log('End Date:', endDate);
        }
        // You can make an API call here with the selected date range
        get_history();
    };
    
    const get_history = async () => {
            
        console.log('showing history');

        try {
            const response = await fetch('http://127.0.0.1:3000/api/stock/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                mode: 'cors',
                body: JSON.stringify({ symbol: value, start: startDate, end: endDate }),
            });
      
            const json = await response.json();
            setData(`data:image/png;base64,${json.image}`);
            //setData(json);
          } catch (error) {
            console.error('Error fetching data:', error);
          }
          
        };    

        useEffect(() => {
            console.log(value);
            get_history();
            console.log(data);
        }, [data]);
    
    return (
        <div>
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
                <Button onClick={handleSubmit}>Change Range</Button>
            </div>
            
        </div>
    );

}