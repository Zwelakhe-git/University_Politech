#GivensTransformation.py
import numpy as np
import initsyalizatsyaMatristy as im
from Tests import *

def makeTkj(A, k, j):
    #k -= 1
    #j -= 1

    a_kj = A[k,j]
    a_jj = A[j,j]

    r = np.hypot(a_kj, a_jj)
    if r == 0:
        c, s = 1.0, 0.0
    else:
        s = -a_kj / r
        c = a_jj / r
    
    T = np.eye(A.shape[0])

    T[[j, j, k, k],[j, k, j, k]] = c, -s, s, c
    return T

def transform(A):
    m, n = A.shape
    Q = np.eye(m)
    for j in range(n):
        for i in range(m-1, j, -1):
            Tkj = makeTkj(A, i, j)
            A = Tkj @ A
            Q = Tkj @ Q
    return Q.T, A

"""A = im.A.copy()
m = A.shape[0]

for j in range(1, m - 1):
    for k in range(j + 1, m):
        Tkj = makeTkj(A, k + 1, j + 1)
        A = Tkj @ A
        #print(f"{k + 1}{j + 1}", end=",")
   #print("")"""


#"""
A = im.A.copy()
Q,R = transform(A)
print(Q.T @ im.A @ Q)
#print(Q, R, sep="\n")
print(f"A = QR: {np.allclose(im.A, Q @ R)}")
print(f"Q.T @ Q = E: {np.allclose(Q.T @ Q, np.eye(Q.shape[0]))}")
print(f"Q isHessenberg: {isHessenberg(Q)}")
print(f"R isUpperTriangular: {isUpperTriangular(R)}")
print(f"Q isSimmetrical: {symmetryTest(Q)}")
#"""

