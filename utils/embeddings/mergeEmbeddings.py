#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Averages embeddings for words that appear in two different models
    Note: it only makes sense if the models share the space
    ToDo: input files from command line
    Date: 15.07.2019
    Author: cristinae
"""

import numpy as np

FILE1 = 'medical.32.en.ft.mapped'
FILE2 = 'medical.32.fr.ft.mapped'
OUTPUT = 'medical.32.enfr.ft.merged'
dim=32

embeddings1 = {}
k=0
with open(FILE1) as f:
    for line in f:
        k=k+1
        if (k>1):
           fields = line.strip().split(" ") 
           word = fields[0]
           vec = [float(v) for v in fields[1:]]
           embeddings1[word] = vec
print(str(k) + " words in " + FILE1)

embeddings2 = {}
j=0
with open(FILE2) as f:
    for line in f:
        j=j+1
        if (j>1):
          fields = line.strip().split(" ") 
          word = fields[0]
          vec = [float(v) for v in fields[1:]]
          #vec = [np.array(v) for v in fields[1:]]
          embeddings2[word] = vec
print(str(j) + " words in " + FILE2)


embeddingsMerge = embeddings1
#correct the ones that are in the other language by average
i=0
for word, vec in embeddings2.items():
    if (word in embeddings1):
        embeddingsMerge[word] =' '.join(map("{:.7f}".format, np.average(np.array([embeddings1[word], vec]), axis=0)))
        i=i+1
    else:
        embeddingsMerge[word] = ' '.join(map("{:.7f}".format, vec))
print(str(i) + " common words")

f = open(OUTPUT,'w')
f.write(str(k+i)+ " " + str(dim) + "\n")
for word, vec in embeddingsMerge.items():
    if type(vec) is str:
       f.write(word + " " + vec + "\n")
    else:
       f.write(word + " " + ' '.join(map("{:.7f}".format, vec)) + "\n")
f.close()
