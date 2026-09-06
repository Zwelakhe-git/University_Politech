import numpy as np
from matrices import *

def isULt(L, U):
    u = L.T
    K = U @ np.linalg.inv(u)
    print("K \n", K)
    for i in range(K.shape[0]):
        for j in range(K.shape[1]):
            if i != j and not np.isclose(K[i, j], 0, atol=1e-6):
                print("K is not diagonal if U2 = LT")
                return
    print("K is diagonal if U2 = LT")
    
A = np.dot(L,U)
if not np.allclose(A, A.T, 1e-6):
    print("матрица не симметричная. разложение может не работать")
    exit()


def isnotULt(L,U):
    #global A
    K = np.eye(A.shape[0])

    indx = np.array([i for i in range(A.shape[0])])
    K[indx, indx] *= np.diag(U)
    Ki = K.copy()

    d = np.diag(K)
    for i in indx:
        if d[i] != 0:
            Ki[i,i] = 1/d[i]

    U2 = Ki @ U
    print("U2 \n", U2)
    if not np.allclose(U2, L.T):
        print("if K is diagonal, then U2 != LT")
    else:
        print("if K is diagonal, then U2 = LT")
    return K, U2


def formS(L,U):
    K = np.eye(A.shape[0])

    du = np.diag(U)
    indx = np.array([i for i in range(A.shape[0])])
    K[indx, indx] *= du

    k1 = np.eye(A.shape[0])
    k1[indx, indx] = np.sqrt(np.abs(du))

    D = np.eye(A.shape[0])
    dk = np.diag(K)
    D[indx, indx] = dk / np.abs(dk)

    if not np.allclose(K, k1 @ D @ k1):
        print("k1 not is valid")
        z = np.zeros_like(D)
        return z, z
    S = k1 @ L.T
    
    return S, D


K, u2 = isnotULt(L, U)

print(u2 @ np.linalg.inv(L.T),end="\n\n")
print(np.linalg.inv(K) @ np.linalg.inv(L) @ u2.T @ K, end="\n\n")

S, D = formS(L, U)

decomp = S.T @ D @ S
if np.allclose(A, decomp, atol=1e-6):
    print("Cholesky decomposition works")
else:
    print("decomposition doesnt work")

print(A, decomp, sep='\n\n')
