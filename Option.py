# -*- coding: utf-8 -*-

import numpy as np
import scipy.stats as stats

class Instrument(object):

    def __init__(self, isinCode, description):
        self._NPV = 0.0
        self._isExpired = False
        self._isinCode = isinCode
        self._description = description
        self._calculated = False

    def isinCode(self):
        return self._isinCode

    def description(self):
        return self._description

    def NPV(self):
        self.__caluculate()
        return self._NPV

    def isExpired(self):
        self.__caluculate()
        return self._isExpired

    def __update(self):
        self._calculated = False
        self.notifyObservers()

    def recaluculate(self):
        self.performCaluculations()
        self._calculated = True
        self.notifyObservers()

    def __caluculate(self):
        if not(self._calculated):
            self.performCaluculations()
        self._calculated = True
        return 0.0

class Option(Instrument):

    def __init__(self, price, strike, vol, rate, div, T, opType, exercise):
        Instrument.__init__(self, True, None)
        self.price = price
        self.strike = strike
        self.vol = vol
        self.rate = rate
        self.div = div
        self.T = T
        self.opType = opType
        self.exercise = exercise
        self.d1 = (np.log(price / strike) + (rate - div + 0.5 * vol * vol) * T)/ (vol * np.sqrt(T))
        self.d2 = self.d1 - vol * np.sqrt(T)

    def n(self, x):
        return stats.norm.pdf(x, loc=0, scale=1)

    def N(self, x):
        return stats.norm.cdf(x, loc=0, scale=1)

    def calcDelta(self):
        if self.opType == "C":
            self.delta = np.exp(-self.div * self.T) * self.n(self.d1)
        else:
            self.delta = np.exp(-self.div * self.T) * (self.n(self.d1) -1)
        return self.delta

    def calcVega(self):
        self.vega = self.n(self.d1)* np.exp(- self.div * self.T) * self.price * np.sqrt(self.T)
        return self.vega

    def calcGamma(self):
        self.gamma = self.n(self.d1)* np.exp(- self.div * self.T) * self.price * self.vol * np.sqrt(self.T)
        return self.gamma

    def calcRho(self):
        if self.opType == "C":
            self.rho = self.strike * self.T * np.exp(- self.rate * self.T) * self.N(self.d2)
        else:
            self.rho = self.strike * self.T * np.exp(- self.rate * self.T) * self.N(-self.d2)
        return self.rho

    def calcTheta(self):
        if self.opType == "C":
            self.Theta = - self.price * self.N(self.d1) * self.vol * np.exp(- self.div * self.T) / (2 * np.sqrt(self.T)) \
            + self.div * self.price * self.N(self.d1) * np.exp(-self.div * self.T)\
            - self.rate * self.strike * np.exp(-self.rate * self.T) * self.N(self.d2)
        else:
            self.Theta = - self.price * self.N(self.d1) * self.vol * np.exp(- self.div * self.T) / (2 * np.sqrt(self.T)) \
            + self.div * self.price * self.N(-self.d1) * np.exp(-self.div * self.T)\
            - self.rate * self.strike * np.exp(-self.rate * self.T) * self.N(-self.d2)
        return self.Theta

class BlackScholesOption(Option):

    def __init__(self, price, strike, vol, rate, div, T, opType, exercise):
        Option.__init__(self, price, strike, vol, rate, div, T, opType, exercise)

    def normalCalc(self, d):
        # Currently not used
        a1 = 0.319381530
        a2 = - 0.356563782
        a3 = 1.781477937
        a4 = -1.821255978
        a5 = 1.330274429
        gamma = 0.2316419
        k1 = 1.0 / (1.0 + gamma * d)
        k2 = 1.0 / (1.0 - gamma * d)
        normalprime = (1.0 / np.sqrt(2.0 * np.pi)) * np.exp(- 0.5 * d * d)

        if d >= 0:
            return 1 - normalprime * (a1 * k1 + a2 *  np.power(k1, 2.0) + a3 * np.power(k1, 3.0) \
            + a4 * np.power(k1, 4.0) + a5 * np.power(k1, 5.0))
        else:
            return 1 - normalprime * (a1 * k2 + a2 *  np.power(k2, 2.0) + a3 * np.power(k2, 3.0) \
            + a4 * np.power(k2, 4.0) + a5 * np.power(k2, 5.0))

    def calcBSCallPrice(self):
        return self.price * np.exp(self.div * self.T) * self.N(self.d1) \
        - self.strike * np.exp(-self.rate * self.T) * self.N(self.d2)

    def calcBSPutPrice(self):
        return self.strike * np.exp(-self.rate * self.T) * self.N(-self.d2) \
        - self.price * np.exp(self.div * self.T) * self.N(-self.d1)

if __name__ == '__main__':
    op = BlackScholesOption(100.0, 200.0, 0.5, 0.01, 0.04, 1.0, "C", None)
    print op.calcDelta()
    print op.calcVega()
    print op.calcGamma()
    print op.calcRho()
    print op.calcTheta()
    print op.calcBSCallPrice()
    print op.calcBSPutPrice()
