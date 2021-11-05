# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 15:49:15 2021

@author: judith.grieves@city.ac.uk

INM363 Individual Project

Program to load Perspectum metrics CSV data to RDF triples.
Calls CSVtoRDF module

"""
import os
from os.path import dirname, abspath

from create_kg import CSVtoRDF

def get_map_metric():      
    """
    A function to define/retrieve the CSV to RDF mapping.
    Currently hardcoded here but may be read from a file later.
    """
    # mapping: [subject class,uri col,label col,label const, external URI?
    #          [data props: predicate,column,dataType], 
    #          [object props: predicate, column] ]
    # if no prefix in predicate mapping value, then use default (psp)
    mapping = [["Patient", "Patient_ID", "Patient_ID","",""
                    ,[["PatientSex","Sex","string"]
                    ,["PatientAge","Age","int"]
                    ,["PatientBMI","BMI","float"]]
                    ,[]] # no object properties
               ,["ScanVisit", "Scan visit", "Scan visit","",""
                     ,[] # no data properties
                     ,[["isAttendedBy", "Patient_ID","Patient"] ] ]
               ,["liver_T2Star", "URI", "Patient_ID","liver_T2Star",""
                 ,[["qudt:value","liver_T2star","float"]]
                 ,[["isMetricForPatient", "Patient_ID","Patient"]
                 ,["isMetricForVisit", "Scan visit","ScanVisit"]
                 ,["qudt:unit", "unit:MilliSEC","unit"]]]
               ,["liver_cT1", "URI", "Patient_ID","liver_cT1",""
                 ,[["qudt:value","liver_cT1","float"]]
                 ,[["isMetricForPatient", "Patient_ID","Patient"]
                 ,["isMetricForVisit", "Scan visit","ScanVisit"]
                 ,["qudt:unit", "unit:MilliSEC","unit"]]]
               ,["liver_PDFF", "URI", "Patient_ID","liver_PDFF",""
                 ,[["qudt:value","liver_PDFF","float"]]
                 ,[["isMetricForPatient", "Patient_ID","Patient"]
                 ,["isMetricForVisit", "Scan visit","ScanVisit"]
                 ,["qudt:unit", "unit:PERCENT","unit"]]]
               ,["MRIScannerModel", "Scanner", "Scanner","","EXT"
                     ,[] # no data properties
                     ,[["usedInVisit", "Scan visit","ScanVisit"]] ]]
               
    return mapping


          
def main():
    
    print("\nStarting create_metrics_kg() ....")   
    
    # set up file variables
    global data_dir
    data_dir = os.path.join(dirname(dirname(abspath(__file__))), 'data')
    infile="metrics_data.csv"   
    infile = os.path.join(data_dir,infile)
    mapping=get_map_metric()
    print("infile: ", infile) 
    
    ns= "http://www.perspectum.com/resources/metric/"
    prefix="psp"
    print("infile: ", infile,"Namespace",ns,prefix) 
    
    # read in the CSV file and convert to RDF triples
    CSVtoRDF(infile,mapping,ns,prefix)
    
    print("\nFinished create_metrics_kg() ....")      

if __name__ == "__main__":
    main()    
