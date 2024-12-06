import { fetchData, downloadFile } from './dataModel';

export const handleDownload = async (symbol, setDownloaded) => {
    try {
        console.log('Downloading data for:', symbol);
        setDownloaded(true);
    } catch (err) {
        console.error('Error downloading data:', err);
    }
};

