import random
import numpy as np
import math


def std_normal_distribution(x):  # Standard normal distribution calculator
    return (1/(2*math.pi)**0.5)*math.exp((-x**2)/2)


def normal_ran_polar(mean, variance, seed, mul, mod):  # Polar method for normal distribution
    w = 2
    muC = MultiCongruential(seed, mul, mod)
    while w > 1:
        # v1 = 2*random.uniform(0, 1) - 1
        # v2 = 2*random.uniform(0, 1) - 1
        v1 = 2 * muC.gen_ran() - 1
        v2 = 2 * muC.gen_ran() - 1
        w = v1**2 + v2**2

    z1 = ((-2)*np.log(w)/w)**0.5 * v1
    z2 = ((-2)*np.log(w)/w)**0.5 * v2

    return (mean + variance**0.5 * z1), (mean + variance**0.5 * z2)


def normal_ran_rej(mean, variance, seed, mul, mod):  # Rejection for normal distribution
    muC = MultiCongruential(seed, mul, mod)
    sd = (variance**(1/2))
    a = mean - 3 * sd
    b = mean + 3 * sd
    c = 1/(sd * (2*math.pi)**0.5)
    fx = 0
    y = 1
    while y > fx:
        # x = a + random.uniform(0, 1) * (b - a)
        # y = random.uniform(0, 1) * c
        x = a + muC.gen_ran() * (b - a)
        y = muC.gen_ran() * c
        fx = round(std_normal_distribution(x), 4) * variance + mean
    # accept
    return x


def normal_ran_conv(mean, variance, seed, mul, mod):  # Convolution for normal distribution
    muC = MultiCongruential(seed, mul, mod)
    sd = (variance**(1/2))
    sum = 0
    for i in range(12):
        # sum += random.uniform(0, 1)
        sum += muC.gen_ran()
    z = sum - 6
    return z * sd + mean


def exp_ran_inv(mean, seed, mul, mod):  # Inverse transformation for exponential distribution
    muC = MultiCongruential(seed, mul, mod)
    #  return (-mean) * np.log(1 - random.uniform(0, 1))
    return (-mean) * np.log(1 - muC.gen_ran())
    # inverse transformation

# The following 5 classes generate 0 - 1 random numbers that follows uniform distribution from 0 to 1


class SeedAndMul:  # Seed and multiplier method (not sure if it follows U(0, 1))
    def __init__(self, seed, mul):
        self.seed = seed
        self.mul = mul

    def gen_ran(self):
        seed_square = self.seed * self.mul
        str_square = str(seed_square)
        while len(str_square) < 8:
            str_square = '0' + str_square
        self.mul = int(str_square[-4:])
        return int(str_square[2:6]) / 10000


class MidSquare:  # Mid square method (not sure if it follows U(0, 1))
    def __init__(self, seed):
        self.seed = seed

    def gen_ran(self):
        seed_square = self.seed**2
        str_square = str(seed_square)
        while len(str_square) < 8:
            str_square = '0' + str_square
        self.seed = int(str_square[2:6])
        return self.seed / 10000


class MultiCongruential:  # Multiplicative congruential method
    def __init__(self, seed, mul, mod):
        if mul > mod or seed > mod:
            print('False input.')
            return
        self.seed = seed
        self.mul = mul
        self.mod = mod

    def gen_ran(self):
        self.seed = (self.mul * self.seed) % self.mod
        return self.seed / self.mod


class MixedCongruential:  # Mixed Congruential method
    def __init__(self, seed, mul, const, mod):
        if mul > mod or const > mod or seed > mod:
            print('False input.')
            return
        self.seed = seed
        self.mul = mul
        self.const = const
        self.mod = mod

    def gen_ran(self):
        self.seed = (self.seed * self.mul + self.const) % self.mod
        return self.seed / self.mod


class AdditiveCongruential:  # Additive Congruential method
    def __init__(self, seed1, seed2, mod):
        self.seed1 = seed1
        self.seed2 = seed2
        self.mod = mod

    def gen_ran(self):
        next_x = (self.seed1 + self.seed2) % self.mod
        self.seed1 = self.seed2
        self.seed2 = next_x
        return next_x / self.mod


if __name__ == '__main__':
    SM = SeedAndMul(5678, 1234)
    MS = MidSquare(5678)
    muC = MultiCongruential(9876, 479, 10000)
    miC = MixedCongruential(9876, 479, 9827, 10000)
    AC = AdditiveCongruential(239086, 982372, 1000)

    print([MS.gen_ran() for i in range(20)])

    print(SM.gen_ran())
    print(MS.gen_ran())
    print(muC.gen_ran())
    print(miC.gen_ran())
    print(AC.gen_ran())


    print(normal_ran_conv(240, 120, 9876, 479, 10000))
    print(normal_ran_polar(480, 200, 9876, 479, 10000))
    print(normal_ran_rej(240, 120, 9876, 479, 10000))
    print(exp_ran_inv(120, 9876, 479, 10000))

