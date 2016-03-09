#!/usr/bin/env python

import sys
from predict_node import PredNode
import tickers
import os
import pickle
from sklearn import svm
from sklearn.externals import joblib
import numpy as np

class Predictor:
    def set_up_day(self, ticker):
        f = open(ticker + '_expanded.csv', 'r')
        f.readline()
        
        # Set up
        nodes = []
        for line in f:
            parts = line.split(",")
            nodes.insert(0, PredNode(parts[0].strip(), parts[8], parts[9], parts[10], parts[4]))
        
        self.ticks[ticker] = nodes
        
    def __init__(self):
        self.ticks = {}
        self.prices = {}
        for ticker in tickers.tickers:
            self.set_up_day(ticker)
        
        
    def get_day_pred(self, info, ticker):
        # retrain the data for the specific ticker
        year = '20' + info[2] + info[3]
        os.system("python3 trainer.py " + year + " " + ticker)
            
        clf = joblib.load(ticker + '_data_model.pkl')
        #print(info)
        parts = info.split(",")
        temp = []
        temp.append(float(parts[8]))
        temp.append(float(parts[9]) - float(parts[10]))
        result = clf.predict(temp)
        return result