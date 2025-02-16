PRAGMA foreign_keys = true;

/* Drop tables */
DROP TABLE IF EXISTS varients;
DROP TABLE IF EXISTS chromosomes;
DROP TABLE IF EXISTS genomes;


/* Create tables */


CREATE TABLE genomes (
    genome_id STRING PRIMARY KEY,
    metadata_json TEXT NOT NULL
);



CREATE TABLE chromosomes (
    chromosome_id STRING PRIMARY KEY,
    reference STRING NOT NULL,
    start INTEGER NOT NULL,
    end INTEGER NOT NULL,
);
    

CREATE TABLE varients (
    varient_id INTEGER AUTOINCREMENT PRIMARY KEY,
    chromosome_id STRING NOT NULL,
    position INTEGER NOT NULL,
    ref STRING NOT NULL,
    alt STRING NOT NULL,
    is_snp BOOLEAN NOT NULL,
    quality STRING NOT NULL,
    filter STRING NOT NULL,
    info TEXT NOT NULL,
    genotype TEXT NOT NULL,
    eff TEXT,
    snpeff_match TEXT,
    genome_id STRING NOT NULL,
    FOREIGN KEY (chromosome_id) REFERENCES chromosomes(chromosome_id),
    FOREIGN KEY (genome_id) REFERENCES genomes(genome_id)

    