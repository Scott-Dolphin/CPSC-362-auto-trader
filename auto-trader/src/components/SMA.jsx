import { Button, Card } from 'react-bootstrap';
import React, { useState, useEffect } from 'react';


export default function SMA({data}) {
    const [smaData, setSmaData] = useState(null);

    const get_SMA = async () => {
        console.log('showing SMA');

        try {
            const response = await fetch('http://127.0.0.1:3000/api/sma', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                mode: 'cors',
                body: JSON.stringify({ symbol: data }),
            });
            
            const json = await response.json();
            setSmaData(json);
            //setData(json);
          } catch (error) {
            console.error('Error fetching data:', error);
          }
    };
    useEffect(() => {
        console.log(smaData);
    }, [smaData]);
    return(
    <Button onClick={() => get_SMA()}>Show SMA</Button>
    );
}