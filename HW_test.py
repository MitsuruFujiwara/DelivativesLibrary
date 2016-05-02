# -*- coding: utf-8 -*-

import numpy as np
import scipy.stats as stats
import scipy.optimize as optimize
import math

import Black

class PriceCapHW:

    def __init__(self, mats, vols, rates, a, FV, vol, Rcap, tenor, L):
        self.mats = mats
        self.vols = vols
        self.rates = rates
        self.a = a
        self.FV = FV
        self.vol = vol
        self.Rcap = Rcap
        self.tenor = tenor
        self.L = L

    def __P(self):
        mats = self.mats
        rates = self.rates

        P = []
        for i, t in enumerate(mats):
            DF_t = math.exp(- t * rates[i])
            P.append(DF_t)

        self.P = P
        return self.P

    def __N(self, x):
        return stats.norm.cdf(x)

    def priceHWCap(self, params):
        # pricing Cap value with Hull-White model
        a = params[0]
        vol = params[1]
        vols = self.vols
        P = self.__P()
        mats = self.mats
        Rcap = self.Rcap
        L = self.L
        tenor = self.tenor

        BK = Black.Black(vols, P, mats, Rcap, L, tenor)
        self.market = BK.priceBlackCap()

        model = []
        for i in range(0, len(vols) - 1):
            volP = np.sqrt(((vol * vol) / (2 * a * a * a))  * (1 - math.exp(-2 * mats[i] * a)) \
            * (1 - math.exp(-a * (mats[i+1] - mats[i]))) ** 2)

            d1 = math.log((FV * P[i + 1])/(L * P[i]))/ volP +  0.5 * volP
            d2 = d1 - volP
            tmp = L * P[i] * self.__N(-d2) - FV * P[i+1] * self.__N(-d1)

            model.append(tmp)

        return model

    def calibrateToMarketPrice(self, params):
        # get squared errors between market quote and model
        model = self.priceHWCap(params)
        market = self.market

        se = 0.0
        for i in range(0, len(vols) - 1):
            se += ((model[i] - market[i]) / market[i]) ** 2

        return se

    def getParameters(self):
        # two dimensional minimization
        # to use "Newton-CG", must difine volatility derivative and alpha derivative
        params = [1.0, 1.0]
        res  = optimize.minimize(self.calibrateToMarketPrice, params)

        return res

if __name__ == '__main__':
    mats = [1.0, 2.0 ,3.0, 4.0] # caplet maturities
    vols = [0.5, 0.5, 0.5, 0.5] # market quote caplet volatilities
    rates = [0.01, 0.02, 0.03, 0.04] # short rates
    Rcap = 0.05 # cap rate
    a = 0.001 # mean reversion parameter
    FV = 100 # face value of loan
    vol = 0.5 # length between payment time
    tenor = 0.5 # length of time between payment date
    L = 100 # principal amount of loan

    HW = PriceCapHW(mats, vols, rates, a, FV, vol, Rcap, tenor, L)
    p = HW.getParameters()
    print p
