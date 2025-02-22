/* Test load vcf database with hardcoded data */


/* Truncate tables */
DELETE FROM variants;
DELETE FROM chromosomes;
DELETE FROM genomes;


INSERT INTO chromosomes (chromosome_id, genome_id, reference, start, end) 
VALUES 
('chr01', 'RF_001', 'SL2.50', 1, 100),
('chr02', 'RF_001', 'SL2.50', 101, 200),
('chr03', 'RF_001', 'SL2.50', 201, 300),
('chr01', 'RF_041', 'SL2.50', 1, 100),
('chr02', 'RF_041', 'SL2.50', 101, 200),
('chr03', 'RF_041', 'SL2.50', 201, 300),
('chr01', 'RF_090', 'SL2.50', 1, 100),
('chr02', 'RF_090', 'SL2.50', 101, 200),
('chr03', 'RF_090', 'SL2.50', 201, 300);

INSERT INTO genomes (genome_id, metadata_json)
VALUES 
('RF_001', '{"fileformat": "VCFv4.1", "samtoolsVersion": ["0.1.18 (r982:295)"], "SnpEffVersion": ["\"3.2 (build 2013-05-23), by Pablo Cingolani\""], "SnpEffCmd": ["\"SnpEff  -no-upstream -no-downstream -ud 0 -csvStats Slyc2.40 /home/assembly/tomato150/reseq/mapped/Heinz/RF_041_SZAXPI009320-94.vcf.gz \""], "reference": "S_lycopersicum_chromosomes.2.50.fa", "genome_id": "RF_001"}'),
('RF_041', '{"fileformat": "VCFv4.1", "samtoolsVersion": ["0.1.18 (r982:295)"], "SnpEffVersion": ["\"3.2 (build 2013-05-23), by Pablo Cingolani\""], "SnpEffCmd": ["\"SnpEff  -no-upstream -no-downstream -ud 0 -csvStats Slyc2.40 /home/assembly/tomato150/reseq/mapped/Heinz/RF_041_SZAXPI009320-94.vcf.gz \""], "reference": "S_lycopersicum_chromosomes.2.50.fa", "genome_id": "RF_041"}'),
('RF_090', '{"fileformat": "VCFv4.1", "samtoolsVersion": ["0.1.18 (r982:295)"], "SnpEffVersion": ["\"3.2 (build 2013-05-23), by Pablo Cingolani\""], "SnpEffCmd": ["\"SnpEff  -no-upstream -no-downstream -ud 0 -csvStats Slyc2.40 /home/assembly/tomato150/reseq/mapped/Heinz/RF_041_SZAXPI009320-94.vcf.gz \""], "reference": "S_lycopersicum_chromosomes.2.50.fa", "genome_id": "RF_090"}');

INSERT INTO variants (chromosome_id, position, vcf_id, ref, alt, quality, filter, info, format, genotype, snpeff_match, is_snp, genome_id)
VALUES 
('chr01', 1, 'None', 'A', '[T]', '222.0', 'None', '{"DP": 37, "VDB": 0.0371, "AF1": 1.0, "AC1": 2.0, "DP4": [0, 0, 16, 17], "MQ": 60, "FQ": -126.0, "EFF": ["INTERGENIC(MODIFIER||||||||||1)"]}', 'GT:PL:DP:GQ', '[Call(sample=RF_041, CallData(GT=1/1, PL=[255, 99, 0], DP=33, GQ=99))]', 'HIGH', 1, 'RF_041'),
('chr01', 2, 'None', 'A', '[C]', '222.0', 'None', '{"DP": 37, "VDB": 0.0371, "AF1": 1.0, "AC1": 2.0, "DP4": [0, 0, 16, 17], "MQ": 60, "FQ": -126.0, "EFF": ["INTERGENIC(MODIFIER||||||||||1)"]}', 'GT:PL:DP:GQ', '[Call(sample=RF_041, CallData(GT=1/1, PL=[255, 99, 0], DP=33, GQ=99))]', 'HIGH', 1, 'RF_041'),
('chr01', 3, 'None', 'A', '[G]', '222.0', 'None', '{"DP": 37, "VDB": 0.0371, "AF1": 1.0, "AC1": 2.0, "DP4": [0, 0, 16, 17], "MQ": 60, "FQ": -126.0, "EFF": ["INTERGENIC(MODIFIER||||||||||1)"]}', 'GT:PL:DP:GQ', '[Call(sample=RF_041, CallData(GT=1/1, PL=[255, 99, 0], DP=33, GQ=99))]', 'HIGH', 1, 'RF_041'),
('chr01', 4, 'None', 'A', '[T]', '222.0', 'None', '{"DP": 37, "VDB": 0.0371, "AF1": 1.0, "AC1": 2.0, "DP4": [0, 0, 16, 17], "MQ": 60, "FQ": -126.0, "EFF": ["INTERGENIC(MODIFIER||||||||||1)"]}', 'GT:PL:DP:GQ', '[Call(sample=RF_041, CallData(GT=1/1, PL=[255, 99, 0], DP=33, GQ=99))]', 'HIGH', 1, 'RF_041')
;