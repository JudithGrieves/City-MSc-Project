# -*- coding: utf-8 -*-
'''
Created on 29 June 2021

@author: judith.grieves@city.ac.uk

INM363 Individual Project

UPDATE TO WRITE CSV OUTPUT FROM SPARQL_EXAMPLES
AMEND TO RETURN METRIC TYPE/SCANNER MODEL LABELS W/O FULL URI PATH?


This code loads the (inferred ontology) and created triples data and executes
SPARQL queries over the graph.

SPARQL to create output results to mimic the input test data CSV to allow a comparison
to be made for testing purposes.

'''
from rdflib import Graph
import csv

import os
from os.path import dirname, abspath

from write_sparql_file import write_sparql



def query_all(g,outfile):
    
    '''
    Query to return all the CSV columns that were converted to RDF
    To be used as part of a test plan
    ''' 
    qres = g.query(
    """SELECT DISTINCT  ?patient_label   ?visit_label  ?sex ?age ?bmi ?liver_cT1   ?liver_PDFF ?liver_T2Star ?scanner_label ?fieldsstr  WHERE
                {
                 ?visit a ?ScanVisit .
                 ?visit rdfs:label ?visit_label .
                 ?visit psp:isAttendedBy ?patient .  
                 ?patient a ?Patient .
                 ?patient rdfs:label ?patient_label .
                 ?patient psp:PatientSex ?sex .  
                 ?patient psp:PatientAge ?age . 
                 ?patient psp:PatientBMI ?bmi . 
                 ?scanner psp:usedInVisit ?visit .
                 ?scanner rdfs:label ?scanner_label .
                 ?scanner psp:FieldStrength ?fieldsstr
                 {?metric1 psp:isMetricForPatient  ?patient  .
                 ?metric1 psp:MetricValue ?liver_cT1 .
                 ?metric1 a <http://www.perspectum.com/resources/liver_cT1> .}
                 UNION
                 {?metric2 psp:isMetricForPatient  ?patient  .
                 ?metric2 psp:MetricValue ?liver_PDFF .
                 ?metric2 a <http://www.perspectum.com/resources/liver_PDFF> .}
                 UNION
                 {?metric3 psp:isMetricForPatient  ?patient  .
                 ?metric3 psp:MetricValue ?liver_T2Star .
                 ?metric3 a <http://www.perspectum.com/resources/liver_T2Star> .}
} GROUP BY ?patient_label 
    ORDER BY ASC(?patient_label) """) 
    
    #    FILTER regex(?metric_type, "Named", "i" )

    print("Show all Data")   
    header='"PatientID","Visit","Age","Sex","BMI","liver_cT1","liver_PDFF","liver_T2Star","Scanner","Field Strength"'  
    write_sparql(outfile,header,qres,1,1)  
    
def main():
    
    print("\nStarting SPARQLqueries")
    
    data_dir = os.path.join(dirname(dirname(abspath(__file__))), 'data')
    output_dir = data_dir
        
        
    inFile="test_data14.ttl" 
    outFile=inFile.replace(".ttl", "-")+"replicate.csv"  
    
    inFile = os.path.join(data_dir,inFile)
    outFile = os.path.join(output_dir,outFile)
    

    
    print("Load a graph from input file: ", inFile)
    g = Graph()    
    g.parse(inFile, format="ttl")         
    print("Loaded '" + str(len(g)) + "' triples.\n")    

    # run SPARQL queries against the loaded graph
    query_all(g,outFile)   
    
    print("\nFinished SPARQLqueries")
          

Display=False       

if __name__ == "__main__":
    main()
