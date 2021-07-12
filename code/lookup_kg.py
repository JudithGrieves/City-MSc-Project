# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 13:25:43 2021

@author: judith.grieves@city.ac.uk

INM363 Individual Project

Program to lookup data in an existing KG, specified as a TTL file.

"""

import os
from os.path import dirname, abspath
from rdflib import Graph
from rdflib import Namespace

from rdflib import plugins
from rdflib.plugins.sparql import prepareQuery


def get_uri_lit(g):
    '''
    Query local graph g for a literal search term, embedded in the SPARQL.
    For information only.
    '''           
    print("\nSingle Scanner literal=philips:")
    qres = g.query(
    """SELECT DISTINCT ?urimod ?fs
       WHERE {
          ?urimod rdf:type scn:MRIScannerModel .
          ?urimod  scn:FieldStrength ?fs  . 
    FILTER(CONTAINS(STR(?urimod),"Philips_ModelB"))} 
    ORDER BY ASC(?urimod)  """)    

    for row in qres:
        print("%s is a scanner with fs %s" % row)
        
def get_scanner_sparql(search_term):
       
    sparql1='SELECT DISTINCT ?urimod ?model ?manf ?fs ?unit WHERE \
        { ?urimod rdf:type scn:MRIScannerModel . \
          ?urimod scn:FieldStrength ?fs  . \
          ?urimod  scn:FieldStrengthUnit ?unit  . \
          ?urimod  rdfs:label ?model  . \
          ?urimanf   scn:isMakerOf ?urimod . \
          ?urimanf  rdfs:label ?manf  . \
    FILTER(CONTAINS(STR(?model),'
    
    
    sparql2='))}   ORDER BY DESC(?urimod)'
    query=sparql1+"'"+search_term+"'"+sparql2      
    
    return query
        
def get_uri(g,search_term,Display=False): 
    '''
    Function to query a graph g of scanner data for a label value 
    (parameter=search_term) and return the scanner entity URI.
    Assumes graph, g, is already loaded.
    Returns blank when not found and first row when multiples found.
    '''           
    
    ns= "http://www.perspectum.com/resources/scanner/"       
    scn = Namespace(ns)
    row=''
 
    query=get_scanner_sparql(search_term)
    #print("\nSingle Scanner variable:",search_term)  
    q = prepareQuery(query,initNs = { "scn": scn })
    
    # add a check on multiple rows returned
    for row in g.query(q):
        if Display:
            print(row.urimod,row.model,row.manf,row.fs,row.unit)
    
    #return the first URI by alphabetical order    
    if row:
        return row.urimod
    else:
        return ''
 
def load_triples(fileKG,Display=False):
    '''
    Function to load a graph g from a TTL file (parameter fileKG)
    '''             

    data_dir = os.path.join(dirname(dirname(abspath(__file__))), 'data')
    infile = os.path.join(data_dir,fileKG)
    
    g = Graph()
    g.parse(infile, format="ttl")
    
    
    if Display:
        print("Loaded '" + str(len(g)) + "' triples.")
            
    if Display:
        for s, p, o in g:
            print((s.n3(), p.n3(), o.n3()))
    return g    
           
def get_scanner_uri(search_term):
    '''
    Function to load a graph g of scanner data, search for an entity for a 
    parameter search term, scanner_label, and return the URI.
    Returns blank when not found and first row when multiples found.
    '''           
    fileKG="scanner_data.ttl"
    g=load_triples(fileKG)
    uri = get_uri(g,search_term)
    return uri
    
def main():
    
    print("\nStarting main() ....")   
    
    global Display
    Display=False
    # set the parameter search term    
    scanner_label="Siemens_ModelA"
    
    # test get_scanner_uri
    uri =  get_scanner_uri(scanner_label)
    print("uri returned from get_scanner_uri: ",uri)
    
    
    # test get_uri, needs an explicit load of graph triples
    #Load triples
    fileKG="scanner_data.ttl"
    s=load_triples(fileKG)
    uri = get_uri(s,scanner_label)
    print("uri returned from get_uri: ",uri)
    
    # query local graph for a literal search term
    #get_scanner_lit(g)
    
    
    print("\nFinished main() ....")      


if __name__ == "__main__":
    main()    
