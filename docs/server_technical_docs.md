Technical Documentation is best viewed from GitHub. See <a hfre='https://github.com/ms2206/GenomeVarAPI/tree/main'>https://github.com/ms2206/GenomeVarAPI/tree/main</a>.

<h2>Overview</h2>
The tool comes with an API which is served on `http://localhost:3000/api/` to allows the user to interact with the database.

The server is hosted from `src/api/server.js` using a router defined at `src/api/routes/router.js`. The tool assumes node and nmp are installed, if not follow the set up instructions on the nodesource <a href='https://github.com/nodesource/distributions'>GitHub</a>. To verify the installation, run the following commands:

```
# check node exists
node -v
npm -v
```

The standard installation via <code>./src/entrypoint.sh</code> will run `npm install` for you.

There is a useful option to run <code>./src/entrypoint.sh --server-only</code> if you have already populated the database and you just want to interact with the API. This option means you don't have to reload the database each time. 


<h2>Endpoints</h2>
The <a href='./user_guide.md'>User Documentation</a> does a good job explaining how to interact with the endpoints, so refer to this page for interacting with the links.

This section will discuss design choices of some of the endpoints.

<code>api/genomes</code>
This endpoint is useful to see at a glance what genomes you have in the database. It returns a simple list of dictionaries with the genome_id key. I envision it being used to first get the genomes and then calling some of the other endpoints. e.g. 

```
#!/bin/python
import requests

url='http://localhost:3000/api/genomes'
headers = {'accept': 'application/json'}
response = requests.get(url, headers=headers)

json = response.json()

for genome in json['genome_id']:
    print(genome)
```

<li><code>api/genomes/:genome_id</code></li>
This end point will list metadata from a given VCF in database. This is useful if the user wants to inspect the high-level information about the file. It returns a list of dictionaries, with a 'metadata_json' key. Inside this key is a JSON object with data on fileformats, samtoolsVersions, any annotations and reference geneome used.



<h2>Documentation</h2>
<ul>
<li><a href='./user_guide.md'>User Documentation</a></li>
<li><a href='./database_technical_docs.md'>Database Technical Documentation</a></li>
<li><a href='./parse_vcf_technical_docs.md'>VCF Parser Technical Documentation</a></li>
<li><a href='./server_technical_docs.md'>API Technical Documentation</a></li>
</ul>