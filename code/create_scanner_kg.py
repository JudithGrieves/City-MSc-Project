# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 15:49:15 2021

@author: judith.grieves@city.ac.uk

INM363 Individual Project

Program to load Perspectum scanner CSV data to RDF triples.
Calls CSVtoRDF module

"""
import os
from os.path import dirname, abspath

from create_triples import CSVtoRDF

def get_mapping():        
    """
    A function to define/retrieve the CSV to RDF mapping.
    Currently hardcoded here but may be read from a file later.
    """
    # mapping: [subject class,uri col,label col, [data props], [object props]]
    mapping = [["MRIScannerModel", "Scanner Model", "Scanner Model",
                    [["FieldStrength","Scanner Field Strength","double"]
                    ,["FieldStrengthUnit","Unit","string"]]
                    ,[]] # no object properties
               ,["ScannerManufacturer", "Scanner Manufacturer", "Scanner Manufacturer"
                     ,[] # no data properties
                     ,[["isMakerOf", "Scanner Model"]] ] ]
    return mapping

          
def main():
    
    print("\nStarting create_scanner_kg() ....")   
    
    # set up file variables
    global data_dir
    data_dir = os.path.join(dirname(dirname(abspath(__file__))), 'data')
    infile="scanner_data.csv"   
    infile = os.path.join(data_dir,infile)
    mapping=get_mapping()
    print("infile: ", infile) 
    
    # read in CSV file and convert to RDF triples
    CSVtoRDF(infile,mapping)
    
    print("\nFinished create_scanner_kg() ....")      

if __name__ == "__main__":
    main()    