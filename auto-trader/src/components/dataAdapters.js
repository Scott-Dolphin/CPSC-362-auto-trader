import { format } from 'date-fns';

const API_URL = 'http://127.0.0.1:3000/api';

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