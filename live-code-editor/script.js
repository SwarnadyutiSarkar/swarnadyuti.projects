document.getElementById('run').addEventListener('click', async () => {
    const code = document.getElementById('code').value;

    try {
        const response = await fetch('/run', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code }),
        });
        
        const result = await response.json();
        document.getElementById('output').textContent = result.output || result.error;
    } catch (err) {
        document.getElementById('output').textContent = 'Error: ' + err.message;
    }
});
