# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 10:04:04 2021

@author: judith.grieves@city.ac.uk

INM363 Individual Project

Program to run all modules in a system test:
    
    create scanner kg
    create metrics kg
    Test query on KGs

ADD THIS PROG TO GITHUB    
ADD sparql EXAMPLE QUERIES
MERGE CREATE_SCANNER_KG AND CREATE_METRICS_KG AND PARAMETERISE    
"""
import os
from os.path import dirname, abspath
from rdflib import Graph

from create_kg import CSVtoRDF
from create_scanner_kg import get_map_scan
from create_metrics_kg import get_map_metric
from SPARQL_test import query_all

def main():
    
    global data_dir
    data_dir = os.path.join(dirname(dirname(abspath(__file__))), 'data')
    infile="scanner_data.csv"   
    infile = os.path.join(data_dir,infile)
    mapping=get_map_scan()
    ns= "http://www.perspectum.com/resources/scanner/"
    prefix="scn"
    print("infile: ", infile,"Namespace",ns,prefix) 
    
    # run external function to read in CSV file and convert to RDF triples
    CSVtoRDF(infile,mapping,ns,prefix)
    
    
    infile="metrics_data.csv"   
    infile = os.path.join(data_dir,infile)
    mapping=get_map_metric()
    
    ns= "http://www.perspectum.com/resources/metric/"
    prefix="psp"
    print("infile: ", infile,"Namespace",ns,prefix) 
    CSVtoRDF(infile,mapping,ns,prefix)
    
    
    inFile1="metrics_data.ttl" 
    inFile2="scanner_data.ttl" 
    outFile=inFile1.replace(".ttl", "-")+"replicate.csv"  
    
    inFile1 = os.path.join(data_dir,inFile1)
    inFile2 = os.path.join(data_dir,inFile2)
    output_dir = data_dir
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
    
if __name__ == "__main__":
    main()   