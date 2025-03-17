document.getElementById('parcelForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const parcelData = {
        source: document.getElementById('source').value,
        destination: document.getElementById('destination').value,
        weight: parseFloat(document.getElementById('weight').value)
    };

    try {
        const response = await fetch('/api/route', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(parcelData)
        });

        const data = await response.json();

        // Display the route
        document.getElementById('routeDisplay').innerHTML = `
            <h3>Route:</h3>
            <p>${data.route.join(' → ')}</p>
        `;

        // Display the cost
        document.getElementById('costDisplay').innerHTML = `
            <h3>Total Cost:</h3>
            <p>$${data.cost.toFixed(2)}</p>
        `;
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while calculating the route');
    }
});
