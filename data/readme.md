The data folder contains:
- CSV files required by the transformation and load process
- TTL knowledge graph files produced by the transformation and load process
- CSV result files produced by the test queries

Details:

- metric_data.csv, scanner_data.csv : input CSV files for metric and scanner data
- metric_map.rml.ttl, scan_map.rml.ttl : RML mapping files
- metric_data.ttl, scanner_data.ttl : knowledge graph files created by RMLmapper input CSV files and RML mapping files
- metric_data-sparql1/2/3.csv : SPARQL query results
- metric_data-replicate.csv: system test query results
- metric_data-compare.csv : Test comparison results
