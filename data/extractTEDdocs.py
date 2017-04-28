#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Usage:
## Script to extract parallel documents from the TED data obtained from OPUS


import re
from itertools import izip

folder = './TED'
srcLang = '.en'
trgLang = '.es'
srcFile = 'train.tags.en-es'+srcLang
trgFile = 'train.tags.en-es'+trgLang

fileName = 'None'
sourceSentences = ''
targetSentences = ''
i = 10000  #so that they are listed in the same order

patternIni = re.compile("^<url>(.+)</url>")
patternTitle = re.compile("^\s*<title>(.+)</title>$")
patternIDde = re.compile("^\s*<talkid>(\d+)</talkid>$")
patternID = re.compile("^\s*<doc docid=\"(\d+)\"\s")
patternDesc = re.compile("^\s*<description>(.+)</description>$")
#patternText = re.compile("^(?!<)\w+$")
name = ''

with open(srcFile) as src, open(trgFile) as trg: 
    for ss, ts in izip(src, trg):
 	if patternIni.match(ss):
 	     if i>10000:
 	        fileBase = folder+'/'+str(i)+'_'+name
		print fileBase
 	        with open(fileBase+srcLang,'wb') as fs:
                  fs.write(sourceSentences)
	        with open(fileBase+trgLang,'wb') as ft:
   	          ft.write(targetSentences)
		sourceSentences = ''
		targetSentences = ''
	     i += 1
	elif patternID.match(ss): 
	     name = patternID.match(ss).group(1)
	     if not patternID.match(ts):
		print 'Some error occurred: IDs are not aligned'
	elif patternTitle.match(ss): 
	     sourceSentences = patternTitle.match(ss).group(1) + "\n"
	     if patternTitle.match(ts):
	        targetSentences = patternTitle.match(ts).group(1)+ "\n"
	     else:
		print 'Some error occurred: Titles are not aligned'
        # we dont add descriptions for the moment
	#elif patternDesc.match(ss): 
	#     sourceSentences = sourceSentences + patternDesc.match(ss).group(1)+ "\n"
	#     if patternDesc.match(ts):
	#        targetSentences = targetSentences + patternDesc.match(ts).group(1)+ "\n"
	#     else:
	#	print 'Some error occurred: Descriptions are not aligned'
	elif not ss.startswith("<"): 
	     sourceSentences = sourceSentences + ss
	     if not ts.startswith("<"):
	        targetSentences = targetSentences + ts
	     else:
		print 'Some error occurred: Texts are not aligned'


          
