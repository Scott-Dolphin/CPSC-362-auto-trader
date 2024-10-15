import { Button } from 'react-bootstrap';

export default function Navbar() {
    return (
        <div className="nav">
            <select >
                <option value="FNGU">FNGU</option>
                <option value="FNGD">FNGD</option>
            </select>
            <Button>download</Button>
        </div>
    );
}