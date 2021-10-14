# A knowledge graph to orchestrate a multi-organ quantitative assessment of long Covid
Code, data and other information.
 
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

## Source dependencies

- [Python 3](https://www.python.org/)  
- [Owlready2](https://pypi.org/project/Owlready2/): pip install Owlready2  
- [RDFLib](https://rdflib.readthedocs.io/en/stable/gettingstarted.html): pip install rdflib  

This software consists of an ontology and code to create a knowledge graph based upon tabular input data.

## Ontology
- Current version (v0.1, October, 2021): [OWL format](https://raw.githubusercontent.com/JudithGrieves/City-MSc-Project/main/ontology/ont_metric.owl)  
- Created with [Protégé Desktop](https://protege.stanford.edu/)  


The ontology consists of two sub-ontologies:
- metric : information about patients, visits and biomarkers and other data collected during a visit.
- scanner : information about MRI scanner models, their features and manufacturers

## Input data
The input data required are two CSV files:
- metric_data.csv : columns Patient_ID,	Scan, visit,	Age,	Sex,	BMI,	liver_cT1, liver_PDFF	,liver_T2star. 
- scanner_data.csv : columns Scanner Model, Manufacturer, Field Strength, Unit.  
-   See [example data](https://github.com/JudithGrieves/City-MSc-Project/tree/main/data) for required format.


## References

## To use 
1.  To create the knowledge graph(s)
    1. Ensure input study data is in data/metric_data.csv, data/scanner_data.csv
    2. Run code/create_kg_rml.py.  This will create knowledge graph files data/metric_data.ttl, data/scanner_data.ttl

2.  To query the knowledge graph(s)
    1.  Ensure knowledge graph data exists: data/metric_data.ttl, data/scanner_data.ttl
    2.  Run code/SPARQL_examples.py.  
    3.  Output in data/metric_data-sparql[n].csv for reports where n=1, 2, 3
