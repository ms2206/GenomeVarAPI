import vcf
import itertools
import regex as re
import logging
import os
import json
import sqlite3

# set logger at global scope
logger = logging.getLogger()

# set up database connection
conn = sqlite3.connect('./src/db/vcf_db.sqlite3')

# set up cursor
cursor = conn.cursor()

#################
### FUNCTIONS ###
#################

def setup_logging(log_file: str):
    """
    Set up logging configuration.
    """

    
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(log_file, mode='w')

    # set the level of the file handler
    file_handler.setLevel(logging.INFO)
    log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(log_format)

    logger.addHandler(file_handler)

    return logger





    # # set up logging
    # logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_vcf_files(dir: str = './data/raw'):
    """
    Get a list of VCF files in a directory.

    param directory: str: path to the directory containing VCF files.
    return: set: set of VCF files in the directory.
    """
    vcf_files = set()
    for vcf in os.listdir(dir):
        if vcf.endswith('.vcf'):
            full_path = os.path.join(dir, vcf)
            vcf_files.add(full_path)
    return vcf_files


def import_vcf(vcf_filepath: str) -> vcf.Reader:
    """
    Import a VCF file and return a vcf.Reader object with the genome_id added to the metadata object.
    param vcf_filepath: str: path to the VCF file
    return: vcf.Reader: vcf.Reader object
    """

    logger.info(f'Importing VCF file from: {vcf_filepath}')
    vcf_reader = vcf.Reader(open(vcf_filepath, 'r'))

    # consume first row to access genome_id from record
    first_record = next(vcf_reader)

    # access the genome_id from first record
    genome_id = first_record.samples[0].sample

    logger.info(f'Extracted genome_id: {genome_id} from the first record')

    # Rewind the file to the beginning
    vcf_reader = vcf.Reader(open(vcf_filepath, 'r'))

    # add genome_id to metadata object
    vcf_reader.metadata['genome_id'] = genome_id

    logger.info('Added genome_id to VCF reader metadata')

    return vcf_reader


def check_unique_constaints(table: str, cols: list) -> list:
    """
    Function to pass in a table and a list of columns from db_vcf and return the UNIQUE rows.

    param table: str: table name
    param cols: list: column names
    
    return: list: list of tuples of unique values in the column
    """
   
    col_csv = ', '.join(cols)

    # query to get unique values from a column
    qry = f"""
            SELECT DISTINCT {col_csv}
            FROM {table}
            """
    
    qry_result = conn.execute(qry)

    # set comprehension to get unique values
    unique_rows = qry_result.fetchall()

    return unique_rows


def make_chromosome_index(record: vcf.model._Record) -> dict:
    """
    Make an index of the start and end positions for each chromosome in the VCF file.

    param record: vcf.model._Record: record from VCF object.
    return: dict: dictionary with chromosome_id as key and start and end positions as values.
    """

    # create index for each choromosomes
    chr_index = dict()
    
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


def load_chromosomes_table(record: vcf.model._Record, chr_index: dict, metadata: dict) -> None:
    """
    Load the CHROMOSOMES table from records in the VCF file. Using chr_index as index to access start and stop positions.

    param record: vcf.model._Record: record from VCF object.
    param chr_index: dict: dictionary with chromosome_id as key and start and end positions as values.
    param metadata: dict: metadata object from the VCF file
    """

    #TODO: use a function to check if chromosome_id exists in CHROMOSOMES table
    current_keys_list_of_tuples = check_unique_constaints('chromosomes', ['chromosome_id, genome_id'])
    current_chromosomes = [(c[0], c[1]) for c in current_keys_list_of_tuples]


    # extract reference from CHROM field
    reference_genome = record.CHROM.split('ch')[0]

    # extract chromosome_id from CHROM field
    chromosome_id = 'chr' + record.CHROM.split('ch')[1]

    primary_key_check = (chromosome_id, metadata["genome_id"])

    if primary_key_check not in current_chromosomes:

        logger.info(f'Updating CHROMOSOMES table for chromosome_id: {chromosome_id}')
        logger.info(f'Updating CHROMOSOMES table for genome_id: {metadata["genome_id"]}')
        logger.info(f'Updating CHROMOSOMES table for reference: {reference_genome}')
        logger.info(f'Updating CHROMOSOMES table for start: {chr_index[record.CHROM]["start"]}')
        logger.info(f'Updating CHROMOSOMES table for end: {chr_index[record.CHROM]["end"]}')

        # update CHROMOSOMES table
        qry = """
                INSERT INTO chromosomes (chromosome_id, genome_id, reference, start, end)
                VALUES 
                (?, ?, ?, ?, ?)
                """
        
        conn.execute(qry, (chromosome_id, metadata["genome_id"], reference_genome, chr_index[record.CHROM]["start"], chr_index[record.CHROM]["end"]))

        conn.commit()
        logger.info(f'Database commit successful')

    else:
        logger.info(f'Skipping CHROMOSOMES table for chromosome_id | reference : {chromosome_id} {metadata["genome_id"]}')

    return None


def load_genomes_table(metadata: dict) -> None:
    """
    Load the GENOMES table from records in the VCF file.

    param metadata: dict: metadata object from the VCF file
    """

    # get current genomes from GENOMES table
    current_genomes_list_of_tuples = check_unique_constaints('genomes', ['genome_id'])
    current_genomes = [g[0] for g in current_genomes_list_of_tuples]

    logger.info(f'current_genomes: {current_genomes}')


    if metadata["genome_id"] not in current_genomes:

        logger.info(f'Updating GENOMES table for genome_id: {metadata["genome_id"]}')
        logger.info(f'Updating GENOMES table for metadata json: \'{json.dumps(metadata)}\'')

         # update GENOMES table
        qry = """
                INSERT INTO genomes (genome_id, metadata_json)
                VALUES 
                (?, ?)
                """

        conn.execute(qry, (metadata["genome_id"], json.dumps(metadata)))
    
        conn.commit()
        logger.info(f'Database commit successful')


    else:
        logger.info(f'Skipping GENOMES table for genome_id: {metadata["genome_id"]}')
        
    return None


def load_variants_table(record: vcf.model._Record, line_number) -> None:
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
    
    try:
        eff_match = regex.search(record.INFO["EFF"][0])

    except KeyError as e:

        eff_match = None
        logger.warning(
            f'No SnpEff annotation found for {record.INFO} '
            f'on line {line_number} of the VCF file (excluding header and metadata).'
            f'KeyError: {e}'
        )
        

    if eff_match:
        snpEff_match = regex.search(record.INFO["EFF"][0]).group()

    else:
        # empty dict is falsey but retains the same type
        snpEff_match = dict()
    

    logger.info(f'Updating VARIANTS table for chromosome_id: {chromosome_id}')
    logger.info(f'Updating VARIANTS table for POS: {record.POS}')
    logger.info(f'Updating VARIANTS table for ID: {record.ID}')
    logger.info(f'Updating VARIANTS table for REF: {record.REF}')
    logger.info(f'Updating VARIANTS table for ALT: {record.ALT}')
    logger.info(f'Updating VARIANTS table for QUAL: {record.QUAL}')
    logger.info(f'Updating VARIANTS table for FILTER: {record.FILTER}')
    logger.info(f'Updating VARIANTS table for INFO: \'{json.dumps(record.INFO)}\'')
    logger.info(f'Updating VARIANTS table for FORMAT: {record.FORMAT}')
    logger.info(f'Updating VARIANTS table for GENOTYPES: {record.samples}')

    if snpEff_match:
        # logger.info(f'Updating VARIANTS table for EFF: {record.INFO["EFF"][0]}')
        logger.info(f'Updating VARIANTS table for snpEff: {snpEff_match}')
    else:
        # logger.info(f'Skipping VARIANTS table for EFF')
        logger.info(f'Skipping VARIANTS table for snpEff')
    
    logger.info(f'Updating VARIANTS table for is_SNP: {is_SNP}')
    logger.info(f'Updating VARIANTS table for genome_id: {record.samples[0].sample}')
    

############
### MAIN ###
############

def main():
    
    # configure logging
    logger = setup_logging('./src/utils/parse_vcf.log')

    # get VCF files
    for vcf_filepath in get_vcf_files():

        # import specific VCF file
        vcf_file = import_vcf(vcf_filepath)    

        # initialize a line number counter
        line_number = 0

        for record in vcf_file:

            # Log the line number of the current record
            line_number += 1
            logger.info(f'Processing record at line number: {line_number}')

            # create chromosome index specific to the vcf file
            chr_index = make_chromosome_index(record)

            # load_chromosomes_table
            if chr_index:
                load_chromosomes_table(record, chr_index, vcf_file.metadata)
            else:
                logger.info('No chromosome index found')
                raise ValueError('No chromosome index found')

            # load_samples_table
            load_genomes_table(vcf_file.metadata)

            # load_variants_table
            load_variants_table(record, line_number)

            logger.info('Processed record')

        logger.info(f'Processed {line_number} records for {vcf_file.metadata["genome_id"]}.')

    # close the database connection
    conn.close()

if __name__ == '__main__':
    main()