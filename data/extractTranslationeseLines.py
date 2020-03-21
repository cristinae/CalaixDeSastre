#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Extract translationese sentences (line number) from news testsets
    Date: 21.03.2020
    Author: cristinae
"""

from BeautifulSoup import BeautifulSoup

f = open('newstest2018-ende-ref.de.sgm', 'r')
data= f.read()
soup = BeautifulSoup(data)
i=0
for docs in soup('doc'):
     lang=docs['origlang']
     for segs in docs.findChildren('seg'):
         if(lang == 'en'):
            print(i+1)
         i=i+1

