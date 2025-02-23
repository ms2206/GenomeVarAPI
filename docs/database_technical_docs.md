<h5>>> Initialize the database</h5>

A schema `src/db/schema.sql` script is provided which contains table declarations for the database. This must be run first.
To run this file execute the below code:<br>
```
sqlite3 src/db/vcf_db.sqlite3 < src/db/schema.sql
```