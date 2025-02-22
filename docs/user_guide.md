<h1> GenomeVarAPI USER GUIDE </h1>

<h3> Overview</h3>
<div>

GenomeVarAPI is a lunix-based tool for parsing and interacting with VCF (Variant Call Format) files.
The tool has 3 elements: a python parsing module, an sqlite database, and a REST API for end-user interface.

</div>

<h3> Getting Started</h3>
<div>
To download the tool: <br>
```
git clone https://github.com/ms2206/GenomeVarAPI.git
```

TODO: Add docker image.

<h5>Initialize the database</h5>

A schema `src/db/schema.sql` script is provided which contains table declarations for the database. This must be run first.
To run this file execute the below code:<br>
```
sqlite3 src/db/vcf_db.sqlite3 < src/db/schema.sql
```

<h5>Populate the database</h5>

One of the core features of this tool as a VCF parser written in python `src/utils/parse_vcf.py`.

The python tool requires a virtual environment setup. It is recommend to use <a href="https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html">conda</a> for this installation. The tool requires python version 3.9.*.

```
conda env create -f src/utils/environment.yml
```

<h6>Alternative installation:</h6>
```
conda create --name genomeVarAPI_pyenv_3.9 python=3.9
conda activate genomeVarAPI_pyenv_3.9
conda install regex
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





</div>

<h3> Features and Functionality</h3>

<h3> Support and Feedback</h3>