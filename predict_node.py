#!/usr/bin/env python

class PredNode:
    def __init__(self, day, MACD, a_up, a_down, close):
        self.day = day
        self.macd = MACD
        self.a_up = a_up
        self.a_down = a_down
        self.close = close