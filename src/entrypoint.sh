#!/bin/bash

################################################################################
# Script Name: entrypoint.sh
# Description: This script acts as a wrapper to start the application.
#              The script checks if the required python environment exists,
#              if not, it creates the environment. It then initializes the
#              SQLite database, parses VCF files, and starts the Node.js server.
#
# Parameters: --server-only: Start the Node.js server only.
# Dependencies: sqlite3, python, node.js      
# Author: Matthew Spriggs
# Date: 2025-02-23
# Usage: ./entrypoint.sh [--server-only]
################################################################################

# Constants
DB_FILEPATH='src/db/vcf_db.sqlite3'
DB_SCHEMA='src/db/schema.sql'
VCF_PARSER='src/utils/parse_vcf.py'
ENV_PATH='src/utils/genomeVarAPI_pyenv_3.9'
PACKAGE_JSON='./package.json'
SERVER_INIT='src/api/server.js'
DATE=$(date +"%d-%m-%Y %H:%M:%S")

echo "[LOG] - ${DATE} -- Tool started at: ${DATE}"

# User option to start server only, this option assumes the node modules are installed, if not run without this flag first.
if [ "$1" == "--server-only" ]; then
    echo "[LOG] - ${DATE} -- Starting the Node.js server..."
    node ${SERVER_INIT}
    exit 0
fi


# Check if the environment 'genomeVarAPI_pyenv_3.9' exists
if [ -d "${ENV_PATH}" ]; then
    echo "[LOG] - ${DATE} -- The environment "genomeVarAPI_pyenv_3.9" already exists."
    # Activate the virtual environment
    source ${ENV_PATH}/bin/activate
else
    echo "[LOG] - ${DATE} -- The environment 'genomeVarAPI_pyenv_3.9' does not exist. Creating it now..."
    # Create a virtual environment
    python3 -m venv ${ENV_PATH}

    # add sleep to allow for the environment to be created
    sleep 5

    # Activate the virtual environment
    source ${ENV_PATH}/bin/activate

    # Install the packages using pip
    pip install regex
    pip install "setuptools<58" --upgrade
    pip install pyvcf
fi

# Check the exit status of the last command
if [ $? -ne 0 ]; then
    echo "[LOG] - ${DATE} -- Failed to create the Python environment."
    exit 1
fi
echo "[LOG] - ${DATE} -- Python environment loaded successfully."


# Initialize the database
echo "[LOG] - ${DATE} -- Initializing the SQLite database..."
sqlite3 ${DB_FILEPATH} < ${DB_SCHEMA}

# Check the exit status of the last command
if [ $? -ne 0 ]; then
    echo "[LOG] - ${DATE} -- Failed to apply schema to the SQLite database."
    exit 1
fi
echo "[LOG] - ${DATE} -- Schema applied successfully."

# Run python tool to parse VCF files
echo "[LOG] - ${DATE} -- Parsing VCF file using Python script..."
echo "[LOG] - ${DATE} -- Note: This may take a while depending on CPU size and the size of the VCF file(s) provided."
python3 ${VCF_PARSER}

# Check the exit status of the last command
if [ $? -ne 0 ]; then
    echo "[LOG] - ${DATE} -- Failed to parse VCF using the Python script."
    exit 1
fi
echo "[LOG] - ${DATE} -- VCF parsed successfully."

# Load node modules
if [ -f ${PACKAGE_JSON} ]; then
    echo "[LOG] - ${DATE} -- Installing Node.js modules..."
    npm install
    echo "[LOG] - ${DATE} -- Node.js modules installed successfully."
else
    echo "[LOG] - ${DATE} -- No package.json file found. Ensure node is installed."
    echo "[LOG] - ${DATE} -- Run 'node -v' to check if node is installed."
    echo "[LOG] - ${DATE} -- Run 'npm -v' to check if npm is installed."
    exit 1
fi


# Start the server
echo "[LOG] - ${DATE} -- Starting the Node.js server..."
node ${SERVER_INIT}

# Check the exit status of the last command
if [ $? -ne 0 ]; then
    echo "[LOG] - ${DATE} -- Failed to start the Node.js server."
    exit 1
fi
echo "[LOG] - ${DATE} -- Node.js server started successfully."

# Print the finish time of the script
echo "[LOG] - ${DATE} -- Script finished at: ${DATE}"