#!/usr/bin/env python

import urllib.request
import time 
from datetime import date as td
import tickers

base_url = "http://ichart.finance.yahoo.com/table.csv?s="

# ---------------------- GETTING EXPANDED INFO FOR ONE DAY----------------------
def get_single_day(day, ticker):
    if day == None:
        return None
    f = open(ticker + '_expanded.csv', 'r')
    line = f.readline()
    while True:
        line = f.readline()
        if line is None:
            return None
        if day in line:
            return line.replace("\n", "")


# -------------------------- GETTING INFO FOR SCRIPTS --------------------------
def get_single_point(ticker):
	# this is a lot of data. need to add date stuff yo.
	# As it turns out, yahoo finance has month start at 0. but nothing else, and not in the CSV file. go figure
	p = str(td.today()).split("-")
	url = "http://ichart.finance.yahoo.com/table.csv?s=" + ticker + "&a=" + str(int(p[1])-1) + "&b=" + p[2] + "&c=" + p[0]+ "&g=d&ignore=.csv"
	print(url)
	data = urllib.request.urlopen(url).read()
	return data.split("\n")[1]


# ------------------------------ GETTING CSV FILES -----------------------------
def make_url(ticker_symbol):
 	return base_url + ticker_symbol

def make_filename(ticker_symbol):
   	return ticker_symbol + ".csv"

def pull_historical_data():
	# loop through file of tickers, and add to the tickers array
	for ticker_symbol in tickers.tickers:
		urllib.request.urlretrieve(make_url(ticker_symbol), make_filename(ticker_symbol))
		# yahoo finance no longer seems to support getting the current day?
		#current_day = get_single_day(None, ticker_symbol)
		#f = open(ticker_symbol+ ".csv", 'a')
		#f.write(current_day)

def main():
	pull_historical_data()

if __name__ == "__main__":
	main()