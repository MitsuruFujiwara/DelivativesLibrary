# -*- coding: utf-8 -*-

import numpy as np

class StatUtility:

    def __init__(self, a, b, n, t, T):
        self.a = a # lower limit of integration
        self.b = b # upper limit of integration
        self.n = n # number of segments for approximation
        self.t = t # current time
        self.T = T # maturity

    def EvaluateSimpson(self):
        # evaluates integral using Simpson's rule

        self.h = (self.b - self.a) / self.n
        x = []
        g = []
        x.append(self.a)
        g.append(self.__F(x[0], self.t, self.T))

        for i in range(1, self.n):
            x.append(self.h + x[i - 1])
            g.append(self.__F(x[i], self.t, self.T))

        self.g = g
        value = self.__calcIntegral()

        return value

    def __calcIntegral(self):
        # caluculates integral approximation using Simpson's rule
        oddValues = 0.0
        evenValues = 0.0

        for i in range(1, self.n, 2):
            oddValues += self.g[i]
        for j in range(2, self.n - 1, 2):
            evenValues += self.g[j]

        value = (self.h / 3.0) * (self.g[0] + 4.0 * oddValues + 2.0 * evenValues + self.g[self.n - 1])

        return value

    def __F(self, t, s, T):
        # volatility function to evaluate for LFM ssimulation

        a = 0.19085664
        b = 0.97462314
        c = 0.08089168
        d = 0.0134498

        f = ((a * (T - t) + d) * np.exp(-b *(T - t) + c)) * \
        ((a * (T - s) + d)* np.exp(-b * (T - s)+ c))

        return f

if __name__ == '__main__':
    u = StatUtility(50.0, 1.0, 100, 0, 1.0)
    print u.EvaluateSimpson()
