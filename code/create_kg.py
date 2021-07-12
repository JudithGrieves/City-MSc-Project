# -*- coding: utf-8 -*-
"""
Created on 28 June 2021

@author: judith.grieves@city.ac.uk

INM363 Individual Project

Creating a Knowledge Graph of Perspectum Covid study data.

This module contains code to load a CSV file to RDF triples.  
CSVtoRDF(infile,mapping,ns,prefix) can be called from another module.
main() runs CSVtoRDF for Perspectum metrics data as a default.

Currently tested for metrics and scanner KGs.

"""

import os
from os.path import dirname, abspath
import pandas as pd
import string

from rdflib import Graph
from rdflib import Namespace
from rdflib import URIRef, Literal
from rdflib.namespace import OWL, RDF, RDFS, XSD

from lookup_kg import get_scanner_uri

               
def save_graph(g, file_output):
        
        g.serialize(destination=file_output, format='ttl')     
        
def add_subject_triples(g,URI,subj_class,label):       
    """
    A function to add subject triples to a graph g.
    Needs URI (subject), class (subject) to be used as an RDF.type
    and the literal string to use as a label.
    """

    g.add((URI, RDF.type, OWL.NamedIndividual)) 
    g.add((URI, RDF.type, subj_class)) 
    g.add((URI, RDFS.label, Literal(label,datatype=xsd + "string")) )   

def add_dataprop_triples(g,URI,predicate,literal):

    g.add((URI,predicate,literal))          
        
def create_triples(df,mapping,ns,prefix):  
    
    # function to read dataframe df and write as RDF triples on a graph 'g'. 

    if Display:           
        print("create_triples: ", ns,prefix)
    # set up KG variables
    global xsd
    xsd = "http://www.w3.org/2001/XMLSchema#"  
    g = Graph()          
                   
    scn = Namespace("http://www.perspectum.com/resources/scanner/")
    g.bind("scn", scn)   
    
    psp = Namespace("http://www.perspectum.com/resources/metric/")
    g.bind("psp", psp)     
    
    # Prefixes for the serialization,
    g.bind("owl", OWL) 
    g.bind("rdfs", RDFS) 
    g.bind("xsd", XSD) 
    
    # Dictionary to hold the URIs.
    stringToURI = dict()

    if Display:
        print(df)
            
    # Process each mapping. 
    for subj_class, subj_uri_col,label_col,label_const,ext_uri,dataprops,objprops in mapping: 
        if Display:           
            print("Process mapping: ", subj_class, subj_uri_col,label_col, dataprops, objprops)
        if(label_const):
            label_const+=" "   
        # Add subject triples.
        for subj_uri,label_val in  zip(df[subj_uri_col], df[label_col]):
            if pd.notnull(label_val):
                label_val=str(label_val)  
                subj_uri=str(subj_uri)                               
                stringToURI[subj_uri] = ns + "URI_" + subj_class + "_" + subj_uri.replace(" ", "_")
                if ext_uri=='EXT':
                    if Display:
                        print("Find External URI")                    
                    uri = get_scanner_uri(label_val)
                    if uri:                              
                        stringToURI[subj_uri] = uri
                if Display:
                    print("subj_uri: ",subj_uri,"subj_label: ",label_val)     
                add_subject_triples(g,URIRef(stringToURI[subj_uri]),URIRef(ns + subj_class),label_const+label_val)

 
        # Add data property triples, if specified.     
        for dataprop, dataprop_col, dataprop_type in dataprops:
            if Display:
                print("dataprops:",dataprop, dataprop_col, dataprop_type)
            if dataprop:
                # get a distinct list of values for subject URI and data property
                for subj_uri, dataprop_lit in zip(df[subj_uri_col], df[dataprop_col]):  
                    if dataprop_lit:                    
                        if Display:
                            print("create dataProps for subject: ",subj_uri \
                                  ," : with attr col/type: ",dataprop \
                                  , dataprop_lit, dataprop_type)
                        subject_URI = URIRef(stringToURI[str(subj_uri)])  
                        literal=Literal(dataprop_lit ,datatype=xsd + dataprop_type)
                        predicate=URIRef(ns + dataprop)
                        add_dataprop_triples(g,subject_URI,predicate,literal)
                        
        # Add object property triples, if specified.  
        # this code assumes that a class already exists for the object
        # ie. that classes and object properties are created in order
        # correctly determined by the mapping
        for objprop, objprop_col in objprops:
            if Display:
                print(subj_uri_col, objprop, objprop_col )
            # get a distinct list of values for subject and object properties 
            for subj_uri, Object in zip(df[subj_uri_col], df[objprop_col]):    
                Object=str(Object)
                subj_uri=str(subj_uri)
                if Object: 
                    if Display:
                        print("create objectProps for subject: ",subj_uri \
                              ," : with object: ",Object \
                              , " : with verb: ", objprop)
                    subject_URI = URIRef(stringToURI[subj_uri])  
                    object_URI = URIRef(stringToURI[Object])                 
                    g.add((subject_URI, URIRef(ns + objprop)\
                           ,object_URI ))
    return g
            
def CSVtoRDF(infile,mapping,ns,prefix):   
    """
    Read a CSV file and convert the data out to RDF triples.   
    """     
    print("\nStarting CSVtoRDF ....")  
    global Display
    Display=False          
    print("Reading file: ",infile)        
    df = pd.read_csv(infile, sep=',', quotechar='"',escapechar="\\") 
       
    # replace DF  with cleaned version
    #df =  df.applymap(cleanString)
     
    # load triples from CSV and return the graph
    g=create_triples(df,mapping,ns,prefix) 
    
    # write completed graph to .ttl file in the infile data directory
    outfile=infile.replace("csv", "ttl")        
    print("Writing file: ",outfile)
    save_graph(g,outfile)
        
    print("Finished CSVtoRDF ....")
    

def get_mapping_metric():        
    """
    A function to define/retrieve the CSV to RDF mapping.
    Currently hardcoded here but may be read from a file later.
    The mapping should be supplied from the calling program to 
    correspond with the input file but this is given as the default for
    testing.
    """
    # mapping: [subject class,uri col,label col,label const, external URI?
    #          [data props: predicate,column,dataType], 
    #          [object props: predicate, column] ]
    mapping = [["Patient", "Patient_ID", "Patient_ID","",""
                    ,[["PatientSex","Sex","string"]
                    ,["PatientAge","Age","int"]
                    ,["PatientBMI","BMI","float"]]
                    ,[]] # no object properties
               ,["ScanVisit", "Scan visit", "Scan visit","",""
                     ,[] # no data properties
                     ,[["isAttendedBy", "Patient_ID"] ] ]
               ,["liver_T2Star", "URI", "Patient_ID","liver_T2Star",""
                 ,[["MetricValue","liver_T2star","float"]]
                 ,[["isMetricForPatient", "Patient_ID"]
                 ,["isMetricForVisit", "Scan visit"]]]
               ,["liver_cT1", "URI", "Patient_ID","liver_cT1",""
                 ,[["MetricValue","liver_cT1","float"]]
                 ,[["isMetricForPatient", "Patient_ID"]
                 ,["isMetricForVisit", "Scan visit"]]]
               ,["liver_PDFF", "URI", "Patient_ID","liver_PDFF",""
                 ,[["MetricValue","liver_PDFF","float"]]
                 ,[["isMetricForPatient", "Patient_ID"]
                 ,["isMetricForVisit", "Scan visit"]]]
               ,["Scanner", "Scanner", "Scanner","","EXT"
                     ,[] # no data properties
                     ,[["usedInVisit", "Scan visit"]] ]]
               
    return mapping
               
def main():
    
    print("\nStarting main() ....")   
    
    # set up file variables
    global data_dir
    data_dir = os.path.join(dirname(dirname(abspath(__file__))), 'data')
    infile="metrics_data.csv"   
    infile = os.path.join(data_dir,infile)
    mapping=get_mapping_metric()
    ns= "http://www.perspectum.com/resources/metric/"
    prefix="psp"
    print("infile: ", infile,"Namespace",ns,prefix) 
    
    # read in CSV file and convert to RDF triples
    CSVtoRDF(infile,mapping,ns,prefix)
    
    print("\nFinished main() ....")      


if __name__ == "__main__":
    main()    