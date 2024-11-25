import { fetchData, downloadFile } from './dataModel';

export const handleDownload = async (symbol, setData, setDownloaded) => {
    try {
        console.log('Downloading data for:', symbol);
        const data = await fetchData(symbol);
        setData(data);
        setDownloaded(true);
    } catch (err) {
        console.error('Error downloading data:', err);
    }
};

export const handleFileDownload = (data) => {
    if (data) {
        downloadFile(data);
        console.log(data);
    }
};