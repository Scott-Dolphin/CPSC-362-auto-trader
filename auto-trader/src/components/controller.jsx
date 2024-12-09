import { fetchData, downloadFile } from './dataModel';

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
 
