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
    !!! an dummy first csv column of 'tmp' has been added to metrics_data.csv to fix an error of 'Patient_ID' not found!!!!
    metric units of measure should be retrieved from a lookup - currently hard-coded
"""
import subprocess
from subprocess import check_output
import os
from os.path import dirname, abspath

def run_rmlmapper_hardcoded(map_file,rdf_outfile):
    '''
    Function runs rmlmapper.jar to create RDF triples for a given mapping
    Parameters:
        map_file:   the RML mapping file containing the mapping rules
        rdf_outfile: the file to write RDF triples output
    BUT PARAMETER SUBSTITUTION NOT WORKING SO CURRENTLY HARDCODED TO DO BOTH KGs
    '''
    
    rmlmapper1="java -jar C:/Users/judit_k4b0noc/Downloads/rmlmapper.jar  -d -s turtle -m "
    
    rmlmapper2=" -o "
    rmlmapper3=""
    rmlmapper_cmd = rmlmapper1 + map_file + rmlmapper2 + rdf_outfile + rmlmapper3
    print("Running ... ",rmlmapper_cmd)
    #cmdline="cmd /c "+rmlmapper_cmd
    #print(cmdline)
    #subprocess.call(['java -jar C:/Users/judit_k4b0noc/Downloads/rmlmapper.jar  -d -s turtle -m ', map_file, ' -o  ', rdf_outfile])
    #subprocess.call([rmlmapper_cmd])
    os.system('cmd /c "java -jar C:/Users/judit_k4b0noc/Downloads/rmlmapper.jar  -d -s turtle -m ../data/scan-map.rml.ttl -o  ../data/scanner_data.ttl "')
    os.system('cmd /c "java -jar C:/Users/judit_k4b0noc/Downloads/rmlmapper.jar  -d -s turtle -m ../data/metric-map.rml.ttl -o  ../data/metrics_data.ttl "')
    #subprocess.run(["ls -l"])
    
def run_rmlmapper(map_file,rdf_outfile):
    '''
    Function runs rmlmapper.jar to create RDF triples for a given mapping
    Parameters:
        map_file:   the RML mapping file containing the mapping rules
        rdf_outfile: the file to write RDF triples output
    
    EXPECTS code to be running in code/ directory and output to be written to data/       
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
    map_file="metric-uom-map.rml.ttl"
    rdf_outfile="metric_uom_data.ttl"
    run_rmlmapper(map_file,rdf_outfile)
    
    map_file="scan-map.rml.ttl"
    rdf_outfile="scanner_data.ttl"
    run_rmlmapper(map_file,rdf_outfile)
    '''
    map_file="metric-map.rml.ttl"
    rdf_outfile="metric_data.ttl"
    run_rmlmapper(map_file,rdf_outfile)


if __name__ == "__main__":
    main()