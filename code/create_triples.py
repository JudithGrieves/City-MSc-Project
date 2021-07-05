# -*- coding: utf-8 -*-
"""
Created on 28 June 2021

@author: judith.grieves@city.ac.uk

INM363 Individual Project

Controlling program to load Perspectum Covid study CSV data to RDF triples.

"""

import os
from os.path import dirname, abspath
import pandas as pd
import string

from rdflib import Graph
from rdflib import Namespace
from rdflib import URIRef, Literal
from rdflib.namespace import OWL, RDF, RDFS, XSD



               
def save_graph(g, file_output):
        
        g.serialize(destination=file_output, format='ttl')     
        
def add_subject_triples(g,URI,subj_class,label):       
    """
    A function to add triples to a graph g.
    Needs URI (subject), class (subject) to be used as an RDF.type
    and the literal string to use as a label.
    """

    g.add((URI, RDF.type, OWL.NamedIndividual)) 
    g.add((URI, RDF.type, URIRef(ns + subj_class))) 
    g.add((URI, RDFS.label, Literal(label,datatype=xsd + "string")) )   

def add_dataprop_triples(g,URI,predicate,literal):

    g.add((URI,predicate,literal))          
        
def createTriples(df,g):  
    
    # function to read dataframe df and write as RDF triples on a graph 'g'. 
        
    # namespaces class to create directly URIRefs in python.           
    psp = Namespace(ns)
        
    # Prefixes for the serialization,
    g.bind("psp", psp)     
    g.bind("owl", OWL) 
    g.bind("rdfs", RDFS) 
    g.bind("xsd", XSD) 
    
    # Dictionary to hold the URIs.
    stringToURI = dict()

    if Display:
        print(df)
        
    mapping=get_mapping()
    
    # Process each mapping. 
    for subj_class, subj_uri_col,label_col, dataprops ,objprops in mapping:            
        print("Process mapping: ", subj_class, subj_uri_col,label_col, dataprops, objprops)
        
        # Add subject triples.
        for subj_uri,label_val in  zip(df[subj_uri_col], df[label_col]):
            if pd.notnull(label_val):
                label_val=str(label_val)   
                subj_uri=str(subj_uri)                
                if Display:
                    print("subj_label: ",label_val,"subj_uri: ",subj_uri)                    
                stringToURI[subj_uri] = ns + "URI_" + subj_class + "_" + subj_uri.replace(" ", "_")
                add_subject_triples(g,URIRef(stringToURI[subj_uri]),subj_class,label_val)

        # Add data property triples, if specified.     
        for dataprop, dataprop_col, dataprop_type in dataprops:
            if Display:
                print("dataprops:",dataprop, dataprop_col, dataprop_type)
            if dataprop:
                # get a distinct list of values for subject URI and data property
                for subj_uri, dataprop_lit in zip(df[subj_uri_col], df[dataprop_col]):  
                    if dataprop_lit:                    
                        if Display:
                            print("create dataProperties for : ",subj_uri \
                                  ," : with attr col/type: ",dataprop \
                                  , dataprop_lit, dataprop_type)
                        subject_URI = URIRef(stringToURI[str(subj_uri)])  
                        literal=Literal(dataprop_lit ,datatype=xsd + dataprop_type)
                        predicate=URIRef(ns + dataprop)
                        add_dataprop_triples(g,subject_URI,predicate,literal)
                        
        # Add object property triples, if specified.  
        for objprop, objprop_col in objprops:
            if Display:
                print(subj_uri_col, objprop, objprop_col )
            # get a distinct list of values for subject and object properties  
            for subj_uri, Object in zip(df[subj_uri_col], df[objprop_col]):    
                Object=str(Object) 
                subj_uri=str(subj_uri)
                if Object: 
                    if Display:
                        print("create objectProperties for subject: ",subj_uri \
                              ," : with object: ",Object \
                              , " : with verb: ", objprop)
                    subject_URI = URIRef(stringToURI[subj_uri])  
                    object_URI = URIRef(stringToURI[Object])                 
                    g.add((subject_URI, URIRef(ns + objprop)\
                           ,object_URI ))
            
def CSVtoRDF(infile="test_data.csv"):   
    """
    Read a CSV file and write the data out to RDF triples.   
    """     
    print("\nStarting CSVtoRDF ....")            
    print("Reading file: ",infile)        
    df = pd.read_csv(infile, sep=',', quotechar='"',escapechar="\\") 
       
    # replace DF  with cleaned version
    #df =  df.applymap(cleanString)
     
    # create a graph, g, and load triples from CSV    
    g = Graph()    
    createTriples(df,g) 
    
    # write completed graph to .ttl file        
    #outfile = "test_data.ttl"          
    outfile=infile.replace("csv", "ttl")       
    outfile = os.path.join(data_dir,outfile)    
    print("Writing file: ",outfile)
    save_graph(g,outfile)
        
    print("Finished CSVtoRDF ....")
    

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
               ,["LiverT2Star", "URI", "liver_T2star"
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
    
    print("\nStarting main() ....")   
    # set up variables
    global data_dir
    data_dir = os.path.join(dirname(dirname(abspath(__file__))), 'data')
    infile="test_data14.csv"    
    global ns
    ns= "http://www.perspectum.com/resources/"
    global xsd
    xsd = "http://www.w3.org/2001/XMLSchema#"
    
    print("Data dir: ", data_dir)
    #externalURI=True
    global Display
    Display=True
    
    # read in CSV file and convert to a dataframe
    infile = os.path.join(data_dir,infile)
    print("infile: ", infile)

    CSVtoRDF(infile)
    print("\nFinished main() ....")      


if __name__ == "__main__":
    main()    