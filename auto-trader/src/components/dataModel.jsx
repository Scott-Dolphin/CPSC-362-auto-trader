import { format } from 'date-fns';


export const fetchData = async (symbol) => {
    try {
        const response = await fetch(`http://127.0.0.1:3000/api/stock/real/${symbol}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const jsonData = await response.json();
        return jsonData;
    } catch (err) {
        console.error('Error fetching data:', err);
        throw err;
    }
};

export const fetchHistory = async (symbol, startDate, endDate) => {
    try {
        const response = await fetch('http://127.0.0.1:3000/api/stock/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            mode: 'cors',
            body: JSON.stringify({
                symbol: symbol,
                start: format(startDate, 'yyyy-MM-dd'),
                end: endDate ? format(endDate, 'yyyy-MM-dd') : null,
            }),
        });

        const json = await response.json();
        return `data:image/png;base64,${json.image}`;
    } catch (error) {
        console.error('Error fetching data:', error);
        throw error;
    }
};