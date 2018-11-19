#!/usr/bin/python3
#  -*- coding: utf-8  -*-
 
#import ijson
import ijson.backends.yajl2 as ijson
import bz2

fileComplete = 'wikidata.allLabels2'
fileDifferents = 'wikidata.diffsLabels2'
file4ling = 'wikidata.4Labels2'
f = bz2.BZ2File('wikidata.31.10.2018.json.bz2', 'rb') 

parser = ijson.parse(f)
#stream.write('<geo>')
es = 'EMPTY'
en = 'EMPTY'
de = 'EMPTY'
fr = 'EMPTY'
esTrue = False
enTrue = False
deTrue = False
frTrue = False
topic = 'labels'
#topic = 'descriptions'
id_ant = 'EMPTY'
id = 'EMPTY'
idMesh = 'EMPTY'  #p486
codeMesh = 'EMPTY'  #p672

i = 0
j = 0
with open(fileComplete, 'w') as all, open(fileDifferents, 'w') as difs, open(file4ling, 'w') as quad:
  for prefix, event, value in parser:
    i = i+1
    #print ('i: '+str(i))
    #print (prefix)
    if prefix.startswith('item.id'):
        id = value
        if (id is not id_ant):
            id_ant = id
            if (esTrue and enTrue and frTrue and deTrue):
                all.write(('en::'+en+'|||de::'+de+'|||es::'+es+'|||fr::'+fr+'|||WDid::'+id+'|||IDmesh::'+idMesh+'|||CodeMesh::'+codeMesh+'\n').encode('utf-8'))
                quad.write(('en::'+en+'|||de::'+de+'|||es::'+es+'|||fr::'+fr+'\n').encode('utf-8'))
                if not (en.lower() == es.lower() and es.lower() == fr.lower() and fr.lower() == de.lower()):
                    difs.write(('en::'+en+'|||de::'+de+'|||es::'+es+'|||fr::'+fr+'\n').encode('utf-8'))
#    if (enTrue and frTrue):
#        print('en::'+en+'|||fr::'+fr).encode('utf-8')
   	    esTrue = False
	    enTrue = False
	    deTrue = False
	    frTrue = False
	    es = 'EMPTY'
	    en = 'EMPTY'
	    de = 'EMPTY'
	    fr = 'EMPTY'
            idMesh = 'EMPTY'  
            codeMesh = 'EMPTY' 


    if prefix.startswith('item.claims.P486.item.mainsnak.datavalue.value'):
        idMesh = value
        #print ('kkid:' + str(value))
    if prefix.startswith('item.claims.P672.item.mainsnak.datavalue.value'):
        codeMesh = value
        #print ('kkcode:' + str(value))
    if prefix.endswith(topic+'.en.value'):
        en = value 
        enTrue = True     
    elif prefix.endswith(topic+'.es.value'):
        es = value
        esTrue = True     
    elif prefix.endswith(topic+'.de.value'):
        de = value
        deTrue = True     
    elif prefix.endswith(topic+'.fr.value'):
        fr = value
        frTrue = True     


f.close()
