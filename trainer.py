#!/usr/bin/env python

import sys
import pickle
from sklearn import svm
from sklearn.externals import joblib
import numpy as np

def main():
    ticker = sys.argv[2]
    print("Training " + ticker + "...")
    year = int(sys.argv[1])
    byear = str(year - 5)
    eyear = str(year)
    # These are what we'll feed the SVM for training
    sb_data = []
    sb_class = []
    nums = 0
    sells = 0
    # read all the info to feed the SVM
    f = open(ticker + '_expanded.csv', 'r')
    dummy = f.readline()
    while dummy[3] != byear[3]:
        dummy = f.readline()
    for line in f:
        parts = line.split(',')
        # train on all data before 2008
        if(parts[0][3] == eyear[3]):
            break
        temp = []
        temp.append(float(parts[8]))
        temp.append(float(parts[9]) - float(parts[10]))
        sb_data.append(temp)
        sb_class.append(parts[12].replace("\n",""))
        nums += 1
        if parts[12].replace("\n","") == "sell":
            sells += 1
    
    learner = svm.SVC()
    learner.fit(sb_data, sb_class)
    joblib.dump(learner, ticker + "_data_model.pkl")
    print(ticker + " trained")

if __name__ == "__main__":
    main()