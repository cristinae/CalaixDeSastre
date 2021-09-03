#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Script (dirty) for the statistical analysis of the manual evaluation for
    the WMT 2021 shared task
    Date: 20.08.2021
    Author: cristinae
"""

import sys
import warnings
import math
import numpy as np
import collections
import pandas as pd

from pandas.core.common import SettingWithCopyWarning
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

def getAnnotatorsIDs(df,column):
   return(df[column].unique())

def getSystemsIDs(df,column):
   return(df[column].unique())

def fleiss_kappa(M):
    """
    https://gist.github.com/skylander86/65c442356377367e27e79ef1fed4adee
    See `Fleiss' Kappa <https://en.wikipedia.org/wiki/Fleiss%27_kappa>`_.
    :param M: a matrix of shape (:attr:`N`, :attr:`k`) where `N` is the number of subjects and `k` is the number of categories into which assignments are made. `M[i, j]` represent the number of raters who assigned the `i`th subject to the `j`th category.
    :type M: numpy matrix
    """
    N, k = M.shape  # N is # of items, k is # of categories
    n_annotators = float(np.sum(M[0, :]))  # # of annotators
    #print(N,k,n_annotators)

#    n_annotators = 2.0
    p = np.sum(M, axis=0) / (N * n_annotators)  
    P = (np.sum(M * M, axis=1) - n_annotators) / (n_annotators * (n_annotators - 1))
    Pbar = np.sum(P) / N
    PbarE = np.sum(p * p)

    kappa = (Pbar - PbarE) / (1 - PbarE)
    stdErr = math.sqrt(Pbar*(1-Pbar)/(N*(1-PbarE)**2))

    return (str(round(kappa,2))+'$\pm$'+str(round(stdErr,2)))
  
def nominal_metric(a, b):
    return a != b


def interval_metric(a, b):
    return (a-b)**2


def ratio_metric(a, b):
    return ((a-b)/(a+b))**2


def krippendorff_alpha(data, metric=interval_metric, force_vecmath=False, convert_items=float, missing_items=None):
    '''
    https://github.com/grrrr/krippendorff-alpha/blob/master/krippendorff_alpha.py
    Calculate Krippendorff's alpha (inter-rater reliability):
    
    data is in the format
    [
        {unit1:value, unit2:value, ...},  # coder 1
        {unit1:value, unit3:value, ...},   # coder 2
        ...                            # more coders
    ]
    or 
    it is a sequence of (masked) sequences (list, numpy.array, numpy.ma.array, e.g.) with rows corresponding to coders and columns to items
    
    metric: function calculating the pairwise distance
    force_vecmath: force vector math for custom metrics (numpy required)
    convert_items: function for the type conversion of items (default: float)
    missing_items: indicator for missing items (default: None)
    '''
    
    # number of coders
    m = len(data)
    
    # set of constants identifying missing values
    if missing_items is None:
        maskitems = []
    else:
        maskitems = list(missing_items)
    if np is not None:
        maskitems.append(np.ma.masked_singleton)
    
    # convert input data to a dict of items
    units = {}
    for d in data:
        try:
            # try if d behaves as a dict
            diter = d.items()
        except AttributeError:
            # sequence assumed for d
            diter = enumerate(d)
            
        for it, g in diter:
            if g not in maskitems:
                try:
                    its = units[it]
                except KeyError:
                    its = []
                    units[it] = its
                its.append(convert_items(g))


    units = dict((it, d) for it, d in units.items() if len(d) > 1)  # units with pairable values
    n = sum(len(pv) for pv in units.values())  # number of pairable values
    
    if n == 0:
        raise ValueError("No items to compare.")
    
    np_metric = (np is not None) and ((metric in (interval_metric, nominal_metric, ratio_metric)) or force_vecmath)
    
    Do = 0.
    for grades in units.values():
        if np_metric:
            gr = np.asarray(grades)
            Du = sum(np.sum(metric(gr, gri)) for gri in gr)
        else:
            Du = sum(metric(gi, gj) for gi in grades for gj in grades)
        Do += Du/float(len(grades)-1)
    Do /= float(n)

    if Do == 0:
        return 1.

    De = 0.
    for g1 in units.values():
        if np_metric:
            d1 = np.asarray(g1)
            for g2 in units.values():
                De += sum(np.sum(metric(d1, gj)) for gj in g2)
        else:
            for g2 in units.values():
                De += sum(metric(gi, gj) for gi in g1 for gj in g2)
    De /= float(n*(n-1))

    return 1.-Do/De if (Do and De) else 1.  



def call4Fleiss(df, uniqID):

    sentences = df[uniqID].unique()
    M = len(sentences)-1
    print(M, "items")
    N = 6  # likert scale
    input4Fleiss = np.array([[0 for i in range(N)]] * M)
    # Sorting (with a stable algorithm) to later take into account that the same user might have evaluated the same sentence twice
    # For interannotator agreement we only consider the first instance
    df.sort_values(by=['username'], inplace=True, kind='mergesort', ascending=False)
    #df.sort_values(by=['username'], inplace=True, kind='quicksort', ascending=False)
    for i in range(M):
          scores = df.loc[df[uniqID]==i+1]['score']
          raters = np.array(df.loc[df[uniqID]==i+1]['username'])
          #print(df.loc[df['sentence']==i+1])
          #scores = df.loc[(df['sentence']==i+1 and df['username']=='catoci6603')]['score']
          input4Fleiss[i] = [0 for k in range(N)]   # necessito aquesta linea i no entenc per que
          # some sentences were annotated twice, we only keep the first one per annotator
          ann = 'nobody'
          j = 0
          for score in scores:
              if (ann != raters[j]):
                 #input4Fleiss[i][score-1] = input4Fleiss[i][score-1] + 1
                 input4Fleiss[i][score] = input4Fleiss[i][score] + 1
              ann = raters[j]
              j += 1
    fleiss = fleiss_kappa(input4Fleiss)
    print(fleiss)

  
  
def main(inputCSV):

    extractCols = ['username','documentID','targetID','seg_id','score','phrase_evaluation','itemType']
    df = pd.read_csv(inputCSV, usecols=extractCols)
    print(len(df))
    # this below is the noise artificially added
    df.drop(df[df.itemType=='BAD'].index, inplace=True)
    print(len(df))
    # this below are the ratings of the full documents
    # df.drop(df[df.documentID==df.seg_id].index, inplace=True)
    # print(len(df))
    #df.drop(df[df.username=='catita6503'].index, inplace=True)
    #df.drop(df[df.username=='catita6501'].index, inplace=True)
    
    annotators = getAnnotatorsIDs(df,'username')
    systems = getSystemsIDs(df,'targetID')
    
    ## Adding standardized scores
    completeDF = pd.DataFrame()
    for annotator in annotators:
        tmpDF = df[df['username']==annotator]
        tmpDF['z-score'] =  (tmpDF['score'] - tmpDF['score'].mean())/ tmpDF['score'].std()
        completeDF = pd.concat([completeDF,tmpDF])
        
    ## mean and std for the raw scores and z-scores
    # notice that pandas use ddof=1
    means = df.groupby("targetID")['score'].mean().round(decimals=1)
    devs= df.groupby("targetID")['score'].std().round(decimals=1) 
    zmeans = completeDF.groupby("targetID")['z-score'].mean().round(decimals=1)
    zdevs = completeDF.groupby("targetID")['z-score'].std().round(decimals=1) 
    print("z-scores,  raw scores")
    print(zmeans.astype(str) + u"$\pm$" + zdevs.astype(str)+ u"    " +means.astype(str) + u"$\pm$" + devs.astype(str))
    print()
    #print(u"$" +zmeans.astype(str) + u"\pm" + zdevs.astype(str)+ u"$    $" +means.astype(str) + u"\u00B1" + devs.astype(str)+ u"$")


    ## Term translation
    # For Occitan user catoci6603 seem did not understand the task
    # 59 terms in total for Romance languages
    terms = df[df.username!='catoci6603'].groupby(["seg_id","targetID"])['phrase_evaluation'] 
    termsCounts = {}
    for group_key, group_value in terms:
        if(group_value.mode().size==1):
           if (group_key[1] in termsCounts):
               termsCounts[group_key[1]].append(group_value.mode()[0])
           else:
               termsCounts[group_key[1]] = [group_value.mode()[0]] 
    #print(termsCounts['baselineMT5.ca2oc.sgm'])
    print("Translation of terms")
    for system in systems:
        elements = collections.Counter(termsCounts[system])
        print(system, ": ", elements)
    print()


    ## Intraannotator agreement
    df['sentenceIntra'] = df['targetID'] + df['seg_id'] 
    print("Intra Annotator agreement (Fleiss kappa)")
    for annotator in annotators:
        print("Annotator: ",annotator)
        tmpDF = df[df['username']==annotator]
        duplicatesTMP = tmpDF[tmpDF.duplicated(['sentenceIntra'],  keep='first')]
        duplicatesTMP.loc[duplicatesTMP['username']==annotator, 'username'] = annotator+'a'
        duplicatesDF = tmpDF[tmpDF.duplicated(['sentenceIntra'],  keep='last')]
        duplicatesDF.loc[duplicatesDF['username']==annotator, 'username'] = annotator+'b'
        duplicatesDF = pd.concat([duplicatesDF,duplicatesTMP])
        #if (annotator=='catita6503'):
        #    duplicatesDF.to_csv('catita6503.csv', encoding='utf-8')
        #    print(duplicatesDF.sort_values(by=['sentenceIntra']))
        duplicatesDF['sentenceIntra'] = duplicatesDF[['sentenceIntra']].apply(lambda x: (pd.factorize(x)[0] + 1))
        call4Fleiss(duplicatesDF, uniqID='sentenceIntra')
    print()
     
        
    ## Interannotator agreement
    # Let's generate uniq IDs for the sentences
    df['sentence'] = df['targetID'] + df['seg_id']
    df['sentence'] = df[['sentence']].apply(lambda x: (pd.factorize(x)[0] + 1))
    print("Inter Annotator agreement (Fleiss kappa)")
    call4Fleiss(df, uniqID='sentence')
    print()
     
    # 4Krippendorff alpha
    # str seems needed for K-alpha:
    df['sentence'] = df[['sentence']].apply(lambda x: (pd.factorize(x)[0]+1)).astype(str)
    input4Krippendorff = df.pivot_table(index='username', columns='sentence', values='score', aggfunc="first")
    #print(input4Krippendorff)
    print("Inter Annotator agreement (Krippendorff alpha)")
    print(krippendorff_alpha(input4Krippendorff))
    print()



    ## Interannotator agreement for term extraction
    # Let's generate uniq IDs for the sentences
    df.drop(df[df.phrase_evaluation=='no_bold'].index, inplace=True)
    df.drop(df[df.username=='catoci6603'].index, inplace=True)
    df['sentenceTerm'] = df['targetID'] + df['seg_id'] 
    df['sentenceTerm'] = df[['sentenceTerm']].apply(lambda x: (pd.factorize(x)[0] + 1))

    ## Fleiss kappa
    sentences = df['sentenceTerm'].unique()
    M = len(sentences)-1
    print(M)
    N = 3  # likert scale
    input4Fleiss = np.array([[0 for i in range(N)]] * M)
    # Sorting (with a stable algorithm) to later take into account that the same user might have evaluated the same sentence twice
    # For interannotator agreement we only consider the first instance
    df.sort_values(by=['username'], inplace=True, kind='mergesort', ascending=False)
    #df.sort_values(by=['username'], inplace=True, kind='quicksort', ascending=False)
    for i in range(M):
          df['phrase_evaluation_cat']=df.phrase_evaluation.astype('category').cat.codes #convert categories to numbers
          scores = df.loc[df['sentenceTerm']==i+1]['phrase_evaluation_cat']
          raters = np.array(df.loc[df['sentenceTerm']==i+1]['username'])
          #print(df.loc[df['sentence']==i+1])
          #scores = df.loc[(df['sentence']==i+1 and df['username']=='catoci6603')]['score']
          input4Fleiss[i] = [0 for k in range(N)]   # necessito aquesta linea i no entenc per que
          # some sentences were annotated twice, we only keep the first one per annotator
          ann = 'nobody'
          j = 0
          for score in scores:
              if (ann != raters[j]):
                 input4Fleiss[i][score] = input4Fleiss[i][score] + 1
              ann = raters[j]
              j += 1
    fleiss = fleiss_kappa(input4Fleiss)
    print("Intra Annotator agreement for terms (Fleiss kappa)")
    print(fleiss)




if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        sys.stderr.write('Usage: python3 %s inputCSV\n' % sys.argv[0])
        sys.exit(1)

main(sys.argv[1])
