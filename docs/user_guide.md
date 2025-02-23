<h1>GenomeVarAPI USER GUIDE </h1>

<h2>Overview</h2>
<div>

GenomeVarAPI is a lunix-based tool for parsing and interacting with VCF (Variant Call Format) files.
The tool has 3 elements: a python parsing module, an sqlite database, and a REST API for end-user interface.

<em> The tool is not gauenteed to work on Windows PC and makes no claims to be platform independant. </em>

</div>

<h2>Getting Started</h2>
<div>
To download the tool: <br>

```
git clone https://github.com/ms2206/GenomeVarAPI.git
```

TODO: Add docker image. use ./src/entrypoint.sh as a wrapper.

1. <b>Option 1</b> <br>
./src/entrypoint.sh 

./src/entrypoint.sh --server-only

##########
##########
##########
<h5>>> Initialize the database</h5>

A schema `src/db/schema.sql` script is provided which contains table declarations for the database. This must be run first.
To run this file execute the below code:<br>
```
sqlite3 src/db/vcf_db.sqlite3 < src/db/schema.sql
```

<h5>>> Populate the database</h5>

One of the core features of this tool as a VCF parser written in python `src/utils/parse_vcf.py`.

The python tool requires a virtual environment setup. It is recommend to use <a href="https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html">conda</a> for this installation. The tool requires python version 3.9.*.

```
# Create a virtual environment from yml file
conda env create -f src/utils/environment.yml
```

Alternative installation:
An alternative way to set up the required python environment without installing conda is as follows.

```
# Create a virtual environment
python3.9 -m venv genomeVarAPI_pyenv_3.9

# Activate the virtual environment
source genomeVarAPI_pyenv_3.9/bin/activate

# Install the packages using pip
pip install regex
pip install "setuptools<58" --upgrade
pip install pyvcf
```

The python tool `src/utils/parse_vcf.py` can be run using the below command: <br>
```
python src/utils/parse_vcf.py
```

This tool will parse each VCF files in `src/data/raw` and load them to the database `src/db/vcf_db.sqlite3`.

<strong>Note: This step is quite CPU intensive and can take upto 10 minuets.</strong> 

The tool output logs can be found at `src/utils/parse_vcf.log`. The logs are quite verbos but provide the 
user with tool to inspect the inner workings of the python code.

For example:
To identify warning messages;<br>
```
grep "WARNING" src/utils/parse_vcf.log
```

<h5>Interacting with endpoints</h5>

The API has 6 main endpoints:
<div>
* api/genomes<br>
* api/genomes/:genome_id/variants<br>
* api/genomes/:genome_id/snps<br>
* api/genomes/:genome_id/indels<br>
* api/genomes/:genome_id/:chromosome_id/:mbp?<br>
* api/variants/gene/:gene_name<br>
<br>
</div>

<div>
1. List all VCF in database.<br>
`http://localhost:3000/api/genomes`

2. List number of variants in each VCF {genome_id} by chromosome.<br>
`http://localhost:3000/api/genomes/RF_001/variants`

3. List number of SNPs in each VCF {genome_id} by chromosome.<br>
`http://localhost:3000/api/genomes/RF_001/snps`

4. List number of INDELs in each VCF {genome_id} by chromosome.<br>
`http://localhost:3000/api/genomes/RF_001/indels`

5. List genes impacted by moderate or high impact variants in a specific chromosome region for a specific VCF {genome_id}. <br>
<em>:mbp is an optional parameter to be the number of mbp from the start of the chromosome. If NULL then the whole chromosome will be shown.</em><br>
`http://localhost:3000/api/genomes/RF_001/chr03/20`

6. List sample which contains a variant that impacts a specific gene.<br>
`http://localhost:3000/api/variants/gene/Solyc03g006480.1.1`
</div>


```
# check node exists
node -v
nmp -v
```
```
npm install express
npm install sqlite3
npm install path
```

</div>

<h3> Features and Functionality</h3>

<h3> Support and Feedback</h3>