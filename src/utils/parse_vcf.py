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
#TODO: think about relative path for db connection

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

    try:
        #TODO: add try except block for file not found error
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
    
    except Exception as e:
        logger.error(f'Error importing VCF file: {vcf_filepath}')
        logger.error(f'Error: {e}')

    # Log the error and continue processing the next file
    logger.error(f'Skipping file due to import error: {vcf_filepath}')
    return None    # how will the app will handle downstream?


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


def make_chromosome_index(chr_index: dict, record: vcf.model._Record, metadata: dict) -> dict:
    """
    Make an index of the start and end positions for each chromosome in the VCF file.

    param chr_index: dict: dictionary with geneome_id + chromosome as key and start and end positions as values.
    param record: vcf.model._Record: record from VCF object.
    param metadata: dict: metadata object from the VCF file
    return: dict: dictionary with chromosome_id as key and start and end positions as values.
    """
    
    # extract the chromosome, start, and end and genome_id positions
    
    genome_id = metadata["genome_id"]
    chrom = 'chr' + record.CHROM.split('ch')[1] # convert ch{xx} to chr{xx}
    dict_key = f'{genome_id}-{chrom}'

    start = record.POS
    end = start + len(record.REF) - 1    # calculate end as start position plus length (-1 python is inclusive).
    
    # check if dict_key exists in chr_index
    if dict_key not in chr_index:

    #if chrom not in chr_index:
        chr_index[dict_key] = {'start': start, 'end': end}

    else:
        # update start if the record start is less than the index start 
        if start < chr_index[dict_key]['start']:
            chr_index[dict_key]['start'] = start

        # update end if the record end is greater than the index end
        if end >= chr_index[dict_key]['end']:
            chr_index[dict_key]['end'] = end

    return chr_index


def load_chromosomes_table(record: vcf.model._Record, metadata: dict) -> None:
    """
    Load the CHROMOSOMES table from records in the VCF file. 
    note: start and end positions are committed in this function but may be updated later in the process.

    param record: vcf.model._Record: record from VCF object.
    param metadata: dict: metadata object from the VCF file
    """

    # check if chromosome_id exists in CHROMOSOMES table
    current_keys_list_of_tuples = check_unique_constaints('chromosomes', ['chromosome_id, genome_id'])
    current_chromosomes = [(c[0], c[1]) for c in current_keys_list_of_tuples]

    # extract reference from CHROM field
    reference_genome = record.CHROM.split('ch')[0]

    # extract chromosome_id from CHROM field
    chromosome_id = 'chr' + record.CHROM.split('ch')[1]

    # extract the start and end positions
    start = record.POS
    end = start + len(record.REF) - 1    # calculate end as start position plus length (-1 python is inclusive).

    primary_key_check = (chromosome_id, metadata["genome_id"])

    if primary_key_check not in current_chromosomes:

        logger.info(f'Updating CHROMOSOMES table for chromosome_id: {chromosome_id}')
        logger.info(f'Updating CHROMOSOMES table for genome_id: {metadata["genome_id"]}')
        logger.info(f'Updating CHROMOSOMES table for reference: {reference_genome}')
        logger.info(f'Updating CHROMOSOMES table for start: {start}')
        logger.info(f'Updating CHROMOSOMES table for end: {end}')

        # update CHROMOSOMES table
        qry = """
                INSERT INTO chromosomes (chromosome_id, genome_id, reference, start, end)
                VALUES 
                (?, ?, ?, ?, ?)
                """
        
        conn.execute(qry, (chromosome_id, metadata["genome_id"], reference_genome, start, end))

        conn.commit()
        logger.info(f'Database commit successful')

    else:
        logger.info(f'Skipping CHROMOSOMES table for chromosome_id | reference : {chromosome_id} {metadata["genome_id"]}')

    return None


def update_chromosomes_start_end_positions(chr_index: dict) -> None:
    """
    Update the CHROMOSOMES table with the start and end positions from the chromosome index.
    note: chr_index is only accurate after all records have been processed.

    param chr_index: dict: dictionary with chromosome_id as key and start and end positions as values.

    """
    
    keys = list(chr_index.keys())
    
    # extract genome_id from the keys in the chr_index
    intermedite_list = [intermedite_list.split('-') for intermedite_list in keys]
    genome_id = set([i[0] for i in intermedite_list])

    # extract chromosomes from the keys in the chr_index
    chromosomes = set([i[1] for i in intermedite_list]) # ugly but works

    # make a list of tuples for the current genome_id and chromosome_id
    database_keys = [(list(genome_id)[0], c) for c in chromosomes]

    # loop through the database_keys and retrieve the start and end positions
    for key in database_keys:
        qry = """
                SELECT start, end
                FROM chromosomes
                WHERE chromosome_id = ? AND genome_id = ?
                """   
        
        db_start_end = conn.execute(qry, (key[1], key[0])).fetchone()

        # update db if the db start is greater than the current chr_index start
        if db_start_end[0] > chr_index[f'{key[0]}-{key[1]}']["start"]:
            logger.info(f'Updating CHROMOSOMES table for start at {key}: {chr_index[f"{key[0]}-{key[1]}"]["start"]}')
            conn.execute('UPDATE chromosomes SET start = ? WHERE chromosome_id = ? AND genome_id = ?', (chr_index[f'{key[0]}-{key[1]}']["start"], key[1], key[0]))
            conn.commit()
            logger.info(f'Database commit successful')
        
        # update db if the db end is less than the current chr_index end
        if db_start_end[1] < chr_index[f'{key[0]}-{key[1]}']["end"]:
            logger.info(f'Updating CHROMOSOMES table for end at {key}: {chr_index[f"{key[0]}-{key[1]}"]["end"]}')
            conn.execute('UPDATE chromosomes SET end = ? WHERE chromosome_id = ? AND genome_id = ?', (chr_index[f'{key[0]}-{key[1]}']["end"], key[1], key[0]))
            conn.commit()
            logger.info(f'Database commit successful')

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
    if len(record.ALT[0]) != 1:
        is_SNP = 0
    else:
        is_SNP = 1

    # extract SnpEff annotation
    SnpEff_regex = re.compile(r'HIGH|MODERATE|LOW')
    
    try:
        eff_match = SnpEff_regex.search(record.INFO["EFF"][0])

    except KeyError as e:

        eff_match = None
        logger.warning(
            f'No SnpEff annotation found for {record.INFO} '
            f'on line {line_number} of the VCF file (excluding header and metadata).'
            f'KeyError: {e}'
        )
      
    if eff_match:
        snpEff_match = SnpEff_regex.search(record.INFO["EFF"][0]).group()

    else:
        # empty dict is falsey but retains the same type
        snpEff_match = dict() 

   
    # extract gene annotation
    gene_name_regex = re.compile(r'mRNA:([^|]+)') # bit hardcoding here; what if NOT mRNA gene... # ugly object type

    try:
        gene_name_match = gene_name_regex.search(record.INFO["EFF"][0])
    
    except KeyError as e:

        gene_name_match = None
        logger.warning(
            f'No gene annotation found for {record.INFO} '
            f'on line {line_number} of the VCF file (excluding header and metadata).'
            f'KeyError: {e}'
        )

    if gene_name_match:
        gene_name = gene_name_regex.search(record.INFO["EFF"][0]).group(1)

    else:
        gene_name = None    # might not be necessary could use snpEff_match is falsey

    # update VARIANTS table
    # query depends on whether snpEff_match is empty or not
    if snpEff_match:
       
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
        logger.info(f'Updating VARIANTS table for snpEff: {snpEff_match}')
        logger.info(f'Updating VARIANTS table for is_SNP: {is_SNP}')
        logger.info(f'Updating VARIANTS table for genome_id: {record.samples[0].sample}')
        logger.info(f'Updating VARIANTS table for gene_name: {gene_name}')

         # update VARIANTS table
        qry = """
                INSERT INTO variants (chromosome_id, position, vcf_id, ref, alt, quality, filter, info, format, genotype, snpEff_match, is_SNP, genome_id, gene_name)
                VALUES
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
        
        conn.execute(qry, (chromosome_id, record.POS, str(record.ID), record.REF, str(record.ALT), record.QUAL, str(record.FILTER), json.dumps(record.INFO), record.FORMAT, str(record.samples), snpEff_match, is_SNP, record.samples[0].sample, gene_name))

        conn.commit()

        logger.info(f'Database commit successful')
    else:
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
        logger.info(f'Skipping VARIANTS table for snpEff')
        logger.info(f'Updating VARIANTS table for is_SNP: {is_SNP}')
        logger.info(f'Updating VARIANTS table for genome_id: {record.samples[0].sample}')
        logger.info(f'Skipping VARIANTS table for gene_name')

        # update VARIANTS table
        qry = """
                INSERT INTO variants (chromosome_id, position, vcf_id, ref, alt, quality, filter, info, format, genotype, is_SNP, genome_id)
                VALUES
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
        
        conn.execute(qry, (chromosome_id, record.POS, str(record.ID), record.REF, str(record.ALT), record.QUAL, str(record.FILTER), json.dumps(record.INFO), record.FORMAT, str(record.samples), is_SNP, record.samples[0].sample))

        conn.commit()

        logger.info(f'Database commit successful')
   

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

        # make a chromosome index
        chr_index = dict()  

        # initialize a line number counter
        line_number = 0

        for record in vcf_file:

            try:

                # Log the line number of the current record
                line_number += 1
                logger.info(f'Processing record at line number: {line_number}')

                # create chromosome index specific to the vcf file
                chr_index = make_chromosome_index(chr_index, record, vcf_file.metadata)

                # load_chromosomes_table
                load_chromosomes_table(record, vcf_file.metadata)
                
                # load_samples_table
                load_genomes_table(vcf_file.metadata)

                # load_variants_table
                load_variants_table(record, line_number)

                logger.info('Processed record')

            except Exception as e:
                logger.error(f'Error processing record at line number: {line_number}')
                logger.error(f'Error: {e}')
                continue

        # update start and end positions in CHROMOSOMES table
        update_chromosomes_start_end_positions(chr_index) # all records have been processed by this point
        
        logger.info(f'Processed {line_number} records for {vcf_file.metadata["genome_id"]}.')
        

    # close the database connection
    conn.close()

if __name__ == '__main__':
    main()