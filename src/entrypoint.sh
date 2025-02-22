#!/bin/bash

# constants
DB_FILEPATH='src/db/vcf_db.sqlite3'
DB_SCHEMA='src/db/schema.sql'
VCF_PARSER='src/utils/parse_vcf.py'
SERVER_INIT='src/api/server.js'

echo "Tool started at: $(date +"%d-%m-%Y %H:%M:%S")"

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