# -*- coding: utf-8 -*-
'''
Created on 29 June 2021

@author: judith.grieves@city.ac.uk

INM363 Individual Project

NEEDS TO RETURN :FEMALE/MALE ENUMERATED TYPES W/O FULL URI PATH?


This code loads the (inferred ontology) and created triples data and executes
SPARQL queries over the graph.

SPARQL to create output results to mimic the input test data CSV to allow a comparison
to be made for testing purposes.

ISSUES:
    metrics should also be metrics for visit (as well as patient) - add multiple patient visits to test data to test this
    using this triple in query ?visit omet:usesScannerModel  ?scanner  . instead of ?scanner omet:usedInVisit ?visit .

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
    """SELECT DISTINCT  ?a ?b ?c ?d ?e ?f ?g WHERE
                { 
                 OPTIONAL {?a oscn:isFieldStrengthForScanner ?b .
                           ?fs oscn:FieldStrengthValue ?fsval .
                           ?fs oscn:FieldStrengthUnit ?fsunit . 
                           ?fsunit rdfs:label ?fsunitlabel .  }.
                 }
    ORDER BY ASC(?a)  ASC(?b)
                """) 

    print("Show all Data")   
    for row in qres:
        print(row.a,  row.b, row.c,  row.d, row.e, row.f, row.g)
        
    '''
    ?a a owl:NamedIndividual .
                 ?a omet:hasPatientSex ?c .
    '''

def query_all(g,outfile):
    
    '''
    Query to return all the CSV columns that were converted to RDF
    To be used as part of a test plan
    RDFS:LABEL FOR SEX ENUMERATED TYPE NOT WORKING
    ''' 
    # ?fsunit not in original TabularData sheet but included here to show 
    # that the scanner data is being picked up from a separate KG
    qres = g.query(
    """SELECT DISTINCT  ?patient_label   ?visit_label ?age  ?sex ?bmi  \
                        ?livercT1   ?liverPDFF ?liverT2Star ?scanner_label \
                          ?fsval ?fsunitlabel  ?manf_label \
                       WHERE
                {
                 ?visit a omet:Imaging_Scan_Visit .
                 ?visit rdfs:label ?visit_label .
                 ?visit omet:isAttendedBy ?patient .  
                 ?patient a omet:Patient .
                 ?patient rdfs:label ?patient_label .
                 ?patient omet:hasPatientSex ?sex . 
                  OPTIONAL {?sex  rdfs:label ?label . }
                 ?visit omet:usesScannerModel  ?scanner  .
                 ?scanner rdfs:label ?scanner_label .
                 ?scanner a oscn:MRIScannerModel .
                 ?manf a oscn:ScannerManufacturer .
                 ?manf rdfs:label ?manf_label .
                 ?manf oscn:isMakerOfScanner ?scanner.
                 OPTIONAL {?fs oscn:isFieldStrengthForScanner ?scanner .
                           ?fs oscn:FieldStrengthValue ?fsval .
                           ?fs oscn:FieldStrengthUnit ?fsunit . 
                           ?fsunit rdfs:label ?fsunitlabel .  }
                 
                 
                 {?PatientAge omet:isMetricForPatient  ?patient  .
                  ?PatientAge omet:isMetricForVisit  ?visit  .
                 ?PatientAge qudt:value ?age .
                 ?PatientAge a omet:PatientAge  .}
                 
                 {?PatientBMI omet:isMetricForPatient  ?patient  .
                  ?PatientBMI omet:isMetricForVisit  ?visit  .
                 ?PatientBMI qudt:value ?bmi .
                 ?PatientBMI a omet:PatientBMI  .}
                 
                 {?metric1 omet:isMetricForPatient  ?patient  .
                  ?metric1 omet:isMetricForVisit  ?visit  .
                 ?metric1 qudt:value ?livercT1 .
                 ?metric1 a omet:LivercT1  .}
                 
                 {?metric2 omet:isMetricForPatient  ?patient  .
                  ?metric2 omet:isMetricForVisit  ?visit  .
                 ?metric2 qudt:value ?liverPDFF .
                 ?metric2 a omet:LiverPDFF .}
                 
                 {?metric3 omet:isMetricForPatient  ?patient  .
                  ?metric3 omet:isMetricForVisit  ?visit  .
                 ?metric3 qudt:value ?liverT2Star .
                 ?metric3 a omet:LiverT2Star .}
} 
    ORDER BY ASC(?patient_label)  ASC(?visit_label) """) 

    print("Show all Data")   
    header='"PatientID","Visit","Age","Sex","BMI","livercT1","liverPDFF","liverT2Star","Scanner","Field Strength","Unit","Manufacturer"'  
            
    write_sparql(outfile,header,qres,1,1)  
    '''
    
                 ?scanner omet:usedInVisit ?visit .
                 ?sex  rdfs:label ?sex_label . 
    '''
 
    
def main():
    
    print("\nStarting SPARQLqueries")
    
    data_dir = os.path.join(dirname(dirname(abspath(__file__))), 'data')
    output_dir = data_dir
        
        
    inFile1="metric_data.ttl" 
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
    # suppressed to save time in testing
    g.parse(inFile3, format="ttl")         
    print("Loaded '" + str(len(g)) + "' triples.\n",inFile3)     
    
    ont_dir = os.path.join(dirname(dirname(abspath(__file__))), 'ontology')
    inFile4="ont_metric.ttl" 
    inFile4 = os.path.join(ont_dir,inFile4)
    g.parse(inFile4, format="ttl")         
    print("Loaded '" + str(len(g)) + "' triples.\n",inFile4)    

    # run SPARQL queries against the loaded graph
    query_all(g,outFile)   
    
    #debug_query_all(g,outFile) 
    
    print("\nFinished SPARQLqueries")
          

Display=False       

if __name__ == "__main__":
    main()
