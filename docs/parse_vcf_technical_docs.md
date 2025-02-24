<h1>VCF Parser Technical Documentation</h1>

<h2>Overview</h2>
One of the core features of this tool as a VCF parser written in python `src/utils/parse_vcf.py`.

The python tool requires a virtual environment setup. The tool requires python version 3.9.*.

It is reccomened to use the standard installation from the <a href='./user_guide.md'>User Documentation</a> using the
<code>./src/entrypoint.sh</code>. However, should you will to run this module separately follow the below steps.


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
user with tools to inspect the inner workings of the python code.

For example:
To identify warning messages;<br>
```
grep "WARNING" src/utils/parse_vcf.log
```
<h2>Design Comments</h2>

Python was chosen as the language of choice for this module, in part because there exist existing libraires to parse VCF files. pysam and pyvcf were considered for this tool. pyvcf was chosen for it's lightweight simplicity. Additionally, Python was preferred over a fully integrated JavaScript front-end/back-end solution due to the developers' greater proficiency with Python.

The tool as it stands represent MPV (minimul viable product) meeting user needs assigned in the <a href='../I-BIX-DAT Assignment Brief 2025-1.pdf'>Design Brief</a>



why was python chosen instead of just a js application, design choice

limitations of ReGex:: two regex queries offer limitaions EFF (what is ANN or other)mRNA what if not mRNA gene

GENOTYPES is poorly formatted


if you add same vcf file to /data/raw it will likely update varients table -- look like duplicated SNPs and INDELs

<h2>Documentation</h2>
<ul>
<li><a href='./user_guide.md'>User Documentation</a></li>
<li><a href='./database_technical_docs.md'>Database Technical Documentation</a></li>
<li><a href='./parse_vcf_technical_docs.md'>VCF Parser Technical Documentation</a></li>
<li><a href='./server_technical_docs.md'>API Technical Documentation</a></li>
</ul>