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

import os
from os.path import dirname, abspath

from write_sparql_file import write_sparql


def debug_query_all(g,outfile):
    
    '''
    Query to return all the CSV columns that were converted to RDF
    To be used as part of a test plan
    ''' 
    # ?fsunit not in original TabularData sheet but included here to show 
    # that the scanner data is being picked up from a separate KG
    qres = g.query(
    """SELECT DISTINCT  ?fs ?scanner   WHERE
                { 
                 ?fs scn:isFieldStrengthForScanner ?scanner .}
                """) 

    print("Show all Data")   
    for row in qres:
        print(row.fs, row.scanner)

def query_all(g,outfile):
    
    '''
    Query to return all the CSV columns that were converted to RDF
    To be used as part of a test plan
    ''' 
    # ?fsunit not in original TabularData sheet but included here to show 
    # that the scanner data is being picked up from a separate KG
    qres = g.query(
    """SELECT DISTINCT  ?patient_label   ?visit_label ?age  ?sex ?bmi  \
                        ?liver_cT1   ?liver_PDFF ?liver_T2Star ?scanner_label?fsval ?fsunitlabel  ?manf_label \
                       WHERE
                {
                 ?visit a psp:ScanVisit .
                 ?visit rdfs:label ?visit_label .
                 ?visit psp:isAttendedBy ?patient .  
                 ?patient a psp:Patient .
                 ?patient rdfs:label ?patient_label .
                 ?patient psp:PatientSex ?sex .  
                 ?patient psp:PatientAge ?age . 
                 ?patient psp:PatientBMI ?bmi . 
                 ?scanner psp:usedInVisit ?visit .
                 ?scanner rdfs:label ?scanner_label .
                 ?scanner a scn:MRIScannerModel .
                 ?manf a scn:ScannerManufacturer .
                 ?manf rdfs:label ?manf_label .
                 ?manf scn:isMakerOf ?scanner.
                 OPTIONAL {?fs scn:isFieldStrengthForScanner ?scanner .
                           ?fs qudt:value ?fsval .
                           ?fs qudt:unit ?fsunit . 
                           ?fsunit rdfs:label ?fsunitlabel .  }
                 
                 
                 {?metric1 psp:isMetricForPatient  ?patient  .
                 ?metric1 qudt:value ?liver_cT1 .
                 ?metric1 a psp:liver_cT1  .}
                 UNION
                 {?metric2 psp:isMetricForPatient  ?patient  .
                 ?metric2 qudt:value ?liver_PDFF .
                 ?metric2 a psp:liver_PDFF .}
                 UNION
                 {?metric3 psp:isMetricForPatient  ?patient  .
                 ?metric3 qudt:value ?liver_T2Star .
                 ?metric3 a psp:liver_T2Star .}
} GROUP BY ?patient_label 
    ORDER BY ASC(?visit_label) ASC(?patient_label) """) 

    print("Show all Data")   
    header='"PatientID","Visit","Age","Sex","BMI","liver_cT1","liver_PDFF","liver_T2Star","Scanner","Field Strength","Unit","Manufacturer"'  
            
    write_sparql(outfile,header,qres,1,1)  
 
    
def main():
    
    print("\nStarting SPARQLqueries")
    
    data_dir = os.path.join(dirname(dirname(abspath(__file__))), 'data')
    output_dir = data_dir
        
        
    inFile1="metrics_data.ttl" 
    inFile2="scanner_data.ttl" 
    outFile=inFile1.replace(".ttl", "-")+"replicate.csv"  
    
    inFile1 = os.path.join(data_dir,inFile1)
    inFile2 = os.path.join(data_dir,inFile2)
    outFile = os.path.join(output_dir,outFile)
    
    g = Graph()    
    g.parse(inFile1, format="ttl")         
    print("Loaded '" + str(len(g)) + "' triples.\n",inFile1)  
    g.parse(inFile2, format="ttl")         
    print("Loaded '" + str(len(g)) + "' triples.\n",inFile2)    
    
    inFile3="http://qudt.org/2.1/vocab/unit"
    g.parse(inFile3, format="ttl")         
    print("Loaded '" + str(len(g)) + "' triples.\n",inFile3)    

    # run SPARQL queries against the loaded graph
    query_all(g,outFile)   
    
    #debug_query_all(g,outFile) 
    
    print("\nFinished SPARQLqueries")
          

Display=False       

if __name__ == "__main__":
    main()
