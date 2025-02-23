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
CONDA_ENV_PATH='src/utils/bio_python_base_python_3.9'
SERVER_INIT='src/api/server.js'

echo "Tool started at: $(date +"%d-%m-%Y %H:%M:%S")"

# User option to start server only
if [ "$1" == "--server-only" ]; then
    echo 'Starting the Node.js server...'
    node ${SERVER_INIT}
    exit 0
fi


# Check if the environment 'genomeVarAPI_pyenv_3.9' exists
if [ -d "${ENV_PATH}" ]; then
    echo 'The environment "genomeVarAPI_pyenv_3.9" already exists.'
    # Activate the virtual environment
    source ${ENV_PATH}/bin/activate
    # conda activate genomeVarAPI_pyenv_3.9
else
    echo 'The environment "genomeVarAPI_pyenv_3.9" does not exist. Creating it now...'
    # Create a virtual environment from yml file
    # conda env create --prefix ${CONDA_ENV_PATH} -f src/utils/environment.yml
    # conda activate genomeVarAPI_pyenv_3.9
    # Create a virtual environment
    python3.9 -m venv ${CONDA_ENV_PATH}

    # add sleep to allow for the environment to be created
    sleep 5

    # Activate the virtual environment
    source ${CONDA_ENV_PATH}/genomeVarAPI_pyenv_3.9/bin/activate

    # Install the packages using pip
    pip install regex
    pip install "setuptools<58" --upgrade
    pip install pyvcf
fi

# Check the exit status of the last command
if [ $? -ne 0 ]; then
    echo 'Failed to create the Python environment.'
    exit 1
fi
echo 'Python environment created successfully.'


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
python3 ${VCF_PARSER}

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