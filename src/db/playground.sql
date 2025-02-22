/* 
Space to play around with SQL queries
*/

-- List all VCF in database
SELECT 
    DISTINCT genome_id
FROM genomes;

/*
RF_001
RF_041
RF_090
*/

-- List number of varients in each VCF {genome_id}
-- GROUP BY chromosome_id
SELECT 
     
    genome_id,
    chromosome_id,
    COUNT(*) AS num_variants

FROM variants

GROUP BY genome_id, chromosome_id;

/*
RF_001|chr01|75
RF_001|chr02|38
RF_001|chr03|81
RF_001|chr04|77
...
*/

-- List number of SNPs in each VCF {genome_id}
-- GROUP BY chromosome_id
SELECT 
     
    genome_id,
    chromosome_id,
    COUNT(*) AS num_variants

FROM variants
WHERE is_snp = 1

GROUP BY genome_id, chromosome_id;

/*
RF_001|chr01|66
RF_001|chr02|34
RF_001|chr03|77
RF_001|chr04|71
*/

-- List number of INDELs in each VCF {genome_id}
-- GROUP BY chromosome_id
SELECT 
     
    genome_id,
    chromosome_id,
    COUNT(*) AS num_variants

FROM variants
WHERE is_snp = 0

GROUP BY genome_id, chromosome_id;

/*
RF_001|chr01|9
RF_001|chr02|4
RF_001|chr03|4
RF_001|chr04|6
*/

-- List genes impacted by moderate or high impact variants in a specific 
-- chromosome region for a specific VCF {genome_id}

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
AND variants.snpeff_match IN ('HIGH')
AND variants.genome_id = 'RF_041'
AND variants.chromosome_id = 'chr03'
AND variants.position > start
AND variants.position < start + (20 * 1000000) -- 20 is user variable

LIMIT 5;

-- /*
-- gene_name|genome_id|chromosome_id|snpeff_match
-- Solyc03g006480.1.1|RF_041|chr03|HIGH
-- Solyc03g033330.2.1|RF_041|chr03|HIGH
-- */

-- -- List sample which contains a variant that impacts a specific gene
SELECT 
    DISTINCT
    genomes.genome_id
FROM genomes
JOIN variants
    ON genomes.genome_id = variants.genome_id

WHERE variants.gene_name = 'Solyc03g006480.1.1'

-- I could improve the query to something more useful

SELECT 
    genomes.genome_id,
    variants.variant_id,
    variants.gene_name,
    variants.chromosome_id,
    variants.snpeff_match,
    variants.quality,
    variants.is_snp,
    variants.alt


FROM genomes
JOIN variants
    ON genomes.genome_id = variants.genome_id

WHERE variants.gene_name = 'Solyc03g006480.1.1'

GROUP BY genomes.genome_id;