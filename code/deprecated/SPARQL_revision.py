# -*- coding: utf-8 -*-
'''
Created on 29 June 2021

@author: judith.grieves@city.ac.uk

INM363 Individual Project

code to try out different SPARQL syntaxes: for references and to fix a bug. ?visit .

'''
from rdflib import Graph

import os
from os.path import dirname, abspath

from write_sparql_file import write_sparql


def query1(g):
    # basic SELECT WHERE
    qres = g.query(
    """SELECT DISTINCT  ?a ?b ?c ?d ?e ?f ?g WHERE
                { 
                 ?p a omet:Patient .
                 ?p rdfs:label ?a . FILTER (?a < "P978") 
                 }
    ORDER BY ASC(?a) 
    LIMIT 5
    OFFSET 5 
                """) 
    print("Results 1:")                
    for row in qres:
        print(row.a,  row.b, row.c,  row.d, row.e, row.f, row.g)
    
def query2(g):
    # all PDFFs
    qres = g.query(
    """SELECT DISTINCT  ?a ?b ?c ?d ?e ?f ?g WHERE
                {  
                 ?p a omet:Patient .
                 ?p rdfs:label ?a .
                 OPTIONAL {?metric omet:isMetricForPatient ?p .
                           ?metric qudt:value ?b .
                           ?metric qudt:unit ?c .
                           ?metric a omet:liver_PDFF}
                 }
    ORDER BY ASC(?a)  
    LIMIT 10
                """) 
    print("Results 2:")    
    for row in qres:
        print(row.a,  row.b, row.c,  row.d, row.e, row.f, row.g)
        
def query3(g):
    # single metric with FILTER
    qres = g.query(
    """SELECT DISTINCT  ?a ?b ?c ?d ?e ?f ?g WHERE
                { 
                 ?p a omet:Patient .
                 ?p rdfs:label ?a .
                 OPTIONAL {?metric omet:isMetricForPatient ?p .
                           ?metric qudt:value ?b .
                           ?metric qudt:unit ?c .
                           ?metric a omet:liver_PDFF}
                 FILTER ( ?b < 6.0 )
                 }
    ORDER BY ASC(?a)  
                """) 
    print("Results 3:")    
    for row in qres:
        print(row.a,  row.b, row.c,  row.d, row.e, row.f, row.g)
        
def query4(g):
    '''
    multi metric without filter or group
    note that Metric rows are merged without UNION or GROUP BY
    when returning by visit
    '''
    qres = g.query(
    """SELECT DISTINCT  ?a ?b ?c ?d ?e ?f ?g WHERE
                { 
                 ?p a omet:ScanVisit.
                 ?p rdfs:label ?a .
                 OPTIONAL {?PDFF omet:isMetricForVisit ?p .
                           ?PDFF qudt:value ?b .
                           ?PDFF a omet:liver_PDFF}
                 OPTIONAL {?cT1 omet:isMetricForVisit ?p .
                           ?cT1 qudt:value ?c .
                           ?cT1 a omet:liver_cT1}
                 }
    ORDER BY ASC(?a)  
                """) 
    print("Results 4:")    
    for row in qres:
        print(row.a,  row.b, row.c,  row.d, row.e, row.f, row.g)
        
def query5(g):
    '''
    multi metric grouped.  note that rows are merged where a Patient has > 1
    visit but the single Metric value is arbitrarily chosen from multiples
    '''
    qres = g.query(
    """SELECT DISTINCT  ?a ?b ?c ?d ?e ?f ?g WHERE
                { 
                 ?p a omet:Patient.
                 ?p rdfs:label ?a .
                  {?PDFF omet:isMetricForPatient ?p .
                           ?PDFF qudt:value ?b .
                           ?PDFF a omet:liver_PDFF}
                  {?cT1 omet:isMetricForPatient ?p .
                           ?cT1 qudt:value ?c .
                           ?cT1 a omet:liver_cT1}
                 } 
    GROUP BY ?a
    ORDER BY ASC(?a)  
                """) 
    print("Results 5:")    
    for row in qres:
        print(row.a,  row.b, row.c,  row.d, row.e, row.f, row.g)
        
def query6(g):
    '''
    Multi metric by visit - 3 filters but no group needed
    applying all filters as expected.
    '''
    qres = g.query(
    """SELECT DISTINCT  ?a ?b ?c ?d ?e ?f ?g WHERE
                { 
                 ?p a omet:ScanVisit.
                 ?p rdfs:label ?a .
                 OPTIONAL {?PDFF omet:isMetricForVisit ?p .
                           ?PDFF qudt:value ?b .
                           ?PDFF a omet:liver_PDFF}
                 FILTER ( ?b < 6.0 )
                 OPTIONAL {?cT1 omet:isMetricForVisit ?p .
                           ?cT1 qudt:value ?c .
                           ?cT1 a omet:liver_cT1}
                 FILTER ( ?c > 800 )
                 OPTIONAL {?Age omet:isMetricForVisit ?p .
                           ?Age qudt:value ?d .
                           ?Age a omet:PatientAge}
                 FILTER ( ?d > 40 )
                 }
    ORDER BY ASC(?a)  
                """) 
    print("Results 6:")    
    for row in qres:
        print(row.a,  row.b, row.c,  row.d, row.e, row.f, row.g)
        
    
def main():
    
    print("\nStarting SPARQLqueries")
    
    data_dir = os.path.join(dirname(dirname(abspath(__file__))), 'data')        
        
    inFile1="metric_data.ttl" 
    inFile1 = os.path.join(data_dir,inFile1)
    
    g = Graph()    
    g.parse(inFile1, format="ttl")         

    # run SPARQL queries against the loaded graph
    
    query1(g) 
    query2(g) 
    query3(g) 
    query4(g) 
    query5(g) 
    query6(g) 
    
    print("\nFinished SPARQLqueries")
          

Display=False       

if __name__ == "__main__":
    main()
