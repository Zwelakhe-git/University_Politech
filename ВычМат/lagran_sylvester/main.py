"""DEPRECATED!!"""

import numpy as np
import LagranSylvester as LS
import matrixFunction as mf
import getEigVect as GEV

N = 4
beg = 0
end = 1

A = [
    [2,1,3,4],
    [1,3,2,5],
    [3,2,4,1],
    [4,5,1,6]
]

eigvals = np.linalg.eigvals(A)
eigVects = []

for val in eigvals:
    eigVects.append(GEV.getEigVect(A,val))

print("")
eigVect1 = [0.5964668593304898, 0.70199279143435, 0.4994907956912823, 1]
#print(eigVect1)

t = [beg]
step = 0.001
i = 0
while t[i] <= end:
    t.append(t[i] + step)
    i += 1

Tk = LS.Lagr(A, eigvals, t[3])

uk = mf.matrixByVector(Tk,eigVects[3])

if uk != -1:
    print("\n\n[", end="")
    for v in uk:
        print(f"{v} ",end="")

    print("]")
print(eigVects[3])