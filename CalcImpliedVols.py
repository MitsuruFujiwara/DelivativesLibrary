# -*- coding: utf-8 -*-

import numpy as np

class CalcImpliedVols:

    def __init__(self, price, opPrices, strikes, rate, dividend, T, optType):
        self.price = price
        self.opPrices = opPrices
        self.strikes = strikes
        self.rate = rate
        self.dividend = dividend
        self.T = T
        self.optType = optType

    def computeImpliedVols(self):
        for i, t in enumerate(self.opPrices):
            marketprice = t
            vol1 = 0.55
            error = 0.0
            while abs(error) > epsilon:
                BSPrice =



if __name__ == '__main__':
    price = 100
    opPrices = [10, 9, 8, 7]
    strikes = [100, 100, 100, 100]
    rate = 0.01
    dividend = 0.04
    T = 1.0
    optType = "C"

    IV = CalcImpliedVols(price, opPrices, strikes, rate, dividend, T, optType)
    IV.computeImpliedVols()
