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
        self.d1 = (np.log(price / strike) + (rate - div + vol * vol / 2) * T)/ (vol * np.sqrt(T))
        self.d2 = self.d1 - vol * np.sqrt(T)

    def __n(self, x):
        return stats.norm.pdf(x, loc=0, scale=1)

    def __N(self, x):
        return stats.norm.cdf(x, loc=0, scale=1)

    def calcDelta(self):
        if self.opType == "C":
            self.delta = np.exp(-self.div * self.T) * self.__n(self.d1)
        else:
            self.delta = np.exp(-self.div * self.T) * (self.__n(self.d1) -1)
        return self.delta

    def calcVega(self):
        self.vega = self.__n(self.d1)* np.exp(- self.div * self.T) * self.price * np.sqrt(self.T)
        return self.vega

    def calcGamma(self):
        self.gamma = self.__n(self.d1)* np.exp(- self.div * self.T) * self.price * self.vol * np.sqrt(self.T)
        return self.gamma

    def calcRho(self):
        if self.opType == "C":
            self.rho = self.strike * self.T * np.exp(- self.rate * self.T) * self.__N(self.d2)
        else:
            self.rho = self.strike * self.T * np.exp(- self.rate * self.T) * self.__N(-self.d2)
        return self.rho

    def calcTheta(self):
        if self.opType == "C":
            self.Theta = - self.price * self.__N(self.d1) * self.vol * np.exp(- self.div * self.T) / (2 * np.sqrt(self.T)) \
            + self.div * self.price * self.__N(self.d1) * np.exp(-self.div * self.T)\
            - self.rate * self.strike * np.exp(-self.rate * self.T) * self.__N(self.d2)
        else:
            self.Theta = - self.price * self.__N(self.d1) * self.vol * np.exp(- self.div * self.T) / (2 * np.sqrt(self.T)) \
            + self.div * self.price * self.__N(-self.d1) * np.exp(-self.div * self.T)\
            - self.rate * self.strike * np.exp(-self.rate * self.T) * self.__N(-self.d2)
        return self.Theta

if __name__ == '__main__':
    op = Option(100, 100, 0.5, 0.01, 0.04, 1.0, "C", None)
    print op.calcDelta()
    print op.calcVega()
    print op.calcGamma()
    print op.calcRho()
    print op.calcTheta()
