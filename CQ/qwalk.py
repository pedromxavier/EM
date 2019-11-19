from functools import reduce;
from operator import add, mul;

import matplotlib.pyplot as plt

def SUM(x):
    return reduce(add, x)

def MUL(x):
    return reduce(mul, x)

from q import *;

def shift(i0, n0):
    uu = QState.u ^ QState.u
    vv = QState.v ^ QState.v

    i = i0 + 1;
    n = n0 - 1;

    x = [];
    y = [];

    m = int(np.ceil(np.log2(n0)))

    while i <= n:
        a = QState.to_qubits(i-1, m)
        b = QState.to_qubits(i  , m)
        c = QState.to_qubits(i+1, m)

        x.append(a ^ b)
        y.append(c ^ b)

        i += 1

    x = SUM(x)
    y = SUM(y)

    X = uu * x
    Y = vv * y

    return X + Y


S = shift(0, 100)

def quantum_walk(x, i0=0, n0=100, steps=40):
    N = (n0 - i0) + 1;

    c0 = np.array([[1], [x]], dtype=np.complex128) / np.sqrt(2); # initial coin

    c = QState(c0); # inital coin

    m = int(np.ceil(np.log2(n0)))

    s = QState.to_qubits(50, m) # initial position

    phi = c * s; # inital state

    C = QGate.H * QGate.I(6)

    S = shift(i0, n0)

    for _ in range(steps):
        phi = C @ phi;
        phi = S @ phi;


    amp = np.zeros(N, dtype=np.float64) #amplitudes
    for k in range(i0, n0+1):
        q = QState.to_qubits(k, m);
        M = QGate.I * (q ^ q); # measurement operator

        p = M @ phi

        amp[k] = (p @ p).real

    return amp

def random_walk(i0=0, n0=100, steps=40, num_reads=1000000):
    # line positions
    x = np.zeros((n0 - i0) + 1, dtype=np.float64)

    # initial positions
    s = 50 * np.ones(num_reads, dtype=np.int32)

    # random steps for every read
    # 2 * r - 1 takes from {0, 1} to {-1, 1}
    # sum(r) accounts the total movement for each read.
    # s + r broadcasts the sum, giving the final position
    #
    # x[s + r] += 1 adds 1 for every final position on the line

    r = np.sum(2 * (np.random.random((num_reads, steps)) > 0.5) - 1, axis=1)

    for k in (s + r):
        x[k] += 1;

    return x / num_reads # normalizes for probability

if __name__ == '__main__':
    x = np.linspace(0, 100, num=101, dtype=np.int32)[::2]

    quantum_amp0 = quantum_walk(1)
    quantum_amp = quantum_walk(1j)
    random_amp = random_walk()

    kw = {
        'markerfmt': " ",
        'basefmt' : " "
    }
    lbl = r"$\left|\Psi_0\right\rangle  = \frac{\left|0\right\rangle + \left|1\right\rangle}{\sqrt{2}}$"
    plt.stem(x, quantum_amp0[::2], "green", label=lbl, **kw)
    lbl = r"$\left|\Psi_0\right\rangle  = \frac{\left|0\right\rangle + \mathbb{i} \left|1\right\rangle}{\sqrt{2}}$"
    plt.stem(x, quantum_amp[::2], "blue",  label=lbl, **kw)
    plt.stem(x, random_amp[::2], "red",label="Moeda",  **kw)
    plt.legend(fontsize='x-large')
    plt.show()
