<h1>GenomeVarAPI User Guide </h1>

Technical Documentation is best viewed from GitHub. See <a href='https://github.com/ms2206/GenomeVarAPI/tree/main'>https://github.com/ms2206/GenomeVarAPI/tree/main</a>.

<h2>Overview</h2>
<div id='overveiw-section'>

GenomeVarAPI is a linux-based tool for parsing and interacting with VCF (Variant Call Format) files.
The tool has 3 elements: a python parsing module, an sqlite database, and a REST API for end-user interface.

<em> The tool is not guaranteed to work on Windows PC and makes no claims to be platform independent. </em>


<img src='./figures/overview.svg' alt='Flowchart of overview'>

</div>


<h2>Getting Started</h2>
<div id='getting-started-section'>
Tool Dependencies: python, node, npm.
<h3>Download the tool</h3>

GitHub clone:
```
git clone https://github.com/ms2206/GenomeVarAPI.git
```

Change directory: <br>
```
cd GenomeVarAPI
```

Run the entrypoint.sh: <br>
```
Usage: ./src/entrypoint.sh [--server-only]
```
Description: This script acts as a wrapper to start the application. The script checks if the required python environment exists,
if not, it creates the environment. It then initializes the SQLite database, parses VCF files, installs the node dependencies and
starts the Node.js server. <br>

The <code>--server-only</code> option is useful if you just want to load the server without re-populating the database. This option assumes
node the node packages are already installed. <br>

<h3>Adding VCF files</h3>
Any VCF files placed in the <code>./data.raw</code> directory will be parsed by the tool upon initalization. The current release supports
parsing VCF files annotated using SnpEff legacy 'EFF' format. The 'ANN' is not yet supported but will be made avaliable in a future release.
Considering gene annotations, the tool is limited to extracting gene names for 'mRNA' labeled genes, a future release will expand on these capabilities. <br><em>Note: if your annotations do not follow this format the tool should still complete but their annotations and gene names
will not be entered into the database</em><br><br>



Flowchart for entrypoint.sh: <br>
<img src='./figures/entrypoint.svg' alt='Flowchart of entrypoint.sh'>

<i>TODO: Add docker image. use ./src/entrypoint.sh as a wrapper.</i>

</div>
<h2>Interacting with endpoints</h2>
Upon running the entrypoint script you shall have a server running on http://localhost:3000.
<br><br>
The API has 8 main endpoints:

<div id='api-endpoints-list'>
<ul>
<li><code>api/genomes</code></li>
<li><code>api/genomes/:genome_id</code></li>
<li><code>api/genomes/:genome_id/variants</code></li>
<li><code>api/genomes/:genome_id/snps</code></li>
<li><code>api/genomes/:genome_id/indels</code></li>
<li><code>api/genomes/:genome_id/:chromosome_id/:mbp?</code></li>
<li><code>api/variants/gene/:gene_name</code></li>
<li><code>api/variants/:genome_id</code></li>
</ul><br>
</div>

<div id='api-endpoints-examples'>
<ol>
<li>List all VCF in database.</li>
<code>http://localhost:3000/api/genomes</code><br><br>

<li>List metadata from a given VCF in database.</li>
<code>http://localhost:3000/api/genomes/RF_041/</code><br><br>

<li>List number of variants in each VCF {genome_id} by chromosome.</li>
<code>http://localhost:3000/api/genomes/RF_001/variants</code><br><br>

<li>List number of SNPs in each VCF {genome_id} by chromosome.</li>
<code>http://localhost:3000/api/genomes/RF_001/snps</code><br><br>

<li>List number of INDELs in each VCF {genome_id} by chromosome.</li>
<code>http://localhost:3000/api/genomes/RF_001/indels</code><br><br>

<li>List genes impacted by moderate or high impact variants in a specific chromosome region for a specific VCF {genome_id}.</li>
<em>:mbp is an optional parameter to be the number of mbp from the start of the chromosome. If NULL then the whole chromosome will be shown.</em><br>
<code>http://localhost:3000/api/genomes/RF_001/chr03/20</code><br><br>

<li>List genomes which contains a variant that impacts a specific gene.</li>
<code>http://localhost:3000/api/variants/gene/Solyc03g006480.1.1</code><br><br>

<li>List vartiants from a specific genome.</li>
<code>http://localhost:3000/api/variants/RF_041</code><br><br>
</ol>
</div>
</div>

<h2>Documentation</h2>
<ul>
<li><a href='./user_guide.md'>User Documentation</a></li>
<li><a href='./database_technical_docs.md'>Database Technical Documentation</a></li>
<li><a href='./parse_vcf_technical_docs.md'>VCF Parser Technical Documentation</a></li>
<li><a href='./server_technical_docs.md'>API Technical Documentation</a></li>
</ul>

<h3> Support and Feedback</h3>
<b>Support Email</b>:<br>
For general inquiries and technical support contact: <em>matspriggs@gmail.com</em><br><br>

<b>Social Media</b>:<br>
<a href='https://www.linkedin.com/in/matthew-spriggs-324215121/'>LinkedIn</a><br>
