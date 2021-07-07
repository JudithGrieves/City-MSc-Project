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

from create_triples import CSVtoRDF

def get_mapping():      
    """
    A function to define/retrieve the CSV to RDF mapping.
    Currently hardcoded here but may be read from a file later.
    """
    # mapping: [subject class,uri col,label col, [data props], [object props]]
    mapping = [["Patient", "Patient_ID", "Patient_ID",
                    [["PatientSex","Sex","string"]
                    ,["PatientAge","Age","int"]
                    ,["PatientBMI","BMI","float"]]
                    ,[]] # no object properties
               ,["ScanVisit", "Scan visit", "Scan visit"
                     ,[] # no data properties
                     ,[["isAttendedBy", "Patient_ID"]] ]
               ,["liver_T2Star", "URI", "liver_T2star"
                 ,[["MetricValue","liver_T2star","float"]]
                 ,[["isMetricForPatient", "Patient_ID"]
                 ,["isMetricForVisit", "Scan visit"]]]
               ,["liver_cT1", "URI", "liver_cT1"
                 ,[["MetricValue","liver_cT1","float"]]
                 ,[["isMetricForPatient", "Patient_ID"]
                 ,["isMetricForVisit", "Scan visit"]]]
               ,["liver_PDFF", "URI", "liver_PDFF"
                 ,[["MetricValue","liver_PDFF","float"]]
                 ,[["isMetricForPatient", "Patient_ID"]
                 ,["isMetricForVisit", "Scan visit"]]]
               ,["Scanner", "Scanner", "Scanner"
                    ,[["FieldStrength","Field Strength","float"]]
                     ,[["usedInVisit", "Scan visit"]] ]]
    return mapping


          
def main():
    
    print("\nStarting create_metrics_kg() ....")   
    
    # set up file variables
    global data_dir
    data_dir = os.path.join(dirname(dirname(abspath(__file__))), 'data')
    infile="test_data14.csv"   
    infile = os.path.join(data_dir,infile)
    mapping=get_mapping()
    print("infile: ", infile) 
    
    # read in CSV file and convert to RDF triples
    CSVtoRDF(infile,mapping)
    
    print("\nFinished create_metrics_kg() ....")      

if __name__ == "__main__":
    main()    