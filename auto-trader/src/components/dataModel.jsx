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