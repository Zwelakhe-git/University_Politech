import numpy as np

def isHessenberg(A):
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            if i > j + 1 and not np.isclose(A[i, j], 0):
                return False
    return True

def symmetryTest(U):
    if not np.allclose(U,U.T):
        return False
    return True

def isUpperTriangular(A):
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            if i > j and not np.isclose(A[i,j],0):
                return False
    return True

def isDiagonal(A):
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            if i != j and not np.isclose(A[i,j], 0):
                return False
    return True