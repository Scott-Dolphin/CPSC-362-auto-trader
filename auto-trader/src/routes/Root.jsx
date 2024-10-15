import React from 'react';
import { Button } from 'react-bootstrap';

export default function Root() {

    return (
        <div style={{
            display: "flex",
            justifyContent: "space-between",

            width: "300px",
            margin: "auto"
        }}>


            <select style={{ background: "#103074", borderRadius: "10px" }}>

                <option value="FNGU">FNGU</option>
                <option value="FNGD">FNGD</option>

            </select>

            <Button style={{ background: "#103074" }}>download</Button>
        </div>
    );
}