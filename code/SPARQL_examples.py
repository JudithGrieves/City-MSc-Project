'''
Created on 29 June 2021

@author: judith.grieves@city.ac.uk

INM363 Individual Project

This code loads the Perspectum Knowledge Graph triples (metrics and scanner)
and executes the Iteration 1 example queries over the graph.

ISSUES:
    
    NEEDS TO RETURN :FEMALE/MALE ENUMERATED TYPES W/O FULL URI PATH?
    FIELD STRENGTH VALUES MISSING
    using this triple in query ?visit omet:usesScannerModel  ?scanner  . instead of ?scanner omet:usedInVisit ?visit .

'''
from rdflib import Graph

import os
from os.path import dirname, abspath

from write_sparql_file import write_sparql

def query1(g,outfile):
    
    '''
    Example Query 1: 
    all the Females with age above 40 and BMI above 25 that have liver cT1 above 800 ms    '''    

    qres = g.query(
    """SELECT DISTINCT  ?patient_label ?visit_label ?sex ?age ?bmi ?livercT1  WHERE
                {
                 ?visit a omet:Imaging_Scan_Visit .
                 ?visit rdfs:label ?visit_label .
                 ?visit omet:isAttendedBy ?patient .  
                 ?patient a ?Patient .
                 ?patient rdfs:label ?patient_label .
                 ?patient omet:hasPatientSex ?sex . 
                 {?PatientAge omet:isMetricForPatient  ?patient  .
                  ?PatientAge omet:isMetricForVisit  ?visit  .
                 ?PatientAge qudt:value ?age .
                 ?PatientAge a omet:PatientAge  .}
                 FILTER( ?age > 40 )
                 {?PatientBMI omet:isMetricForPatient  ?patient  .
                  ?PatientBMI omet:isMetricForVisit  ?visit  .
                 ?PatientBMI qudt:value ?bmi .
                 ?PatientBMI a omet:PatientBMI  .}
                 FILTER( ?bmi  > 25  )
                 {?cT1 omet:isMetricForPatient  ?patient  .
                  ?cT1 omet:isMetricForVisit  ?visit  .
                 ?cT1 qudt:value ?livercT1 .
                 ?cT1 a omet:LivercT1  .} 
                 FILTER( ?livercT1 > 800 )
                 } 
    ORDER BY ASC(?patient_label)  """)  

    print("Query 1 - Females with age above 40 and BMI above 25 that  \
            have liver cT1 above 800 ms:\n")   
       
    header='"Patient","Visit","Sex","Age","BMI","livercT1"'  
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
    """SELECT DISTINCT  ?patient_label ?visit_label  ?age ?bmi 
                        ?liverPDFF ?scanner_label ?fsval ?fsunit_label ?manf_label
            WHERE
                {?visit a ?Imaging_Scan_Visit .
                 ?visit rdfs:label ?visit_label .
                 ?visit omet:isAttendedBy ?patient . 
                 ?patient rdfs:label ?patient_label .
                 ?patient omet:hasPatientSex ?sex . 
                 {?PatientAge omet:isMetricForPatient  ?patient  .
                  ?PatientAge omet:isMetricForVisit  ?visit  .
                 ?PatientAge qudt:value ?age .
                 ?PatientAge a omet:PatientAge  .}
                 {?PatientBMI omet:isMetricForPatient  ?patient  .
                  ?PatientBMI omet:isMetricForVisit  ?visit  .
                 ?PatientBMI qudt:value ?bmi .
                 ?PatientBMI a omet:PatientBMI  .}
                 {?metric omet:isMetricForPatient  ?patient  .
                  ?metric omet:isMetricForVisit  ?visit  .
                 ?metric qudt:value ?liverPDFF .
                 ?metric a omet:LiverPDFF  .} 
                 FILTER(?liverPDFF < 5 )
                 ?visit omet:usesScannerModel  ?scanner  . 
                 OPTIONAL {
                     ?scanner rdfs:label ?scanner_label .
                     ?scanner a oscn:MRIScannerModel .
                     ?manf a oscn:ScannerManufacturer .
                     ?manf rdfs:label ?manf_label .
                     ?manf oscn:isMakerOfScanner ?scanner.  
                     }                
                 FILTER( ?manf_label = "Siemens" )
                 OPTIONAL {
                     ?fs oscn:isFieldStrengthForScanner ?scanner .
                     ?fs oscn:FieldStrengthValue ?fsval .
                     ?fs oscn:FieldStrengthUnit ?fsunit .
                     ?fsunit rdfs:label ?fsunit_label . } 
                 FILTER(?fsval = 1.5 ) 
                 } 
    ORDER BY ASC(?patient_label)  """)   

    print("\nQuery 2 - Siemens 1.5 Tesla visits (patients scans) where PDFF is below 5%:\n")   
       
    header='"Patient","Visit","Age","BMI","liverPDFF","Scanner"\
            ,"Field Strength","Units","Manufacturer"'  
    outfile=outfile.replace("x", "2")       
    write_sparql(outfile,header,qres,1,1)  
        
def query3(g,outfile):
    
    '''
    Example Query3: 
    cases where cT1 is above 800 ms but PDFF is below 10%
    '''    
    qres = g.query(
    """SELECT DISTINCT  ?patient_label ?visit_label  ?age ?bmi 
                        ?livercT1 ?liverPDFF 
            WHERE
                {?visit a ?Imaging_Scan_Visit .
                 ?visit rdfs:label ?visit_label .
                 ?visit omet:isAttendedBy ?patient .  
                 ?patient a ?Patient .
                 ?patient rdfs:label ?patient_label .
                 ?patient omet:hasPatientSex ?sex . 
                 {?PatientAge omet:isMetricForPatient  ?patient  .
                  ?PatientAge omet:isMetricForVisit  ?visit  .
                 ?PatientAge qudt:value ?age .
                 ?PatientAge a omet:PatientAge  .}
                 {?PatientBMI omet:isMetricForPatient  ?patient  .
                  ?PatientBMI omet:isMetricForVisit  ?visit  .
                 ?PatientBMI qudt:value ?bmi .
                 ?PatientBMI a omet:PatientBMI  .}
                 {?metric_PDFF omet:isMetricForPatient  ?patient  .
                  ?metric_PDFF omet:isMetricForVisit  ?visit  .
                 ?metric_PDFF qudt:value ?liverPDFF .
                 ?metric_PDFF a omet:LiverPDFF  .} 
                 FILTER(?liverPDFF < 10 )
                 {?metric_cT1 omet:isMetricForPatient  ?patient  .
                  ?metric_cT1 omet:isMetricForVisit  ?visit  .
                 ?metric_cT1 qudt:value ?livercT1 .
                 ?metric_cT1 a omet:LivercT1  .} 
                 FILTER(?livercT1 > 800 )
                 } 
    ORDER BY ASC(?patient_label)  """)    
           
    print("\nQuery3 - cases where cT1 is above 800 ms but PDFF is below 10%")
    
    header='"Visit","Patient","Age","BMI","livercT1","liverPDFF"'  
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
    #g.parse(inFile3, format="ttl")         
    #print("Loaded '" + str(len(g)) + "' triples.\n",inFile3)       

    # run SPARQL queries against the loaded graph
    query1(g,outfile)
    query2(g,outfile)
    query3(g,outfile)
    
    print("\nFinished SPARQLqueries")
          

Display=False       

if __name__ == "__main__":
    main()