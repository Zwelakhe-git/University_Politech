from math import exp
def F(t,eig):
    return exp(eig * t)

def matrixByVector(M, v):
    if len(M[0]) != len(v):
        return -1
    
    N = len(M)
    tmpVec = [0, 0, 0, 0]

    for i in range(N):
        tmpVec[i] = 0
        for j in range(N):
            tmpVec[i] += M[i][j]*v[j]
        
    return tmpVec

def addMatrix(A, B):
    """
    сложить 2 кдрадратных матриц, резльтат сохранить в A
    """
    if len(A) != len(B):
        print("different size Matrices")
        return -1
    
    N = len(A[0])
    for i in range(N):
        for j in range(N):
            A[i][j] += B[i][j]
    
    return A
    
def showMatrix(M):
    if M == None:
        print("The matrix is empty")
        return -1
    
    N = len(M)

    for i in range(N):
        for j in range(N):
            print(M[i][j], "   ",end="")
        print("")
