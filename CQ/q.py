import numpy as np

class QGate:

    _H = (1.0/np.sqrt(2)) * np.matrix([[ 1, 1],
                                       [ 1,-1]], dtype=np.complex128);

    _I = np.matrix([[ 1, 0],
                    [ 0, 1]], dtype=np.complex128);

    _X = np.matrix([[ 0, 1],
                    [ 1, 0]], dtype=np.complex128);

    _Y = np.matrix([[1j, 0],
                    [ 0,1j]], dtype=np.complex128);

    _Z = np.matrix([[ 1, 0],
                    [ 0,-1]], dtype=np.complex128);

    def __init__(self, buffer):
        self.array = np.matrix(buffer, dtype=np.complex128)

    def __repr__(U):
        return np.ndarray.__repr__(U.array)

    def __call__(U, k):
        V = QGate(U.array)
        for _ in range(k):
            V = U * V
        return V
        
    def __add__(U, V):
        return QGate(U.array + V.array)

    def __sub__(U, V):
        return QGate(U.array - V.array)

    def __mul__(U, V):
        return QGate(np.kron(U.array, V.array))

    def __xor__(U, V):
        return QGate(np.matmul(U.array, (~V).array))

    def __matmul__(U, V):
        if type(V) is QGate:
            return QGate(np.matmul(U.array, V.array))
        else:
            return QState(np.matmul(U.array, V.array))

    def __invert__(U):
        return QGate(np.conjugate(np.transpose(U.array)))

class QState:

    BASE = {
            '0' : np.matrix([[1], [0]], dtype=np.complex128),
            '1' : np.matrix([[0], [1]], dtype=np.complex128)
        }

    _u = BASE['0']
    _v = BASE['1']

    def __init__(self, buffer):
        self.array = np.matrix(buffer, dtype=np.complex128)
        
    def __call__(U, k):
        V = QState(U.array)
        for _ in range(k):
            V = U * V
        return V

    def __repr__(U):
        return np.ndarray.__repr__(U.array)

    def __xor__(U, V):
        return QGate(np.matmul(U.array, (~V).array))
        
    def __add__(U, V):
        return QState(U.array + V.array)

    def __sub__(U, V):
        return QState(U.array - V.array)

    def __mul__(U, V):
        return QState(np.kron(U.array, V.array))

    def __matmul__(U, V):
        return np.matmul((~U).array, V.array)

    def __invert__(U):
        return QState(np.conjugate(np.transpose(U.array)))

    @staticmethod
    def to_qubits(n : int, m : int):
        X = [QState(QState.BASE[c]) for c in "{:0{digits}b}".format(n, digits=m)]

        u = X[0];

        for v in X[1:]:
            u = u * v;

        return u

QGate.H = QGate(QGate._H)
QGate.I = QGate(QGate._I)
QGate.X = QGate(QGate._X)
QGate.Y = QGate(QGate._Y)
QGate.Z = QGate(QGate._Z)

QState.u = QState(QState._u)
QState.v = QState(QState._v)

