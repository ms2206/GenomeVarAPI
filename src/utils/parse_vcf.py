# conda create --name genomeVarAPI_pyenv_3.9 python=3.9
# conda activate genomeVarAPI_pyenv_3.9
# pip install "setuptools<58" --upgrade
# pip install pyvcf

import vcf
import itertools
import regex as re
import logging
import os

# set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def get_vcf_files(dir: str = './data/raw'):
    """
    Get a list of VCF files in a directory.

    param directory: str: path to the directory containing VCF files.
    return: set: set of VCF files in the directory.
    """
    vcf_files = set()
    for vcf in os.listdir(dir):
        if vcf.endswith('.vcf'):
            vcf_files.add(vcf)
    return vcf_files


def get_current_samples() -> list:
    """
    Get the current samples in the SAMPLES table.
    return: list: list of current samples
    """
    pass


def load_samples_table(metadata: dict) -> None:
    """
    Load the SAMPLES table from records in the VCF file.

    param metadata: dict: metadata object from the VCF file
    """

    #TODO: use a function to check if genome_id exists in SAMPLES table
    current_samples = get_current_samples()
    # for testing
    current_samples = ['RF_001', 'RF_041', 'RF_090']

    logging.info(f'Updating SAMPLES table for genome_id: {metadata["genome_id"]}')
    logging.info(f'Updating SAMPLES table for metadata json: {metadata}')

    return None


def load_chromosomes_table(record: vcf.model._Record, chr_index: dict) -> None:
    """
    Load the CHROMOSOMES table from records in the VCF file. Using chr_index as index to access start and stop positions.

    param record: vcf.model._Record: record from VCF object.
    param chr_index: dict: dictionary with chromosome_id as key and start and end positions as values.
    """

    #TODO: use a function to check if chromosome_id exists in CHROMOSOMES table

    # extract reference from CHROM field
    reference_genome = record.CHROM.split('ch')[0]

    # extract chromosome_id from CHROM field
    chromosome_id = 'chr' + record.CHROM.split('ch')[1]

    logging.info(f'Updating CHROMOSOMES table for reference: {reference_genome}')
    logging.info(f'Updating CHROMOSOMES table for chromosome_id: {chromosome_id}')
    logging.info(f'Updating CHROMOSOMES table for start: {chr_index[record.CHROM]["start"]}')
    logging.info(f'Updating CHROMOSOMES table for end: {chr_index[record.CHROM]["end"]}')

    return None

def make_chromosome_index(record: vcf.model._Record) -> dict:
    """
    Make an index of the start and end positions for each chromosome in the VCF file.

    param record: vcf.model._Record: record from VCF object.
    return: dict: dictionary with chromosome_id as key and start and end positions as values.
    """

    # extract the chromosome, start, and end positions
    chrom = record.CHROM
    start = record.POS

    # calculate end as start position plus length (-1 python is inclusive).
    end = start + len(record.REF) - 1

    if chrom not in chr_index:
        chr_index[chrom] = {'start': start, 'end': end}

    else:
        # update start if the record start is less than the index start 
        if start < chr_index[chrom]['start']:
            chr_index[chrom]['start'] = start

        # update end if the record end is greater than the index end
        if end >= chr_index[chrom]['end']:
            chr_index[chrom]['end'] = end

    return chr_index



def load_variants_table(record: vcf.model._Record) -> None:
    """
    Load the VARIANTS table from records in the VCF file.

    param record: vcf.model._Record: record from VCF object.
    """

    # extract chromosome_id from CHROM field
    chromosome_id = 'chr' + record.CHROM.split('ch')[1]

    # set is_SNP bool
    if len(record.ALT) != 1:
        is_SNP = 0
    else:
        is_SNP = 1

    # extract SnpEff annotation
    regex = re.compile(r'HIGH|MODERATE|LOW')
    eff_match = regex.search(record.INFO["EFF"][0])
    if eff_match:
        # print('Match')
        snpEff_match = regex.search(record.INFO["EFF"][0]).group()
        # print(regex.search(record.INFO["EFF"][0]).group())
    else:
        snpEff_match = 'Unknown'
    

    logging.info(f'Updating VARIANTS table for chromosome_id: {chromosome_id}')
    logging.info(f'Updating VARIANTS table for POS: {record.POS}')
    logging.info(f'Updating VARIANTS table for ID: {record.ID}')
    logging.info(f'Updating VARIANTS table for REF: {record.REF}')
    logging.info(f'Updating VARIANTS table for ALT: {record.ALT}')
    logging.info(f'Updating VARIANTS table for is_SNP: {is_SNP}')
    logging.info(f'Updating VARIANTS table for QUAL: {record.QUAL}')
    logging.info(f'Updating VARIANTS table for FILTER: {record.FILTER}')
    logging.info(f'Updating VARIANTS table for INFO: {record.INFO}')
    logging.info(f'Updating VARIANTS table for FORMAT: {record.FORMAT}')
    logging.info(f'Updating VARIANTS table for GENOTYPES: {record.samples}')
    logging.info(f'Updating VARIANTS table for EFF: {record.INFO["EFF"][0]}')
    logging.info(f'Updating VARIANTS table for genome_id: {record.samples[0].sample}')
    logging.info(f'Updating VARIANTS table for snpEff: {snpEff_match}')
    


def import_vcf(vcf_filepath: str) -> vcf.Reader:
    """
    Import a VCF file and return a vcf.Reader object with the genome_id added to the metadata object.
    param vcf_filepath: str: path to the VCF file
    return: vcf.Reader: vcf.Reader object
    """

    logging.info(f'Importing VCF file from: {vcf_filepath}')
    vcf_reader = vcf.Reader(open(vcf_filepath, 'r'))

    # consume first row to access genome_id from record
    first_record = next(vcf_reader)

    # access the genome_id from first record
    genome_id = first_record.samples[0].sample

    logging.info(f'Extracted genome_id: {genome_id} from the first record')

    # Rewind the file to the beginning
    vcf_reader = vcf.Reader(open(vcf_filepath, 'r'))

    # add genome_id to metadata object
    vcf_reader.metadata['genome_id'] = genome_id

    logging.info('Added genome_id to VCF reader metadata')

    return vcf_reader


test_vcf = import_vcf('./data/raw/RF_001_subset.vcf')

# create index for each choromosomes
chr_index = dict()

for record in test_vcf:

    # create chromosome index
    chr_index = make_chromosome_index(record)

    # load_chromosomes_table
    if chr_index:
        load_chromosomes_table(record, chr_index)
    else:
        logging.info('No chromosome index found')
        raise ValueError('No chromosome index found')

    # load_samples_table
    load_samples_table(test_vcf.metadata)

    # load_variants_table
    load_variants_table(record)

 
    logging.info('Processed record')



