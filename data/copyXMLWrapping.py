#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, re

def main(inputXML,inputRAW):

    outputXML = inputRAW+".xml"

    patternIni = re.compile("^\s*<\?xml version=")
    patternRoot = re.compile("^\s*<dataset id=")
    patternDoc = re.compile("^\s*<doc link=")
    patternGeneral = re.compile("^\s*<.+>\s*$")

    segments = []
    with open(inputRAW) as inRaw:
         segments = [line.strip() for line in inRaw]
    with open(outputXML,'wb') as fs:
         with open(inputXML) as inXML:
              for line in inXML:
                  if patternGeneral.match(line):
                     fs.write(line)
		  else:
                     # segments could be empty
                     fs.write(segments.pop(0)+"\n")
              if segments: 
                 print ("mismatch error")


if __name__ == "__main__":
    
    if len(sys.argv) is not 3:
        sys.stderr.write('Usage: python3 %s inputXML inputRAW\n' % sys.argv[0])
        sys.exit(1)

main(sys.argv[1], sys.argv[2])
