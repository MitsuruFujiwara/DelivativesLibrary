# -*- coding: utf-8 -*-

import numpy as np

class MatrixUtil(object):

    def __init__(self, R, dt):
        self.R = R # symmetric correlation matrix
        self.dt = dt # time step size
        self.m = len(R)
        self.D, self.V = np.linalg.eig(R)

    def dw(self):
        for i in range(0, self.m):
            yield np.random.normal(0.0, 1.0) * np.sqrt(self.dt)

    def genCorrelatedDeviates(self):
        dw = list(self.dw())
        for i in range(0, self.m):
            _sum = 0.0
            for j in range(0, self.m):
                _sum += self.V[i][j] * np.sqrt(self.D[j]) * dw[j]
            yield _sum

class Cholesky(MatrixUtil):

    def __init__(self, R, dt):
        MatrixUtil.__init__(self, R, dt)
        self.lb = np.linalg.cholesky(R)

    def genCorrelatedDeviates(self):
        dw = list(self.dw())
        for i in range(0, self.m):
            _sum = 0.0
            for j in range(0, self.m):
                _sum += self.lb[i][j] * dw[j]
            yield _sum

if __name__ == '__main__':
    R = np.array([[ 1.,  0.3,  0.2],[ 0.3,  1.,  0.1],[ 0.2,  0.1,  1.]])
    dt = 0.1
    m = MatrixUtil(R, dt)
    print list(m.genCorrelatedDeviates())

    c = Cholesky(R, dt)
    print list(c.genCorrelatedDeviates())
