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

// Define end for the VCF datasets (genomes)
router.get('/genomes', function(req, res) {
    const query = ` 
    SELECT 
        DISTINCT genome_id
    FROM genomes
    `;

    db.all(query, [], function(err, rows){
        if(err){
            console.error(err);
            res.status(500).send('Internal server error');
        } else {
            res.status(200).json(rows);
        }
    });
});


// Define end for the number of variants in a genome
router.get('/genomes/:genome_id/variants', function(req, res) {
    const query = `
    SELECT 
     
        genome_id,
        chromosome_id,
        COUNT(*) AS num_variants

    FROM variants
    WHERE genome_id = ?

    GROUP BY genome_id, chromosome_id
    ORDER BY chromosome_id
    ;
    `
    db.all(query, [req.params.genome_id], function(err, rows){
        if(err){
            console.error(err);
            res.status(500).send('Internal server error');
        } else {
            res.status(200).json(rows);
        }
    });
});


// Define end for the number of SNPs in a genome
router.get('/genomes/:genome_id/snps', function(req, res) {
    const query = `
    SELECT 
     
        genome_id,
        chromosome_id,
        COUNT(*) AS num_variants

    FROM variants
    WHERE genome_id = ?
    AND is_snp = 1

    GROUP BY genome_id, chromosome_id
    ORDER BY chromosome_id
    ;
    `
    db.all(query, [req.params.genome_id], function(err, rows){
        if(err){
            console.error(err);
            res.status(500).send('Internal server error');
        } else {
            res.status(200).json(rows);
        }
    });
});


// Define end for the number of INDELs in a genome
router.get('/genomes/:genome_id/indels', function(req, res) {
    const query = `
    SELECT 
     
        genome_id,
        chromosome_id,
        COUNT(*) AS num_variants

    FROM variants
    WHERE genome_id = ?
    AND is_snp = 0

    GROUP BY genome_id, chromosome_id
    ORDER BY chromosome_id
    ;
    `
    db.all(query, [req.params.genome_id], function(err, rows){
        if(err){
            console.error(err);
            res.status(500).send('Internal server error');
        } else {
            res.status(200).json(rows);
        }
    });
});


// List genes impacted by moderate or high impact variants in a specific 
// chromosome region for a specific VCF {genome_id}

router.get('/genomes/:genome_id/:chromosome_id/:mbp', function(req, res) {});



module.exports = router;