# -*- coding: utf-8 -*-

import numpy as np
import scipy.stats as stats
import math

class Black:

    def __init__(self, capVol, PDB, maturity, Rcap, L , tenor):
        self.capVol = capVol
        self.PDB = PDB
        self.maturity = maturity
        self.Rcap = Rcap
        self.L = L
        self.tenor = tenor
        self.faceValue = L * (1 + Rcap * tenor)

    def __N(self, x):
        return stats.norm.cdf(x)

    def __getFowardRates(self):
        capV = self.capVol
        P = self.PDB
        t = self.maturity
        tenor = self.tenor
        R = []
        F =[]

        for i in range(0, len(capV) - 1):
            r = -(1/t[i]) * (np.log(P[i]))
            f = -(1/tenor) * np.log(P[i+1] / P[i])
            R.append(r)
            F.append(f)
        self.R = R
        self.F = F

    def priceBlackCap(self):

        self.__getFowardRates()

        F = self.F
        R = self.R
        P = self.PDB
        faceValue = self.faceValue
        Rcap = self.Rcap
        capV = self.capVol
        t = self.maturity
        tenor = self.tenor

        caplet = []
        for i in range(0, len(capV) - 1):
            yield self.__BlackFormula(F[i], P[i], faceValue, Rcap, capV[i], t[i], tenor)

    def __BlackFormula(self, F, P, L, Rcap, vol, tau, dtau):
        # compute cap price with Black's 1976 model
        d1 = np.log(F / Rcap) + (0.5 * vol * vol * tau )/ (vol * np.sqrt(tau))
        d2 = d1 - vol * np.sqrt(tau)

        return P * dtau * L * self.__N(d1) - Rcap * self.__N(d2)
