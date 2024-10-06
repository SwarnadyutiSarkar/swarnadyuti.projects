const express = require('express');
const bodyParser = require('body-parser');
const { exec } = require('child_process');

const app = express();
const PORT = 3000;

app.use(bodyParser.json());
app.use(express.static('public'));

app.post('/run', (req, res) => {
    const code = req.body.code;

    exec(`node -e "${code.replace(/"/g, '\\"')}"`, (error, stdout, stderr) => {
        if (error) {
            res.json({ error: stderr });
            return;
        }
        res.json({ output: stdout });
    });
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
