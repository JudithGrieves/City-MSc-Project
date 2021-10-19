# -*- coding: utf-8 -*-
'''
Created on 29 June 2021

@author: judith.grieves@city.ac.uk

INM363 Individual Project

code to query the ontology

'''
from rdflib import Graph

import os
from os.path import dirname, abspath



def query_obj_props(g):
    
    qres = g.query(
    """SELECT DISTINCT     ?objprop ?domain ?range ?comment WHERE
                { 
                 ?objprop_URI rdf:type owl:ObjectProperty .
                 ?objprop_URI rdfs:label ?objprop .
                 
                 OPTIONAL { ?objprop_URI rdfs:comment ?comment . }
                 
                 OPTIONAL { ?objprop_URI rdfs:domain ?domain_URI .
                           ?domain_URI rdfs:label ?domain . }
                 OPTIONAL { ?objprop_URI rdfs:range ?range_URI . 
                           ?range_URI rdfs:label ?range . }
                 }
    ORDER BY  ASC(?objprop) 
                """) 
    print("\nObject Properties:")                  
    for row in qres:
        print(row.domain,":",row.objprop,":",row.range,":",row.comment)
        
def query_classes(g):
    
    qres = g.query(             
    """SELECT DISTINCT    ?Class ?subclass  ?comment WHERE
                { 
                 ?class_URI rdf:type owl:Class .
                 ?class_URI rdfs:label ?Class .
                 OPTIONAL { ?class_URI rdfs:comment ?comment . }
                 OPTIONAL { ?class_URI  rdfs:subClassOf ?subclass_URI . 
                 ?subclass_URI rdfs:label ?subclass .}
                 }
    ORDER BY  ASC(?Class) 
                """) 
    print("Classes:")              
    for row in qres:
        print(row.Class,"; subclass of ( ", row.subclass," ) ;", row.comment )
           
    
def main():
    
    print("\nStarting SPARQL_ontology")
    
    ont_dir = os.path.join(dirname(dirname(abspath(__file__))), 'ontology')        
        
    inFile1="ont_metric.ttl" 
    inFile1 = os.path.join(ont_dir,inFile1)
    
    g = Graph()    
    g.parse(inFile1, format="ttl")   
    owlrl.DeductiveClosure(owlrl.RDFS_Semantics, axiomatic_triples=True, datatype_axioms=True).expand(g)      

    # run SPARQL queries against the loaded graph
    
    query_classes(g) 
    query_obj_props(g)
    
    print("\nFinished SPARQL_ontology")

def main_new():
    
    print("\nStarting SPARQL_ontology")
    
    ont_dir = os.path.join(dirname(dirname(abspath(__file__))), 'ontology')        
        
    #for inFile in ["ont_metric.ttl" ,"ont_scanner.ttl" ]:  
    for inFile in ["ont_liver.ttl" ]:   
        print("\nOntology: ",inFile)
        inFile = os.path.join(ont_dir,inFile)    
        g = Graph()    
        g.parse(inFile, format="ttl")  
        query_classes(g) 
        query_obj_props(g)
    
    print("\nFinished SPARQL_ontology")
          

Display=False       

if __name__ == "__main__":
    main_new()
