import numpy as np

def F(t,eig):
    return np.exp(eig * t)

def matrixByVector(M, v):
    if len(v.shape) >= len(M.shape):
        return None
    try:
        tempv = v.reshape((M.shape)[1], 1)
        if (M.shape)[1] != (tempv.shape)[0]:
            return None
    except IndexError as e:
        pass
    return M @ v

def addMatrix(A, B):
    if A.shape != B.shape:
        return None
    A += B
    return A

def showMatrix(M):
    if M != None:
        print(M)
    else:
        print("Empty Matrix")

def vectorByvector(a, b):
    if a.size != b.size:
        print("Убедись, что векторы имеют одинаковые размеры")
        return -1
    a = a.reshape(a.size, 1)
    b = b.reshape(1, b.size)
    return a @ b

def Transpose(v):
    return v.reshape(1, v.size)