# -*- coding: utf-8 -*-

import numpy as np

class DiffusionProcess(object):
    """ Base Class for Generating Diffusion Process"""

    def __init__(self, x0):
        self.x0 = x0

    def drift(self, t, x):
        return 0.0

    def diffusion(self, t, x):
        return 0.0

    def expectation(self, t0, x0, dt):
        return x0 + self.drift(t0, x0) * dt

    def variance(self, t0, x0, dt):
        sigma = self.diffusion(t0, x0)
        return sigma * sigma * dt

class BlackScholesPricess(DiffusionProcess):

    def __init__(self, rate, volatility, s0 = 0.0):
        DiffusionProcess.__init__(self, s0)
        self._r = rate
        self._sigma = volatility

    def drift(self, t, x):
        return self._r - 0.5 * self._sigma * self._sigma

    def diffusion(self, t, x):
        return self._sigma

class OrnsteinUlenbeckProcess(DiffusionProcess):

    def __init__(self, speed, vol, x0 = 0.0):
        DiffusionProcess.__init__(self, x0)
        self._speed = speed
        self._vol = vol

    def drift(self, t, x):
        return - self._speed * x

    def diffusion(self, t, x):
        return self._vol

    def expectation(self, t0, x0, dt):
        return x0 * np.exp(- self._speed * dt)

    def variance(self, t0, x0, dt):
        return 0.5 * self._vol * self._vol / self._speed * (1.0 - np.exp(-2.0 * self._speed * dt))

class SquareRootProcess(DiffusionProcess):

    def __init__(self, b, a, sigma, x0 = 0.0):
        DiffusionProcess.__init__(self, x0)
        self._mean = b
        self._speed = a
        self._volatility = sigma

    def drift(self, t, x):
        return self._speed * (self._mean - x)

    def diffusion(self, t, x):
        return self._volatility * np.sqrt(x)

if __name__ == '__main__':
    # test

    bs = BlackScholesPricess(0.01, 0.4)
    print bs.variance(1,1,1)
    print bs.expectation(1,1,1)

    ou = OrnsteinUlenbeckProcess(0.001, 0.1)
    print ou.variance(1,1,1)
    print ou.expectation(1,1,1)

    sr = SquareRootProcess(0.1, 0.01, 0.4)
    print sr.variance(1,1,1)
    print sr.expectation(1,1,1)
