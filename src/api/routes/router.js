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

/*
Define end for the VCF datasets (genomes)
*/

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


/* 
Define end for the number of variants in a genome
*/

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


/* 
Define end for the number of SNPs in a genome
*/

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


/* 
Define end for the number of INDELs in a genome
*/

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



/*
List genes impacted by moderate or high/moderate impact variants in a specific 
chromosome region for a specific VCF {genome_id}

#TODO: add feature to filter by snpeff_match
*/

router.get('/genomes/:genome_id/:chromosome_id/:mbp', function(req, res) {

const mbp_string = req.params.mbp;
const mbp = parseInt(mbp_string);

// check if mbp is a number
if (isNaN(mbp)){
    res.status(400).send('Invalid value for :mbp, must be a number');
    return; // Stop further execution
}

// convert mbp to bp
const bp = mbp * 1000000


    const query = `
    SELECT 
    DISTINCT
    variants.gene_name,
    variants.genome_id,
    variants.chromosome_id,   
    variants.snpeff_match,
    variants.position,
    (SELECT start FROM chromosomes WHERE chromosomes.chromosome_id = variants.chromosome_id) AS start,
    (SELECT end FROM chromosomes WHERE chromosomes.chromosome_id = variants.chromosome_id) AS end


    FROM variants
    JOIN chromosomes
        ON variants.chromosome_id = chromosomes.chromosome_id

    WHERE variants.gene_name IS NOT NULL
    AND variants.snpeff_match IN ('HIGH', 'MODERATE')
    AND variants.genome_id = ?
    AND variants.chromosome_id = ?
    AND variants.position > start
    AND variants.position < start + ?

    ORDER BY snpeff_match
    ;`

db.all(query, [req.params.genome_id, req.params.chromosome_id, bp], 
    function(err, rows){
        if(err){
            console.error(err);
            res.status(500).send('Internal server error');
        } else {
            res.status(200).json(rows);
        }
    });
});

 /* 
 List genomes with a specific variant in a specific gene and other useful variant information
 */

 router.get('/variants/gene/:gene_name', function(req, res) {

    const query = `
    
    SELECT 
        genomes.genome_id,
        variants.variant_id AS vcf_db_variant_id,
        variants.gene_name,
        variants.chromosome_id,
        variants.snpeff_match,
        variants.quality,
        variants.is_snp,
        variants.ref,
        variants.alt

    FROM genomes
    JOIN variants
        ON genomes.genome_id = variants.genome_id

    WHERE variants.gene_name = ?

    GROUP BY genomes.genome_id;
    ;`

    db.all(query, [req.params.gene_name], 
        function(err, rows){
            if(err){
                console.error(err);
                res.status(500).send('Internal server error');
            } else {
                res.status(200).json(rows);
            }
        });
    });
    
db.close();
 

module.exports = router;