# -*- coding: utf-8 -*-

import numpy as np
import scipy.stats as stats
import scipy.optimize as optimize
import math

import Black

class HW:

    def __init__(self, mats, vols, rates, a, FV, vol, Rcap, tenor, L):
        self.mats = mats # caplet maturities
        self.vols = vols # market quote caplet volatilities
        self.rates = rates # short rates
        self.a = a # mean reversion parameter
        self.FV = FV # face value of loan
        self.vol = vol # length between payment time
        self.Rcap = Rcap # cap rate
        self.tenor = tenor # length of time between payment date
        self.L = L # principal amount of loan

    def P(self):
        for i, t in enumerate(self.mats):
            yield math.exp(- t * self.rates[i])

    def __N(self, x):
        return stats.norm.cdf(x)

    def priceHWCap(self, params):
        # pricing Cap value with Hull-White model
        a = params[0]
        vol = params[1]
        vols = self.vols
        P = list(self.P())
        mats = self.mats
        Rcap = self.Rcap
        L = self.L
        tenor = self.tenor

        BK = Black.Black(vols, P, mats, Rcap, L, tenor)
        self.market = list(BK.priceBlackCap())

        for i in range(0, len(vols) - 1):
            volP = np.sqrt(((vol * vol) / (2 * a * a * a))  * (1 - math.exp(-2 * mats[i] * a)) \
            * (1 - math.exp(-a * (mats[i+1] - mats[i]))) ** 2)

            d1 = math.log((FV * P[i + 1])/(L * P[i]))/ volP +  0.5 * volP
            d2 = d1 - volP
            yield L * P[i] * self.__N(-d2) - FV * P[i+1] * self.__N(-d1)

    def calibrateToMarketPrice(self, params):
        # get squared errors between market quote and model
        model = list(self.priceHWCap(params))
        market = self.market
        se = 0.0

        for i in range(0, len(vols) - 1):
            se += ((model[i] - market[i]) / market[i]) ** 2

        return se

    def getParameters(self):
        # two dimensional minimization
        # to use "Newton-CG", must difine volatility derivative and alpha derivative
        params = [1.0, 1.0]
        return optimize.minimize(self.calibrateToMarketPrice, params)

if __name__ == '__main__':
    mats = [1.0, 2.0 ,3.0, 4.0]
    vols = [0.5, 0.5, 0.5, 0.5]
    rates = [0.01, 0.02, 0.03, 0.04]
    Rcap = 0.05
    a = 0.001
    FV = 100
    vol = 0.5
    tenor = 0.5
    L = 100

    hw = HW(mats, vols, rates, a, FV, vol, Rcap, tenor, L)
    p = hw.getParameters()
    print p
