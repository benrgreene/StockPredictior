#!/usr/bin/env python

import urllib
import sys
from ticker_node import TickerNode
import tickers
import math

# Note: in the calculations, we use adjusted close. While I believe this is correct, I'm not 100% sure.
# I also calculate the adjusted open and write that to the expanded file. 

# Should also calculate the Aroon values (up, down) and the aroon oscilations.

def main():
    for ticker in tickers.tickers:
        # Start by reading through all ticker data points. 
        # We'll create a node for each data point and add it to the beggining of a list
        # to keep everything in chronological order
        nodes = []
        f = open(ticker + '.csv', 'r')
        f.readline()
        for line in f:
            parts = line.split(',')
            int_open = float(parts[1])
            int_close_adj = float(parts[6])
            int_close = float(parts[4])
            int_high = float(parts[2])
            int_low = float(parts[3])
            volume = int(parts[5])
            nodes.insert(0, TickerNode(int_open, int_close, int_close_adj, int_high, int_low, parts[0].replace('\n', ''), volume))
        
        # Now we want the averages of the first 26 and 12 days. we'll use a sum and a list to keep track of 
        # the closing prices for these averages. Add new values to the end of the arrays, and pop of the
        # values at the beggining of the arrays.
        
        
        # Set up the averages (and lists) for the first 26 days.
        last_26 = []
        sum_26 = 0
        for i in range(0, 26):
            last_26.append(nodes[i].int_close)
            sum_26 += nodes[i].int_close
            
        last_12 = []
        sum_12 = 0
        for i in range(14, 26):
            last_12.append(nodes[i].int_close)
            sum_12 += nodes[i].int_close
            
        # Now we'll start at day 26, and iterate through every day. We'll add its (adjusted) closing price, 
        # and remove the oldest closing price from the sum. Take the averages, use them to calculate the MACD
        # Write the new info the the tickers expanded info file.
        r12 = 2.0/13
        r26 = 2.0/27
        max_range = len(nodes)
        fw = open(ticker + '_expanded.csv', 'w')
        fw.write("date,open,high,low,close,volume,SMA 26, SMA12, MACD, Aroon High, Aroon Low, Kaufman, BuySell\n")
        for i in range(25, max_range):
            # Modify SMA for last 16 days
            temp = last_26.pop(0)
            sum_26 -= temp
            sum_26 += nodes[i].int_close
            last_26.append(nodes[i].int_close)
            # Modify SMA for last 12 days
            temp = last_12.pop(0)
            sum_12 -= temp
            sum_12 += nodes[i].int_close
            last_12.append(nodes[i].int_close)
            
            # get SMA
            SMA_26 = sum_26 / 26
            SMA_12 = sum_12 / 12
            nodes[i].sma_12 = SMA_12
            nodes[i].sma_26 = SMA_26
            
            # Calculate the MACS and EMA_12
            if i == 25:
                nodes[25].EMA_12 = nodes[25].sma_12
                nodes[25].EMA_26 = nodes[25].sma_26
            else:
                EMA_12 = (nodes[i].int_close - nodes[i-1].EMA_12) * r12 + nodes[i-1].EMA_12
                EMA_26 = (nodes[i].int_close - nodes[i-1].EMA_26) * r26 + nodes[i-1].EMA_26
                nodes[i].EMA_12 = EMA_12
                nodes[i].EMA_26 = EMA_26
                nodes[i].MACD = EMA_12 - EMA_26 
            
            # This is all the Kaufman stuff
            change = math.fabs(last_12[11] - last_12[0])
            volatility = 0
            for a in range(1, 11):
                volatility += math.fabs(last_12[11] - last_12[11-a])
            ER = float(change) / volatility
            SC = ER * (float(2)/3 - float(2)/31) + float(2)/3
            SC *= SC
            if i == 25:
                # we use the SMA12
                nodes[i].kama = SMA_12
            else:
                nodes[i].kama = nodes[i-1].kama + SC * (nodes[i].int_close - nodes[i-1].kama)
            
            # get aroon
            a_h = ((1.0 + last_26.index(max(last_26))) / 25) * 100
            a_l = ((1.0 + last_26.index(min(last_26))) / 25) * 100
            nodes[i].a_h = int(a_h)
            nodes[i].a_l = int(a_l)
                
        for i in range(26, max_range):
            str_buy_sell = ""
            if i == max_range - 1:                
                str_buy_sell = "?"
            else:
                buy_sell = nodes[i].int_close - nodes[i+1].int_close
                if buy_sell < 0:
                    str_buy_sell = "buy"
                else:
                    str_buy_sell = "sell"
            fw.write(nodes[i].date + "," + str(nodes[i].int_open)+","+str(nodes[i].int_high)+","+str(nodes[i].int_low)+","+str(nodes[i].int_close)+","+str(nodes[i].volume)+","+str(nodes[i].sma_26)+","+str(nodes[i].sma_12)+","+str(nodes[i].MACD)+","+str(nodes[i].a_h)+","+str(nodes[i].a_l)+"," + str(nodes[i].kama) + "," + str_buy_sell + "\n")
    
if __name__ == "__main__":
    main()