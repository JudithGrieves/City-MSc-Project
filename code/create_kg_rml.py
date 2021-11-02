# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 16:56:41 2021


@author: judith.grieves@city.ac.uk

INM363 Individual Project

Code to run the RMLmapper command for a specified RML mapping file and
RDF triples output file.

ISSUES:
    subprocess.run not working with full file paths - to be investigated.
    the current run_rmlmapper function has ../data hardcoded in them
    a dummy first csv column of 'tmp' has been added to metrics_data.csv to fix an error of 'Patient_ID' not found
"""
import subprocess
from subprocess import check_output
import os
from os.path import dirname, abspath

    
def run_rmlmapper(map_file,rdf_outfile):
    '''
    Function runs rmlmapper.jar to create RDF triples for a given mapping
    Parameters:
        map_file:   the RML mapping file containing the mapping rules
        rdf_outfile: the file to write RDF triples output
    
    expects code to be running in code/ directory and output to be written to data/       
    '''
    data_sub="../data/"
    map_file=data_sub + map_file
    rdf_outfile=data_sub + rdf_outfile
    rmlmapper_cmd = str.format(
        "java -jar rmlmapper.jar  -d -s turtle -m {0} -o  {1} ", \
            map_file,rdf_outfile)
    print("Running rmlmapper_param function ... ",rmlmapper_cmd)
    subprocess.run(rmlmapper_cmd,  check=True)

def main():
    
    print("\nStarting create_kg_rml.py")
    
    '''
    # deprecated UoM ontology
    map_file="metric-uom-map.rml.ttl"
    rdf_outfile="metric_uom_data.ttl"
    run_rmlmapper(map_file,rdf_outfile)
    '''
    map_file="scan-map.rml.ttl"
    rdf_outfile="scanner_data.ttl"
    run_rmlmapper(map_file,rdf_outfile)
    
    map_file="metric-map.rml.ttl"
    rdf_outfile="metric_data.ttl"
    run_rmlmapper(map_file,rdf_outfile)


if __name__ == "__main__":
    main()