#!/bin/bash

################################################################################
# Script Name: entrypoint.sh
# Description: This script acts as a wrapper to start the application.
#              The script checks if the required python environment exists,
#              if not, it creates the environment. It then initializes the
#              SQLite database, parses VCF files, and starts the Node.js server.
#
# Parameters: --server-only: Start the Node.js server only.
# Dependencies: conda, sqlite3, python, node.js      
# Author: Matthew Spriggs
# Date: 2025-02-23
# Usage: ./entrypoint.sh [--server-only]
################################################################################

# Constants
DB_FILEPATH='src/db/vcf_db.sqlite3'
DB_SCHEMA='src/db/schema.sql'
VCF_PARSER='src/utils/parse_vcf.py'
SERVER_INIT='src/api/server.js'

echo "Tool started at: $(date +"%d-%m-%Y %H:%M:%S")"

# User option to start server only
if [ "$1" == "--server-only" ]; then
    echo 'Starting the Node.js server...'
    node ${SERVER_INIT}
    exit 0
fi


# Check if the environment 'genomeVarAPI_pyenv_3.9' exists
if conda env list | grep -q 'genomeVarAPI_pyenv_3.9'; then
    echo 'The environment "genomeVarAPI_pyenv_3.9" already exists.'
    # Initialize conda environment 
    conda init bash 
    conda activate genomeVarAPI_pyenv_3.9
else
    echo 'The environment "genomeVarAPI_pyenv_3.9" does not exist. Creating it now...'
    # Create a virtual environment from yml file
    # Initialize conda environment
    conda init bash
    conda env create -f src/utils/environment.yml
    conda activate genomeVarAPI_pyenv_3.9
fi

# Initialize the database
echo 'Initializing the SQLite database...'
sqlite3 ${DB_FILEPATH} < ${DB_SCHEMA}

# Check the exit status of the last command
if [ $? -ne 0 ]; then
    echo 'Failed to apply schema to the SQLite database.'
    exit 1
fi
echo 'Schema applied successfully.'

# Run python tool to parse VCF files
echo 'Parsing VCF file using Python script...'
echo 'Note: This may take a while depending on the size of the VCF file(s) provided.'
python ${VCF_PARSER}

# Check the exit status of the last command
if [ $? -ne 0 ]; then
    echo 'Failed to parse VCF using the Python script.'
    exit 1
fi
echo 'VCF parsed successfully.'

# Start the server
echo 'Starting the Node.js server...'
node ${SERVER_INIT}

# Check the exit status of the last command
if [ $? -ne 0 ]; then
    echo 'Failed to start the Node.js server.'
    exit 1
fi
echo 'Node.js server started successfully.'

# Print the finish time of the script
echo "Script finished at: $(date +"%d-%m-%Y %H:%M:%S")"