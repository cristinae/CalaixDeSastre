#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Usage:
## Script to extract parallel documents from a parallel corpus with the documents IDs in a separate file
## With minor modifications it can be used for NCv9, IWSLT15 as given for the DiscoMT shared task, and
## for JRC-Acquis


import re
from itertools import izip

#cut -f3 NCv9.de-en.data > NCv9.de
#cut -f3 NCv9.en-de.data > NCv9.en
#cut -f1 NCv9.de-en.doc-ids > NCv9.ids

#cut -f3 IWSLT15.de-en.data > IWSLT15.de
#cut -f3 IWSLT15.en-de.data > IWSLT15.en
#cut -f1 IWSLT15.de-en.doc-ids > IWSLT15.ids

folder = './JRC-Acquis.de-en'
srcLang = '.en'
trgLang = '.de'
srcFile = folder+srcLang
trgFile = folder+trgLang
idsFile =  folder+'.ids'

fileName = 'None'
sourceSentences = ''
targetSentences = ''
i = 10000  #so that they are listed in the same order
with open(idsFile) as ids, open(srcFile) as src, open(trgFile) as trg: 
    for name, ss, ts in izip(ids, src, trg):
        name = name.strip()
        # Only of JRC
	try:
    	    name0 = re.search('..\/\d\d\d\d\/(.+?)-..\.xml.gz', name).group(1)
	except AttributeError:
 	    name0 = '' # apply your error handling

 	if (name0 != fileName):
	     i += 1
	     fileName = name0
	     sourceSentences = ss
	     targetSentences = ts
	else:
	     sourceSentences = sourceSentences + ss
	     targetSentences = targetSentences + ts
  	fileBase = folder+'/'+str(i)+'_'+name0
	with open(fileBase+srcLang,'wb') as fs:
             fs.write(sourceSentences)
	with open(fileBase+trgLang,'wb') as ft:
   	     ft.write(targetSentences)
           
