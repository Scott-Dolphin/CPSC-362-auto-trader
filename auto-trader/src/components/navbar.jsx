import React, { useState } from 'react';
import { Button } from 'react-bootstrap';

export default function Navbar() {

    const [data, setData] = useState(null);

    const Download = async () => {
        try {
            const response = await fetch('http://192.168.1.52:5000/api/data', {
              method: 'GET',
              headers: {
                'Content-Type': 'application/json',
              },
              mode: 'cors',
            });
      
            const json = await response.json();
            setData(json);
          } catch (error) {
            console.error('Error fetching data:', error);
          }

          console.log(data);

        };
    return (
        <div className="nav">
            <select >
                <option value="FNGU">FNGU</option>
                <option value="FNGD">FNGD</option>
            </select>
            <Button onClick={() => Download()}>download</Button>
        </div>
    );
}