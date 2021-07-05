'''
Created on 29 June 2021

@author: judith.grieves@city.ac.uk

INM363 Individual Project

This code loads the Perspectum Knowledge Graph triples and executes the 
Iteration 1 example queries over the graph.

'''
from rdflib import Graph
import csv

import os
from os.path import dirname, abspath


def write_results(outfile,header,qres,todisp,tofile):
    '''
    Write the results of a SPARQL query 'qres', with comma-delimited 
    'header' string to file 'outFile'
    '''
    with open(outfile, 'w', newline='', encoding='utf-8') as file:
        if todisp:
            print(header) # dynamically written csv row 
        if tofile:
            file.write(header+"\n") # dynamically written csv row 
        for row in qres:
            printstr=""
            for x in range(len(row)):
                printstr= printstr + "%s,"
            if todisp:
                print(printstr % row)
            if tofile:
                file.write(printstr % row) # dynamically written csv row
                file.write('\n')

def query1(g,outfile):
    
    '''
    Example Query 1: 
    Give me all the Females with age above 40 and BMI above 25 that have liver cT1 above 800 ms
    '''    

    qres = g.query(
    """SELECT DISTINCT  ?patient_label ?sex ?age ?bmi ?value ?metric_type WHERE
                {?patient a ?Patient .
                 ?patient rdfs:label ?patient_label .
                 ?patient psp:PatientSex ?sex .  
                 ?patient psp:PatientAge ?age .
                 ?patient psp:PatientBMI ?bmi .  
                 ?metric psp:isMetricForPatient  ?patient  .
                 ?metric psp:MetricValue ?value .
                 ?metric a  ?metric_type . 
    FILTER(?age > 40 
           && ?sex = "F" 
           && ?bmi  > 25 
           && ?value > 800 
           && CONTAINS(STR(?metric_type),"liver_cT1"))} """)    

    print("Query 1 - Females with age above 40 and BMI above 25 that  \
            have liver cT1 above 800 ms:\n")   
       
    header='"Patient","Sex","Age","BMI","Metric Value","Type"'  
    print("outfile",outfile)
    #outfile=str(outfile)
    outfile=outfile.replace("x", "1")       
    write_results(outfile,header,qres,1,1)
            
        
def query2(g,outfile):
    
    '''
    Example Query2: 
    Siemens 1.5 Tesla visits (patients scans) where PDFF is below 5%
    '''    

    qres = g.query(
    """SELECT DISTINCT  ?visit_label ?patient_label ?sex ?age ?bmi 
                        ?metric_value ?metric_type ?scanner ?field_strength 
            WHERE
                {?visit a ?ScanVisit .
                 ?visit rdfs:label ?visit_label .
                 ?visit psp:isAttendedBy ?patient .  
                 ?patient a ?Patient .
                 ?patient rdfs:label ?patient_label .
                 ?patient psp:PatientSex ?sex .  
                 ?patient psp:PatientAge ?age .
                 ?patient psp:PatientBMI ?bmi .  
                 ?metric psp:isMetricForPatient  ?patient  .
                 ?metric psp:MetricValue ?metric_value .
                 ?metric a  ?metric_type .
                 ?scanner psp:usedInVisit ?visit .
                 ?scanner psp:FieldStrength ?field_strength
    FILTER(?field_strength = 1.5
           && ?metric_value < 5
           && CONTAINS(STR(?metric_type),"liver_PDFF")
           && CONTAINS(STR(?scanner),"Siemens")) } """)    

    print("\nQuery 2 - Siemens 1.5 Tesla visits (patients scans) where PDFF is below 5%:\n")   
       
    header='"Visit","Patient","Sex","Age","BMI","Metric Value","Type","Scanner","Field Strength"'  
    outfile=outfile.replace("x", "2")       
    write_results(outfile,header,qres,1,1)  
        

def query3(g,outfile):
    
    '''
    Example Query3: 
    cases where cT1 is above 800 ms but PDFF is below 10%
    '''    
    # this is currently returning all rows where either condition holds
    # need to expand the SPARQL to 'pivot' to show both metrics before filtering
    # on both conditions
    qres = g.query(
    """SELECT DISTINCT  ?visit_label ?patient_label ?sex ?age ?bmi 
                        ?metric_value ?metric_type 
            WHERE
                {?visit a ?ScanVisit .
                 ?visit rdfs:label ?visit_label .
                 ?visit psp:isAttendedBy ?patient .  
                 ?patient a ?Patient .
                 ?patient rdfs:label ?patient_label .
                 ?patient psp:PatientSex ?sex .  
                 ?patient psp:PatientAge ?age .
                 ?patient psp:PatientBMI ?bmi .  
                 ?metric psp:isMetricForPatient  ?patient  .
                 ?metric psp:MetricValue ?metric_value .
                 ?metric a  ?metric_type .
    FILTER(
            (?metric_value > 800  && CONTAINS(STR(?metric_type),"liver_cT1"))
            || (?metric_value < 10   && CONTAINS(STR(?metric_type),"liver_PDFF"))
           ) } """)    
       
    print("\nQuery3 - cases where cT1 is above 800 ms but PDFF is below 10%")
    
    header='"Visit","Patient","Sex","Age","BMI","Metric Value","Type"'  
    outfile=outfile.replace("x", "3")       
    write_results(outfile,header,qres,1,1)   
        

        
def main():
    
    print("\nStarting SPARQLqueries")
    
    data_dir = os.path.join(dirname(dirname(abspath(__file__))), 'data')
    output_dir = os.path.join(dirname(dirname(abspath(__file__))), 'data')        
        
    inFile="test_data14.ttl" 
    outfile=inFile.replace(".ttl", "-")+"sparqlx.csv"  
    
    inFile = os.path.join(data_dir,inFile)
    outfile = os.path.join(output_dir,outfile)
    
    print("Load a graph from input file: ", inFile)
    g = Graph()    
    g.parse(inFile, format="ttl")         
    print("Loaded '" + str(len(g)) + "' triples.\n")    

    # run SPARQL queries against the loaded graph
    query1(g,outfile)
    query2(g,outfile)
    query3(g,outfile)
    
    print("\nFinished SPARQLqueries")
          

Display=False       

if __name__ == "__main__":
    main()