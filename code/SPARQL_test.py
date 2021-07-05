# -*- coding: utf-8 -*-
'''
Created on 29 June 2021

@author: judith.grieves@city.ac.uk

INM363 Individual Project

MAKE SURE ADDED TO GITHUB
UPDATE TO MATCH TEST_dATA.CSV
UPDATE TO WRITE CSV OUTPUT FROM SPARQL_EXAMPLES
AMEND TO RETURN METRIC TYPE/SCANNER MODEL LABELS W/O FULL URI PATH?
AMEND TO PIVOT RESULTS TO SHOW METRIC TYPES AS SEPARATE COLUMNS


This code loads the (inferred ontology) and created triples data and executes
SPARQL queries over the graph.

SPARQL to create output results to mimic the input test data CSV to allow a comparison
to be made for testing purposes.

'''
from rdflib import Graph
import csv

import os
from os.path import dirname, abspath



def query_all(g):
    
    '''
    Query to return all the CSV columns that were converted to RDF
    To be used as part of a test plan
    '''    
    qres = g.query(
    """SELECT DISTINCT  ?patient_label ?visit_label ?sex ?age ?bmi  ?metric_value ?metric_type ?scanner ?fieldsstr WHERE
                {?visit a ?ScanVisit .
                 ?visit rdfs:label ?visit_label .
                 ?visit psp:isAttendedBy ?patient .  
                 ?patient rdfs:label ?patient_label .
                 ?patient psp:PatientSex ?sex .  
                 ?patient psp:PatientAge ?age . 
                 ?patient psp:PatientBMI ?bmi . 
                 ?metric psp:isMetricForPatient  ?patient  .
                 ?metric psp:MetricValue ?metric_value .
                 ?metric a  ?metric_type . 
                 ?scanner psp:usedInVisit ?visit .
                 ?scanner psp:FieldStrength ?fieldsstr
    FILTER(!CONTAINS(LCASE(STR(?metric_type)),"namedindividual"))} 
    ORDER BY ASC(?visit_label) ASC(?patient_label)  ASC(?metric_type)""") 
    
    #    FILTER regex(?metric_type, "Named", "i" )

    print("Show all Data")   
    print("PatientID","Visit ID","Age","Sex","BMI","Metric Value","Metric Type")   
    for row in qres:
        print(row.patient_label,row.visit_label,row.age,row.sex,row.bmi,row.metric_value,row.metric_type,row.scanner,row.fieldsstr)    
        
         
def main():
    
    print("\nStarting SPARQLqueries")
    
    data_dir = os.path.join(dirname(dirname(abspath(__file__))), 'data')
    output_dir = os.path.join(dirname(dirname(abspath(__file__))), 'SPARQLresults')
        
        
    inFile="test_data14.ttl" 
    outFile=inFile.replace(".ttl", "-")+"-results.csv"  
    
    inFile = os.path.join(data_dir,inFile)
    outFile = os.path.join(output_dir,outFile)
    

    
    print("Load a graph from input file: ", inFile)
    g = Graph()    
    g.parse(inFile, format="ttl")         
    print("Loaded '" + str(len(g)) + "' triples.\n")    

    # run SPARQL queries against the loaded graph
    query_all(g)
    #query2(g,outFile)   
    
    print("\nFinished SPARQLqueries")
          

Display=False       

if __name__ == "__main__":
    main()
