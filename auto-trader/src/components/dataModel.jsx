export const fetchData = async (symbol) => {
    try {
        const response = await fetch(`http://ec2-3-138-198-12.us-east-2.compute.amazonaws.com/api/stock/real/${symbol}`);
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
 
export const downloadFile = (data) => {
    if (data == null) { return; }

    const fileName = 'data.json';
    const json = JSON.stringify(data);
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = fileName;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}; 