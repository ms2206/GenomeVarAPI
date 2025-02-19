/* 
Space to play around with SQL queries
*/

-- List all VCF in database
-- SELECT 
--     DISTINCT genome_id
-- FROM genomes;

/*
RF_001
RF_041
RF_090
*/

-- List number of varients in each VCF {genome_id}
-- GROUP BY chromosome_id
-- SELECT 
     
--     genome_id,
--     chromosome_id,
--     COUNT(*) AS num_variants

-- FROM variants

-- GROUP BY genome_id, chromosome_id;

/*
RF_001|chr01|75
RF_001|chr02|38
RF_001|chr03|81
RF_001|chr04|77
...
*/

-- List number of SNPs in each VCF {genome_id}
-- GROUP BY chromosome_id
-- SELECT 
     
--     genome_id,
--     chromosome_id,
--     COUNT(*) AS num_variants

-- FROM variants
-- WHERE is_snp = 1

-- GROUP BY genome_id, chromosome_id;

/*
RF_001|chr01|66
RF_001|chr02|34
RF_001|chr03|77
RF_001|chr04|71
*/

-- List number of INDELs in each VCF {genome_id}
-- GROUP BY chromosome_id
-- SELECT 
     
--     genome_id,
--     chromosome_id,
--     COUNT(*) AS num_variants

-- FROM variants
-- WHERE is_snp = 0

-- GROUP BY genome_id, chromosome_id;

/*
RF_001|chr01|9
RF_001|chr02|4
RF_001|chr03|4
RF_001|chr04|6
*/

-- List genes impacted by moderate or high impact variants in a specific 
-- chromosome region for a specific VCF {genome_id}

SELECT 
    variants.genome_id,
    variants.chromosome_id,
    variants.info,    
    variants.snpeff_match

    

FROM variants
JOIN chromosomes
ON variants.chromosome_id = chromosomes.chromosome_id

