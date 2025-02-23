const express = require('express');
const path = require('path');
const { marked } = require('marked');
const fs = require('fs');

const app = express();
const port = 3000;


// Serve static files from the 'docs' directory
app.use(express.static(path.join(__dirname, '..', '..', 'docs')));

// Serve the user guide from a Markdown file
app.get('/', (req, res) => {
    const markdownFilePath = path.join(__dirname, '..', '..', 'docs', 'user_guide.md');
    fs.readFile(markdownFilePath, 'utf8', (err, data) => {
        if (err) {
            res.status(500).send('Error reading the Markdown file.');
            return;
        }
        const htmlContent = marked(data);
        res.send(htmlContent);
    });
});


app.listen(port, function() {
    console.log(`Server is running on http://localhost:${port}`);
    });

// Construct the router file path relative to src/api/
const routerPath = path.join(__dirname, 'routes', 'router.js');


const router = require(routerPath);

app.use('/api', router);


