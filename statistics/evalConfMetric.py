#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Confidence intervals and paired statistical tests via bootstraping
    Valid for MT metrics calculated at sentence level within Huggingface transformers
    Date: 23.07.2021
    Author: cristinae
    TODO: - command line parameters 
          - implement PAR
"""

import sys
import random
import numpy as np

import torch
import datasets
from datasets import load_metric

device = "cuda:0" if torch.cuda.is_available() else "cpu"


def avgList(valuesList):
    return sum(valuesList)/len(valuesList)

def ci_bs(distribution, n, confLevel):
    ''' Calculates confidence intervals for distribution at confLevel after the 
        generation of n boostrapped samples 
    '''

    bsScores = np.zeros(n)
    size = len(distribution)
    random.seed(16) 
    for i in range(0, n):
        # generate random numbers with repetitions, to extract the indexes of the sysScores array
        bootstrapedSys = np.array([distribution[random.randint(0,size-1)] for x in range(size)])
        # scores for all the bootstraped versions
        # this works because we assume the MT metric is calculated at sentence level
        bsScores[i] = np.mean(bootstrapedSys,0)

    # we assume distribution of the sample mean is normally distributed
    # number of bootstraps > 100
    mean = np.mean(bsScores,0)
    stdDev = np.std(bsScores,0,ddof=1)
    # Because it is a bootstraped distribution
    alpha = (100-confLevel)/2
    confidenceInterval = np.percentile(bsScores,[alpha,100-alpha])

    return (mean, mean-confidenceInterval[0])


def compute_p_value(stats, real_difference):
    """Computes the p-value given the sample statistics and the real statistic.
    :param stats: A numpy array with the sample statistics.
    :real_difference: The real statistic.
    :return: The p-value.
    """
    # Taken from: sacrebleu
    # https://github.com/mjpost/sacrebleu/blob/master/sacrebleu/significance.py
    # Taken from: significance/StratifiedApproximateRandomizationTest.java
    # https://github.com/jhclark/multeval.git

    # "the != is important. if we want to score the same system against itself
    # having a zero difference should not be attributed to chance."

    c = np.sum(stats > real_difference)
    print(c)

    # "+1 applies here, though it only matters for small numbers of shufflings,
    # which we typically never do. it's necessary to ensure the probability of
    # falsely rejecting the null hypothesis is no greater than the rejection
    # level of the test (see william and morgan on significance tests)
    p = float(c + 1) / (len(stats) + 1)

    return p


def pbs(baseline, system, n):
    '''   Paired bootstrap resampling test for segment level metrics. 
    '''

    bsScoresBase = np.zeros(n)
    bsScoresSys = np.zeros(n)
    bsDiffScores = np.zeros(n)
    size = len(baseline)
    random.seed(16) 
    for i in range(0, n):
        # generate random numbers with repetitions, to extract the indexes of the sysScores array
        indexes = [random.randint(0,size-1) for x in range(size)]
        bootstrapedBase = np.array([baseline[x] for x in indexes])
        bootstrapedSys = np.array([system[x] for x in indexes])
        # scores for all the bootstraped versions
        # this works because we assume the MT metric is calculated at sentence level
        bsScoresBase[i] = np.mean(bootstrapedBase,0)
        bsScoresSys[i] = np.mean(bootstrapedSys,0)
        bsDiffScores[i] = np.abs(bsScoresSys[i]-bsScoresBase[i])

    # naming to match sacrebleu implementation
    stats = bsDiffScores - np.mean(bsDiffScores,0)
    # original test statistic: absolute difference between baseline and the system
    realDiff = np.abs(np.mean(np.array(baseline))-np.mean(np.array(system)))
    p = compute_p_value(stats, realDiff)

    return p


def par(baseline, system, n):
    '''   Paired two-sided approximate randomization (AR) test for segment level metrics. 
    '''
    p = "not implemented yet"
    return p



def main(baselineF, candidates1F, candidates2F, referencesF, lan):

    with open(baselineF) as f:
        base = [line.strip() for line in f]

    with open(candidates1F) as f:
        cands1 = [line.strip() for line in f]

    with open(candidates2F) as f:
        cands2 = [line.strip() for line in f]

    with open(referencesF) as f:
        refs = [line.strip() for line in f]

    bertscore = datasets.load_metric("bertscore")
    sys1Scores = bertscore.compute(predictions=cands1, references=refs, lang="lan")
    print("System1 computed")
    sys2Scores = bertscore.compute(predictions=cands2, references=refs, lang="lan")
    print("System2 computed")
    baseScores = bertscore.compute(predictions=base, references=refs, lang="lan")
    print("Baseline computed")

    bootstraps = 1000
    confLevel = 95
    precision = 4
    #mean, interval = ci_bs(sysScores["f1"], args.bootstraps, args.confLevel)
    #print(np.around(mean, args.precision), np.around(interval, args.precision))
    #pValue = pbs(baseScores["f1"], sysScores["f1"], args.bootstraps)

    mean, interval = ci_bs(baseScores["f1"], bootstraps, confLevel)
    print("Baseline: ", np.around(mean, precision), np.around(interval, precision))
    mean, interval = ci_bs(sys1Scores["f1"], bootstraps, confLevel)
    print("System1: ", np.around(mean, precision), np.around(interval, precision))
    mean, interval = ci_bs(sys2Scores["f1"], bootstraps, confLevel)
    print("System2: ", np.around(mean, precision), np.around(interval, precision))

    pValue1 = pbs(baseScores["f1"], sys1Scores["f1"], bootstraps)
    pValue2 = pbs(baseScores["f1"], sys2Scores["f1"], bootstraps)
    print("p-values: ", pValue1, pValue2)

    #print(f'{results["hashcode"]}: P={avgList(results["precision"]):.6f}  R={avgList(results["recall"]):.6f}')
    #print(f'{results["hashcode"]}: F1={avgList(results["f1"]):.4f}')

    #comet = datasets.load_metric("comet")
    #results = comet.compute(predictions=predictions, references=references, lang="ca")
    #print(f'{COMET: avgList(results["scores"]):.6f}')


#    print([round(v, 2) for v in results["f1"]])
#    print(f'{results["hashcode"]}: P={results["precision"].mean().item():.6f} R={results["recall"].mean().item():.6f} F={results["f1"].mean().item():.6f}')

if __name__ == "__main__":
    
    if len(sys.argv) != 6:
        sys.stderr.write('Usage: python3 %s baselineFile hypotheses1File hypotheses2File referencesFile language\n' % sys.argv[0])
        sys.exit(1)

main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
#main()
