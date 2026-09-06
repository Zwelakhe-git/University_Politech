import numpy as np

errA = 5e-4
systemMatrix = np.array([
    [-5, -2, -2],[10, 4, 2],[2, 1, 3]
])
A = systemMatrix
Aeigs = np.linalg.eigvals(A)

#собственные векторы A и AT одному собственному значению различаются
u1 = np.array([2, -8, 2])
u1T = np.array([2, 1, 1])

#собственный вектор AT, отвечающий другому значению, eigs[2]
u2 = np.array([0, -3, 3])
u2T = np.array([2, 1, 2])

#иследуем изменения собственных значений при ошибке в матрице
dA = (errA*np.ones_like(A))

dEigs = np.linalg.eigvals(A + dA)
#вектор ошибки собствнных значений
errEigs = Aeigs - dEigs

#проверяем равенство dA * uk = dl*uk
print(f"\\lambda_1 = {errEigs[1]}")
print(f"dA*u1 = {dA @ u1}")
print(f"dl1 * u1 = {errEigs[1] * u1}")
