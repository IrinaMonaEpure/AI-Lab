# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 11:08:14 2020

@author: irina
"""
import numpy as np

samples = ["GAGGTAAAC","TCCGTAAGT","CAGGTTGGA","ACAGTCAGT","TAGGTCATT","TAGGTACGT","ATGGTAACT","CAGGTATAC","TGTGTGAGT","AAGGTAAGT"]

count = [[0 for x in range(9)] for y in range(4)]

#print(count)
        
for i in range(len(samples)):
    for j in range(len(samples[i])):
        if samples[i][j]=='A':
            count[0][j] += 1
        if samples[i][j]=='C':
            count[1][j] += 1
        if samples[i][j]=='G':
            count[2][j] += 1
        if samples[i][j]=='T':
            count[3][j] += 1

print("Count matrix: ",count)
no = len(samples)
weight = [[0 for x in range(9)] for y in range(4)]
for i in range(len(count)):
    for j in range(len(count[i])):
        weight[i][j] = count[i][j]/no
print("Weight matrix: ",weight)

avg_likelihood = 0.25
log_likelihood = [[0 for x in range(9)] for y in range(4)]
for i in range(len(weight)):
    for j in range(len(weight[i])):
        if weight[i][j]==0:
            log_likelihood[i][j] = 0
        else:
            log_likelihood[i][j] = np.log(weight[i][j]/avg_likelihood)
print("Log-likelihood matrix: ",log_likelihood)

S="CAGGTTGGAAACGTAATCAGCGATTACGCATGACGTAA"
score = 0
for i in range(len(S)-9):
    for j in range(9):
        if S[i+j]=='A':
            #print(log_likelihood[0][j])
            score += log_likelihood[0][j]
        if S[i+j]=='C':
            #print(log_likelihood[1][j])
            score += log_likelihood[1][j]
        if S[i+j]=='G':
            #print(log_likelihood[2][j])
            score += log_likelihood[2][j]
        if S[i+j]=='T':
            #print(log_likelihood[3][j])
            score += log_likelihood[3][j]
    print("Score of sequence starting from index ", i, " is: ", score)
    score = 0