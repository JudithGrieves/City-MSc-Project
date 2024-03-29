# A knowledge graph to orchestrate a multi-organ quantitative assessment of long Covid
Ontologies, code, data and other information to create a knowledge graph of MRI study biomarkers and patient metrics from tabular data.
 
## Report Abstract 
The results and metrics produced in biomedical imaging clinical studies are an invaluable resource for 
analysis and future work but only if they are well-structured and easily accessible. This project 
investigates whether Semantic Web Technologies are a useful means of achieving these objectives. 
The project analyses data gathered for a single study on long Covid patients, models its meaning in an 
ontology and stores it in a knowledge graph. SPARQL queries are provided to extract subsets of the 
data for given parameters. We evaluate several current methods, tools and standards used to make the 
creation task easier, more efficient and repeatable: the Pay-as-you-go methodology, RDF Mapping 
Language and the FAIR data standards. The resulting proof of concept design and build answers 
given business competency questions and should provide a useful starting point to take forward into 
building a comprehensive and useful tool.


## User Guide
[Installation](https://github.com/JudithGrieves/City-MSc-Project#source-dependencies) 
- [Source Dependencies](https://github.com/JudithGrieves/City-MSc-Project#source-dependencies) 

[Overview](https://github.com/JudithGrieves/City-MSc-Project#ontology) 
- [Ontology](https://github.com/JudithGrieves/City-MSc-Project#ontology) 
- [Folders](https://github.com/JudithGrieves/City-MSc-Project#Folders) 
- [Input Data](https://github.com/JudithGrieves/City-MSc-Project#input-data)  

[Running the Code](https://github.com/JudithGrieves/City-MSc-Project#creating-the-knowledge-graph) 
- [Creating the Knowledge Graph](https://github.com/JudithGrieves/City-MSc-Project#creating-the-knowledge-graph) 
- [Querying the Knowledge Graph](https://github.com/JudithGrieves/City-MSc-Project#querying-the-knowledge-graph) 


[FAQS](https://github.com/JudithGrieves/City-MSc-Project#faqs)  


[Outstanding Software Issues](https://github.com/JudithGrieves/City-MSc-Project#outstanding-software-issues) 


## Source dependencies

- [Python 3](https://www.python.org/)  
- [Owlready2](https://pypi.org/project/Owlready2/): pip install Owlready2  
- [RDFLib](https://rdflib.readthedocs.io/en/stable/gettingstarted.html): pip install rdflib  
- [RMLmapper](https://github.com/RMLio/rmlmapper-java/releases/): download latest version of rmlmapper.jar 

## Folders
[data](https://github.com/JudithGrieves/City-MSc-Project/tree/main/data) contains
- input CSV files for metric and scanner data: metric_data.csv, scanner_data.csv
- RML mapping files : metric_map.rml.ttl, scan_map.rml.ttl  
- knowledge graph files created by RMLmapper : metric_data.ttl, scanner_data.ttl 
- SPARQL query results: metric_data-sparql1/2/3.csv
- system test query results: metric_data-replicate.csv
- Test comparison results: metric_data-compare.csv

[code](https://github.com/JudithGrieves/City-MSc-Project/tree/main/code) contains:
- main knowledge graph transform and load program: create_kg_rml.py
- business competency queries: SPARQL_examples.py
- system test queries: SPARQL_test.py
- queries to show the ontology classes: SPARQL_ontology
- module to write queries to CSV file: write_sparql_file.py

[ontology](https://github.com/JudithGrieves/City-MSc-Project/tree/main/ontology) for each sub-ontology (metric, scanner, liver), contains:
- ontology extract file in 3 formats: .OWL, .XML, .TTL
- Graph diagram of the ontology: .JPG 
- Protege diagram format file: .graph

## Ontology
- Current version (v0.1, October, 2021): [OWL format](https://raw.githubusercontent.com/JudithGrieves/City-MSc-Project/main/ontology/ont_metric.owl)  
- Created with [Protégé Desktop](https://protege.stanford.edu/)  


The ontology consists of three sub-ontologies:
- metric : information about patients, visits and biomarkers and other data collected during a visit.
- scanner : information about MRI scanner models, their features and manufacturers.
- liver : context of the liver and health assessment data featured in the metrics ontology - this ontology has no associated knowledge graph.

## Input data
The input data required are two CSV files:
- metric_data.csv : columns Patient_ID,	Scan, visit,	Age,	Sex,	BMI,	liver_cT1, liver_PDFF	,liver_T2star, Scanner Model. 
- scanner_data.csv : columns Scanner Model, Manufacturer, Field Strength, Unit.  

See [example data](https://github.com/JudithGrieves/City-MSc-Project/tree/main/data) for required format.

-  Columns must be named as the examples but can be in any order.
-  There is no limit to the number of rows loaded.
- Scanner Models referenced in metric_data should exist in scanner_data but this integrity is not enforced.


## Creating the knowledge graph

-  To create the knowledge graph(s)
    1. Ensure the required input study data is in data/metric_data.csv, data/scanner_data.csv
    2. Run code/create_kg_rml.py.  This will create knowledge graph files data/metric_data.ttl, data/scanner_data.ttl  



## Querying the knowledge graph

- To query the knowledge graph(s)
    1.  Ensure knowledge graph files exist: data/metric_data.ttl, data/scanner_data.ttl
    2.  Run code/SPARQL_examples.py.  
    3.  Output is written to data/metric_data-sparql[n].csv for reports where n=1, 2, 3


## FAQS

### Data Mappings
- Input CSV data must have the columns specified in the RML mapping files; column names must match exactly, including case and spaces, though they may appear in any order and may contain other non-specified columns (which will be ignored).
-  Metric and Scanner columns must appear in separate CSV files, as in the examples given here. 
-  Any Scanner Model specified in Metric CSV must also appear in the Scanner CSV
-  column 'sex' can only contain valid values 'M', 'F', 'NA'.

## Outstanding software issues

- The original metrics were given to 12 decimal places but were returned from knowledge graph as 8 d.p.s - these are defined as an XML double data type - if 12 d.p.s are required another type should be used.
- a failed RML load, due to data anomalies, is not notifying as an error - to be improved to report and stop the process. 
- 'Not quantifiable' was successfully loaded into the metric value field but you might want to think in future about what other non-numeric status could be relevant for the value fields and model differently.

## References
