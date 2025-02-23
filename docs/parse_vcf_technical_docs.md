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


why was python chosen instead of just a js application, design choice

limitations of ReGex



<h3>Documentation</h3>
<ul>
<li><a href='http://localhost:3000/'>User Documentation</a></li>
<li><a href='http://localhost:3000/database-technical-docs'>Database Techincal Documentation</a></li>
<li><a href='http://localhost:3000/parser-technical-docs'>VCF Parser Techincal Documentation</a></li>
<li><a href='http://localhost:3000/api-technical-docs'>API Techincal Documentation</a></li>