'''
Created on 29 June 2021

@author: judith.grieves@city.ac.uk

INM363 Individual Project

This code loads the Perspectum Knowledge Graph triples (metrics and scanner)
and executes the Iteration 1 example queries over the graph.

ISSUES:
    
    NEEDS TO RETURN :FEMALE/MALE ENUMERATED TYPES W/O FULL URI PATH?
    using this triple in query ?visit omet:usesScannerModel  ?scanner  . instead of ?scanner omet:usedInVisit ?visit .

'''
from rdflib import Graph

import os
from os.path import dirname, abspath

from write_sparql_file import write_sparql

def query1(g,outfile):
    
    '''
    Example Query 1: 
    Give me all the Females with age above 40 and BMI above 25 that have liver cT1 above 800 ms
    NOT FILTERING FOR SEX UNTIL ENUMERATED TYPES QUERY IS WORKING
    '''    

    qres = g.query(
    """SELECT DISTINCT  ?patient_label ?sex ?age ?bmi ?liver_cT1  WHERE
                {?patient a ?Patient .
                 ?patient rdfs:label ?patient_label .
                 ?patient omet:hasPatientSex ?sex . 
                 ?patient omet:PatientAge ?age .
                 ?patient omet:PatientBMI ?bmi .   
                 {?metric omet:isMetricForPatient  ?patient  .
                  ?metric omet:isMetricForVisit  ?visit  .
                 ?metric qudt:value ?liver_cT1 .
                 ?metric a omet:liver_cT1  .}
    FILTER(?age > 40 
           && ?bmi  > 25 
           && ?liver_cT1 > 800 )} 
    ORDER BY ASC(?patient_label)  """)    
    '''
    
           && ?sex = "F" 
    '''

    print("Query 1 - Females with age above 40 and BMI above 25 that  \
            have liver cT1 above 800 ms:\n")   
       
    header='"Patient","Sex","Age","BMI","liver_cT1"'  
    print("outfile",outfile)
    #outfile=str(outfile)
    outfile=outfile.replace("x", "1")       
    write_sparql(outfile,header,qres,1,1)
            
        
def query2(g,outfile):
    
    '''
    Example Query2: 
    Siemens 1.5 Tesla visits (patients scans) where PDFF is below 5%
    
    '''    

    qres = g.query(
    """SELECT DISTINCT  ?visit_label ?patient_label ?sex ?age ?bmi 
                        ?liver_PDFF ?scanner_label ?fsval ?fsunitlabel ?manf_label 
            WHERE
                {?visit a ?ScanVisit .
                 ?visit rdfs:label ?visit_label .
                 ?visit omet:isAttendedBy ?patient . 
                 ?patient rdfs:label ?patient_label .
                 ?patient omet:hasPatientSex ?sex . 
                 ?patient omet:PatientAge ?age .
                 ?patient omet:PatientBMI ?bmi .  
                 {?metric omet:isMetricForPatient  ?patient  .
                  ?metric omet:isMetricForVisit  ?visit  .
                 ?metric qudt:value ?liver_PDFF .
                 ?metric a omet:liver_PDFF  .}
                 ?visit omet:usesScannerModel  ?scanner  . 
                 ?scanner rdfs:label ?scanner_label .
                 ?scanner a scn:MRIScannerModel .
                 ?manf a scn:ScannerManufacturer .
                 ?manf rdfs:label ?manf_label .
                 ?manf scn:isMakerOf ?scanner.
                 OPTIONAL {?fs scn:isFieldStrengthForScanner ?scanner .
                           ?fs qudt:value ?fsval .
                           ?fs qudt:unit ?fsunit . 
                           ?fsunit rdfs:label ?fsunitlabel .  }
    FILTER(?liver_PDFF < 5
           && ?fsval = 1.5 
           && ?manf_label = "Siemens" ) } 
    ORDER BY ASC(?patient_label)  """)   

    print("\nQuery 2 - Siemens 1.5 Tesla visits (patients scans) where PDFF is below 5%:\n")   
       
    header='"Visit","Patient","Sex","Age","BMI","liver_PDFF","Scanner"\
            ,"Field Strength","Units","Manufacturer"'  
    outfile=outfile.replace("x", "2")       
    write_sparql(outfile,header,qres,1,1)  
        
def query3(g,outfile):
    
    '''
    Example Query3: 
    cases where cT1 is above 800 ms but PDFF is below 10%
    '''    
    qres = g.query(
    """SELECT DISTINCT  ?visit_label ?patient_label ?sex ?age ?bmi 
                        ?liver_cT1 ?liver_PDFF 
            WHERE
                {?visit a ?ScanVisit .
                 ?visit rdfs:label ?visit_label .
                 ?visit omet:isAttendedBy ?patient .  
                 ?patient a ?Patient .
                 ?patient rdfs:label ?patient_label .
                 ?patient omet:hasPatientSex ?sex . 
                 ?patient omet:PatientAge ?age .
                 ?patient omet:PatientBMI ?bmi .   
                 {?metric_PDFF omet:isMetricForPatient  ?patient  .
                  ?metric_PDFF omet:isMetricForVisit  ?visit  .
                 ?metric_PDFF qudt:value ?liver_PDFF .
                 ?metric_PDFF a omet:liver_PDFF  .}
                 {?metric_cT1 omet:isMetricForPatient  ?patient  .
                  ?metric_cT1 omet:isMetricForVisit  ?visit  .
                 ?metric_cT1 qudt:value ?liver_cT1 .
                 ?metric_cT1 a omet:liver_cT1  .}
    FILTER(?liver_PDFF < 10
           && ?liver_cT1 > 800) } 
    ORDER BY ASC(?patient_label)  """)    
       
    print("\nQuery3 - cases where cT1 is above 800 ms but PDFF is below 10%")
    
    header='"Visit","Patient","Sex","Age","BMI","liver_cT1","liver_PDFF"'  
    outfile=outfile.replace("x", "3")       
    write_sparql(outfile,header,qres,1,1)   
        

        
def main():
    
    print("\nStarting SPARQLqueries")
    
    data_dir = os.path.join(dirname(dirname(abspath(__file__))), 'data')
    output_dir = os.path.join(dirname(dirname(abspath(__file__))), 'data')        
        
    inFile1="metric_data.ttl" 
    inFile2="scanner_data.ttl" 
    outfile=inFile1.replace(".ttl", "-")+"sparqlx.csv"  
    
    inFile1 = os.path.join(data_dir,inFile1)
    inFile2 = os.path.join(data_dir,inFile2)
    inFile3="http://qudt.org/2.1/vocab/unit"
    outfile = os.path.join(output_dir,outfile)
    
    print("Load a graph from input file: ", inFile1)
    g = Graph()    
    g.parse(inFile1, format="ttl")         
    print("Loaded '" + str(len(g)) + "' triples.\n")   
    g.parse(inFile2, format="ttl")         
    print("Loaded '" + str(len(g)) + "' triples.\n")  
    # SUPPRESS THIS WHILE TESTING
    g.parse(inFile3, format="ttl")         
    print("Loaded '" + str(len(g)) + "' triples.\n",inFile3)       

    # run SPARQL queries against the loaded graph
    query1(g,outfile)
    query2(g,outfile)
    query3(g,outfile)
    
    print("\nFinished SPARQLqueries")
          

Display=False       

if __name__ == "__main__":
    main()