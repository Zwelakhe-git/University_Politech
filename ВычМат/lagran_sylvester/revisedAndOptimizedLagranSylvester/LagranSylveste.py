import numpy as np
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
    if(A.shape != B.shape):
        return None
    A = A @ B
    return A

def WA(A, eigs, eig, n):
    """
    Вычислить числитель разложения Лгранжа-Сильвестра
    (A - l1E) *...* (A - lk-1E) * (A - lk+1E) *...* (A - lmE)
    ln - собственные числа

    eigs - массив или списoк собственных чисел

    eig - собственное число, которое исключается из числителя в данный момент. lk

    n - число, являющееся индексом собственного числа, которое используется для текущего вычисления A - lnE
        ln = eigs[n]
    
    Функция работает рекурсивно.
    """
    if n >= (A.shape)[0]:
        #возвращать единичную матрицу если достигли конца собственных чисел
        return np.identity((A.shape)[0])
    
    elif eigs[n] == eig:
        return WA(A, eigs, eig, n+1)
    
    tempMatr = np.copy(A) - eigs[n]*np.identity((A.shape)[0])
        
    return multMatrix(tempMatr,WA(A, eigs, eig, n+1))

def Lagr(A, eigs, t, shape, retstep=None):
    """Функция вычисляет матрицу Tk в разложение Лангранжа-Сильвестра.
    A - Матрица

    eigs - массив или список собственных значений

    t - значение t, в которой вычисляется значение матричной функции
    """
    N = shape
    temp = np.zeros_like(A)
    count = 0
    for eig in eigs:
        Tk = WA(A, eigs,eig, 0)     #Числитель
        tempDen = Wk(eigs, eig)     #Знаменатель
        #F_eig = mf.F(t, eig)        #Значение функции в некоторой точке

        Tk /= tempDen
        
        if count == retstep:
            return Tk
        
        mf.addMatrix(temp,Tk)
        count += 1

    return temp