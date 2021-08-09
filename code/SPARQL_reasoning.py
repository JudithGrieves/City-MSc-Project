# -*- coding: utf-8 -*-
"""
Created on Thursday 1 July 2021

@author: judith.grieves@city.ac.uk

INM363 Individual Project

Revision and evaluation of OWL2 reasoning to establish whether expected 
 elements of the created ontology are being inferred.

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
    
    # Queries - asserted
    triple_list=[]
    # asserted triples - all should be true
    triple_list.append("met:URI_Patient_P005 a omet:Patient .")
    triple_list.append("met:URI_liver_PDFF_P974_1 a omet:LiverPDFF .")
    triple_list.append("met:URI_liver_PDFF_P974_1 omet:isMetricForPatient met:URI_Patient_P974 .")
    #  Queries - inferred triples
    # LiverPDFF is a subclass of ScanMetric - not working
    triple_list.append("met:URI_liver_PDFF_P974_1 a :ScanMetric .")
    # LiverPDFF is a subclass of QMetric - working
    triple_list.append("met:URI_liver_PDFF_P974_1 a :QuantitativeMetric .")
    # :isMetricForPatient has inverse property :hasPatientMetric
    triple_list.append("met:URI_Patient_P974 omet:hasPatientMetric met:URI_liver_PDFF_P974_1 .")
    
    print("Run queries:")                   
    for triple in triple_list:
        askQueries(g, triple)      
    
    
def askQueries(g, triple):
    
    # run an ASK query on the triple
    qres = g.query(
    """ASK {""" + triple + """ }""")

    #Single row with one boolean vale
    for row in qres:
        print("Does '" + triple + "' hold? " + str(row))

def OWLRLReasoning():
    '''
    Function to read in an ontology and related instance TTL files,
    apply OWL2 reasoning to the triples and save the graph, including
    the newly inferred data triples, to a new file.
    Execute a testQueries function on the inferred data.
    '''
    print("\nStarting OWLRLReasoning")    
    
    ont_dir = os.path.join(dirname(dirname(abspath(__file__))), 'ontology')    
    ontology_file="ont_metric.xml"
    ontology_file = os.path.join(ont_dir,ontology_file)
    
    data_dir = os.path.join(dirname(dirname(abspath(__file__))), 'data')
    instance_file="metric_data.ttl"
    instance_file = os.path.join(data_dir,instance_file)
    
    output_file="metric_inference"
    output_file = os.path.join(data_dir,output_file)    
    
    g = Graph()
    
    print("Reading file: ",instance_file)   
    g.parse(instance_file, format="ttl")    
    print("Loaded '" + str(len(g)) + "' triples.")    

    print("Reading file: ",ontology_file)   
    g.load(ontology_file)    
    print("Triples including ontology: '" + str(len(g)) + "'.")    
    
    Infer=True
    #  apply reasoning and expand the graph with new triples 
    if Infer:        
        owlrl.DeductiveClosure(owlrl.OWLRL_Semantics, axiomatic_triples=True, datatype_axioms=False).expand(g)
        print("Triples after OWL 2 RL reasoning: '" + str(len(g)) + "'.")    
        print("Writing file: ",output_file+'.ttl')
        g.serialize(destination=output_file+'.ttl', format='ttl')      
        print("Writing file: ",output_file+'.owl')
        g.serialize(destination=output_file+'.owl', format='xml')     
    else:
        # to debug 'default1:' prefix in the inferred graph data, manually
        # edit the file produced and read it in instead of DeductiveClosure
        # ExpatError: not well-formed (invalid token): line 1, column 0
        inferred_file="metric_inference_man.ttl"
        inferred_file = os.path.join(data_dir,inferred_file)
        print("Reading file: ",inferred_file)   
        g.load(inferred_file)    
        print("Triples including manual inferred triples file: '" + str(len(g)) + "'.")    
    
    # test queries
    testQueries(g)  
    print("Finished OWLRLReasoning")
    
def main():
    OWLRLReasoning()
    
    
if __name__ == "__main__":
    main()    

