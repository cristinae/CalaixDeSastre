#!/usr/bin/env python
# -*- coding: utf-8 -*-

##Usage:
##Script to be used after gigawordCompile.sh to extract the raw text from the xml text. All gigaword should be in one text file.

import re

infile = open("gigaword.txt", "r")
outfile = open("gigawordRaw.txt", "w")

inline = infile.readline()
while inline != '': ##blank lines == "\n", the end of the file == ''
	counter = 0
	bufferstring = ''
	while counter < 500 and inline != '':
		while inline.strip().lower() != '<text>' and inline.strip() != '':
			inline = infile.readline()
                inline = infile.readline()
		while inline.strip().lower() != '</text>' and inline.strip() != '':
			if inline.strip().lower() != '<p>':
				bufferstring = ''.join([bufferstring, inline])
				inline = infile.readline()
				counter += 1
			else:
				inline = infile.readline()

	#order matters
	bufferstring = bufferstring.replace("\n\n", "\n")
        bufferstring = bufferstring.replace("\n", " ")
	bufferstring = bufferstring.replace("</p>", "\n")
        bufferstring = bufferstring.replace("</P>", "\n")
        bufferstring = bufferstring.replace("<text>", "\n")
        bufferstring = bufferstring.replace("<TEXT>", "\n")
        bufferstring = bufferstring.strip()
        bufferstring = bufferstring.replace("\n ", "\n")
        bufferstring = bufferstring.replace("\n\n", "\n")
        outfile.write(bufferstring)
        outfile.write('\n')
	inline = infile.readline()

