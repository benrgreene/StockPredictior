#!/usr/bin/env python

class TickerNode:
    def __init__(self, openp, close, close_adj, high, low, date, v):
        self.int_open = openp * (close_adj / close)
        self.int_close = close_adj
        self.int_high = high
        self.int_low = low
        self.date = date
        self.volume = v