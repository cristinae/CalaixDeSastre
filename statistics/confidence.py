#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Confidence intervals and paired statistical tests via bootstraping
    Valid for MT metrics calculated at sentence level
    Date: 23.07.2021
    Author: cristinae
    TODO: - input files
          - implement PAR
"""

import sys, warnings
import argparse
import random
import numpy as np

def get_parser():
    """
    Creates a new argument parser.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--iFile',
                    required=False,
                    type=str,
                    default="", 
                    metavar="<inputFile>",
                    help="Input file" )
    parser.add_argument('-b', '--bootstraps',
                    required=False,
                    type=int,
                    default=1000, 
                    help="Number of bootstraped versions (default 1000)" )
    parser.add_argument('-c', '--confLevel',
                    required=False,
                    type=float,
                    default=95, 
                    help="Confidence level (from 0 to 100, default 95)" )
    parser.add_argument('-p', '--precision',
                    required=False,
                    type=int,
                    default=4, 
                    help="Number of significant digits (default 4)" )
    return parser


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



def main(args=None):

    '''Get command line arguments'''
    parser = get_parser()
    args = parser.parse_args(args)
 
    #''' Read the input file'''
    #nameINfile=args.iFile
    #with open(nameINfile, 'r') as file:
    #    fullCorpus=file.read().split('\n')

    sysScores = [2.4, 3.2, 8.2, 4.3, 6.5]
    baseScores = [3.4, 3.3, 8.2, 4.3, 6.5]

    mean, interval = ci_bs(sysScores, args.bootstraps, args.confLevel)
    print(np.around(mean, args.precision), np.around(interval, args.precision))
    pValue = pbs(baseScores, sysScores, args.bootstraps)
    print(pValue)


if __name__ == "__main__":
   main()

