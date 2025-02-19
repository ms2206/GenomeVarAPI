const express = require('express');
const sqlite3 = require('sqlite3');
const path = require('path');


// Construct the database file path relative to src/api/routes
const dbPath = path.join(__dirname, '..', '..', 'db', 'vcf_db.sqlite3');

// Create a database connection
const db = new sqlite3.Database(dbPath, (err) => {
    if (err) {
        console.error('Failed to connect to the database:', err);
    } else {
        console.log('Connected to the database');
    }
});

// Create a new router
const router = express.Router();

router.use(function(req, res, next) {
    console.log('Request received', Date.now());
    next();
});

module.exports = router;