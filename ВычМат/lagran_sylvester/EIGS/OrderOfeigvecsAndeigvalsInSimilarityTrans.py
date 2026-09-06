import numpy as np
import random
import initsyalizatsyamatritsy as im

def isOrtogonal(A):
    E = np.eye(A.shape[0])
    return np.allclose(A @ A.T, E) and np.allclose(A.T @ A, E)

def isSimmetrical(A):
    return np.allclose(A,A.T)


A = im.A.copy()
m = A.shape[0]

eigvals, eigvecs = np.linalg.eig(A)
L = np.eye(m)
indx = [i for i in range(m)]
L[indx,indx] = eigvals
U = eigvecs

print(f"A isSimilar L: {np.allclose(A,U @ L @ U.T)}")
print(f"U isOrtogonal: {isOrtogonal(U)}")
print(f"U isSimmetrical: {isSimmetrical(U)}")

#изменяем порядко столбцов U и тестируем подобие
randInstance = random.Random()
i = randInstance.randint(0,U.shape[1]-1)
j = randInstance.randint(0,U.shape[1]-1)
while(j == i):
    j = randInstance.randint(0,U.shape[1]-1)

U[:, [i,j]] = U[:, [j,i]]
print("After swapping columns in U")
print(f"A isSimilar L: {np.allclose(A,U @ L @ U.T)}")
print(f"U isOrtogonal: {isOrtogonal(U)}")
print("")
print(f"(A@A@B)T = AT@AT@BT: {np.all((A@A@U).T == (A @ A).T @ U.T)}")