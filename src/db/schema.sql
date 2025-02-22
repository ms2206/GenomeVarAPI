PRAGMA foreign_keys = true;

/* Drop tables */
DROP TABLE IF EXISTS variants;
DROP TABLE IF EXISTS chromosomes;
DROP TABLE IF EXISTS genomes;
DROP TABLE IF EXISTS varients;

/* Create tables */
CREATE TABLE genomes (
    genome_id STRING PRIMARY KEY NOT NULL,
    metadata_json TEXT NOT NULL
);


CREATE TABLE chromosomes (
    chromosome_id STRING NOT NULL,
    genome_id STRING NOT NULL,
    reference STRING NOT NULL,
    start INTEGER NOT NULL,
    end INTEGER NOT NULL,
    PRIMARY KEY (chromosome_id, genome_id)
    FOREIGN KEY (genome_id) REFERENCES genomes(genome_id)
);
    

CREATE TABLE variants (
    variant_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    chromosome_id STRING NOT NULL,
    position INTEGER NOT NULL,
    vcf_id STRING NOT NULL,
    ref STRING NOT NULL,
    alt STRING NOT NULL,
    quality REAL NOT NULL,
    filter STRING NOT NULL,
    info TEXT NOT NULL,
    format TEXT NOT NULL,
    genotype TEXT NOT NULL,
    snpeff_match TEXT,
    is_snp BOOLEAN NOT NULL,
    genome_id STRING NOT NULL,
    gene_name STRING,
    FOREIGN KEY (chromosome_id) REFERENCES chromosomes(chromosome_id),
    FOREIGN KEY (genome_id) REFERENCES genomes(genome_id)
);

    