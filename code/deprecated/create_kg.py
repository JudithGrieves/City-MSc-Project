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
    g.add((URI, RDFS.label, Literal(label,datatype=XSD.string)) )   

def add_dataprop_triples(g,URI,predicate,literal):

    g.add((URI,predicate,literal))     


def get_prefix(string_to_split='psp:classType'):
    '''
    Function to parse the mapping predicate and return any prefix found
    '''
    prefix=''
    string_split = string_to_split.split(":")
    if len(string_split)==1:
        predicate=string_split[0]
    else:
        predicate=string_split[1]
        prefix=string_split[0]
                        
    return prefix,predicate

        
def create_triples(df,mapping,ns,prefix):  
    
    # function to read dataframe df and write as RDF triples on a graph 'g'. 

    if Display:           
        print("create_triples: ", ns,prefix)
    # set up KG variables
    g = Graph()          
                   
    scn = Namespace("http://www.perspectum.com/resources/scanner/")
    psp = Namespace("http://www.perspectum.com/resources/metric/")
    qudt = Namespace("http://qudt.org/schema/qudt/")
    unit = Namespace("http://qudt.org/vocab/unit/")
    
    # Prefixes for the serialization,
    # these prefixes will be used in the resulting TTL file
    g.bind("owl", OWL) 
    g.bind("rdfs", RDFS) 
    g.bind("xsd", XSD) 
    
    g.bind("scn", scn)   
    g.bind("psp", psp)    
    g.bind("qudt", qudt)   
    g.bind("unit", unit)    
    
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
                stringToURI[subj_class+subj_uri] = ns + "URI_" + subj_class + "_" + subj_uri.replace(" ", "_")
                if ext_uri=='EXT':
                    if Display:
                        print("Find External URI")                    
                    uri = get_scanner_uri(label_val)
                    if uri:                              
                        stringToURI[subj_class+subj_uri] = uri
                if Display:
                    print("subj_uri: ",subj_uri,"subj_label: ",label_val)     
                add_subject_triples(g,URIRef(stringToURI[subj_class+subj_uri]),URIRef(ns + subj_class),label_const+label_val)

 
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
                        subject_URI = URIRef(stringToURI[subj_class+str(subj_uri)])  
                        literal=Literal(dataprop_lit ,datatype=XSD + dataprop_type)
                        
                        # if dataprop mapping value has prefix: 
                        # lookup namespace and prefix to dataprop, otherwise use default ns
                        dp_namesspace=ns
                        prefix,predicate=get_prefix(dataprop)   
                        if prefix=='qudt':
                            dp_namesspace=qudt               
                        predicate=URIRef(dp_namesspace + predicate)
                        add_dataprop_triples(g,subject_URI,predicate,literal)
                        
        # Add object property triples, if specified.  
        # this code assumes that a class already exists for the object
        # ie. that classes and object properties are created in order
        # correctly determined by the mapping
        for objprop, objprop_col,objprop_class in objprops:
            if Display:
                print("subj_uri_col, objprop, objprop_col: ",subj_uri_col, objprop, objprop_col )
            prefix,predicate=get_prefix(objprop_col)  
            if prefix=='unit': # object given
                object_URI=URIRef(unit + predicate) 
                objprop_col=subj_uri_col # no column given so just use subject
            # get a distinct list of values for subject and object properties 
            for subj_uri, objprop_val in zip(df[subj_uri_col], df[objprop_col]):    
                objprop_val=str(objprop_val)
                subj_uri=str(subj_uri)
                if objprop_val: 
                    if Display:
                        print("create objectProps for subject: ",subj_uri \
                              ," : with object: ",objprop_val \
                              , " : with verb: ", objprop)
                        print("**",objprop_col,subj_uri_col)
                    if not(prefix): # object given
                        object_URI = URIRef(stringToURI[objprop_class+objprop_val])  # just looking up (scanner model val, same as sub)                      
                    subject_URI = URIRef(stringToURI[subj_class+subj_uri])  
                    #print("OBJECT URI: ", object_URI,prefix)
                    
                    prefix,predicate=get_prefix(objprop)    
                    if prefix=='qudt':
                        predicate=URIRef(qudt + predicate) # works qudt:unit
                    else:
                        predicate=URIRef(ns + predicate)
                        
                    g.add((subject_URI, predicate,object_URI ))
    #print(stringToURI)
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
    
    print("\nStarting main() ....")   
    
    # set up file variables
    global data_dir
    data_dir = os.path.join(dirname(dirname(abspath(__file__))), 'data')
    infile="metrics_data.csv"   
    infile = os.path.join(data_dir,infile)
    mapping=get_mapping_metric()
    ns= "http://www.perspectum.com/resources/metric/"
    prefix="psp"
    print("infile: ", infile,"default Namespace",ns,prefix) 
    
    # read in CSV file and convert to RDF triples
    CSVtoRDF(infile,mapping,ns,prefix)
        
    print("\nFinished main() ....")      


if __name__ == "__main__":
    main()    
