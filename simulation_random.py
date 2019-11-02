import random
import numpy as np

#TODO: change random.uniform to hand-by function
def two_normal_ran(mean, variance):
    w = 2
    while w > 1:
        v1 = 2*random.uniform(0, 1) - 1
        v2 = 2*random.uniform(0, 1) - 1
        w = v1**2 + v2**2

    z1 = ((-2)*np.log(w)/w)**0.5 * v1
    z2 = ((-2)*np.log(w)/w)**0.5 * v2

    return (mean + variance**0.5 * z1), (mean + variance**0.5 * z2)


def exp_ran(mean):
    return (-mean) * np.log(1 - random.uniform(0, 1))  # u is equivalent to (1 - u)random.uniform(0, 1)


if __name__ == "__main__":
    print(two_normal_ran(240, 120))
    print(two_normal_ran(480, 200))
    print(exp_ran(120))
    print(exp_ran(360))

