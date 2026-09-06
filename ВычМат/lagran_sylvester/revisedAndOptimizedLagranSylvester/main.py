import numpy as np
import LagranSylveste as LS
import matrixFunction as mf
import initsyalizatsyaMatristy as im

N = 4
beg = 0
end = 1

A = im.A
AT = A.T

eiginfo = np.linalg.eig(A)
eigvals = eiginfo[0]
eigVects = eiginfo[1]

_,vT = np.linalg.eig(AT)

t = [beg]
step = 0.001
i = 0
while t[i] <= end:
    t.append(t[i] + step)
    i += 1

retstep = 1
try:
    Tk = LS.Lagr(A, eigvals, t[3], (A.shape)[0], retstep=retstep)
    uk = mf.matrixByVector(Tk,eigVects[:,retstep])

    print(f"\n{uk}")
    print(eigVects[:,retstep])

    #vk = uk.reshape(uk.size, 1) @ vT[:, retstep].reshape(1, uk.size)
    vk = mf.vectorByvector(eigVects[:, retstep], vT[:, retstep])

    vkT = vT[:,retstep]
    tmp = vkT.reshape(1, vkT.size) @ uk.reshape(uk.size, 1)
    print("Tk\n", Tk)
    print("vTk\n", vk)

    if np.allclose(Tk, vk):
        print("Tk = uk@vTk")

except IndexError as e:
    print("invalid retstep")
