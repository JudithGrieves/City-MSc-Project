# -*- coding: utf-8 -*-
"""
Created on Thursday 1 July 2021

@author: judith.grieves@city.ac.uk

INM363 Individual Project


This code loads .owl file for an Ontology and .ttl for a set of data instances
and performs OWL RL Reasoning on the triples, writing out a new file of 
the asserted and inferred triples (.ttl and .owl).

Instance data from Perspectum Covid study CSV data converted to RDF triples.

    
"""
from rdflib import Graph

import owlrl

import os
from os.path import dirname, abspath


def testQueries(g):
    
    print("\nTest Queries: ")
    
    triple1 = "psp:URI_LiverT2Star_997 psp:isMetricForPatient psp:URI_Patient_P005 ."
    triple2 = "psp:URI_Patient_P005 psp:isMetricForPatient psp:URI_LiverT2Star_997 ."
    triple3 = "psp:URI_Patient_P005 psp:hasPatientMetric psp:URI_LiverT2Star_997 ."
    
    askQueries(g, triple1)
    askQueries(g, triple2)
    askQueries(g, triple3)
      
    
    
def askQueries(g, triple):
    
    # run an ASK query on the triple
    qres = g.query(
    """ASK {""" + triple + """ }""")

    #Single row with one boolean vale
    for row in qres:
        print("Does '" + triple + "' hold? " + str(row))

def OWLRLReasoning():
    
    print("\nStarting OWLRLReasoning")
    
    
    ont_dir = os.path.join(dirname(dirname(abspath(__file__))), 'ontology')    
    ontology_file="ontologyV1_0.xml"
    ontology_file = os.path.join(ont_dir,ontology_file)
    
    data_dir = os.path.join(dirname(dirname(abspath(__file__))), 'data')
    instance_file="test_data14.ttl"
    instance_file = os.path.join(data_dir,instance_file)
    
    output_file="test14_inference"
    output_file = os.path.join(data_dir,output_file)
    
    
    g = Graph()
    
    print("Reading file: ",instance_file)   
    g.parse(instance_file, format="ttl")
    
    print("Loaded '" + str(len(g)) + "' triples.")    

    print("Reading file: ",ontology_file)   
    g.load(ontology_file) 
    
    print("Triples including ontology: '" + str(len(g)) + "'.")    
    
    #  apply reasoning and expand the graph with new triples 
    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics, axiomatic_triples=False, datatype_axioms=False).expand(g)
    
    print("Triples after OWL 2 RL reasoning: '" + str(len(g)) + "'.")
        
    # test queries
    testQueries(g)
    
    
    print("Writing file: ",output_file+'.ttl')
    g.serialize(destination=output_file+'.ttl', format='ttl')  
    
    print("Writing file: ",output_file+'.owl')
    g.serialize(destination=output_file+'.owl', format='xml')  
    
    
    print("Finished OWLRLReasoning")
    
def main():
    OWLRLReasoning()
    
    
if __name__ == "__main__":
    main()    

