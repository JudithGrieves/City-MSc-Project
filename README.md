# City-MSc-Project
Code, data and other information: a Knowledge Graph to orchestrate a multi-organ quantitative assessment of long-COVID
 
1.  To create the knowledge graph
    1. Ensure input study data is in data/metric_data.csv, data/scanner_data.csv
    2. Run code/create_kg_rml.py.  This will create knowledge graph files data/metric_data.ttl, data/scanner_data.ttl

2.  To query the knowledge graph(s)
    1.  Ensure knowledge graph data exists: data/metric_data.ttl, data/scanner_data.ttl
    2.  Run code/SPARQL_examples.py.  
    3.  Output in data/metric_data-sparql[n].csv for reports where n=1, 2, 3

