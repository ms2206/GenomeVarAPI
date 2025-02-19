const express = require('express');
const path = require('path');

const app = express();
const port = 3000;
app.listen(port, function() {
    console.log(`Server is running on http://localhost:${port}`);
    });

// Construct the router file path relative to src/api/
const routerPath = path.join(__dirname, 'routes', 'router.js');
const router = require(routerPath);

app.use('/api', router);


