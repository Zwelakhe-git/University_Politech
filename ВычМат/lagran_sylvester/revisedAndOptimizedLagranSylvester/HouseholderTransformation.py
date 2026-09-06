#householderTransformation.py
import numpy as np
import initsyalizatsyaMatristy as im
from Tests import *

def transform(A):
    m = A.shape[0]
    S = np.eye(m)

    for i in range(1, m - 1):
        x = A[i:, i-1]

        e = np.zeros_like(x)
        e[0] = 1

        v = x + np.linalg.norm(x)*e
        v = v / np.linalg.norm(v)

        H = np.eye(m - i) - 2 * (v.reshape(-1, 1) @ v.reshape(1, -1))
        U = np.eye(m)
        U[i:, i:] = H

        A = U @ A @ U
        S = S @ U
    return S, A

"""
def householderTest(Ar,A,S):
    if not isHessenberg(A) or not np.allclose(Ar,S @ A @ S.T):
        return False
    return True
    
orig = im.A
S, A = transform(orig.copy())
eigs1, eigs2 = np.linalg.eigvals(A), np.linalg.eigvals(orig)
print(A)
print(f"S - symmetrical: {symmetryTest(S)}")
print(f"A isHessenberg: {householderTest(orig,A,S)}")
print(np.linalg.eigvals(orig))
print(np.linalg.eigvals(A))
print(np.allclose(S @ S.T, np.eye(S.shape[0])))
#"""


