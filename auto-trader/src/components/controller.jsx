import { useEffect } from 'react';
import { format } from 'date-fns';
import { json } from 'react-router-dom';
//import io from 'socket.io-client';


//const socket = io('http://ec2-3-138-198-12.us-east-2.compute.amazonaws.com'); //http://127.0.0.1:3000
const API_URL = 'http://ec2-3-138-198-12.us-east-2.compute.amazonaws.com/api';

export const handleDownload = async (symbol, setData, setDownloaded) => {
    try {
        const response = await fetch(`${API_URL}/symbol/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            mode: 'cors',
            body: JSON.stringify({
                symbol: symbol
            }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        setData(null);
        setDownloaded(true);
    } catch (err) {
        console.error('Error fetching data:', err);
        throw err;
    }
};
 
export const handleFetchHistory = async (symbol, startDate, endDate, setData) => {
    try {
        const response = await fetch(`${API_URL}/stock/`, {
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
        setData(`data:image/png;base64,${json.image}`);

    } catch (error) {
        console.error('Error fetching history data:', error);
    }
};

/*export const useRealtimeUpdates = (setData) => {
    console.log('useRealtimeUpdates');
    useEffect(() => {
        socket.on('realtime_update', (data) => {
            console.log('Realtime update received:', data);
            setData(data);
        });

        return () => {
            socket.off('realtime_update');
        };
    }, [setData]);
};*/

export class DataAdapter {
    async fetchData(symbol, params) {
        throw new Error('fetchData method must be implemented');
    }

    async runBacktest(signals) {
        const response = await fetch(`${API_URL}/backtest`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ signals }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        return data;
    }

    async logTrades(signals) {
        const response = await fetch(`${API_URL}/backtest_log`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ signals }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        return data;
    }
}

export class SMACrossoverAdapter extends DataAdapter {
    async fetchData(symbol, params) {
        const response = await fetch(`${API_URL}/sma_crossover_plot`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ symbol, ...params }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        return data;
    }
}

export class BBAdapter extends DataAdapter {
    async fetchData(symbol, params) {
        const response = await fetch(`${API_URL}/bollinger_bands_plot`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ symbol, ...params }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        return data;
    }
}

export class MACDAdapter extends DataAdapter {
    async fetchData(symbol, params) {
        const response = await fetch(`${API_URL}/macd_plot`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ symbol, ...params }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        return data;
    }
}

