# -*- coding: utf-8 -*-
'''
Created on 6 July 2021

@author: judith.grieves@city.ac.uk

INM363 Individual Project

This code writes SPARQL query results to a CSV file

'''


def write_sparql(outfile,header,qres,todisp,tofile):
    '''
    Write the results of a SPARQL query 'qres', with comma-delimited 
    'header' string to file 'outFile'
    '''
    with open(outfile, 'w', newline='', encoding='utf-8') as file:
        if todisp:
            print(header) # dynamically written csv row 
        if tofile:
            file.write(header+"\n") # dynamically written csv row 
        for row in qres:
            printstr=""
            for x in range(len(row)):
                printstr= printstr + "%s,"
            if todisp:
                print(printstr % row)
            if tofile:
                file.write(printstr % row) # dynamically written csv row
                file.write('\n')

