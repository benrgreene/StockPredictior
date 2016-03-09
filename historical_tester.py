#!/usr/bin/env python

import sys
import get_data
from datetime import date as td
import get_prediction
import os
import tickers

def main():
    f = open('YHOO_expanded.csv', 'r')
    lines = f.readline()
    while True:
        lines = f.readline()
        if lines[0] == '1':
            pass
        elif lines[3] == '9':
            break
    day = lines.split(',')[0]
    while not (day == "2016-02-10" ):
        line = f.readline()
        parts = line.split(',')
        current_day = parts[0]
        print(current_day)
        day = parts[0]
        os.system("python3 -W ignore driver.py day_predictions  " + parts[0] + "")
        
    
if __name__ == "__main__":
    main()