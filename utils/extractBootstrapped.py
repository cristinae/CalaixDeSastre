#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Generates bootstrapped corpora
    (not optimised for large files)
    Date: 03.10.2020
    Author: cristinae
"""

import sys, warnings
import argparse
import random


def get_parser():
    """
    Creates a new argument parser.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--iFile',
                    required=True,
                    type=str,
                    default="", 
                    metavar="<inputFile>",
                    help="Input file" )
    parser.add_argument('-b', '--bootstraps',
                    required=False,
                    type=int,
                    default=10, 
                    metavar="<#files>",
                    help="Number of bootstraped files to generate (default 10)" )
    parser.add_argument('-s', '--samples',
                    required=False,
                    type=int,
                    default=10000, 
                    metavar="<#samples>",
                    help="Number of sentences to be extracted from the input file (default 10000)" )
    return parser


def main(args=None):

    '''Get command line arguments'''
    parser = get_parser()
    args = parser.parse_args(args)
 
    ''' Read the input file'''
    nameINfile=args.iFile
    with open(nameINfile, 'r') as file:
        fullCorpus=file.read().split('\n')

    if(len(fullCorpus) < args.samples):
       warnings.warn('Your corpus has '+str(len(fullCorpus))+' lines and you are creating files with '+str(args.samples)+' lines')

    i=0
    while i<args.bootstraps:
       fOUT=open(nameINfile+str(i), 'w')
       randomLines = random.choices(fullCorpus, k=args.samples) 
       for line in randomLines:
           fOUT.write("%s\n" % line)
       fOUT.close
       i+=1


if __name__ == "__main__":
   main()
