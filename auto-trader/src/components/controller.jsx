import { useEffect } from 'react';
import { fetchData } from './dataModel';
import { fetchHistory } from './dataModel';
export const handleDownload = async (symbol, setData, setDownloaded) => {
    try {
        fetchData(symbol).then((data) => {
            setData(data);
        });
        console.log('Downloading data for:', symbol);
        setDownloaded(true);
    } catch (err) {
        console.error('Error downloading data:', err);
    }
};
 
export const handleFetchHistory = async (symbol, startDate, endDate, setData) => {
    try {
        const imageData = await fetchHistory(symbol, startDate, endDate);
        setData(imageData);
    } catch (error) {
        console.error('Error fetching history data:', error);
    }
};

