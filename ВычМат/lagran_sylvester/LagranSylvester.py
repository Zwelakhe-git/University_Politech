import matrixFunction as mf

def Wk(eigs, eig):
    """
    Вычлислить знаменатель Разложения
    (lk - l1) *...* (lk - lk-1)*(lk - lk+1) *...*(lk - lm)
    lk - eig
    ln - eigs
    """
    prod = 1
    for v in eigs:
        if v == eig:
            continue
        prod *= (eig - v)
    return prod

def multMatrix(A, B):
    """умножить 2 квадратных матрицы, результат сохранить в матрицу А.
    return A
    """
    if len(A) != len(B):
        return None
    tempMatr = [0, 0 ,0 ,0]
    
    N = len(A)
    for i in range(N):
        for j in range(N):
            tempMatr[j] = 0
            for k in range(N):
                tempMatr[j] += A[i][k] * B[k][j]
        A[i] = [v for v in tempMatr]
    
    return A

def WA(A, eigs, eig, n):
    """
    Вычислить числитель разложения Лгранжа-Сильвестра
    (A - l1E) *...* (A - lk-1E) * (A - lk+1E) *...* (A - lmE)
    ln - собственные числа

    eigs - массив или списко собственных чисел

    eig - собственное число, которое исключается из числителя в данный момент. lk

    n - число, являющееся индексом собственного числа, которое используется для текущего вычисления A - lnE
        ln = eigs[n]
    
    Функция работает рекурсивно.
    """
    if n >= len(A):
        #возвращать единичную матрицу если достигли конца собственных чисел
        return [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
    
    elif eigs[n] == eig:
        return WA(A, eigs, eig, n+1)
    
    
    tempMatr = [
        [v for v in A[0]],
        [v for v in A[1]],
        [v for v in A[2]],
        [v for v in A[3]]
    ]
    for i in range(len(tempMatr)):
        tempMatr[i][i] -= eigs[n]
        
    return multMatrix(tempMatr,WA(A, eigs, eig, n+1))



def Lagr(A, eigs, t):
    """Функция вычисляет матрицу Tk в разложение Лангранжа-Сильвестра.
    A - Матрица

    eigs - массив или список собственных значений

    t - значение t, в которой вычисляется значение матричной функции
    """
    N = len(A)
    temp = [[0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
    count = 0
    for eig in eigs:
        Tk = WA(A, eigs,eig, 0)     #Числитель
        tempDen = Wk(eigs, eig)     #Знаменатель
        #F_eig = mf.F(t, eig)        #Значение функции в некоторой точке

        for i in range(N):
            for j in range(N):
                Tk[i][j] /= tempDen
                #Tk[i][j] *= F_eig
        
        if count == 3:
            return Tk
        
        mf.addMatrix(temp,Tk)
        count += 1

    return temp