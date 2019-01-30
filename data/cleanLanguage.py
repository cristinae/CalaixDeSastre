#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Creates a copy of a corpus only with the sentences identified as the
    desired language 
    Date: 29.01.2019
    Author: cristinae
"""

from langdetect import DetectorFactory
from langdetect import detect
import sys

DetectorFactory.seed = 0


def main(inF, lan):

    outF = inF + '.lanClean'
    fOUT = open(outF, 'w')
    with open(inF) as f:
       count = 0
       for line in f:
           line = line.strip()
           if line == '':
              fOUT.write(line+"\n")
              continue
           try:
              detected = detect(line.decode("utf-8"))
              if detected == lan:
                  fOUT.write(line+"\n")
              else:
                  count = count + 1
           except:
             print(line)
       print(count + ' sentences discarded')
    fOUT.close() 


if __name__ == "__main__":
    
    if len(sys.argv) is not 3:
        sys.stderr.write('Usage: python3 %s inputFile language\n' % sys.argv[0])
        sys.exit(1)
main(sys.argv[1], sys.argv[2])

