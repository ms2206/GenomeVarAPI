# requires pandoc
# pip install pandoc


pandoc -o database_technical_docs.html database_technical_docs.md;
pandoc -o user_guide.html user_guide.md;
pandoc -o parse_vcf_technical_docs.html parse_vcf_technical_docs.md;
pandoc -o server_technical_docs.html server_technical_docs.md;