# -*- coding: utf-8 -*-

import numpy as np

class MonteCalroLFM:
    # A Monte Calro simulation of LIBOR log-foward dynamics to value European swaption

    def __init__(self, R, V, initrate, strike, T, M, N, m, numeraire):
        self.R = R # correlation matrix of foward rates
        self.V = V # variance/covariance matrix of foward rates
        self.F0 = initrate # initial foward (spot) rates
        self.strike = strike # strike of swaption
        self.T = T # time to maturity of swaption
        self.M = M # number of simulation
        self.N = N # number of time steps per simulation path
        self.m = m # number of foward rates to simulate
        self.numeraire = numeraire # numeraire underlying foward rate dynamics

    def __computeVolatilitiesAndTenors(self):
        self.dt = self.T / self.N
        a = 0.19085664
        b = 0.97462314
        c = 0.08089168
        d = 0.0134498

        v = []
        tau = []
        v.append(0.0)
        tau.append(0.0)

        for i in range(1, self.N):
            v.append((a * (i * self.dt) + d) * np.exp(-b * (i * self.dt)) + c)
            tau.append(0.5)

        self.v = v
        self.tau = tau

    def MonteCalro(self):
        self.__computeVolatilitiesAndTenors()
        F0 = self.F0
        T = self.T
        v = self.v
        tau = self.tau
        M = self.M
        N = self.N
        m = self.m
        R = self.R
        dt = self.dt
        deviate = self.__getRandomNumbers()

        fwd = []
        fwd.append(np.zeros(20))
        payoff = 0.0

        for i in range(1, M): # number of simulation
            drift = 0.0
            prod = 1.0
            prod1 = 1.0
            _sum = 0.0
            _sum1 = 0.0
            mu = 0.0
            mu1 = 0.0

            for l in range(0, N): # number of time steps
                F = []
                F.append(self.F0)

                # generate m foward rates
                for k in range(1, m):

                    # compute drift coefficient
                    if k < numeraire:
                        for j in range(k + 1, numeraire):
                            mu += ((R[k][j] * tau[j] * v[k] * F[j -1]) / (1 + tau[j] * F[j-1])) * dt
                    else:
                        for j in range(numeraire, k):
                            mu1 += ((R[k][j] * tau[j] * v[k] * F[j -1]) / (1 + tau[j] * F[j-1])) * dt

                    # compute drift
                    drift = -mu + mu1

                    # simulate log foward rates
                    logF = np.log(F[k-1]) + v[k] * drift - 0.5 * v[k] * v[k] * dt + v[k] * deviate[i][l][k] * np.sqrt(dt)
                    F.append(np.exp(logF))
                    fwd.append(F)

                # compute current swap rates
                for p in range(0, m):
                    prod = prod * (1.0 / (1.0 + tau[p] * fwd[l+1][p]))
                    for n in range(1, m):
                        for q in range(1, n):
                            prod1 = prod1 * (1.0 / (1 + tau[q] * fwd[l+1][q]))

                        _sum += tau[n] * prod1

                swapRate = (1.0 - prod) / _sum
                bondPrice = 1.0 / prod1

                value = max(swapRate - strike, 0.0) * _sum
                payoff += value
                _sum1 += value * value

        swaptionPrice = np.exp(-F0 * T) * payoff / M

        self.SD = np.sqrt((_sum1 - _sum1 * _sum1 / M)) * np.exp(-2.0 * F0 * T / (M - 1.0 ))
        self.SE = self.SD / np.sqrt(M)

        return swaptionPrice

    def __getRandomNumbers(self):
        r = []
        for k in range(0, self.M):
            r_k = []
            for s in range(0, self.N):
                _r = list(np.random.randn(self.m))
                r_k.append(_r)
            r.append(r_k)

        return r

if __name__ == '__main__':
    V = [\
    [0.164, 0.158, 0.146, 0.138, 0.133, 0.129, 0.126, 0.123, 0.120, 0.117],\
    [0.177, 0.156, 0.141, 0.131, 0.127, 0.124, 0.122, 0.119, 0.117, 0.114],\
    [0.176, 0.155, 0.139, 0.127, 0.123, 0.121, 0.119, 0.117, 0.115, 0.113],\
    [0.169, 0.146, 0.129, 0.119, 0.116, 0.114, 0.113, 0.111, 0.110, 0.108],\
    [0.158, 0.139, 0.124, 0.115, 0.111, 0.109, 0.108, 0.107, 0.105, 0.104],\
    [0.145, 0.129, 0.116, 0.108, 0.104, 0.103, 0.101, 0.099, 0.098, 0.096],\
    [0.135, 0.115, 0.104, 0.098, 0.094, 0.093, 0.091, 0.088, 0.086, 0.084],\
    ]

    R = [\
    [1.0],\
    [0.924, 1.0],\
    [0.707, 0.924, 1.0],\
    [0.557, 0.833, 0.981, 1.0],\
    [0.454, 0.760, 0.951, 0.997, 1.0],\
    [0.760, 0.951, 0.997, 0.963, 0.924, 1.0],\
    [0.843, 0.985, 0.976, 0.916, 0.862, 0.990, 1.0],\
    [0.837, 0.983, 0.979, 0.921, 0.867, 0.992, 1.0, 1.0],\
    [0.837, 0.983, 0.979, 0.920, 0.867, 0.992, 1.0, 1.0, 1.0],\
    [0.920, 1.00, 0.928, 0.838, 0.767, 0.954, 0.986, 0.985, 0.985, 1.00],\
    ]

    initrate = 0.05
    strike = 0.065
    T = 1
    M = 10000
    N = 10
    m = 10
    numeraire = 1

    mc = MonteCalroLFM(R, V, initrate, strike, T, M, N, m, numeraire)

    print "Price = " + str(mc.MonteCalro())
    print "Standard Deviation = " + str(mc.SD)
    print "Standard Error = " + str(mc.SE)
