# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 16:56:41 2021


@author: judith.grieves@city.ac.uk

INM363 Individual Project

Code to run the RMLmapper command for a specified RML mapping file and
RDF triples output file.

ISSUES:
    metric units of measure should be retrieved from a lookup - currently hard-coded
    this code should run the rmlmapper command based on input file parameters - currently hard-coded
"""
import subprocess
import os
from os.path import dirname, abspath

def run_rmlmapper(map_file,rdf_outfile):
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
    os.system('cmd /c "java -jar C:/Users/judit_k4b0noc/Downloads/rmlmapper.jar  -d -s turtle -m scan-man-map.rml.ttl -o  scan-man.rdf.ttl "')
    os.system('cmd /c "java -jar C:/Users/judit_k4b0noc/Downloads/rmlmapper.jar  -d -s turtle -m metric-man-map.rml.ttl -o  metric-man.rdf.ttl "')
    #subprocess.run(["ls -l"])
    
def run_rmlmapper_fixed(map_file,rdf_outfile):
    '''
    Function runs rmlmapper.jar to create RDF triples for a given mapping
    Parameters:
        map_file:   the RML mapping file containing the mapping rules
        rdf_outfile: the file to write RDF triples output
    NOT CURRENTLY RUNNING THE CMDLINE CODE        
    '''
    
    rmlmapper1="java -jar C:/Users/judit_k4b0noc/Downloads/rmlmapper.jar  -d -s turtle -m "
    
    rmlmapper2=" -o "
    rmlmapper3=""
    rmlmapper_cmd = rmlmapper1 + map_file + rmlmapper2 + rdf_outfile + rmlmapper3
    rmlmapper_cmd = str.format(
        "java -jar C:/Users/judit_k4b0noc/Downloads/rmlmapper.jar  -d -s turtle -m {0} -o  {1} ",map_file,rdf_outfile)
    print("Running ... ",rmlmapper_cmd)
    #cmdline="cmd /c "+rmlmapper_cmd
    #print(cmdline)
    #os.system(cmdline)

def another_func():
    '''
    Testing string concatenation
    '''
    p1="one"
    p2="two"
    person_string = str.format(
        "Hello, my name is {0}, my siblings are {1} ",p1,p2)
    print(person_string)

def main():
    
    print("\nStarting test.py")
    
    data_dir = dirname(abspath(__file__))
    print("DIR ",data_dir)
    
    map_file="scan-man-map.rml.ttl"
    map_file = os.path.join(data_dir,map_file)
    print(map_file)
    rdf_outfile="scan-man.rdf.ttl"   
    rdf_outfile = os.path.join(data_dir,rdf_outfile)
    
    run_rmlmapper(map_file,rdf_outfile)
    #run_rmlmapper_fixed(map_file,rdf_outfile)
    #another_func()


if __name__ == "__main__":
    main()