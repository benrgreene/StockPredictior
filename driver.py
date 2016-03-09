#!/usr/bin/env python

import sys
import get_data
from datetime import date as td
import get_prediction
import os
import tickers
import warnings
warnings.filterwarnings('ignore')

dollars = 0.0

def day_predictions(date):
    # check if we were passed a day or if passed None
    if date == None:
        date = str(td.today())
        
    # set all the data through script executions
    print("Getting data...")
    os.system("python3 get_data.py")
    
    print("Expanding data...")
    os.system("python3 calculate_indicators.py " + date)
    
    info_today = {}
    for ticker in tickers.tickers:
        info_today[ticker] = get_data.get_single_day(date, ticker)

    print("Getting prediction...")
    # get money stuffs
    rec_stocks = {}
    closing = {}
    stocks = {}
    
    my_pred = get_prediction.Predictor()
    for ticker in tickers.tickers:
        response = my_pred.get_day_pred(info_today[ticker], ticker)
        rec_stocks[ticker] = response
    
    # Open up the file with current money and tickers info
    f = open("Money.txt", "r")
    
    for ticker in tickers.tickers:
        closing[ticker] = float(info_today[ticker].split(',')[4])
    dollars = float(f.readline().replace("\n", ""))
    
    for a in f:
        parts = a.split(" ")
        stocks[parts[0]] = int(parts[1].replace("\n",""))
    
    # do selling
    for a in tickers.tickers:
        if rec_stocks[a] == "sell":
            dollars += closing * float(stocks[a])
            stocks[a] = 0
            
    
    # do buying
    for a in tickers.tickers:
        if rec_stocks[a] == "buy":
            cost = closing[a]
            pos = int(dollars / float(cost))
            dollars = dollars - (pos * float(cost))
            stocks[a] += pos
    
    to_print = date + "\n" + "$" + str(dollars) + "   "
    for a in tickers.tickers:
        to_print = to_print + " " +  a + " $" + str(stocks[a] * closing[a]) + "   "
    print(to_print)
    
    f = open("Money.txt", "w")
    f.write(str(dollars))
    for a in tickers.tickers:
        f.write("\n" + a + " " + str(stocks[a]))

if len(sys.argv) == 1:
    day_predictions(None)
elif len(sys.argv) > 2:
    # Get the prediction type from the args array
    locals()[sys.argv[1]](sys.argv[2])
else:
    day_predictions(sys.argv[1])