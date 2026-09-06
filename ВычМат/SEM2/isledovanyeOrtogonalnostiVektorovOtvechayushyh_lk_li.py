import numpy as np
import matplotlib.pyplot as plt

systemMatrix = np.array([
    [-5, -2, -2],[10, 4, 2],[2, 1, 3]
])
eigs,eigVecs = np.linalg.eig(systemMatrix)
eigsT = np.linalg.eigvals(systemMatrix.T)
print(eigs,eigVecs,sep=" : ")
print(systemMatrix @ eigVecs[1])
print(eigs[1] * eigVecs[1])
print("")
#eigs = eigsT

#собственные векторы одному собственному значению различаются
u1 = np.array([2, -8, 2])
u1T = np.array([2, 1, 1])

#собственный вектор AT, отвечающий другому значению, eigs[2]
u2T = np.array([2, 1, 2])

#проверка равенства
print("$для \\lambda_2 = {0}$".format(eigs[2]))
print("u2T = {0}".format(u2T))
print("$AT*u2T = {0}$".format(systemMatrix.T @ u2T))

#докажем ортогональность векторов vk,ui, отвечающих разным собственным значениям
print("\nортогональность векторов u1, u2T (vk,ui)")
print("$u1^T * u2T = {0}, u2T^T * u1 = {1}$".format(u1.T @ u2T, u2T.T @ u1))

print("\nнормирование вектора u1")
#констант нормирования вектора u1
c1 = u1T.T @ u1
#нормируем u1
Normu1 = u1 / c1
print("nomrU1 = {0}".format(Normu1))
print("$u1^T * u1T = {0}, u1T^T * u1 = {1}$".format(Normu1.T @ u1T, u1T.T @ Normu1))

