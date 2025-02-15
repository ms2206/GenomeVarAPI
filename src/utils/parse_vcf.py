# conda create --name genomeVarAPI_pyenv_3.9 python=3.9
# conda activate genomeVarAPI_pyenv_3.9
# pip install "setuptools<58" --upgrade
# pip install pyvcf

import vcf

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

    print(f'Updating SAMPLES table for genome_id: {metadata["genome_id"]}')
    print(f'Updating SAMPLES table for metadata json: {metadata}')

    return None


def load_chromosomes_table(record: vcf.model._Record) -> None:
    """
    Load the CHROMOSOMES table from records in the VCF file.

    param record: vcf.model._Record: record object from the VCF file
    """

    #TODO: use a function to check if chromosome_id exists in CHROMOSOMES table

    # extract reference from CHROM field
    reference_genome = record.CHROM.split('ch')[0]

    # extract chromosome_id from CHROM field
    chromosome_id = 'chr' + record.CHROM.split('ch')[1]

    print(f'Updating CHROMOSOMES table for reference: {reference_genome}')
    print(f'Updating CHROMOSOMES table for chromosome_id: {chromosome_id}')
    return None


def import_vcf(vcf_filepath: str) -> vcf.Reader:
    """
    Import a VCF file and return a vcf.Reader object with the genome_id added to the metadata object.
    param vcf_filepath: str: path to the VCF file
    return: vcf.Reader: vcf.Reader object
    """

    vcf_reader = vcf.Reader(open(vcf_filepath, 'r'))

    # add genome_id to metadata object
    first_record = next(vcf_reader)

    # access the first record
    genome_id = first_record.samples[0].sample

    # add genome_id to metadata
    vcf_reader.metadata['genome_id'] = genome_id

    return vcf_reader


test_vcf = import_vcf('../../data/raw/RF_001_subset.vcf')


for record in test_vcf:
    ## update samples table

    # load_samples_table
    load_samples_table(test_vcf.metadata)

    # load_chromosomes_table
    load_chromosomes_table(record)

    # print(f' CHROM: {record.CHROM}')
    # print(f' POS: {record.POS}')
    # print(f' ID: {record.ID}')
    # print(f' REF: {record.REF}')
    # print(f' ALT: {record.ALT}')
    # print(f' QUAL: {record.QUAL}')
    # print(f' FILTER: {record.FILTER}')
    # print(f' INFO: {record.INFO}')
    # print(f' EFF: {record.INFO["EFF"][0]}')
    # print(f' GENOTYPES: {record.samples}')
    # print(f' GENOME_ID: {record.samples[0].sample}') 

    print('')
    break
    
    


# add genome_id to metadata
 

