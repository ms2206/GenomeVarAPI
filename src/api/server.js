const express = require('express');
const path = require('path');
const { marked } = require('marked');
const fs = require('fs');

const app = express();
const port = 3000;


/*
This code is used to start the server and listen on port 3000.
*/

app.listen(port, function() {
    console.log(`Server is running on http://localhost:${port}`);
    });

// Construct the router file path relative to src/api/
const routerPath = path.join(__dirname, 'routes', 'router.js');

/*
This code is used to import the router from the router.js file and use it in the Express app.
*/

const router = require(routerPath);

app.use('/api', router);

/*
This code is used to generate the user guides and technical documentation for the API.
*/

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

// Serve the database tec guide from a Markdown file
app.get('/database-technical-docs', (req, res) => {
    const markdownFilePath = path.join(__dirname, '..', '..', 'docs', 'database_technical_docs.md');
    fs.readFile(markdownFilePath, 'utf8', (err, data) => {
        if (err) {
            res.status(500).send('Error reading the Markdown file.');
            return;
        }
        const htmlContent = marked(data);
        res.send(htmlContent);
    });
});

// Serve the python tec guide from a Markdown file
app.get('/parser-technical-docs', (req, res) => {
    const markdownFilePath = path.join(__dirname, '..', '..', 'docs', 'parse_vcf_technical_docs.md');
    fs.readFile(markdownFilePath, 'utf8', (err, data) => {
        if (err) {
            res.status(500).send('Error reading the Markdown file.');
            return;
        }
        const htmlContent = marked(data);
        res.send(htmlContent);
    });
});

// Serve the API tec guide from a Markdown file
app.get('/api-technical-docs', (req, res) => {
    const markdownFilePath = path.join(__dirname, '..', '..', 'docs', 'server_technical_docs.md');
    fs.readFile(markdownFilePath, 'utf8', (err, data) => {
        if (err) {
            res.status(500).send('Error reading the Markdown file.');
            return;
        }
        const htmlContent = marked(data);
        res.send(htmlContent);
    });
});