import React, { useState, useEffect } from 'react';
import { Button, Card } from 'react-bootstrap';

export default function Navbar() {
    const [selectedValue, setSelectedValue] = useState('FNGU');
    const [data, setData] = useState(null);

    const handleSelectChange = (event) => {
        setSelectedValue(event.target.value);
    };

    const Download = async () => {
    
        try {
            const response = await fetch(`http://192.168.1.52:5000/api/stock/${selectedValue}`, {
              method: 'GET',
              headers: {
                'Content-Type': 'application/json',
              },
              mode: 'cors',
            });
      
            const json = await response.json();
            setData(`data:image/png;base64,${json.image}`);
            //setData(json);
          } catch (error) {
            console.error('Error fetching data:', error);
          }

        };

        useEffect(() => {
            if (data) {
                console.log(data);
            }
        }, [data]);

    return (
        <div>
        <div className="nav">
            <select value={selectedValue} onChange={handleSelectChange}>
                <option value="FNGU">FNGU</option>
                <option value="FNGD">FNGD</option>
            </select>
        
            <Button onClick={() => Download()}>Download</Button>
            </div>
            <Card>
                <Card.Img src={data} />
            </Card>
        
        </div>
    );
}