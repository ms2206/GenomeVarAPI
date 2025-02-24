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

limitations of ReGex:: two regex queries offer limitaions EFF (what is ANN or other)mRNA what if not mRNA gene

GENOTYPES is poorly formatted


if you add same vcf file to /data/raw it will likely update varients table -- look like duplicated SNPs and INDELs

<h2>Documentation</h2>
<ul>
<li><a href='docs/user_guide.md'>User Documentation</a></li>
<li><a href='docs/database_technical_docs.md'>Database Technical Documentation</a></li>
<li><a href='docs/parse_vcf_technical_docs.md'>VCF Parser Technical Documentation</a></li>
<li><a href='docs/server_technical_docs.md'>API Technical Documentation</a></li>
</ul>