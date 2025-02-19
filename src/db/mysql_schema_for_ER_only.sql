/* Drop tables */
DROP TABLE IF EXISTS varients;
DROP TABLE IF EXISTS chromosomes;
DROP TABLE IF EXISTS genomes;


/* Create tables */
CREATE TABLE genomes (
    genome_id VARCHAR(255) PRIMARY KEY,
    metadata_json TEXT NOT NULL
);

CREATE TABLE chromosomes (
    chromosome_id VARCHAR(255) NOT NULL,
    genome_id VARCHAR(255) NOT NULL,
    reference VARCHAR(255) NOT NULL,
    start INT NOT NULL,
    end INT NOT NULL,
    PRIMARY KEY (chromosome_id, genome_id),
    FOREIGN KEY (genome_id) REFERENCES genomes(genome_id)
);

CREATE TABLE varients (
    varient_id INT AUTO_INCREMENT PRIMARY KEY,
    chromosome_id VARCHAR(255) NOT NULL,
    position INT NOT NULL,
    vcf_id VARCHAR(255) NOT NULL,
    ref VARCHAR(255) NOT NULL,
    alt VARCHAR(255) NOT NULL,
    quality FLOAT NOT NULL,
    filter VARCHAR(255) NOT NULL,
    info TEXT NOT NULL,
    format TEXT NOT NULL,
    genotype TEXT NOT NULL,
    snpeff_match TEXT,
    is_snp BOOLEAN NOT NULL,
    genome_id VARCHAR(255) NOT NULL,
    gene_name TEXT,
    FOREIGN KEY (chromosome_id) REFERENCES chromosomes(chromosome_id),
    FOREIGN KEY (genome_id) REFERENCES genomes(genome_id)
);