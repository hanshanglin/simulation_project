from scipy.stats import ksone, chi2
from scipy.special import erf
import numpy as np
import math
import simulation_random
import functools

def D_distribution_table(n):
    # alphaList = [0.2, 0.15, 0.10, 0.05, 0.01]
    table = [[0] * 99 for i in range(n)]
    for i in range(n):
        for j in range(99):
            table[i][99 - j - 1] = ksone.ppf(1 - (j + 1) / 200, i + 1)
    return table


def significance_D(Data, table):
    D_s = Kolmogorov_Smirnov(Data)
    n = len(Data)
    for i in range(99):
        if D_s < table[n][i]:
            return i / 100

@functools.lru_cache(maxsize=10)
def Normal_distribution_table():
    table = [0] * 400
    for i in range(400):
        z = i / 100
        table[i] = 1 - (1 + erf(z / (math.sqrt(2)))) / 2
    return table


def significance_N(data, table):
    if data < 0:
        data = 0 - data
    for i in range(400):
        z = i / 100
        if data < z:
            return table[i - 1]

@functools.lru_cache(maxsize=10)
def chi2_distribution_table():
    alpha = [
        0.995,
        0.99,
        0.98,
        0.975,
        0.95,
        0.90,
        0.80,
        0.10,
        0.05,
        0.025,
        0.02,
        0.01,
        0.005,
        0.001,
    ]
    df = [0] * 37
    for i in range(1, 30):
        df[i - 1] = i
    for i in range(30, 101, 10):
        index = round(i / 10) + 26
        df[index] = i
    table = [[0] * 14 for i in range(37)]
    for i in range(37):
        for j in range(14):
            table[i][j] = chi2.isf(alpha[j], df[i])
    return table


def significance_Chi(data, k, table):
    alpha = [
        0.995,
        0.99,
        0.98,
        0.975,
        0.95,
        0.90,
        0.80,
        0.10,
        0.05,
        0.025,
        0.02,
        0.01,
        0.005,
        0.001,
    ]
    for i in range(14):
        if data < table[k][i]:
            return alpha[i]


########################################
def Kolmogorov_Smirnov(Data):
    list.sort(Data)
    k = len(Data)
    D_p = [0] * k
    D_m = [0] * k
    for i in range(k):
        D_p[i] = (i + 1) / k - Data[i]
        D_m[i] = Data[i] - i / k
    D_s = max(max(D_p), max(D_m))
    return D_s


###################################
# k classes
def Chi_square(Data, k):
    c = [0] * k
    n = len(Data)
    # compute test statistics
    for i in range(n):
        for j in range(k):
            if Data[i] < (j + 1) / k:
                c[j] += 1
                break
    #print(c)
    Chi = 0
    mu = n / k
    # compute
    for i in range(k):
        Chi += (c[i] - mu) ** 2 / mu
    
    return significance_Chi(Chi,k-1,chi2_distribution_table())


####################################
def Wald_wolfowitz_EO(Data):  # '+' for even and '-' for odd
    n1 = 0  # even
    n2 = 0  # odd
    r = 0  # run
    n = len(Data)
    pS = ""
    for i in range(n):
        if round(100 * Data[i]) % 2 == 0:
            n1 += 1
            if pS == "+":
                continue
            else:
                pS = "+"
                r += 1
        else:
            n2 += 1
            if pS == "-":
                continue
            else:
                pS = "-"
                r += 1
    print(n1, n2, r)
    mu = 2.0 * n1 * n2 / (n1 + n2) + 1
    sigma = math.sqrt(
        2.0 * n1 * n2 * (2 * n1 * n2 - n1 - n2) / ((n1 + n2) ** 2 * (n1 + n2 - 1))
    )
    Z_s = (r - mu) / sigma
    print(Z_s)
    return significance_N(Z_s,Normal_distribution_table())


def Wald_wolfowitz_BS(Data):  # '+' for bigger >= 0.5 and '-' for small
    n1 = 0  # bigger
    n2 = 0  # small
    r = 0  # run
    n = len(Data)
    pS = ""
    for i in range(n):
        if round(100 * Data[i]) >= 50:
            n1 += 1
            if pS == "+":
                continue
            else:
                pS = "+"
                r += 1
        else:
            n2 += 1
            if pS == "-":
                continue
            else:
                pS = "-"
                r += 1
    print(n1, n2, r)
    mu = 2.0 * n1 * n2 / (n1 + n2) + 1
    sigma = math.sqrt(
        2.0 * n1 * n2 * (2 * n1 * n2 - n1 - n2) / ((n1 + n2) ** 2 * (n1 + n2 - 1))
    )
    Z_s = (r - mu) / sigma
    print(Z_s)
    return significance_N(Z_s,Normal_distribution_table())


################################
# lag k
def correlation(Data, k):
    R_k = 0
    n = len(Data)
    for i in range(n - k):
        R_k += ((Data[i] - 1 / 2) * (Data[i + k] - 1 / 2)) / (n - k)
    Z_s = math.sqrt(n - k) * R_k * 12

    return Z_s,significance_N(Z_s,Normal_distribution_table())


##########################################
# k intervals
def good_serial(Data, k):
    n = len(Data)
    U = 0
    matrix = [[0] * k for i in range(k)]
    for i in range(n - 1):
        matrix[interval(Data[i], 4)][interval(Data[i + 1], 4)] += 1
    for i in range(k):
        N = 0
        for j in range(k):
            U += (k ** 2 / n) * (matrix[i][j] - n / k ** 2) ** 2
            N += matrix[i][j]
        U -= (k / n) * (N - n / k) ** 2
        #print(N)
    #print(matrix)
    return U, significance_Chi(U,k*(k-1),chi2_distribution_table())


def interval(data, k):
    for i in range(k):
        if data < (i + 1) / k:
            return i

##################################


def serial_independent_run(Data):  # assume large n > 50
    n = len(Data)
    R_k = [0] * 8  # run for k
    E_k = [0] * 8  # expect for k
    x_k = [0] * 8  # x for k
    pS = ""  # previous state, initial '', '+' for up and '-' for down
    l = 0  # length of run
    for i in range(n - 1):
        if Data[i] < Data[i + 1] and pS != "-":
            l += 1
            pS = "+"
        elif Data[i] > Data[i + 1] and pS != "+":
            l += 1
            pS = "-"
        elif Data[i] == Data[i + 1]:
            l += 1
        else:
            R_k[l - 1] += 1
            l = 1
            if Data[i] < Data[i + 1]:
                pS = "+"
            else:
                pS = "-"
    R_k[l - 1] += 1
    # compute sum of run
    s_R = 0
    for i in range(8):
        s_R += R_k[i]
    #print(s_R)
    # compute sum of expect
    s_E = 0
    for i in range(7):
        k = i + 1
        # compute expect of k
        if n >= 50:
            E_k[i] = 2 * ((n - k - 2) * (k ** 2 + 3 * k + 1)) / math.factorial(k + 3)
        else:
            E_k[i] = (
                2
                * ((k ** 2 + 3 * k + 1) * n - (k ** 3 + 3 * k ** 2 - k - 4))
                / math.factorial(k + 3)
            )
        s_E += E_k[i]
    E_k[7] = (2 * n - 1) / 3 - s_E
    # compute x
    for i in range(8):
        x_k[i] = E_k[i] * 3 * s_R / (2 * n - 1)
    U = 0
    for i in range(8):
        U += (R_k[i] - x_k[i]) ** 2 / x_k[i]
    # print(E_k, R_k, x_k)
    return U, significance_Chi(U,7,chi2_distribution_table())


DATA_LEN = 30000

print("Chi_square:[bug]")
# CHI_SQUARE_K = 100
# print("numpy:"+str(Chi_square([np.random.uniform(0,1) for i in range(DATA_LEN)],CHI_SQUARE_K)))
# SM = simulation_random.SeedAndMul(7219, 4703)
# print("SM:"+str(Chi_square([SM.gen_ran() for i in range(DATA_LEN)],CHI_SQUARE_K)))
# MS = simulation_random.MidSquare(7219)
# print("MS:"+str(Chi_square([MS.gen_ran() for i in range(DATA_LEN)],CHI_SQUARE_K)))
# muC = simulation_random.MultiCongruential(4703, 5657, 7219)
# print("muC:"+str(Chi_square([muC.gen_ran() for i in range(DATA_LEN)],CHI_SQUARE_K)))
# miC = simulation_random.MixedCongruential(4703, 5657, 1931, 7219)
# print("miC:"+str(Chi_square([miC.gen_ran() for i in range(DATA_LEN)],CHI_SQUARE_K)))
# AC = simulation_random.AdditiveCongruential(4703, 5657, 7219)
# print("AC:"+str(Chi_square([AC.gen_ran() for i in range(DATA_LEN)],CHI_SQUARE_K)))
# print("-----------------------------")

print("Wald_wolfowitz_EO:")
print("numpy:"+str(Wald_wolfowitz_EO([np.random.uniform(0,1) for i in range(DATA_LEN)])))
SM = simulation_random.SeedAndMul(7219, 4703)
print("SM:"+str(Wald_wolfowitz_EO([SM.gen_ran() for i in range(DATA_LEN)])))
MS = simulation_random.MidSquare(7219)
print("MS:"+str(Wald_wolfowitz_EO([MS.gen_ran() for i in range(DATA_LEN)])))
muC = simulation_random.MultiCongruential(4703, 5657, 7219)
print("muC:"+str(Wald_wolfowitz_EO([muC.gen_ran() for i in range(DATA_LEN)])))
miC = simulation_random.MixedCongruential(4703, 5657, 1931, 7219)
print("miC:"+str(Wald_wolfowitz_EO([miC.gen_ran() for i in range(DATA_LEN)])))
AC = simulation_random.AdditiveCongruential(4703, 5657, 7219)
print("AC:"+str(Wald_wolfowitz_EO([AC.gen_ran() for i in range(DATA_LEN)])))
print("-----------------------------")


print("correlation:")
CORRELATION_LAG = 5
print("numpy:"+str(correlation([np.random.uniform(0,1) for i in range(DATA_LEN)],CORRELATION_LAG)))
SM = simulation_random.SeedAndMul(7219, 4703)
print("SM:"+str(correlation([SM.gen_ran() for i in range(DATA_LEN)],CORRELATION_LAG)))
MS = simulation_random.MidSquare(7219)
print("MS:"+str(correlation([MS.gen_ran() for i in range(DATA_LEN)],CORRELATION_LAG)))
muC = simulation_random.MultiCongruential(4703, 5657, 7219)
print("muC:"+str(correlation([muC.gen_ran() for i in range(DATA_LEN)],CORRELATION_LAG)))
miC = simulation_random.MixedCongruential(4703, 5657, 1931, 7219)
print("miC:"+str(correlation([miC.gen_ran() for i in range(DATA_LEN)],CORRELATION_LAG)))
AC = simulation_random.AdditiveCongruential(4703, 5657, 7219)
print("AC:"+str(correlation([AC.gen_ran() for i in range(DATA_LEN)],CORRELATION_LAG)))
print("-----------------------------")

print("good_serial:")
GOODSERIAL_K = 4
print("numpy:"+str(good_serial([np.random.uniform(0,1) for i in range(DATA_LEN)],GOODSERIAL_K)))
SM = simulation_random.SeedAndMul(7219, 4703)
print("SM:"+str(good_serial([SM.gen_ran() for i in range(DATA_LEN)],GOODSERIAL_K)))
MS = simulation_random.MidSquare(7219)
print("MS:"+str(good_serial([MS.gen_ran() for i in range(DATA_LEN)],GOODSERIAL_K)))
muC = simulation_random.MultiCongruential(4703, 5657, 7219)
print("muC:"+str(good_serial([muC.gen_ran() for i in range(DATA_LEN)],GOODSERIAL_K)))
miC = simulation_random.MixedCongruential(4703, 5657, 1931, 7219)
print("miC:"+str(good_serial([miC.gen_ran() for i in range(DATA_LEN)],GOODSERIAL_K)))
AC = simulation_random.AdditiveCongruential(4703, 5657, 7219)
print("AC:"+str(good_serial([AC.gen_ran() for i in range(DATA_LEN)],GOODSERIAL_K)))
print("-----------------------------")


print("serial_independent_run:")
print("numpy:"+str(serial_independent_run([np.random.uniform(0,1) for i in range(DATA_LEN)])))
SM = simulation_random.SeedAndMul(7219, 4703)
print("SM:"+str(serial_independent_run([SM.gen_ran() for i in range(DATA_LEN)])))
MS = simulation_random.MidSquare(7219)
print("MS:"+str(serial_independent_run([MS.gen_ran() for i in range(DATA_LEN)])))
muC = simulation_random.MultiCongruential(4703, 5657, 7219)
print("muC:"+str(serial_independent_run([muC.gen_ran() for i in range(DATA_LEN)])))
miC = simulation_random.MixedCongruential(4703, 5657, 1931, 7219)
print("miC:"+str(serial_independent_run([miC.gen_ran() for i in range(DATA_LEN)])))
AC = simulation_random.AdditiveCongruential(4703, 5657, 7219)
print("AC:"+str(serial_independent_run([AC.gen_ran() for i in range(DATA_LEN)])))
print("-----------------------------")


